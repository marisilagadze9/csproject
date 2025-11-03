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
    try:
      c.execute("ALTER TABLE login_history ADD COLUMN ip_address TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        c.execute("ALTER TABLE login_history ADD COLUMN success INTEGER;")
    except sqlite3.OperationalError:
        pass


    c.execute("""
    CREATE TABLE IF NOT EXISTS blocked_ips(
        ip_address TEXT PRIMARY KEY
    )
    """)
    
    conn.commit()
    conn.close()

    