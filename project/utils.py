# some required imports
from flask import render_template
from functools import wraps
from project.database import mycursor


# get all users from database
def getAllUsers():
    # get all users from databse
    mycursor.execute("select * from user_details")
    users = mycursor.fetchall()
    return users


# get total number of users in database
def getTotalUsers():
    mycursor.execute("select count(*) from user_details")
    count = mycursor.fetchone()[0]
    return count


# get single user
def getSingleUser(email):
    mycursor.execute("select * from user_details where email='"+email+"'")
    user = mycursor.fetchall()
    return user