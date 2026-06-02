# 💲 Expense Tracker

A personal finance web app built with Python and Streamlit. Expense Tracker helps you keep track of your daily spendings. Instead of monitoring your expenses manually, this app makes you log your expenses so you can keep track of your money. It also helps you set a budget and analyze where you stand according to your budget.

🔗 **Live Demo:** https://expensetracker-7vrunutehil2pktbvbzgd3.streamlit.app/

---

## What to Expect

When you open the app you'll see:

- **Expense Table** — all your logged expenses with date, category, amount and notes. Filter by category or date range and the entire dashboard updates instantly
- **Overview** — helps you analyse total spent this month, total all time, and daily average
- **Spending Breakdown** — charts: donut chart by category, line chart over time, and monthly bar chart
- **Budget Tracker** — set a monthly limit per category and track progress with color-coded bars
- **CSV Export** — download your filtered expenses as a spreadsheet
- **Demo Data** — loads automatically on first visit so you can explore without adding anything manually

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| Streamlit | Web framework and UI |
| SQLite + sqlite3 | Database |
| Pandas | Data processing and filtering |
| Plotly Express | Interactive charts |

---


The app is structured across 3 Python files:

**`database.py`** handles all SQLite operations across two tables:

```sql
expenses (id, date, category, amount, note)
budgets  (category, monthly_limit)
```

The `expenses` table uses `AUTOINCREMENT` for the primary key so IDs are assigned automatically. The `budgets` table uses `category` as the primary key — enforcing one budget per category — and uses `INSERT OR REPLACE` so updating a budget overwrites the old one instead of throwing an error. All queries use `?` parameterized statements to prevent SQL injection.

**`charts.py`** contains 3 Plotly Express functions. Each takes a filtered pandas DataFrame, uses `groupby().sum()` to aggregate spending, and returns an interactive figure. `pd.to_datetime()` is applied before charting because SQLite stores dates as TEXT — converting to proper datetime objects is necessary for Plotly to render the time axis correctly.

**`app.py`** ties everything together. Streamlit reruns the entire script top to bottom on every user interaction. Filters are applied to a pandas DataFrame using boolean indexing — both category and date filters are combined with `&` — and the filtered DataFrame is passed to all 3 charts and the table simultaneously so everything stays in sync. `st.session_state` isn't needed here because the database handles persistence.

The app is deployed on Streamlit Community Cloud. The database resets on every restart. Demo data auto-loads whenever the database is empty, ensuring the app always looks populated for anyone who opens it.


---

## Run Locally

```bash
git clone https://github.com/v-1604/Expense_Tracker.git
cd Expense_Tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Requirements
streamlit
pandas
plotly
---

*Varshini — B.Tech Electrical Engineering, IIT Roorkee*
