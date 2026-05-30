import plotly.express as px
import pandas as pd

def spending_by_category(df):
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    fig = px.pie(
        category_totals,
        values='amount',
        names='category',
        title='Spending by Category',
        hole=0.4       
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def spending_over_time(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby('date')['amount'].sum().reset_index()
    fig = px.line(
        daily,
        x='date',
        y='amount',
        title='Spending Over Time',
        markers=True    
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Amount (₹)")
    return fig
def monthly_comparison(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%b %Y')  
    monthly = df.groupby('month')['amount'].sum().reset_index()
    fig = px.bar(
        monthly,
        x='month',
        y='amount',
        title='Monthly Spending',
        color='amount',
        color_continuous_scale='Teal'
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Amount (₹)",plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    return fig
