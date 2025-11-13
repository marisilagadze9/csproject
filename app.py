from flask import Flask, render_template, request
from auth import register_user, login_user, get_all_logins
from database import init_db
from dotenv import load_dotenv
import os

load_dotenv()
app=Flask(__name__)

admin_username=os.environ['ADMIN_USERNAME']
admin_password=os.environ['ADMIN_PASSWORD']

init_db()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        message=register_user(username,password)
        return render_template('register.html',message=message)
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        message=login_user(username,password)
        return render_template('login.html',message=message)
    return render_template('login.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username!=admin_username or password!=admin_password:
            return render_template('admin.html', message="Access Denied")
        logs = get_all_logins()
        return render_template('admin.html', logs=logs)
    return render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)

