# importing packages
from os import access, name
from project.auth import is_architect_access
from project import userDetails, bcrypt
from flask import Blueprint, render_template, url_for, redirect, request, flash
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from project.database import dbs, mycursor
from project.utils import getSingleUser, getPages
import asyncio


# blueprint of the architect which needs to be imported to __init__.py
architect = Blueprint("architect", __name__, template_folder='templates')


@architect.route('/architect', methods=['POST', 'GET'])
@is_architect_access
def userarchitect():
    pages = getPages(current_user.id)

    if request.method == "POST":
        policies = request.form.getlist('policies')
        formname = request.form["formname"]
        scripts = request.form["scripts"]
        print(policies)
        print(formname)
        print(scripts)
        return redirect(url_for('home'))

    return render_template('architect.html', current_user=current_user, pages=pages)
