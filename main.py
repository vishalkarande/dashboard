
import httpx
import threading
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
from flask_mysqldb import MySQL
# import MySQLdb.cursors
from flask import Blueprint, render_template
import time
import const.db as d
from const.login import login
import const.decorators as decorator

print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)
app.register_blueprint(login)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'




# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/')
@decorator.login_check
def login():
    render_template('index.html')


# logout API
@app.route('/logout/')
def logout():
    print("Logout called")
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)