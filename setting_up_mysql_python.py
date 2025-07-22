import mysql.connector

def get_connection():
     Mydb=mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="Mysql@12kk",
                                  database="Expense_tracker")
     return Mydb

