import sqlite3

def initialize_database():
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        qr_code TEXT UNIQUE NOT NULL
    );
    ''')

    # Scans table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')

    # Monthly counts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monthly_counts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        count INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    initialize_database()
