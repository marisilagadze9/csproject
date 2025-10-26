import hashlib
from datetime import datetime
from storage import load_users, save_users, load_history, save_history
from database import get_connection

MAX_ATTEMPTS=5

def generate_salt(username):
    return hashlib.sha256(username.encode()).hexdigest()[:16]

def hash_password(username,password):
    salt=generate_salt(username)
    return hashlib.sha256((password+salt).encode()).hexdigest()



def register():
    conn=get_connection()
    c=conn.cursor()

    username=input("Enter username:  ")
    password=input("Enter password:   ")
    
    c.execute("SELECT* FROM users WHERE username=?",(username,))
    if c.fetchall():
        print("user already exists")
        conn.close()
        return
    
    hashed=hash_password(username,password)
    c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed))
    conn.commit()
    conn.close()
    print("Registration successful")


def log_in():
    conn=get_connection()
    c=conn.cursor()

    username=input("Enter username:  ")
    password=input("Enter password:  ")

    c.execute("SELECT * FROM users WHERE username=?",(username,))
    user=c.fetchone()

    if not user:
        print("User not found")
        conn.close()
        return
    db_username, db_password, attempts, blocked=user

    if blocked:
        print("Account is blocked")
        conn.close()
        return
    
    hashed=hash_password(username,password)

    if hashed==db_password:
        print("Log in successful")
        c.execute("UPDATE users SET attempts=0 WHERE username=?",(username,))
        c.execute("INSERT INTO login_history (username) VALUES (?)",(username,))
    else:
        attempts+=1
        print(f" Wrong password. Attempt {attempts}/{MAX_ATTEMPTS}")
        if attempts>=MAX_ATTEMPTS:
            print("Account blocked")
            c.execute("UPDATE users set blocked=1 WHERE  username=?",(username,))
        else:
            c.execute("UPDATE users SET attempts=? WHERE username=?",(attempts,username))
    conn.commit()
    conn.close()



