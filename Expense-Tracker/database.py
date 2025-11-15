import sqlite3

DB_PATH = "data/expenses.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    """)
    conn.commit()
    return conn, cur

def add_expense(cur, conn, date, category, desc, amount):
    cur.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (date, category, desc, amount)
    )
    conn.commit()

def delete_expense(cur, conn, expense_id):
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

def get_all_expenses(cur):
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    return cur.fetchall()

def get_categories(cur):
    cur.execute("SELECT DISTINCT category FROM expenses")
    return [x[0] for x in cur.fetchall()]

def filter_expenses(cur, month=None, category=None):
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if month and month != "All":
        query += " AND strftime('%m', date) = ?"
        params.append(month.split("-")[0])

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY date DESC"
    cur.execute(query, tuple(params))
    return cur.fetchall()

def total_amount(cur):
    cur.execute("SELECT SUM(amount) FROM expenses")
    return cur.fetchone()[0] or 0
