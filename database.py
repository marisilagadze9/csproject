import sqlite3

db_name="users.db"

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    conn=get_connection()
    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        attempts INTEGER DEFAULT 0,
        blocked INTEGER DEFAULT 0
    )

""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS login_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)  
        )
""")
    
    conn.commit()
    conn.close()

    