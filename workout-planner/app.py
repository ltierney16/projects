import os
import sqlite3
import re

from datetime import datetime, timedelta

# FIX: load environment variables from a .env file (SENDGRID_API_KEY, SECRET_KEY).
# load_dotenv() must run before any code that reads os.environ.
from dotenv import load_dotenv
load_dotenv()

import matplotlib
matplotlib.use('Agg')  # Non-GUI backend; required for plotting from Flask request threads
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config
import json



import math
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


from flask import Flask, request, g, redirect, url_for, render_template, flash
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash



bp = Blueprint('auth', __name__, url_prefix='/auth')

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'workout_planner.db'),
    # FIX: read SECRET_KEY from the environment (.env) so it isn't hardcoded.
    # Falls back to 'development key' only if SECRET_KEY is not set.
    # Original line kept for reference, commented out:
    # SECRET_KEY='development key',
    SECRET_KEY=os.environ.get('SECRET_KEY', 'development key'),
))
app.config.from_envvar('WORKOUT_PLANNER_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/') # added method, even though it is default one, just to clarify for myself, that category form sends get request
def home():
    return render_template('home_page.html')


@app.route('/about_us') # added method, even though it is default one, just to clarify for myself, that category form sends get request
def about_us():
    return render_template('AboutUs.html')

@app.route('/features') # added method, even though it is default one, just to clarify for myself, that category form sends get request
def features():
    return render_template('features.html')

@app.route('/signup') # added method, even though it is default one, just to clarify for myself, that category form sends get request
def sign_up():
    return render_template('sign_up.html')

@app.route('/clear_notification_signup', methods=['POST'])
def clear_notification_signup():
    return render_template('sign_up.html')

@app.route('/login') # added method, even though it is default one, just to clarify for myself, that category form sends get request
def log_in():
    return render_template('login.html')



def validate_email(email):
    # Regular expression pattern for validating an email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
@app.route('/forgot_password')
def forgot_password():
    return  render_template('forgot_password.html')

@app.route('/valid_fp', methods =['POST'])
def valid_fp():
    username = request.form['username']
    email = request.form['email']
    db = get_db()
    cur = db.execute('select username, password, email,id from users order by id desc')
    users = cur.fetchall()

    # checks if the username and email the user inputted is already in the database and if not returns TypeNull
    match_user = db.execute('select username from users where username = ? and email = ?', [username,email]).fetchone()

    if match_user is None:
        flash('Did not find matching user or email.')
        return render_template('login.html')
    # Set your SendGrid API key
    api_key = os.environ.get('SENDGRID_API_KEY')

    #random value to add to the url and makes sure to have the username as a query parameter
    random_num = random.randint(100000,999999)
    url = url_for('fp_submit', _external=True, value= random_num, name=username)

    to_email = email  # Replace with the recipient's email
    subject = username + ' ' +'Forgot passwrd verification'
    print(url)
    content = (f'<a href= "{url}" target="_blank">Forgot Password</a>')
    # Create the email message
    message = Mail(
        from_email='jamarre67@gmail.com',  # Replace with your email
        to_emails=to_email,
        subject=subject,
        html_content=content)

    #adds user data to a database that keeps track of user's who are currently using forgot password
    db = get_db()
    cur = db.execute('select username,email,url,id from forgot_pass order by id desc')
    users = cur.fetchall()
    db.execute('insert into forgot_pass (username, email,url) values  (?, ?, ?)',[username,email,url])
    db.commit()
    print(cur)

    try:
        # Initialize the SendGrid client
        sg = SendGridAPIClient(api_key)

        # Send the email
        response = sg.send(message)

        # Print the response for debugging
        print(response.status_code)
        print(response.body)
        print(response.headers)
        flash('Sent Email')
        return 'Sent Email'
    except Exception as e:
        print(f"Error sending email: {e}")
        return 'False'

    # Example usage

