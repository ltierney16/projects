DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    bank_balance REAL DEFAULT 10000.0,
    investing_balance REAL DEFAULT 0.0
);

DROP TABLE IF EXISTS transactions;

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
