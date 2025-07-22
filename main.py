import features
import setting_up_mysql_python
from datetime import datetime


print("Welcome to expense tracker\n")
print("You can seamlessly track your expenses now!\n")

conn=setting_up_mysql_python.get_connection()
Mycursor=conn.cursor()

choice=int(input("show menu:ys->1,no->2:"))
while(choice==1):
    print("Choose:\n")

    message = "To add new user enter 1:"
    print('*' * len(message))
    print(message)
    print('*' * len(message))
    print("\n")

    message = "To add new category 2:"
    print('*' * len(message))
    print("Existing categories:")
    query = """SELECT * FROM categories"""
    Mycursor.execute(query)  # Execute the SELECT query
    data = Mycursor.fetchall()  # Fetch all the results

    # Check if categories were fetched
    # if data:
    #     print("Categories available:")
    #     for row in data:1

    #         print(row)  # Print each row of data fetched
    # else:
    #     print("No categories found.")
    print(data)
    print(message)
    print('*' * len(message))
    print("\n")
    
    message = "To add expense for existing user 3:"
    print('*' * len(message))
    print(message)
    print('*' * len(message))
    print("\n")

    c=int(input("enter choice:"))

    if(c==1):
        name=input("enter your name:")
        email=input("enter email:")
        features.Add_users(name,email)


        query = "SELECT * FROM user_data WHERE user_name=%s"
        Mycursor.execute(query,(name,))
        
        data = Mycursor.fetchone()
        conn.commit()
        print("Save your user_id for later use:")
        print(data)

        


    
    elif(c==2):
        name=input("enter category name:")
        features.Add_categories(name)
        query="""select * from categories"""
        Mycursor.execute(query)
        
        data=Mycursor.fetchall()
        conn.commit()
        print("Save your category_id/s for later use:")
        print(data)


    elif(c==3):
        try:
            user_id = int(input("Enter User ID (integer): "))
            categ_id=int(input("Enter category ID (integer): "))
            amount = float(input("Enter Expense Amount (decimal round to 2 decimal places only): "))
            date_str = input("Enter Expense Date (YYYY-MM-DD): ")
            description = input("Enter description of expense (string(must be under 255 characters)): ").strip()

    # Validate inputs
            if (user_id and categ_id)< 0:
                raise ValueError("User/category ID cannot be negative!")
            if len(description) > 255:
                raise ValueError("description name must be under 255 characters!")
            if amount < 0:
                raise ValueError("Expense amount cannot be negative!")
            expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()


        except ValueError as e:
            print(f"Input Error: {e}")
        
        features.add_expense(categ_id,user_id,amount,expense_date,description)

    choice=int(input("show menu:ys->1,no->2:"))
    
else:
    Mycursor.close()
    conn.close()
    print("Exiting....")
    print("Thank you!")


    






