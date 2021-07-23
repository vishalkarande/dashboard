from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
import const.db as d
from functools import wraps

def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'loggedin' in session:
            return redirect(url_for("home"))
        else:
            return render_template('index.html')
    return decorated_function

def getUser(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'loggedin' in session:
            if session['user_type']== 'admin':
                d.mycursor.execute("select * from login")
                user = d.mycursor.fetchall()
                return  f(user, *args, **kws)
        else:
            return render_template('index.html')
    return decorated_function


# Get Single user data to edit
def getUserdata(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'loggedin' in session and session['user_type']== 'admin':
            d.mycursor.execute("select * from login where id='%d'" % id)
            userdata = d.mycursor.fetchall()
            return  f(userdata, *args, **kws)
        else:
            return render_template('index.html')
    return decorated_function