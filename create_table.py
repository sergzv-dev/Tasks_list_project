import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL CHECK(length(task) > 0),
    done BOOL NOT NULL DEFAULT 0,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL CHECK (role IN ('admin', 'user')) DEFAULT 'user',
    user_name TEXT NOT NULL UNIQUE CHECK(length(user_name) > 0),
    hash_pass NOT NULL
);
''')