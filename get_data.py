import setting_up_mysql_python
import features
import matplotlib
import pandas as pd
import numpy as nmp

conn=setting_up_mysql_python.get_connection()
Mycursor=conn.cursor()

def show_expense_category_wise(user_id):

    query1="""select user_name
             from user_data
			 where user_id=%s"""
    Mycursor.execute(query1,(user_id,))
    data=Mycursor.fetchall()
    if not data:
        print("User not found!")
        return []
    
    name=data[0][0]
    print(f"Monthwise expense for each category having ID:{user_id} and NAME:{name} is")
    query="""select 
             categories.category_id,
             categories.categories,
             MONTHNAME(expenses.expense_date) AS MONTH,
             sum(expenses.amount) as Total_Amount
             from 
             expenses 
             inner join
             categories on
             expenses.category_id =categories.category_id
             where expenses.user_id=%s
             group by categories.category_id,MONTH,month(expenses.expense_date)
             order by month(expenses.expense_date)"""
    
    Mycursor.execute(query,(user_id,))
    result=Mycursor.fetchall()
    return result

r=show_expense_category_wise(1)
data=pd.DataFrame(r,columns=("category_id","category_name","Month","Total_Amount"))
print(data)



def show_expense_Total_month_wise(user_id):
    
    query1="""select user_name
            from user_data where user_id=%s"""
    Mycursor.execute(query1,(user_id,))
    data=Mycursor.fetchall()

    if not data:
        print("User not found!")
        return []
    
    name=data[0][0]
    print(f"Monthwise expense for user with ID:{user_id} and NAME:{name} is")
    query=""" select
    sum(expenses.amount) as Total_Amount,MONTHNAME(expenses.expense_date) AS MONTH
    from expenses
    inner join categories on
    categories.category_id=expenses.category_id
    where expenses.user_id=%s
    group by MONTH,month(expenses.expense_date)"""
    Mycursor.execute(query,(user_id,))
    r=Mycursor.fetchall()
    return r

# r=show_expense_Total_month_wise(1)
# data=pd.DataFrame(r,columns=("Total_Amount","Month"))
# print(data)

def show_expense_Total_year_wise(user_id):
    
    query1="""select user_name
            from user_data where user_id=%s"""
    Mycursor.execute(query1,(user_id,))
    data=Mycursor.fetchall()

    if not data:
        print("User not found!")
        return []
    
    name=data[0][0]
    print(f"Yearly expense for user with ID:{user_id} and NAME:{name} is")
    query=""" select
    sum(expenses.amount) as Total_Amount,YEAR(expenses.expense_date) AS YEAR
    from expenses
    inner join categories on
    categories.category_id=expenses.category_id
    where expenses.user_id=%s
    group by YEAR"""
    Mycursor.execute(query,(user_id,))
    r=Mycursor.fetchall()
    return r   

# r=show_expense_Total_year_wise(1)
# data=pd.DataFrame(r,columns=("Total_Amount","Year"))
# print(data)


 
