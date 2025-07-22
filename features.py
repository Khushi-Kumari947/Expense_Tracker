import setting_up_mysql_python 

def Add_users(name, email):
    conn = setting_up_mysql_python.get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO user_data (user_name, email) VALUES (%s, %s)"""
    cursor.execute(query, (name, email))
    conn.commit()

    # Fix: fetch the new user_id BEFORE closing the cursor
    cursor.execute("SELECT LAST_INSERT_ID()")
    user_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return user_id


def Add_categories(categry_name):
    conn=setting_up_mysql_python.get_connection()
    Mycursor=conn.cursor()
    
    categories = categry_name.split(',')

    # Insert each category into the database
    for category in categories:
        category = category.strip()  # Remove any leading/trailing spaces
        query = """INSERT INTO categories (categories) VALUES (%s)"""
        Mycursor.execute(query, (category,))

    print("Category added")

    conn.commit()
    Mycursor.close()
    conn.close()

def add_expense(category_id,user_id,amount,expense_date,description):
     conn=setting_up_mysql_python.get_connection()
     Mycursor=conn.cursor()

     query="""INSERT INTO expenses(category_id,
            user_id,
           amount,
           expense_date,
           expense_description) VALUES (%s,%s,%s,%s,%s)"""
     
     Mycursor.execute(query,(category_id,user_id,amount,expense_date,description))

     print("Expense added successfully!!")
     conn.commit()
     Mycursor.close()
     conn.close()
    

    
