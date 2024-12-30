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
                                amount REAL NOT NULL)''')
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
        conn.close()
        return render_template('index.html', expenses=expenses)
    else:
        return "Database connection error", 500

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        expense_amount = request.form['expense_amount']
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (expense_name, expense_amount))
                conn.commit()
                conn.close()
                return redirect('/')
            except sqlite3.Error as e:
                print(f"Error adding expense: {e}")
                return "Error adding expense", 500
        else:
            return "Database connection error", 500
    
    return render_template('add_expense.html')

if __name__ == "__main__":
    create_expenses_table()  # Ensure the table exists
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
