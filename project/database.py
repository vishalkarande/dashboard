
import mysql.connector


# Enter your database connection details below
dbs = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flaskdatabase",
    auth_plugin='mysql_native_password'
)
mycursor = dbs.cursor()
