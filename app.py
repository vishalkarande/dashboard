# importing packages
from os import access, name
from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from project import db, app
from project.auth import is_admin
from project.utils import getAllUsers, getTotalUsers

# route for home


@app.route('/')
@login_required
def home():
    # get all users ount to be shown on homepage
    count = getTotalUsers()
    return render_template('home.html', current_user=current_user, user_count=count)


# route for admin to access all users details
@app.route('/allusers/')
@login_required
@is_admin
def users():
    # get all users  details from database in users
    users = getAllUsers()
    return render_template('allusers.html', current_user=current_user, users=users)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
