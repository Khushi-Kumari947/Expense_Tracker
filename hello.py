import features
import setting_up_mysql_python

conn=setting_up_mysql_python.get_connection()
my=conn.cursor()

query="""drop database Expense_Tracker"""

my.execute(query)
conn.commit()
print("Database droped")

my.close()
conn.close()