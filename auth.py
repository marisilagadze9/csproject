import hashlib
from datetime import datetime
from storage import load_users, save_users, load_history, save_history

MAX_ATTEMPTS=5

def generate_salt(username):
    return hashlib.sha256(username.encode()).hexdigest()[:16]

def hash_password(username,password):
    salt=generate_salt(username)
    return hashlib.sha256((password+salt).encode()).hexdigest()



def register():
    users=load_users()
    username=input("Enter username:  ")

    if username in users:
        print("user already exists")
        return
    
    password=input("Enter password:  ")
    hashed=hash_password(username,password)

    users[username]={
        "password":hashed,
        "attempts":0,
        "blocked":False
    }

    save_users(users)
    print("Registration successful. ")

def log_in():
    users=load_users()
    history=load_history()

    username=input("Enter username:  ")

    if username not in users:
        print("User not found")
        return
    user=users[username]

    if user.get("blocked"):
        print("Account is blocked due to too many failed attempts.")
        return
    
    password=input("Enter password:  ")
    hashed=hash_password(username,password)

    if hashed==user["password"]:
        print("log in successfully")
        user["attempts"]=0

        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if username not in history:
            history[username]=[]

        history[username].append(now)

    else:
        user["attempts"]+=1
        print(f"Wrong password. Attempt {user['attempts']} of {MAX_ATTEMPTS}")
        if user["attempts"]>=MAX_ATTEMPTS:
            user["blocked"]=True
            print("Account blocked due to too many failed attempts.")

    save_users(users)
    save_history(history)

