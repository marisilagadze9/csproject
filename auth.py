import hashlib
from datetime import datetime
from database import get_connection
from ip import checkip,blockip,get_ip

MAX_ATTEMPTS=5

def generate_salt(username):
    return hashlib.sha256(username.encode()).hexdigest()[:16]

def hash_password(username,password):
    salt=generate_salt(username)
    return hashlib.sha256((password+salt).encode()).hexdigest()

def register_user(username,password):
    conn=get_connection()
    c=conn.cursor()

    c.execute("SELECT*FROM users WHERE username=?",(username,))
    if c.fetchone():
        conn.close()
        return "User already exists"
    

    hashed=hash_password(username,password)
    c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed))
    conn.commit()
    conn.close()
    return "Registration successful"

def login_user(username,password):
    conn=get_connection()
    c=conn.cursor()
    ip=get_ip()

    if checkip(ip):
        conn.close()
        return f"Access denied: IP {ip} is blocked"
    
    c.execute("SELECT*FROM users WHERE username=?",(username,))
    user=c.fetchone()
    if not user:
        c.execute("INSERT INTO login_history (username,ip_address,success) VALUES (?,?,0)",(username,ip))
        conn.commit()
        conn.close()
        return "Wrong username or password"
    

    db_username,db_password,attempts,blocked=user
    if blocked:
        conn.close()
        return "Account is blocked"
    
    
    hashed=hash_password(username,password)
    if hashed==db_password:
        c.execute("UPDATE users SET attempts=0 WHERE username=?",(username,))
        c.execute("INSERT INTO login_history (username,ip_address,success) VALUES (?,?,1)",(username,ip))
        conn.commit()
        conn.close()
        return "Login successful"
    else:
        attempts+=1
        c.execute("INSERT INTO login_history (username,ip_address,success) VALUES (?,?,0)",(username,ip))
        if attempts>=MAX_ATTEMPTS:
            c.execute("UPDATE users SET blocked=1 WHERE username=?",(username,))
        c.execute("UPDATE users SET attempts=? WHERE username=?",(attempts,username))
        conn.commit()
        conn.close()
        blockip(ip)
        return "Wrong username or password"

def get_all_logins():
    conn=get_connection()
    c=conn.cursor()
    c.execute(
        """
        SELECT username,login_time,ip_address,success
        FROM login_history
        ORDER BY login_time DESC
        """
    )
    logs=c.fetchall()
    conn.close()
    return logs
