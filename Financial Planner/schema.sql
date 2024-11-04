-- drop users table if it already exists
DROP TABLE IF EXISTS users;

-- table to store user account information by ID
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    bank_balance REAL DEFAULT 10000.0,
    investing_balance REAL DEFAULT 0.0
);

-- drop transaction table if it already exists
DROP TABLE IF EXISTS transactions;

-- table to store transactions for each user by ID
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    period TEXT NOT NULL,
    type TEXT CHECK(type IN ('Income', 'Expense')),
    user_id INTEGER,
    date TEXT DEFAULT (date('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
