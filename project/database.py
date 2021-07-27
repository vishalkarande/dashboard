
import mysql.connector


# Enter your database connection details below
dbs = mysql.connector.connect(
    # host="host.docker.internal",
    host="localhost",
    user="root",
    password="admin",
    database="flaskdatabase",
    auth_plugin='mysql_native_password'
)
mycursor = dbs.cursor()
