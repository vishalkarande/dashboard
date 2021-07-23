import mysql.connector
# Enter your database connection details below
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
mycursor = mydb.cursor()