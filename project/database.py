
import mysql.connector


# Enter your database connection details below
dbs = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="root",
    database="flaskdatabase",
    auth_plugin='mysql_native_password'
)
mycursor = dbs.cursor()
