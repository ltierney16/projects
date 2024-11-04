#all the modules imported for the project
import sqlite3
import os
from flask import Flask, render_template, request, g, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
from datetime import datetime, timedelta

#creates flask application
app = Flask(__name__)

#allows application to have a database path, enable debug mode, have security key
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#handles requests on the /trade route, for GET requests renders an empty form allowing users to
#input stock details. For POST requests retrieves stock data using Yahoo finance API
@app.route('/trade', methods=['GET', 'POST'])
def index():
    plot_div = None
    error_message = None

    if request.method == 'POST':

        #get the stock ticker, period, and interval from the form
        stock = request.form.get('stock')
        period = request.form.get('period', '1d')
        interval = request.form.get('interval', '1m')

        #get stock data from yahoo finance api
        data = yf.download(tickers=stock, period=period, interval=interval)

        #check if data is empty (like stock symbol invalid)
        if data.empty:
            error_message = "Invalid stock symbol. Please enter a valid stock symbol."
        else:
            #flatten the column index if it's multi-level
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = [col[0] for col in data.columns]

            #calculate the 20-period moving average for the trendline
            data['20_MA'] = data['Close'].rolling(window=20).mean()

            #create plotly figure
            fig = go.Figure()

            #add candlestick trace
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))

            #add moving average trendline trace
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['20_MA'],
                mode='lines',
                name='20-Period Moving Average',
                line=dict(width=2, dash='dash')
            ))

            #update layout to skip weekends
            fig.update_layout(
                title=f'{stock} Stock Price with Trendline (20-Period Moving Average)',
                xaxis_title='Time',
                yaxis_title='Stock Price (USD)',
            )
            fig.update_xaxes(
                rangebreaks=[{'bounds': ['sat', 'mon']}],  # Skip weekends
            )

            #render the plot as HTML
            plot_div = pio.to_html(fig, full_html=False)

    return render_template('trade.html', plot_div=plot_div, error_message=error_message)

#function to connect to SQlite database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

#function to initialize database with schema.sql
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

#print message to terminal indicating database has been made
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Initialized the database")

#function to get current database or create a new one
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#closes database at end of each request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#function to get users bank and investing balance by their username
def get_user_balances(user_id):
    db = get_db()
    user = db.execute('SELECT bank_balance, investing_balance FROM users WHERE id = ?', (user_id,)).fetchone()
    return user['bank_balance'], user['investing_balance']

#renders register page
@app.route('/')
def register_page():
    return render_template('create_account.html')

#route to handle user registration form submission
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    db = get_db()
    try:

        #add me user to database
        db.execute(
            'INSERT INTO users (username, password, bank_balance, investing_balance) VALUES (?, ?, 10000.0, 0.0)',
            [username, password]
        )

        #commit changes to database
        db.commit()

        #return to login page
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:

        #flash error message if username already taken
        flash('Username already taken', 'error')  # Ensure category is 'error' for the HTML check
        return redirect(url_for('register_page'))

#route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', [username]).fetchone()

        #check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']  # Store the username in the session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'login')

    return render_template('login.html')

#route to display users dashboard with account information and charts showing projected income
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    username = session.get('username')  # Get the username from the session
    if not user_id:
        return redirect(url_for('login'))

    db = get_db()
    bank_balance, investing_balance = get_user_balances(user_id)

    #query cash flows for the user
    cash_flows = db.execute('SELECT description, amount, period, type FROM transactions WHERE user_id = ?', (user_id,)).fetchall()
    cash_flows = [dict(row) for row in cash_flows]

    #generate cumulative balance data for each time period starting with bank_balance
    data_week = generate_cumulative_data(cash_flows, 'week', bank_balance)
    data_month = generate_cumulative_data(cash_flows, 'month', bank_balance)
    data_year = generate_cumulative_data(cash_flows, 'year', bank_balance)
    data_5years = generate_cumulative_data(cash_flows, '5years', bank_balance)

    #generate the plotly figures for time periods
    fig_week = generate_line_chart(data_week, "Cumulative Balance (Week)")
    fig_month = generate_line_chart(data_month, "Cumulative Balance (Month)")
    fig_year = generate_line_chart(data_year, "Cumulative Balance (Year)")
    fig_5years = generate_line_chart(data_5years, "Cumulative Balance (5 Years)")

    #render charts as HTML
    chart_week = pio.to_html(fig_week, full_html=False)
    chart_month = pio.to_html(fig_month, full_html=False)
    chart_year = pio.to_html(fig_year, full_html=False)
    chart_5years = pio.to_html(fig_5years, full_html=False)

    #pass the username to the template
    return render_template('dashboard.html', bank_balance=bank_balance, investing_balance=investing_balance, chart_week=chart_week, chart_month=chart_month, chart_year=chart_year, chart_5years=chart_5years, username=username)

