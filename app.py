from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['POST', 'GET'])
def add_expense():
    if request.method == 'POST':
        # Get the form data
        expense_name = request.form['expense_name']
        expense_amount = request.form['expense_amount']
        
        # Add expense to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (expense_name, expense_amount))
        conn.commit()
        conn.close()
        
        return redirect('/')
    
    return render_template('add_expense.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
