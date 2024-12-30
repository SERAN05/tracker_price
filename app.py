import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = sqlite3.connect('expenses.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Function to create the table if it doesn't exist
def create_expenses_table():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                amount REAL NOT NULL,
                                created_at TEXT NOT NULL)''')  # Added created_at column
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        
        # Calculate the total cost
        total_cost = sum(expense['amount'] for expense in expenses)
        
        conn.close()
        return render_template('index.html', expenses=expenses, total_cost=total_cost)
    else:
        return "Database connection error", 500

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        expense_amount = request.form['expense_amount']
        
        # Get current date and time
        from datetime import datetime
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (name, amount, created_at) VALUES (?, ?, ?)", 
                               (expense_name, expense_amount, created_at))
                conn.commit()
                conn.close()
                return redirect('/')
            except sqlite3.Error as e:
                print(f"Error adding expense: {e}")
                return "Error adding expense", 500
        else:
            return "Database connection error", 500
    
    return render_template('add_expense.html')

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            conn.close()
            return redirect('/')
        except sqlite3.Error as e:
            print(f"Error deleting expense: {e}")
            return "Error deleting expense", 500
    else:
        return "Database connection error", 500

if __name__ == "__main__":
    create_expenses_table()  # Ensure the table exists
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