#function to generate cumulative balance data for period
def generate_cumulative_data(cash_flows, period, initial_balance):
    today = datetime.today()
    data = []

    #see the range of dates based on the period
    if period == 'week':
        num_days = 7
    elif period == 'month':
        num_days = 30
    elif period == 'year':
        num_days = 365
    elif period == '5years':
        num_days = 365 * 5
    else:
        return []

    #start with the initial balance
    cumulative_balance = initial_balance

    #create a daily timeline
    for i in range(num_days):
        date = today - timedelta(days=num_days - i - 1)
        daily_total = 0

        #calculate the income/expenses for this day based on their frequency
        for flow in cash_flows:
            amount = flow['amount']
            flow_type = flow['type']
            flow_period = flow['period']

            if flow_period == 'Daily':
                daily_total += amount if flow_type == 'Income' else -amount
            elif flow_period == 'Weekly' and i % 7 == 6:
                daily_total += amount if flow_type == 'Income' else -amount
            elif flow_period == 'Monthly' and i % 30 == 29:
                daily_total += amount if flow_type == 'Income' else -amount
            elif flow_period == 'Quarterly' and i % 90 == 89:
                daily_total += amount if flow_type == 'Income' else -amount
            elif flow_period == 'Yearly' and i % 365 == 364:
                daily_total += amount if flow_type == 'Income' else -amount

        #update cumulative balance
        cumulative_balance += daily_total
        data.append({'date': date, 'balance': cumulative_balance})

    return data

#function to create line plot using plotly
def generate_line_chart(data, title):
    dates = [point['date'] for point in data]
    balances = [point['balance'] for point in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=balances, mode='lines', name='Balance'))
    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Balance (USD)')

    return fig

#route to make trades between bank and investing account for different users
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    db = get_db()
    bank_balance, investing_balance = get_user_balances(user_id)

    if request.method == 'POST':
        transfer_amount = float(request.form['amount'])
        transfer_from = request.form['transfer_from']
        transfer_to = request.form['transfer_to']

        #ensure transfer is between different accounts
        if transfer_from == transfer_to:
            flash('Invalid transfer: Please select different account.', 'transfer')
            return redirect(url_for('transfer'))

        #check if the transfer amount is valid
        if transfer_from == 'Bank Account' and transfer_amount <= bank_balance:
            new_bank_balance = bank_balance - transfer_amount
            new_investing_balance = investing_balance + transfer_amount
        elif transfer_from == 'Investing Account' and transfer_amount <= investing_balance:
            new_bank_balance = bank_balance + transfer_amount
            new_investing_balance = investing_balance - transfer_amount
        else:
            flash('Invalid transfer amount.', 'transfer')
            return redirect(url_for('transfer'))

        #change the user's balances in the database
        db.execute('UPDATE users SET bank_balance = ?, investing_balance = ? WHERE id = ?',
                   (new_bank_balance, new_investing_balance, user_id))
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('transfer.html', bank_balance=bank_balance, investing_balance=investing_balance)

#route to view all accounts usernames with hashed password for security
@app.route('/accounts')
def view_accounts():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return render_template('accounts.html', users=users)

#function to connect to SQlite database alternatively
def get_db_connection():
    conn = sqlite3.connect('flaskr.db')
    conn.row_factory = sqlite3.Row
    return conn

#route to track user transactions using get and post methods
@app.route('/track', methods=['GET', 'POST'])
def track():

    #makes sure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    db = get_db()

    #get account balances
    user = db.execute('SELECT bank_balance, investing_balance FROM users WHERE id = ?', (user_id,)).fetchone()
    bank_balance = user['bank_balance'] if user else 0
    investing_balance = user['investing_balance'] if user else 0

    #query all transactions, including the `id` field
    transactions = db.execute('SELECT id, description, amount, period, type FROM transactions WHERE user_id = ?',
                              (user_id,)).fetchall()

    #convert to dictionary format for template rendering
    transactions = [dict(row) for row in transactions]

    #render the track html template with all incomes/expenses
    return render_template('track.html', bank_balance=bank_balance, investing_balance=investing_balance, transactions=transactions)

#route to add new transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():

    #makes sure user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to add a transaction.", "error")
        return redirect(url_for('login'))

    #get form data for transaction to be added
    description = request.form.get('description')
    amount = request.form.get('amount')
    period = request.form.get('period')
    transaction_type = request.form.get('type')

    #makes sure data is inputted for all fields
    if not description or not amount or not period or not transaction_type:
        flash("All fields are required.", "error")
        return redirect(url_for('track'))

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO transactions (description, amount, period, type, user_id) VALUES (?, ?, ?, ?, ?)',
            (description, float(amount), period, transaction_type, user_id)
        )
        conn.commit()
    finally:
        conn.close()

    #return back to track html
    return redirect(url_for('track'))

#route to delete a existing expense/income by ID
@app.route('/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('track'))

#route to show form that allows you to make edits to transactions by ID
@app.route('/edit_transaction/<int:id>', methods=['GET'])
def edit_transaction_form(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (id,))
    cash_flow = cursor.fetchone()
    conn.close()

    #convert to a dictionary if using sqlite3.Row
    if cash_flow:
        cash_flow = dict(cash_flow)

    return render_template('edit_transaction.html', cash_flow=cash_flow)

#route to update income/expense after editing
@app.route('/update_transaction/<int:id>', methods=['POST'])
def update_transaction(id):
    description = request.form['description']
    amount = request.form['amount']
    period = request.form['period']
    transaction_type = request.form['type']  # Make sure this field exists in the form

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET description = ?, amount = ?, period = ?, type = ?
        WHERE id = ?
    """, (description, amount, period, transaction_type, id))
    conn.commit()
    conn.close()
    return redirect(url_for('track'))


#run application with debug mode for development
if __name__ == '__main__':
    app.run(debug=True)