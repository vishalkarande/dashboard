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