@app.route('/fp_submit', methods=['GET'])
def fp_submit():
    user = (request.args.get('name'))
    print(user)

    #returns the user to the login page if they grabbed the link from someone else and to make sure others can change a user's password when they are done.
    db = get_db()
    #checks if user's name is in the database
    unique_user = db.execute('select username from forgot_pass where username = ?', [user]).fetchone()
    print(unique_user)
    if unique_user is None:
        flash('User not in Database')
        return render_template('login.html')

    # FIX (security): previously the reset link was accepted based on the username
    # alone, so anyone who knew a username could construct a working reset link
    # without the emailed token. Now we also verify that the 'value' token in the
    # URL matches the token stored when the reset email was sent.
    submitted_value = request.args.get('value')
    stored_row = db.execute('select url from forgot_pass where username = ?', [user]).fetchone()
    token_ok = False
    if stored_row is not None and submitted_value is not None:
        # The stored 'url' contains "value=<token>"; the link is valid only if the
        # submitted token is present in that stored url.
        token_ok = (f'value={submitted_value}' in stored_row['url'])
    if not token_ok:
        flash('Invalid or expired reset link.')
        return render_template('login.html')

    flash(unique_user)
    return render_template('forgot_pass_c.html',user = user)

@app.route('/fp_done', methods=['POST'])
def fp_done():
    db = get_db()
    password = request.form['password']
    password_c = request.form['password_c']
    cur = db.execute('select username,email,url,id from forgot_pass where username = ?', [request.form['name']])
    fp_db = cur.fetchone()

    # checks if the password is at least 8 characters and confirm password is matching the password you inputted
    if len(password) < 8:
        flash('Password needs to be at least 8 characters.')
        return render_template('forgot_pass_c.html')

    if password != password_c:
        flash("Passwords did not match")
        return render_template('forgot_pass_c.html')

    cur = db.execute('select * from users where username = ?', [request.form['name']])
    cur_user = cur.fetchone()

    db.execute('update users set password = ? where username = ?',
               [generate_password_hash(password), request.form['name']])
    db.commit()


    print(fp_db)
    #deletes user from forgot_pass database because they are no longer looking to change their password and makes the link invalid
    db.execute('delete from forgot_pass where username = ?', [request.form['name']])
    db.commit()
    flash('Changed Password')
    return render_template('login.html')


@app.route('/clear_notification_login', methods=['POST'])
def clear_notification_login():
    return render_template('login.html')




@app.route('/sign_up_submit', methods=['POST'])
def sign_up_submit():
    username = request.form['username']
    password = request.form['password']
    password_c = request.form['password_c']
    email = request.form['email']


    db = get_db()
    cur = db.execute('select username, password, email,id from users order by id desc')
    users = cur.fetchall()

    #checks if the username the user inputted is already in the database and if not returns TypeNull
    unique_user = db.execute('select username from users where username = ?', [username]).fetchone()

    if not validate_email(email):
        flash('Not a valid email')
        return render_template('sign_up.html')

    if unique_user is not None:
        flash('Not a unique username')
        return render_template('sign_up.html')
    #makes sure the user inputs information to create an account
    if username == '' or password == '' or email =='':
        flash("Did not fill out information")
        return render_template('sign_up.html')

    if len(password) < 8:
        flash('Password needs to be at least 8 characters.')
        return render_template('sign_up.html')

    if password != password_c:
        flash("Passwords did not match")
        return render_template('sign_up.html')

    #adds the user profile into the database while hashing their password for security
    db.execute('insert into users (username, password, email) values  (?, ?, ?)',
               [username, generate_password_hash(password),email])

    # create initial empty schedule for a day
    schedule = config.Schedule(None)
    encoded_schedule = json.dumps(schedule.schedule)

    # put the schedule into the schedule table in the db
    db.execute('insert into schedule (username, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) values (?, ?, ?, ?, ?, ?, ?, ?)',
               [username, encoded_schedule, encoded_schedule, encoded_schedule, encoded_schedule, encoded_schedule, encoded_schedule, encoded_schedule])
    db.commit()

    flash('Made New Account')
    return render_template('login.html', users = users)

