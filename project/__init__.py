# importing packages
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, UserMixin, current_user
from flask_bcrypt import Bcrypt
from functools import wraps
#import mysql.connector


bcrypt = Bcrypt()


# current directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# Application instance
app = Flask(__name__)

# app secret key
app.config["SECRET_KEY"] = "newkey"

# connect our app with database
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root@localhost/flaskdatabase"

# don't track every database modification
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# create instance of db
db = SQLAlchemy(app)
Migrate(app, db)

# Manages login
login_manager = LoginManager()
login_manager.init_app(app)

# whenever login is required and user tries to access the page redirect user to login first
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return userDetails.query.get(user_id)


########################################################################################


# databse structure of userdetails table
class userDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    type = db.Column(db.String(100))
    # admin_access = db.Column(db.Integer)
    # developer_access = db.Column(db.Integer)
    # tester_access = db.Column(db.Integer)
    # quality_access = db.Column(db.Integer)

    def __init__(
        self,
        email,
        name,
        password,
        type="user",
        # admin_access=0,
        # developer_access=0,
        # tester_access=0,
        # quality_access=0,
    ):
        self.email = email
        self.name = name
        self.type = type
        self.password = bcrypt.generate_password_hash(password=password)

    # check password with hashed database password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


# blueprint for routes of auth
from project.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


# blueprint for routes of edit
from project.edit import edit as edit_blueprint
app.register_blueprint(edit_blueprint)


# blueprint for routes of delete
from project.delete import delete as delete_blueprint
app.register_blueprint(delete_blueprint)


# blueprint for routes of adduserr
from project.adduser import addusers as adduser_blueprint
app.register_blueprint(adduser_blueprint)


# blueprint for routes of architect
from project.architect import architect as architect_blueprint
app.register_blueprint(architect_blueprint)
