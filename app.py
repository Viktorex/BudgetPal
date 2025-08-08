from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')

        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)", (title, amount, date))
        conn.commit()
        conn.close()

        return redirect('/')

    # Show saved expenses
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()

    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)

