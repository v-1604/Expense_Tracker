# 💲 Expense Tracker

A personal finance web app built with Python and Streamlit. Log your daily expenses, visualize spending patterns through interactive charts, set monthly budgets, and export your data — all from a clean dashboard.

🔗 **Live Demo:** https://expensetracker-7vrunutehil2pktbvbzgd3.streamlit.app/

---

## What to Expect

When you open the app you'll see:

- **Expense Table** — all your logged expenses with date, category, amount and notes. Filter by category or date range and the entire dashboard updates instantly
- **Overview** — 3 key metrics: total spent this month, total all time, and daily average
- **Spending Breakdown** — 3 interactive charts: donut chart by category, line chart over time, and monthly bar chart
- **Budget Tracker** — set a monthly limit per category and track progress with color-coded bars (🟢 safe → 🟡 warning → 🔴 over budget)
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

## How I Built It

The app is structured across 3 Python files:

**`database.py`** handles all SQLite operations across two tables:

```sql
expenses (id, date, category, amount, note)
budgets  (category, monthly_limit)
```

The `expenses` table uses `AUTOINCREMENT` for the primary key so IDs are assigned automatically. The `budgets` table uses `category` as the primary key — enforcing one budget per category — and uses `INSERT OR REPLACE` so updating a budget overwrites the old one instead of throwing an error. All queries use `?` parameterized statements to prevent SQL injection.

**`charts.py`** contains 3 Plotly Express functions. Each takes a filtered pandas DataFrame, uses `groupby().sum()` to aggregate spending, and returns an interactive figure. `pd.to_datetime()` is applied before charting because SQLite stores dates as TEXT — converting to proper datetime objects is necessary for Plotly to render the time axis correctly.

**`app.py`** ties everything together. Streamlit reruns the entire script top to bottom on every user interaction. Filters are applied to a pandas DataFrame using boolean indexing — both category and date filters are combined with `&` — and the filtered DataFrame is passed to all 3 charts and the table simultaneously so everything stays in sync. `st.session_state` isn't needed here because the database handles persistence.

The app is deployed on Streamlit Community Cloud which is stateless — the database resets on every restart. Demo data auto-loads whenever the database is empty, ensuring the app always looks populated for anyone who opens it.

---

## What I Learned

This was my first full-stack Python project. Coming from a background of college lab programs, I had to learn several new concepts from scratch:

- **Streamlit's execution model** — understanding that the entire script reruns on every interaction was the most important concept. It changes how you think about state and data flow completely
- **SQL and databases** — learned SQLite from scratch: creating tables, parameterized queries, the difference between `INSERT` and `INSERT OR REPLACE`, and why `conn.commit()` is non-negotiable
- **Pandas data manipulation** — `groupby()`, `pd.to_datetime()`, boolean indexing, and `df.copy()` to avoid unintended mutations
- **Plotly Express** — building interactive charts from DataFrames in just a few lines, and understanding why raw datetime objects are needed vs string dates
- **Git and deployment** — first time using Git properly with meaningful commits, and deploying a live app on Streamlit Cloud

---

## Challenges Faced

**1. PowerShell execution policy**
Windows blocked virtual environment activation by default. Fixed by running `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` — learned about Windows security policies in the process.

**2. SQL typo that took hours to debug**
The budgets table had `monthlty_limit` instead of `monthly_limit`. Since SQLite uses `CREATE TABLE IF NOT EXISTS`, fixing the code wasn't enough — the old table with the typo already existed. Had to delete the database file entirely and let it recreate. Learned that schema changes require dropping old tables.

**3. Date filtering crash**
Comparing pandas Timestamps with Python `datetime.date` objects threw a `TypeError`. Fixed by using `pd.Timestamp()` for comparisons consistently — learned that Python has multiple date types that aren't directly comparable.

**4. Charts not updating with filters**
Charts were using the unfiltered `df` instead of `filtered_df`. The fix was straightforward once identified — but it taught me to trace data flow carefully through the app.

**5. Streamlit rerun after saving**
After adding an expense, the table wasn't updating. The fix was `st.rerun()` — which forces Streamlit to re-fetch data from the database. Without it, the old cached DataFrame was being displayed.

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

*Built by Varshini — B.Tech Electrical Engineering, IIT Roorkee*
