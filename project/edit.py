from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login.utils import login_required
from project.database import dbs, mycursor
from project.auth import is_admin
import json


# blueprint for edit that needs to be imported to __init__
edit = Blueprint('edit', __name__, template_folder='templates')


# Edit User data and Page records
# edit user route call
@edit.route('/edit/<int:id>')
@login_required
@is_admin
def edituser(id):
    mycursor.execute("select * from user_details where id='%d'" % id)
    userdata = mycursor.fetchall()
    mycursor.execute("select * from page_access where uid='%d'" % id)
    row_headers = [x[0] for x in mycursor.description]
    r = mycursor.fetchall()
    json_data = []
    for result in r:
        json_data.append(dict(zip(row_headers, result)))
    r = json.dumps(json_data)
    res = json.loads(r)
    res = res[0]
    print("inedit")
    print(res)
    return render_template('edit.html', userdata=userdata[0], pages=res)


@edit.route('/update/', methods=['POST', 'GET'])
@login_required
@is_admin
def update():
    try:
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        user = request.form['user']

        admin = request.form['admin']
        developer = request.form['developer']
        tester = request.form['tester']
        # Update User Records
        mycursor.execute(
            "UPDATE user_details SET name=%s,email=%s,type=%s WHERE id=%s", (name, email, user, id))
        dbs.commit()
        mycursor.execute(
                "UPDATE page_access SET adminp=%s,developer=%s,tester=%s WHERE uid=%s", (admin, developer, tester, id))
        dbs.commit()
        return redirect(url_for("users"))

    except Exception as error:
        print(error)
        return redirect(url_for('home'))
