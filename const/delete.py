from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, session , jsonify
import const.db as d

delete = Blueprint('delete', __name__,template_folder='templates')
# Delete User data and Page records

@delete.route('/delete/<int:id>', methods=['POST', 'GET'])
def deleteuser(id):
    print(id)
    try:
        if 'email' in session and session['user_type'] == "admin":
            # Delete User Records
            d.mycursor.execute(
                "DELETE FROM `login` WHERE id='%d'" % id)
            d.mydb.commit()
            # Delete Page Access Records for User
            d.mycursor.execute(
                "DELETE FROM `page_access` WHERE u_id='%d'" % id)
            d.mydb.commit()
            print("delete success")
            return redirect(url_for("user"))
        else:
            print("cant delete")
            return redirect(url_for("user"))
    except Exception as error:
        print("error")
        return redirect(url_for("user"))

