# importing packages
from os import access, name
from project import userDetails
from flask import Blueprint, render_template, url_for, redirect, request, flash
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import asyncio
from project.utils import getPages


# blueprint of the auth which needs to be imported to __init__.py
auth = Blueprint("auth", __name__, template_folder='templates')


# check if user has admin access if yes then pass admin as parameter
def is_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        access = ""
        print(func.__name__)
        if current_user.type == "admin":
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home'))

    return inner


def is_architect_access(func):
    @wraps(func)
    def inner(*args, **kwargs):
        access = False
        pageAccess = getPages(current_user.id)
        if pageAccess['architect'] == 1:
            access = True
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return inner


# route for login
@auth.route("/login", methods=["GET", "POST"])
def login():
    msg = ''

    # when user gave username and password
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        email = request.form.get("username")
        password = request.form.get("password")

        # if this returns a user, then the email already exists in database
        user = userDetails.query.filter_by(email=email).first()
        print(user)

        # if user not present or wrong password flash message and let user try again
        if user == None or not user.check_password(password):
            flash("Email Not registered or wrong password")
            msg = "Some Error occured"

        else:

            # login the user
            login_user(user)
            flash("Login Successful")

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get("next")

            # So let's now check if that next exists, otherwise we'll go to
            # the profile page.
            if next == None or not next[0] == "/":
                next = url_for("home")

            return redirect(next)

    # if user entered wrong password or email then return to login with  error msg
    return render_template("login.html", msg=msg)


# route for loging out the user
@auth.route('/logout')
@login_required
def logout():

    # logout the user
    logout_user()
    print("logout success")

    # return to the home page after logining out
    return redirect(url_for('home'))
