import os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        # Use an environment-specific path or the current directory for SQLite DB
        db_path = os.path.join(os.getcwd(), 'expenses.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        conn.close()
        return render_template('index.html', expenses=expenses)
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
        return "Error retrieving expenses", 500

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        # Get the form data
        expense_name = request.form['expense_name']
        expense_amount = request.form['expense_amount']
        
        # Add expense to the database
        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (expense_name, expense_amount))
            conn.commit()
            conn.close()
            return redirect('/')
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
            conn.close()
            return "Error adding expense", 500
    
    return render_template('add_expense.html')

if __name__ == "__main__":
    # Use host='0.0.0.0' to make the app accessible externally
    # Use the PORT environment variable for dynamic port assignment in Railway
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
