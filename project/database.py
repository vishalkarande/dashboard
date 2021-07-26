
import mysql.connector


# Enter your database connection details below
dbs = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flaskdatabase"
)
mycursor = dbs.cursor()
