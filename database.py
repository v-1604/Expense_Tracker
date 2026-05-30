import sqlite3
import pandas as pd

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets(
            category TEXT PRIMARY KEY,
            monthly_limit REAL NOT NULL
            )
                   
    ''')
    conn.commit()
    conn.close()
def add_expense(date, category, amount, note):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
        (str(date), category, amount, note)
    )
    conn.commit()
    conn.close()
def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY date DESC", 
        conn
    )
    conn.close()
    return df
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
def set_budget(category, limit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
        (category, limit)
    )
    conn.commit()
    conn.close()
def get_budgets():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM budgets", conn)
    conn.close()
    return df
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
