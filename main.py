import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Global variables to track the current user session
CURRENT_USER_ID = None
CURRENT_USERNAME = ""

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password='your password',  
        database="expense_tracker"
    )

def login_user():
    global CURRENT_USER_ID, CURRENT_USERNAME
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n==================================")
    print("      EXPENSE TRACKER SYSTEM      ")
    print("==================================")
    username = input("Enter your Name: ").strip().lower()
    
    if not username:
        print("Name cannot be empty. Please try again.")
        cursor.close()
        conn.close()
        return login_user()

    # Check if user already exists
    cursor.execute("SELECT user_id FROM Users WHERE username = %s;", (username,))
    result = cursor.fetchone()
    
    if result:
        CURRENT_USER_ID = result[0]
        print(f"Welcome back, {username.capitalize()}!")
    else:
        # Create a new user
        cursor.execute("INSERT INTO Users (username) VALUES (%s);", (username,))
        conn.commit()
        CURRENT_USER_ID = cursor.lastrowid
        print(f"Created a new session for {username.capitalize()}.")
        
    CURRENT_USERNAME = username.capitalize()
    cursor.close()
    conn.close()

def add_expense():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"\n--- Add New Expense for {CURRENT_USERNAME} ---")
    amount = float(input("Enter Amount (INR): "))
    description = input("Enter Description: ")
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    # Categories displayed clearly one by one
    print("Select a Category:")
    print("1. Food")
    print("2. Travel")
    print("3. Bills")
    category_id = int(input("Enter Category Number (1/2/3): "))

    query = "INSERT INTO Expenses (amount, description, expense_date, category_id, user_id) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (amount, description, today_date, category_id, CURRENT_USER_ID))
    conn.commit()
    
    print(f"Successfully added INR {amount} to your session.")
    cursor.close()
    conn.close()

def view_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Expenses WHERE user_id = %s;"
    cursor.execute(query, (CURRENT_USER_ID,))
    rows = cursor.fetchall()
    
    print(f"\n--- Expense Logs for {CURRENT_USERNAME} ---")
    if not rows:
        print("No expenses found in this session.")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Amount: INR {row[1]} | Note: {row[2]} | Date: {row[3]}")
            
    cursor.close()
    conn.close()

def show_chart():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT c.category_name, SUM(e.amount) as total_amount 
    FROM Expenses e
    JOIN Categories c ON e.category_id = c.category_id
    WHERE e.user_id = %s
    GROUP BY c.category_name;
    """
    cursor.execute(query, (CURRENT_USER_ID,))
    rows = cursor.fetchall()
    
    if not rows:
        print(f"No data available to show a chart for {CURRENT_USERNAME}.")
        return
        
    df = pd.DataFrame(rows, columns=['Category', 'Total Spent'])
    
    plt.figure(figsize=(6, 6))
    plt.pie(df['Total Spent'], labels=df['Category'], autopct='%1.1f%%', startangle=140)
    plt.title(f'Expense Breakdown - {CURRENT_USERNAME}')
    print("\nDisplaying your chart... (Close the chart window to return to the menu)")
    plt.show()
    
    cursor.close()
    conn.close()

def delete_user_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the user's expenses and user profile
    cursor.execute("DELETE FROM Expenses WHERE user_id = %s;", (CURRENT_USER_ID,))
    cursor.execute("DELETE FROM Users WHERE user_id = %s;", (CURRENT_USER_ID,))
    conn.commit()
    
    print(f"Session closed. All temporary data deleted for {CURRENT_USERNAME}.")
    cursor.close()
    conn.close()

def main():
    login_user() 
    
    while True:
        print(f"\n--- CURRENT USER: {CURRENT_USERNAME.upper()} ---")
        print("1. Add New Expense")
        print("2. View My Expenses")
        print("3. Show My Chart")
        print("4. Switch User")
        print("5. Exit Application")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            show_chart()
        elif choice == '4':
            print(f"\nYou are logging out of '{CURRENT_USERNAME}'.")
            print("Do you want to save your data before switching?")
            print("A. Yes, save it.")
            print("B. No, delete everything.")
            sub_choice = input("Choose (A/B): ").strip().upper()
            
            if sub_choice == 'B':
                delete_user_data()
            login_user()
            
        elif choice == '5':
            print(f"\nYou are exiting the application.")
            print("Do you want to save your data before leaving?")
            print("A. Yes, save it.")
            print("B. No, delete everything.")
            sub_choice = input("Choose (A/B): ").strip().upper()
            
            if sub_choice == 'B':
                delete_user_data()
                print("All temporary data has been deleted.")
            else:
                print(f"Data saved successfully for {CURRENT_USERNAME}.")
                
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()