@app.route('/login_submit', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    db = get_db()

    #if an error is found it will not login the user
    error = None
    user = db.execute('select * from users where username = ?', (username,)).fetchone()

    if user is None:
        print(user)
        error = "Invalid username!"
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password!'

    if error is None:

        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['experience'] = user['experience']
        session['goals'] = user['goals']
        # this is where you put where the user is going to go after they login
        if user['experience'] is None or user['goals'] is None or user['body'] is None or user['weight'] is None or user['height'] is None: # check if the user created profile
            flash('Successful Login')
            return redirect(url_for('experience_goals'))
        flash('Successful Login')
        return redirect(url_for('workout'))

    flash(error, "danger")
    return render_template('login.html')


@app.route('/experience_and_goals', methods=["GET", "POST"])
def experience_goals():
    return render_template('experience_and_goals.html')


@app.route('/experience_and_goals_submit', methods=['GET', 'POST'])
def experience_goals_submit():
   db = get_db()
   experience = request.form.get('experience')
   goals = request.form.get('goals')
   frequency = request.form.get('frequency')
   day_part = request.form.get('day_part')


   if not experience:
       flash('Select Fields')
       return render_template('experience_and_goals.html')
   if experience == 'highly_experienced':
       db.execute('update users set experience = 3 where id = (?)', [session['user_id']])
   if experience == 'not_experienced':
       db.execute('update users set experience = 1 where id = (?)', [session['user_id']])
   if experience == 'some_experience':
       db.execute('update users set experience = 2 where id = (?)', [session['user_id']])
   #flash('Experience has been saved successfully')


   if not goals:
       flash('Select Fields')
       return render_template('experience_and_goals.html')
   if goals == 'gain_muscle':
       db.execute('update users set goals = 1 where id = (?)', [session['user_id']])
   if goals == 'gain_weight':
       db.execute('update users set goals = 2 where id = (?)', [session['user_id']])
   if goals == 'lose_weight':
       db.execute('update users set goals = 3 where id = (?)', [session['user_id']])
   if goals == 'lose_weight_gain_muscle':
       db.execute('update users set goals = 4 where id = (?)', [session['user_id']])
   if goals == 'recovery':
       db.execute('update users set goals = 5 where id = (?)', [session['user_id']])
   #flash('Goals have been saved successfully')

   #flash("Proceed to the next section")




   if not frequency:
       return render_template('experience_and_goals.html')
   else:
       db.execute('update users set frequency = ? where id = (?)', [frequency, session['user_id']])
       #flash("Frequency has been saved successfully")


   if not day_part:
       return render_template('experience_and_goals.html')
   else:
       db.execute('update users set part_of_the_day = (?) where id = (?)', [day_part, session['user_id']])
       #flash("Best time has been saved successfully")

   #flash("Proceed to the next section")
   db.commit()


   #go to the init_schedule route after saving
   return redirect(url_for('init_schedule'))


@app.route('/init_schedule', methods=['POST', 'GET'])
def init_schedule():
    db = get_db()
    username = session['username']
    user_id = session['user_id']
    week_tasks = []

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # get all tasks for a week from the schedule
    for day in days:
        encoded_daily_schedule = db.execute(f"select {day} from schedule where id = ?", [user_id]).fetchone()[0] # get the daily schedule from the db
        decoded_daily_schedule = json.loads(encoded_daily_schedule) # decode the schedule using loads function from json
        new_obj = config.Schedule(decoded_daily_schedule) # create new Schedule class object based on the data structure we got from the db
        all_tasks = new_obj.get_all_tasks() # get all tasks from the schedule using the get_all_tasks() method of the class

        if len(all_tasks) > 0:
            week_tasks.append((day, all_tasks))
        else:
            week_tasks.append((day, None))

    return render_template("init_schedule.html", days=week_tasks)



@app.route('/init_schedule_submit', methods=['POST'])
def init_schedule_submit():
    user_id = session['user_id']
    days = request.form.getlist('day') # get the selected days
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    task = request.form.get('task')

    db = get_db()
    for day in days:
        # FIX (security): 'day' comes from user-submitted form data and is
        # interpolated into the SQL string below (column names cannot be passed
        # as bound parameters). To prevent SQL injection, only allow 'day' values
        # that exactly match a known weekday column name.
        if day not in week_days:
            flash('Invalid day selected.')
            continue
        schedule_encoded = db.execute(f'select {day} from schedule where id = ? ', [user_id]).fetchone()[0] # get the schedule for the selected day
        schedule_decoded = json.loads(schedule_encoded) # decode the data structure using json.loads() function
        new_schedule = config.Schedule(schedule_decoded) # create new object of the Schedule class and pass the decoded schedule there
        new_schedule.add_task(task, start_time, end_time) # call the method to add the task to the schedule
        encode_new_schedule = json.dumps(new_schedule.schedule) # encode new schedule using json.dumps() function
        db.execute(f"update schedule set {day} = ? where id = ?", [encode_new_schedule, user_id]) # update the schedule table in the db

    db.commit()

    return redirect(url_for('init_schedule'))


@app.route('/body_parameters', methods=['GET', 'POST'])
def body_parameters():
    db = get_db()
    if request.method == 'GET':
        # Render the body parameters form for the user to input data
        return render_template('body_parameters.html')

    # Handle the POST request to process the data
    weight = request.form.get('weight')
    height = request.form.get('height')
    body_type = request.form.get('body_type')

    if not weight or not height or not body_type:
        flash('All fields are required')
        return render_template('body_parameters.html')

    weight = float(weight)
    height = float(height)
    if weight < 30 or weight > 300 or height < 1.0 or height > 2.5:
        flash('Enter valid values for weight and height')
        return render_template('body_parameters.html')

    db.execute('update users set weight = ?, height = ?, body = ? where id = ?',
               [weight, height, body_type, session['user_id']])
    db.commit()
    flash('Responses saved successfully')

    return redirect(url_for('review_responses'))


@app.route('/review_responses', methods=['GET'])
def review_responses():
    db = get_db()
    # Fetch updated user data
    user_data = db.execute(
        'SELECT weight, height, body, experience, goals, frequency, part_of_the_day FROM users WHERE id = ?',
        [session['user_id']]
    ).fetchone()

    # Map experience, goals, and preferred time to readable strings
    experience_mapping = {1: 'Not Experienced', 2: 'Some Experience', 3: 'Highly Experienced'}
    goals_mapping = {
        1: 'Gain Muscle/Bulk', 2: 'Gain Weight', 3: 'Lose Weight',
        4: 'Lose Weight and Gain Muscle', 5: 'Recovery'
    }
    preferred_time_mapping = {1: 'First part (Morning-Afternoon)', 2: 'Second part (Afternoon-Evening)', 3: 'Any part of the day'}

    # map the experience to a value or default to 'n/a'
    if user_data['experience'] is not None:
        experience_key = int(user_data['experience'])
        experience_value = experience_mapping.get(experience_key)
    else:
        experience_value = 'N/A'

    # Fetch and decode the schedule
    username = session.get('username')
    schedule_data = db.execute("SELECT * FROM schedule WHERE username = ?", (username,)).fetchone()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_tasks = []

    if schedule_data:
        user_id = session['user_id']
        for day in days_of_week:
            encoded_schedule = db.execute(f"SELECT {day} FROM schedule WHERE id = ?", [user_id]).fetchone()[0]
            if encoded_schedule:
                # Decode schedule and fetch tasks using the Schedule class
                decoded_schedule = json.loads(encoded_schedule)
                schedule_object = config.Schedule(decoded_schedule)
                tasks = schedule_object.get_all_tasks()
                weekly_tasks.append((day, tasks if tasks else "No tasks scheduled"))
            else:
                weekly_tasks.append((day, "No tasks scheduled"))
    else:
        weekly_tasks = [(day, "No tasks scheduled") for day in days_of_week]

    # Render the confirmation page with the fetched data
    return render_template(
        'confirmation_body_params.html',
        weight=user_data['weight'],
        height=user_data['height'],
        body_type=user_data['body'],
        experience=experience_value,
        goals=goals_mapping.get(user_data['goals']),
        frequency=user_data['frequency'],
        day_part=preferred_time_mapping.get(user_data['part_of_the_day']),
        weekly_schedule=weekly_tasks
    )


def create_workout(experience, goals):
    db = get_db()

    recommended = db.execute("select * from workout where experience = ? or goals = ?", [experience, goals]).fetchall()
    workouts = []
    wk = []

    for workout in range(len(recommended)):
        for name in recommended[workout]:
            wk.append(name)


        workouts.append(wk)
        wk = []

    print(workouts)


@app.route('/save_notes', methods=['POST'])
def save_notes():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    day = request.form.get('day')
    notes = request.form.get('notes', '')

    if day not in week_days:
        flash('Invalid day.')
        return redirect(url_for('workout'))

    db = get_db()
    row = db.execute(
        'SELECT id FROM workout_log WHERE user_id = ? AND day_name = ?',
        [user_id, day]
    ).fetchone()
    if row is None:
        flash('Log a workout for that day before adding notes.')
    else:
        db.execute('UPDATE workout_log SET notes = ? WHERE id = ?', [notes, row['id']])
        db.commit()
        flash('Notes saved.')

    return redirect(url_for('workout'))


@app.route('/workout')
def workout():
    if session['user_id']:

        db = get_db()

        exp_goals = db.execute('select experience, goals from users where id = ?', [session['user_id']]).fetchall()

        create_workout(exp_goals[0][0], exp_goals[0][1])

        today = datetime.now().strftime('%A')

        user_id = session['user_id']
        logs = db.execute(
            'SELECT day_name, start_time, end_time, weight_kg, notes '
            'FROM workout_log WHERE user_id = ?',
            [user_id]
        ).fetchall()

        day_info = {}
        for log in logs:
            day = log['day_name']
            if not day:
                continue
            summary_parts = []
            if log['start_time'] is not None and log['end_time'] is not None:
                try:
                    duration = int(log['end_time']) - int(log['start_time'])
                    if duration < 0:
                        duration = 0
                    summary_parts.append(f"{duration} min")
                except (ValueError, TypeError):
                    pass
            if log['weight_kg'] is not None:
                summary_parts.append(f"{log['weight_kg']}kg")
            summary = "Worked out: " + ", ".join(summary_parts) if summary_parts else "Worked out"
            day_info[day] = {'summary': summary, 'notes': log['notes'] or ''}

        return render_template('user_homepage.html', days=week_days, today=today, day_info=day_info)

@app.route('/schedule')
def schedule():

    #make sure user is logged in and use that users data
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        flash("User not found.")
        return redirect(url_for('login'))

    #number of days user said they want to work out
    frequency = user['frequency']

    #time preference, morning=1, afternoon=2, no preference=3
    day_part = user['part_of_the_day']

    #days of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # map preferred part of the day to a recommended start time
    # day_part: 1 = Morning-Afternoon, 2 = Afternoon-Evening, 3 = Any part of day
    recommended_time_by_part = {
        1: "8:00 AM",     # morning
        2: "5:00 PM",     # evening
        3: "12:00 PM",    # midday (no preference)
    }
    rec_time = recommended_time_by_part.get(day_part, "12:00 PM")

    # helper: convert a 24-hour "HH : MM - HH : MM" range into 12-hour AM/PM
    def to_ampm_range(time_range):
        def one(hhmm):
            hh, mm = hhmm.strip().split(':')
            h = int(hh)
            m = int(mm)
            suffix = 'AM' if h < 12 else 'PM'
            display_h = h % 12
            if display_h == 0:
                display_h = 12
            return f"{display_h}:{m:02d} {suffix}"
        try:
            start_raw, end_raw = time_range.split('-')
            return f"{one(start_raw)} - {one(end_raw)}"
        except Exception:
            return time_range

    # read each day's existing commitments (conflicts) from the schedule table
    conflicts_by_day = {}
    user_id = user['id']
    for day in days_of_week:
        row = db.execute(f"SELECT {day} FROM schedule WHERE id = ?", [user_id]).fetchone()
        if row and row[0]:
            decoded = json.loads(row[0])
            tasks = config.Schedule(decoded).get_all_tasks()
            tasks = [(title, to_ampm_range(time_range)) for (title, time_range) in tasks]
        else:
            tasks = []
        conflicts_by_day[day] = tasks

    # decide how many workout days to assign
    try:
        num_days = int(frequency) if frequency is not None else 0
    except (ValueError, TypeError):
        num_days = 0
    num_days = max(0, min(num_days, 7))  # clamp to 0-7

    # choose which days get a workout: weekdays first, least-busy first
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend = ["Saturday", "Sunday"]
    weekdays_sorted = sorted(weekdays, key=lambda d: len(conflicts_by_day.get(d, [])))
    weekend_sorted = sorted(weekend, key=lambda d: len(conflicts_by_day.get(d, [])))
    priority_order = weekdays_sorted + weekend_sorted
    workout_days = set(priority_order[:num_days])

    # build the rows the template will render: (day, rec_time_or_None, conflicts)
    week_schedule = []
    for day in days_of_week:
        workout_time = rec_time if day in workout_days else None
        week_schedule.append((day, workout_time, conflicts_by_day.get(day, [])))

    return render_template('schedule.html', week_schedule=week_schedule)

@app.route('/modify_schedule', methods=['POST'])
def modify_schedule():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    day = request.form.get('day')
    new_start_time = request.form.get('new_start_time')
    new_end_time = request.form.get('new_end_time')
    new_title = request.form.get('new_title')

    # FIX (security): 'day' comes from user-submitted form data and is interpolated
    # into the SQL strings below. Whitelist it against known weekday names to
    # prevent SQL injection.
    if day not in week_days:
        flash('Invalid day selected.')
        return redirect(url_for('schedule'))

    db = get_db()

    # Fetch the current schedule for the user
    cur = db.execute("SELECT * FROM schedule WHERE username = ?", (username,))
    schedule_data = cur.fetchone()

    # Update the specific day's task
    if schedule_data[day]:
        updated_task = f"Title: {new_title}, Start: {new_start_time}, End: {new_end_time}; \n"
    else:
        updated_task = f"Title: {new_title}, Start: {new_start_time}, End: {new_end_time}; \n"

    db.execute(f"UPDATE schedule SET {day} = ? WHERE username = ?", (updated_task, username))
    db.commit()

    flash('Schedule updated successfully')
    return redirect(url_for('schedule'))


@app.route('/progress', methods=['GET'])
def progress():
    db = get_db()
    if session['user_id']:
        selected_workout = request.args.get('workout', '').lower()
        print(selected_workout)

        if selected_workout:
            # Fetch workout details for the selected muscle group
            query = '''
                    SELECT workout_name, time_minutes, user_weight_kg
                    FROM workout
                    WHERE LOWER(muscle) = LOWER(?)
                    ORDER BY id DESC
                '''
            cur = db.execute(query, [selected_workout])
        else:
            # Fetch all workout details grouped by muscle
            query = '''
                    SELECT muscle, workout_name, time_minutes, user_weight_kg
                    FROM workout
                    ORDER BY muscle, id DESC
                '''
            cur = db.execute(query)

        exercises = cur.fetchall()



        # Load workout data into a Pandas DataFrame
        df = pd.read_sql("SELECT * FROM workout", db)

        # Fetch the unique muscle groups from the data
        muscle_groups = df['muscle'].unique()

        # Initialize a list to store plot image paths
        plots = []

        # FIX: the static/plots/ folder is git-ignored and will not exist on a
        # fresh checkout, which caused plt.savefig() below to raise
        # FileNotFoundError. Create it (no-op if it already exists) before saving.
        os.makedirs('static/plots', exist_ok=True)

        # Determine which muscle groups to plot based on the selected workout
        if selected_workout == "all" or not selected_workout:
            muscle_groups_to_plot = muscle_groups
        else:
            muscle_groups_to_plot = [selected_workout]

        # Generate line plots for the selected muscle groups
        for muscle_group in muscle_groups_to_plot:
            # Filter the DataFrame for the current muscle group
            muscle_group_df = df[df['muscle'].str.lower() == muscle_group.lower()]

            # Generate a line plot for each exercise in the muscle group
            exercises_in_group = muscle_group_df['workout_name'].unique()

            for exercise in exercises_in_group:
                exercise_df = muscle_group_df[muscle_group_df['workout_name'] == exercise]

                plt.figure(figsize=(14, 8))
                sns.lineplot(x='time_minutes', y='user_weight_kg', data=exercise_df, marker='o')
                plt.title(f'Weight Progression for {exercise} ({muscle_group.capitalize()})')
                plt.xlabel('Time')
                plt.ylabel('Weight (kg)')
                plt.grid(axis='y')

                # Save the plot image
                plot_filename = f'static/plots/{muscle_group.lower()}_{exercise.lower().replace(" ", "_")}_progression.png'
                plt.savefig(plot_filename)
                plt.close()

                # Add the plot file path to the list
                plots.append(plot_filename)

            # Render the progress layout template with the plots and exercises
        return render_template('progress_layout.html',
                               selected_workout=selected_workout,
                               exercises=exercises,
                               plots=plots)


@app.route('/profile')
def profile():
    if session['user_id']:
        db = get_db()
        cur = db.execute('select * from users where id = ?',[session['user_id']])
        cur_user = cur.fetchone()

        #because the inputs for goals and experience are integers we have to compare the number to display text on the user profile settings
        goal = cur_user["goals"]
        # FIX: the original chain used separate `if` statements with a single
        # trailing `else`, so the `else` only attached to the last `if` (goal == 4).
        # That meant goals 1-3 were set correctly and then immediately overwritten
        # to 'recovery'. Converted to a proper if/elif chain.
        # Original (buggy) code kept for reference, commented out:
        # if goal == 1:
        #     goal_text = 'gain muscle'
        # if goal == 2:
        #     goal_text = 'gain_weight'
        # if goal == 3:
        #     goal_text = 'lose_weight'
        # if goal == 4:
        #     goal_text = 'lose_weight_gain_muscle'
        # else:
        #     goal_text = 'recovery'
        if goal == 1:
            goal_text = 'gain muscle'
        elif goal == 2:
            goal_text = 'gain_weight'
        elif goal == 3:
            goal_text = 'lose_weight'
        elif goal == 4:
            goal_text = 'lose_weight_gain_muscle'
        else:
            goal_text = 'recovery'
        cur_experience = cur_user["experience"]
        # FIX: same if/else bug as above — experience 3 and 1 were always
        # overwritten to 'some_experience'. Converted to a proper if/elif chain.
        # Original (buggy) code kept for reference, commented out:
        # if cur_experience == 3:
        #     experience_text = 'highly_experienced'
        # if cur_experience == 1:
        #     experience_text = 'not_experienced'
        # else:
        #     experience_text = 'some_experience'
        if cur_experience == 3:
            experience_text = 'highly_experienced'
        elif cur_experience == 1:
            experience_text = 'not_experienced'
        else:
            experience_text = 'some_experience'

        flash('Entering Profile')
        return render_template('user_profile.html', cur_user = cur_user, goal_text = goal_text, cur_experience = experience_text)



@app.route('/logout')
def logout():
    return redirect(url_for('home'))
@app.route('/change_password', methods=['POST'])
def change_password():
    return render_template('change_password.html')

@app.route('/profile_redo_info', methods=["POST"])
def profile_redo_info():
    db = get_db()
    cur = db.execute('select * from users where id = ?', [session['user_id']])
    cur_user = cur.fetchone()
    flash('redo information here')
    return render_template('redo_user_info.html', cur_user = cur_user)
@app.route('/submit_change', methods=['POST'])
def submit_change():
    db = get_db()
    experience =  request.form['experience']
    goals = request.form['goals']

    # inputs a number into the database based on what the user selected.
    if experience == 'highly_experienced':
        experience = 3
    if experience == 'not_experienced':
        experience = 1
    if experience == 'some_experience':
       experience = 2

    if goals == 'gain_muscle':
        goals = 1
    if goals == 'gain_weight':
        goals = 2
    if goals == 'lose_weight':
        goals = 3
    if goals == 'lose_weight_gain_muscle':
       goals = 4
    if goals == 'recovery':
       goals = 5

    cur = db.execute('select * from users where id = ?', [session['user_id']])
    cur_user = cur.fetchone()

    #checks that the email is formatted correctly
    if not validate_email(request.form['email']):
        flash('Not a valid email')
        return render_template('redo_user_info.html',cur_user = cur_user)

    #checks if the username is valid if the user is changing their username
    unique_user = db.execute('select username from users where username = ?', [request.form['username']]).fetchone()
    if request.form['username'] != session['username']:
        if unique_user is not None:
            flash('Not a unique username')
            return render_template('redo_user_info.html', cur_user=cur_user)

    cur = db.execute('update users set username = ?, email = ?,experience = ?, goals = ?, body = ?, weight = ?, height = ? where id like ? ', [request.form['username'],
                    request.form['email'],experience,goals, request.form['body_type'],request.form['weight'],request.form['height'],session['user_id']])
    cur_user = cur.fetchone()
    db = get_db()
    cur = db.execute('select * from users where id = ?', [session['user_id']])
    cur_user = cur.fetchone()
    db.commit()

    #text to display on profile settings based on newly inputted user information
    if goals == 1:
        goal_text = 'gain muscle'
    if goals == 2:
        goal_text = 'gain_weight'
    if goals == 3:
        goal_text = 'lose_weight'
    if goals == 4:
        goal_text = 'lose_weight_gain_muscle'
    if goals == 5:
        goal_text = 'recovery'

    if experience == 3:
        experience_text = 'highly_experienced'
    if experience == 1:
        experience_text = 'not_experienced'
    if experience == 2:
        experience_text = 'some_experience'
    session['username'] = cur_user['username']
    flash('successful change')
    return render_template('user_profile.html', cur_user=cur_user,goal_text = goal_text, cur_experience = experience_text)

@app.route('/submit_pass', methods=['POST'])
def submit_pass():
    password = request.form['password']
    password_c = request.form['password_c']
    db = get_db()

    #checks if the password is at least 8 characters and confirm password is matching the password you inputted
    if len(password) < 8:
        flash('Password needs to be at least 8 characters.')
        return render_template('change_password.html')

    if password != password_c:
        flash("Passwords did not match")
        return render_template('change_password.html')

    cur = db.execute('select * from users where id = ?', [session['user_id']])
    cur_user = cur.fetchone()

    db.execute('update users set password = ? where username = ?', [generate_password_hash(password), session['username']])
    db.commit()
    flash('pass changed')
    return render_template('user_profile.html', cur_user = cur_user)

@app.route('/current-workout', methods=['GET', 'POST'])
def current_workout():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    db = get_db()
    user_id = session['user_id']

    # Fetch current workout exercises
    query = '''
        SELECT id, workout_name, muscle, weighted
        FROM workout
        WHERE user_id = ? AND is_current = 1
        ORDER BY id ASC
    '''
    cur = db.execute(query, [user_id])
    current_workouts = cur.fetchall()

    today = datetime.now().strftime('%Y-%m-%d')
    already_row = db.execute(
        'SELECT id FROM workout_log WHERE user_id = ? AND log_date = ?',
        [user_id, today]
    ).fetchone()
    already_logged_today = already_row is not None

    return render_template('workout_button.html',
                           current_workouts=current_workouts,
                           already_logged_today=already_logged_today)



@app.route('/save-current-workout', methods=['POST'])
def save_current_workout():
    if 'user_id' not in session:
        return redirect('/login')

    # FIX: the block below was originally indented INSIDE the `if 'user_id' not in
    # session:` branch, which made all of the save logic unreachable (it only ran
    # when the user was NOT logged in, after a return) and left `updated_workouts`
    # undefined for the final render. De-indented one level so it runs for
    # logged-in users as intended.
    db = get_db()
    user_id = session['user_id']
    data = request.form  # Form data

    # Update the database with time and weight for each exercise
    for key, value in data.items():
        if key.startswith('time-') or key.startswith('weight-'):
            workout_id = key.split('-')[1]  # Extract workout ID
            if value:  # Only update if the value is not empty
                if key.startswith('time-'):
                    db.execute(
                        '''
                        UPDATE workout 
                        SET time_minutes = ? 
                        WHERE id = ? AND user_id = ?
                        ''',
                        (value, workout_id, user_id)
                    )
                elif key.startswith('weight-'):
                    db.execute(
                        '''
                        UPDATE workout 
                        SET user_weight_kg = ? 
                        WHERE id = ? AND user_id = ?
                        ''',
                        (value, workout_id, user_id)
                    )

    db.commit()  # Save changes to the database

    user_id = session['user_id']
    today = datetime.now().strftime('%Y-%m-%d')
    already_row = db.execute(
        'SELECT id FROM workout_log WHERE user_id = ? AND log_date = ?',
        [user_id, today]
    ).fetchone()

    if already_row is None:
        start_time = data.get('time-1')
        end_time = data.get('time-2')
        weight = data.get('weight-1')
        day_name = datetime.now().strftime('%A')
        db.execute(
            'INSERT INTO workout_log (user_id, log_date, day_name, start_time, end_time, weight_kg) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            [user_id, today, day_name, start_time or None, end_time or None, weight or None]
        )
        db.commit()
        flash('Workout logged for today!')
    else:
        flash('You already worked out today.')

    already_logged_today = True

    query = '''
            SELECT workout_name, muscle, weighted, video, time_minutes, user_weight_kg 
            FROM workout 
            WHERE user_id = ? AND is_current = 1
            ORDER BY id ASC
        '''
    updated_workouts = db.execute(query, (user_id,)).fetchall()

    return render_template('workout_button.html',
                           current_workouts=updated_workouts,
                           already_logged_today=already_logged_today)


@app.route('/logo_button1', methods=['GET'])
def logo_button1():
    if session['user_id']:
        return render_template('user_homepage.html')

@app.route('/logo_button2', methods=['GET'])
def logo_button2():
    return render_template('home_page.html')