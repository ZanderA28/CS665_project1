import tkinter
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",     # or your DB host
    user=input("Username: "),
    password=input("Password: "),
    database="alexsaircraft" 
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM aircraft")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()