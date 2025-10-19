import json
import os

USERS_FILE="users.json"
HISTORY_FILE="login_history.json"

def load_json(path):
    if os.path.exists(path):
        if os.path.getsize(path)==0:
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_json(path,data):
    with open(path,"w") as f:
        json.dump(data,f,indent=4)

def load_users():
    return load_json(USERS_FILE)

def save_users(users):
    save_json(USERS_FILE,users)

def load_history():
    return load_json(HISTORY_FILE)

def save_history(history):
    save_json(HISTORY_FILE,history)