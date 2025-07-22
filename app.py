import streamlit as st
import pandas as pd
from datetime import datetime
import features
import get_data
import setting_up_mysql_python

# ----------------- Helper Functions ------------------
def check_user_exists(user_id):
    conn = setting_up_mysql_python.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_category_mapping():
    conn = setting_up_mysql_python.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, categories FROM categories")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {f"{cat_id} - {cat_name}": cat_id for cat_id, cat_name in rows}

def login_or_register_page():
    st.title("🔐 Welcome to Expense Tracker")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        login_user_id = st.text_input("Enter User ID")
        if st.button("Login"):
            username = check_user_exists(login_user_id)
            if username:
                st.success(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.user_id = int(login_user_id)
                st.rerun()
            else:
                st.error("User ID not found. Please register.")

    with col2:
        st.subheader("Register")
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Register"):
            try:
                user_id = features.Add_users(name, email)

        # Store in session state before rerun
                st.session_state.new_user_id = user_id
                st.session_state.new_user_name = name
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

def main_app():
    user_id = st.session_state.user_id
    st.sidebar.title("Expense Menu")
    menu = st.sidebar.radio("Select Option", ["Add Category", "Add Expense", "Monthly Summary", "Yearly Summary", "Category-wise Summary", "Logout"])

    # Fetch user details for greeting
    conn = setting_up_mysql_python.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM user_data WHERE user_id = %s", (user_id,))
    user_details = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_details:
        user_name = user_details[0]
        st.title(f"Welcome back, {user_name}! 😊")

    if menu == "Add Category":
        st.subheader("📂 Add New Category")
        cat_input = st.text_input("Enter categories (comma-separated if multiple)")
        if st.button("Add Category"):
            try:
                features.Add_categories(cat_input)
                st.success("Category(ies) added!!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif menu == "Add Expense":
        st.subheader("💸 Add Expense")
        category_map = get_category_mapping()
        if category_map:
            selected_category = st.selectbox("Select Category", list(category_map.keys()))
            category_id = category_map[selected_category]
        else:
            st.warning("No categories found. Please add categories first.")
            st.stop()

        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        date_input = st.date_input("Expense Date")
        description = st.text_input("Description (max 255 chars)")

        if st.button("Add Expense"):
            if len(description) > 255:
                st.warning("Description too long!")
            else:
                try:
                    features.add_expense(category_id, user_id, amount, date_input, description)
                    st.success("Expense added successfully!")
                except Exception as e:
                    st.error(f"Failed to add expense: {e}")

    elif menu == "Monthly Summary":
        st.subheader("📆 Monthly Expense Summary")
        data = get_data.show_expense_Total_month_wise(user_id)
        if data:
            df = pd.DataFrame(data, columns=["Total Amount", "Month"])
            st.bar_chart(df.set_index("Month"))
            st.dataframe(df)
        else:
            st.warning("No data found.")

    elif menu == "Yearly Summary":
        st.subheader("📅 Yearly Expense Summary")
        data = get_data.show_expense_Total_year_wise(user_id)
        if data:
            df = pd.DataFrame(data, columns=["Total Amount", "Year"])
            st.bar_chart(df.set_index("Year"))
            st.dataframe(df)
        else:
            st.warning("No data found.")

    elif menu == "Category-wise Summary":
        st.subheader("📊 Category-wise Monthly Breakdown")
        data = get_data.show_expense_category_wise(user_id)
        if data:
            df = pd.DataFrame(data, columns=["Category ID", "Category", "Month", "Total Amount"])
            st.dataframe(df)
            st.write("Grouped by Category and Month")
            pivot = df.pivot(index="Month", columns="Category", values="Total Amount").fillna(0)
            st.line_chart(pivot)
        else:
            st.warning("No data found.")

    elif menu == "Logout":
        st.session_state.clear()
        st.rerun()

# ----------------- Entry Point ------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    if "new_user_id" in st.session_state:
        st.success(f"🎉 Welcome, {st.session_state.new_user_name}! You have been registered successfully.\n\n👉 Your User ID is: {st.session_state.new_user_id}\n\n(Please save this for future logins.)")
        del st.session_state.new_user_id
        del st.session_state.new_user_name
    main_app()

else:
    login_or_register_page()
