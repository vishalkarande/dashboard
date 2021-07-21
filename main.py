import asyncio 
import httpx
import threading
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from celery import Celery
import time


print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route("/toy", methods=["GET"])
def test():
    print(f"Inside flask function: {threading.current_thread().name}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop1 = asyncio.get_event_loop()
    result = loop1.run_until_complete(hello())
    print('Hello Here')
    
    return jsonify({"result": result})



@celery.task
def send_async_email():
    """Dummy Wait."""
    time.sleep(10)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
    

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


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

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print('HERE')
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['user_type'] = account['user_type']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/profile' , methods=['GET', 'POST'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        
        if request.method == 'POST' and 'username' in request.form and 'fullname' in request.form and 'email' in request.form:
              # Create variables for easy access
             username = request.form['username']
             fullname = request.form['fullname']
             email = request.form['email']
             age = request.form['age']
             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cursor.execute("UPDATE accounts SET username=%s, fullname=%s, email=%s, age=%s WHERE id=%s", (username, fullname, email, age, session['id']))
             mysql.connection.commit()
             msg = 'You have profile updated!'
             send_async_email.delay()
             return redirect(url_for('profile'))
        elif request.method == 'POST':
             # Form is empty... (no POST data)
             msg = 'Please fill out the form!'
             return redirect(url_for('profile'))
        return render_template('profile.html', account=account )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/async', methods=['GET', 'POST'])
async def async_form():
     start = time.time()
     
     data = {
            "userId" : 1,
            "id":1,
            "title" :'kdwkkwdk',
            "body" : 'jqwjejqwej'
        }
     
     async with httpx.AsyncClient() as client:
            users, postUsers, get_post = await asyncio.gather(
                client.get(f'https://jsonplaceholder.typicode.com/posts', timeout=None),
                client.post(f'https://jsonplaceholder.typicode.com/posts', data=data),
                client.get(f'https://jsonplaceholder.typicode.com/posts/1')
            )
     
     if 1 in users.json() :
         print(users.json())
         return users.json()
         
            
     end = time.time()
     print(end - start)
     return render_template('async.html', msg='Hello')
 
 
@app.route('/sync', methods=['GET', 'POST'])
async def sync_form():
     start = time.time()
     
     data = {
            "userId" : 1,
            "id":1,
            "title" :'kdwkkwdk',
            "body" : 'jqwjejqwej'

        }
     users = httpx.get(f'https://jsonplaceholder.typicode.com/posts', timeout=None)
     post_users = httpx.post(f'https://jsonplaceholder.typicode.com/posts', data=data)
     get_users =  httpx.get(f'https://jsonplaceholder.typicode.com/posts/1', timeout=None)
     
     print(users)
     print(post_users)
     print(get_users)
     
         
            
     end = time.time()
     print(end - start)
     return render_template('async.html', msg='Hello')




if __name__ == "__main__":
    app.run(debug=True)