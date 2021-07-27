from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login.utils import login_required
from project.database import dbs, mycursor
from project.auth import is_admin

# blueprint for delete that needs to be imported to __init__
delete = Blueprint('delete', __name__, template_folder='templates')


# Delete User data and Page records
@delete.route('/delete/<int:id>', methods=['POST', 'GET'])
@is_admin
def deleteuser(id):
    print(id)
    try:
        # Delete User Records
        mycursor.execute(
            "DELETE FROM `user_details` WHERE id='%d'" % id)
        dbs.commit()
        # Delete Page Access Records for User
        mycursor.execute(
            "DELETE FROM `page_access` WHERE uid='%d'" % id)
        dbs.commit()
        print("delete success")
        return redirect(url_for("users"))
    except Exception as error:
        print("error")
        return redirect(url_for("users"))
