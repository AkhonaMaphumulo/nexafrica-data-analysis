import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 NexAfrica Superstore Interactive Dashboard")
st.markdown("### Week 4: Key Performance Indicators & Visual Insights")

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore_cleaned.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
selected_region = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["region"].unique(),
    default=df["region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category:",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Apply Filters
filtered_df = df[
    (df["region"].isin(selected_region)) & 
    (df["category"].isin(selected_category))
]

# 4. Executive KPI Metrics
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
avg_discount = filtered_df["discount"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Avg Discount", f"{avg_discount:.2f}%")

st.markdown("---")

# 5. Interactive Visualizations
col_left, col_right = st.columns(2)

with col_left:
    monthly_df = filtered_df.resample('ME', on='order_date')[['sales', 'profit']].sum().reset_index()
    fig_trend = px.line(
        monthly_df, 
        x='order_date', 
        y=['sales', 'profit'],
        title="Monthly Sales & Profit Trends",
        labels={"value": "USD ($)", "order_date": "Date"},
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    region_df = filtered_df.groupby('region')[['sales', 'profit']].sum().reset_index()
    fig_region = px.bar(
        region_df, 
        x='region', 
        y=['sales', 'profit'], 
        barmode='group',
        title="Sales vs Profit by Region",
        template="plotly_white"
    )
    st.plotly_chart(fig_region, use_container_width=True)

col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    subcat_df = filtered_df.groupby('sub_category')['profit'].sum().reset_index().sort_values(by='profit', ascending=True)
    fig_subcat = px.bar(
        subcat_df, 
        y='sub_category', 
        x='profit', 
        orientation='h',
        color='profit',
        color_continuous_scale='RdYlGn',
        title="Profit Margin Impact by Sub-Category",
        template="plotly_white"
    )
    st.plotly_chart(fig_subcat, use_container_width=True)

with col_bottom2:
    fig_discount = px.scatter(
        filtered_df, 
        x='discount', 
        y='profit', 
        color='category',
        hover_data=['sub_category', 'sales'],
        title="Discount Rate vs Net Profit (20% Threshold Impact)",
        template="plotly_white"
    )
    st.plotly_chart(fig_discount, use_container_width=True)

st.success("Dashboard successfully loaded! Use the sidebar filters to explore data interdependently.")