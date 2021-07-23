from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
import const.db as d
from functools import wraps
import const.decorators as decorator
import asyncio


login = Blueprint('login', __name__,template_folder='templates')


@login.route('/loginuser/', methods=['GET', 'POST'])
async def userlogin():
    print("Login hit")
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        d.mycursor.execute('SELECT * FROM login WHERE email = %s AND password = %s', (username, password,))
        account = d.mycursor.fetchone()
        # If account exists in accounts table in out database
        print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['email'] = account[2]
            session['user_type'] = account[4]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)



@login.route('/adduser/', methods=['GET', 'POST'])
async def adduser():
    print("adduser hit")
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        d.mycursor.execute(
                "INSERT INTO login (name, email, password) VALUES (%s,%s,%s)", (name, email, password))
        d.mydb.commit()
        l_id = d.mycursor.lastrowid
        print(l_id)
        dev = 0
        d.mycursor.execute(
            "INSERT INTO `page_access`( `u_id`, `developer`) VALUES (%s,%s)", (l_id, dev))
        d.mydb.commit()

        # If account exists in accounts table in out database
        return redirect(url_for('user'))
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)



