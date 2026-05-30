import streamlit as st
from datetime import date
import pandas as pd
from database import init_db, add_expense, get_all_expenses, set_budget, delete_expense, get_budgets,DB_NAME
from charts import spending_by_category, spending_over_time, monthly_comparison
import io


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💲",
    layout="wide"
)
init_db()

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills",
    "Entertainment", "Health","Savings","Retirement Fund", "Education", "Other"
]

st.title("💲Expense Tracker")
st.write("Smart tracking. Smarter savings.")


with st.sidebar:
    st.header("➕ Add Expense")
    with st.form("add_expense_form", clear_on_submit=True):
        exp_date = st.date_input("Date", value=date.today())
        category = st.selectbox("Category", CATEGORIES)
        amount_str = st.text_input("Amount (₹)", value="0.0")
        try:
              amount = float(amount_str)
        except ValueError:
              amount = 0.0
              st.error("Please enter a valid number")
        note = st.text_input("Note (optional)")
        submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        if amount <= 0:
            st.error("❌ Amount must be greater than 0")
        else:
            add_expense(exp_date, category, amount, note)
            st.success(f"✅ ₹{amount} for {category} on {exp_date}")
            st.rerun()

    st.divider()
    if st.button("Load Demo Data"):
        demo = [
            ("2026-04-10", "Food", 120, "lunch"),
            ("2026-04-12", "Transport", 50, "auto"),
            ("2026-04-15", "Shopping", 800, "clothes"),
            ("2026-04-20", "Bills", 500, "electricity"),
            ("2026-05-01", "Food", 200, "dinner"),
            ("2026-05-05", "Entertainment", 300, "movie"),
            ("2026-05-10", "Health", 150, "medicine"),
            ("2026-05-15", "Education", 999, "course"),
            ("2026-05-20", "Food", 180, "groceries"),
            ("2026-05-23", "Transport", 80, "cab"),
        ]
        for d in demo:
            add_expense(*d)
        st.rerun()
    st.divider()
    st.subheader(" Set Budget")
    with st.form("budget_form", clear_on_submit=True):
        budget_category = st.selectbox("Category", CATEGORIES, key="budget_cat")
        budget_limit = st.number_input("Monthly Limit (₹)", min_value=0.0, step=1.0)
        budget_submitted = st.form_submit_button("Set Budget")
    
    if budget_submitted:
        if budget_limit <= 0:
            st.error(" Budget must be greater than 0")
        else:
            set_budget(budget_category, budget_limit)
            st.success(f" Budget set: ₹{budget_limit:.0f} for {budget_category}")
            st.rerun()
    st.divider()
    if st.button(" Clear All Data", type="secondary"):
        import os
        os.remove(DB_NAME)
        init_db()
        st.success("All data cleared!")
        st.rerun()
df= get_all_expenses()
if df.empty:
    demo = [
        ("2026-04-10", "Food", 120, "lunch"),
        ("2026-04-12", "Transport", 50, "auto"),
        ("2026-04-15", "Shopping", 800, "clothes"),
        ("2026-04-20", "Bills", 500, "electricity"),
        ("2026-05-01", "Food", 200, "dinner"),
        ("2026-05-05", "Entertainment", 300, "movie"),
        ("2026-05-10", "Health", 150, "medicine"),
        ("2026-05-15", "Education", 999, "course"),
        ("2026-05-20", "Food", 180, "groceries"),
        ("2026-05-23", "Transport", 80, "cab"),
    ]
    for d in demo:
        add_expense(*d)
    df = get_all_expenses()

filtered_df=df.copy()

if df.empty:
    st.info("No expenses yet")

else:
    df['date'] = pd.to_datetime(df['date'])

    st.subheader(" Filters")
    col1, col2 = st.columns(2)

    with col1:
        selected_categories = st.multiselect(
            "Filter by Category",
            options=CATEGORIES,
            default=CATEGORIES
        )
    with col2:
        selected_dates = st.date_input(
            "Filter by Date Range",
            value=[pd.to_datetime(df['date']).min(), 
                   pd.to_datetime(df['date']).max()]
        )
    


    filtered_df = df[
       (df['category'].isin(selected_categories)) &
       (df['date'] >= pd.to_datetime(selected_dates[0])) &
       (df['date'] <= pd.to_datetime(selected_dates[1]))
    ]

    st.subheader("All Expenses")
    st.dataframe(
        filtered_df[['id','date', 'category', 'amount', 'note']],
        use_container_width=True
    )
    st.metric("Filtered Total", f"₹{filtered_df['amount'].sum():,.0f}")

    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="expenses.csv",
        mime="text/csv"
    )
     
    st.subheader("📊 Overview")
    current_month = date.today().strftime('%Y-%m')
    monthly_df = df[df['date'].dt.strftime('%Y-%m') == current_month]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total This Month", f"₹{monthly_df['amount'].sum():,.0f}")
    with col2:
        st.metric("Total All Time", f"₹{df['amount'].sum():,.0f}")
    with col3:
        daily_avg = df.groupby('date')['amount'].sum().mean()
        st.metric("Avg Per Day", f"₹{daily_avg:,.0f}")

    st.subheader("💡 Spending Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(spending_by_category(filtered_df),
                        use_container_width=True)
    with col2:
        st.plotly_chart(spending_over_time(filtered_df),
                        use_container_width=True)

    st.plotly_chart(monthly_comparison(filtered_df),
                    use_container_width=True)
    
    
    st.subheader(" Budget Tracker")
    
    budgets = get_budgets()
    current_month = date.today().strftime('%Y-%m')
    monthly_df = df[df['date'].dt.strftime('%Y-%m') == current_month]
    
    if budgets.empty:
        st.info("No budgets set yet. Set one from the sidebar!")
    else:
        for _, row in budgets.iterrows():
            category = row['category']
            limit = row['monthly_limit']
            
            spent = monthly_df[monthly_df['category'] == category]['amount'].sum()
            percent = min(spent / limit, 1.0) 
            remaining = max(limit - spent, 0)
            
            if percent >= 1.0:
                emoji = "🔴"
                status = "OVER BUDGET"
            elif percent >= 0.8:
                emoji = "🟡"
                status = f"₹{remaining:.0f} left"
            else:
                emoji = "🟢"
                status = f"₹{remaining:.0f} left"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{emoji} **{category}** — ₹{spent:.0f} / ₹{limit:.0f}")
                st.progress(percent)
            with col2:
                st.write(f"_{status}_")
    
    
    st.subheader(" Delete Expense")
    st.write("Find the ID from the table above and enter it below:")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        delete_id = st.number_input("Expense ID", min_value=1, step=1)
    with col2:
        st.write("")  
        st.write("")  
        if st.button("Delete", type="primary"):
            delete_expense(int(delete_id))
            st.success(f" Expense #{delete_id} deleted!")
            st.rerun()