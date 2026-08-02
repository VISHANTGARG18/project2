#!/usr/bin/env python3
"""
Lumina Lifestyle & Living - Interactive Executive Analytics Web Application
Built with Streamlit & SQLite.
Run with: streamlit run scripts/app.py
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Lumina Retail Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "lumina_retail.db")

@st.cache_data
def load_analytics_data():
    if not os.path.exists(DB_PATH):
        st.error(f"Database not found at {DB_PATH}. Please run scripts/etl_pipeline.py first.")
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM vw_sales_analytics WHERE order_status = 'Completed';"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df_raw = load_analytics_data()

if df_raw.empty:
    st.warning("No data available.")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.title("🛍️ Lumina Control Panel")
st.sidebar.markdown("Filter omnichannel sales analytics in real-time.")

min_date = df_raw['order_date'].min().date()
max_date = df_raw['order_date'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

channels = ["All Channels"] + list(df_raw['channel'].unique())
selected_channel = st.sidebar.selectbox("Fulfillment Channel", channels)

regions = ["All Regions"] + list(df_raw['store_region'].unique())
selected_region = st.sidebar.selectbox("Store Region", regions)

# Apply filters
df_filtered = df_raw.copy()
if len(date_range) == 2:
    start_d, end_d = date_range
    df_filtered = df_filtered[(df_filtered['order_date'].dt.date >= start_d) & (df_filtered['order_date'].dt.date <= end_d)]

if selected_channel != "All Channels":
    df_filtered = df_filtered[df_filtered['channel'] == selected_channel]

if selected_region != "All Regions":
    df_filtered = df_filtered[df_filtered['store_region'] == selected_region]

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 Lumina Lifestyle & Living - Omnichannel Retail Analytics")
st.markdown("Executive performance monitoring, RFM customer segmentation, and market basket insights.")

# ---------------------------------------------------------
# METRIC KPI CARDS
# ---------------------------------------------------------
total_revenue = df_filtered['net_revenue'].sum()
total_profit = df_filtered['net_profit'].sum()
overall_margin = (total_profit / total_revenue * 100.0) if total_revenue > 0 else 0.0
total_orders = df_filtered['order_id'].nunique()
aov = (total_revenue / total_orders) if total_orders > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Net Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Net Profit", f"${total_profit:,.2f}")
col3.metric("Net Profit Margin", f"{overall_margin:.2f}%")
col4.metric("Completed Orders", f"{total_orders:,}")
col5.metric("Average Order Value", f"${aov:.2f}")

st.markdown("---")

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Executive Dashboard", "👥 Customer RFM & Cohorts", "🧺 Market Basket Mining"])

with tab1:
    st.subheader("Monthly Sales & Profitability Trends")
    monthly_df = df_filtered.set_index('order_date').resample('M')[['net_revenue', 'net_profit']].sum().reset_index()
    monthly_df['order_date'] = monthly_df['order_date'].dt.strftime('%Y-%m')
    
    st.line_chart(monthly_df.set_index('order_date')[['net_revenue', 'net_profit']])

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Top 10 Products by Net Profit")
        top_products = df_filtered.groupby('product_name')['net_profit'].sum().reset_index()
        top_products = top_products.sort_values(by='net_profit', ascending=False).head(10)
        st.bar_chart(top_products.set_index('product_name'))
        
    with col_right:
        st.subheader("Profitability by Channel")
        channel_df = df_filtered.groupby('channel')[['net_revenue', 'net_profit']].sum()
        st.bar_chart(channel_df)

with tab2:
    st.subheader("Customer Segment Performance")
    segment_df = df_filtered.groupby('customer_segment').agg(
        total_customers=('customer_id', 'nunique'),
        net_revenue=('net_revenue', 'sum'),
        net_profit=('net_profit', 'sum')
    ).reset_index()
    segment_df['margin_pct'] = (segment_df['net_profit'] / segment_df['net_revenue']) * 100.0
    st.dataframe(segment_df, use_container_width=True)

with tab3:
    st.subheader("Market Basket Product Association Rules")
    st.markdown("Top product co-purchasing pairs analyzed across multi-item order baskets.")
    
    # Read market_basket_analysis.md if available
    mb_path = os.path.join(DOCS_DIR, "market_basket_analysis.md")
    if os.path.exists(mb_path):
        with open(mb_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.info("Run scripts/market_basket_analysis.py to generate market basket rules.")
