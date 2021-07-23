from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
import const.db as d

edit = Blueprint('edit', __name__,template_folder='templates')
# Edit User data and Page records
# edit user route call
@edit.route('/edit/<int:id>')
def edituser(id):
    if 'loggedin' in session and session['user_type']== 'admin':
        d.mycursor.execute("select * from login where id='%d'" % id)
        userdata = d.mycursor.fetchall()
        print(userdata)
        return render_template('edit.html',userdata=userdata[0])
    else:
        return render_template('index.html')


@edit.route('/update/', methods=['POST', 'GET'])
def update():
    try:
        if 'email' in session and session['user_type'] == "admin":
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            user = request.form['user']
            # Update User Records
            d.mycursor.execute(
                "UPDATE login SET name=%s,email=%s,type=%s WHERE id=%s", (name, email, user, id))
            d.mydb.commit()
            return  redirect(url_for("user"))
        else:
            print("cant delete")
            return render_template('index.html')
    except Exception as error:
        print("error")
        return render_template('home.html')