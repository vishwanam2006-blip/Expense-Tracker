import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

try:
    # 1. Database Connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password='your password',  
        database="expense_tracker"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
        # 2. SQL query jo Expenses aur Categories ko JOIN karegi
        query = """
        SELECT c.category_name, SUM(e.amount) as total_amount 
        FROM Expenses e
        JOIN Categories c ON e.category_id = c.category_id
        GROUP BY c.category_name;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("Empty Database!")
        else:
            # 3. Data ko Pandas DataFrame mein convert karna
            df = pd.DataFrame(rows, columns=['Category', 'Total Spent'])
            print("\n--- Expense Summary ---")
            print(df)
            
            # 4. Pie Chart banana
            plt.figure(figsize=(6, 6))
            plt.pie(df['Total Spent'], labels=df['Category'], autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            plt.title('Monthly Expense Breakdown by Category')
            
            print("\nShowing Pie Chart... Close the chart window to exit.")
            plt.show()  # Isse graph screen par pop-up hoga

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nConnection closed safely.")