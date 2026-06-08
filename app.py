import mysql.connector
from datetime import datetime

try:
    # 1. Database Connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password='Your Password',  
        database="expense_tracker"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connected to Expense Tracker Database!\n")
        # 2. User se Expense ki details input lena
        print("--- Add New Expense ---")
        amount = float(input("Enter Amount (₹): "))
        description = input("Enter Description: ")
        
        # Aaj ki date automatic lene ke liye
        today_date = datetime.today().strftime('%Y-%m-%d')
        
        # Abhi ke liye hum Category ID 1 (Food) ya 2 (Travel) manually de rahe hain
        print("\nCategories: 1 = Food, 2 = Travel, 3 = Bills")
        category_id = int(input("Choose Category ID (1/2/3): "))

        # 3. SQL Insert Query (Parametrized Query for Security)
        insert_query = """
        INSERT INTO Expenses (amount, description, expense_date, category_id) 
        VALUES (%s, %s, %s, %s);
        """
        data_to_insert = (amount, description, today_date, category_id)
        
        # Query ko execute karna
        cursor.execute(insert_query, data_to_insert)
        
        # SQL mein jab bhi data change karte hain, COMMIT karna zaroori hai!
        connection.commit()
        print(f"\nExpense of ₹{amount} added successfully!")

        # 4. Saari Expenses wapas dekhna
        print("\n--- Updated Expenses List ---")
        cursor.execute("SELECT * FROM Expenses;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Amount: ₹{row[1]} | Note: {row[2]} | Date: {row[3]}")

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nConnection closed safely.")