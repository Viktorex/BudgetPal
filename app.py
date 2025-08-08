from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for flash messages

@app.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        date = datetime.strptime(value, '%Y-%m-%d')
        return date.strftime('%d %b %Y')  # e.g. 07 Aug 2025
    except:
        return value

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  amount REAL NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']

        if not name or not amount or not date:
            flash("Please fill all fields.", "danger")
        elif float(amount) < 0:
            flash("Amount cannot be negative.", "danger")
        else:
            c.execute("INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)", (name, amount, date))
            conn.commit()
            flash("✅ Expense added successfully!", "success")
            return redirect(url_for('index'))

    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()

    total = sum([expense[2] for expense in expenses])
    return render_template('index.html', expenses=expenses, total=total)


@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Expense deleted!", "info")
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']

        if not name or not amount or not date:
            flash("Please fill all fields.", "danger")
        else:
            c.execute("UPDATE expenses SET name=?, amount=?, date=? WHERE id=?", (name, amount, date, id))
            conn.commit()
            conn.close()
            flash("✏️ Expense updated successfully!", "success")
            return redirect(url_for('index'))

    c.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = c.fetchone()
    conn.close()
    return render_template('edit.html', expense=expense)


if __name__ == '__main__':
    app.run(debug=True)
