"""
Streamlit High-Performance Caching Wrapper Utility.
"""

import pandas as pd
import streamlit as st
from .database import execute_query

@st.cache_data(ttl=3600, show_spinner="Loading Lumina Analytics Data...")
def load_all_analytics_data() -> pd.DataFrame:
    """Loads all completed sales transaction line-item analytics records."""
    query = """
    SELECT 
        order_id,
        order_date,
        order_year_month,
        order_year,
        order_month,
        order_status,
        payment_method,
        customer_id,
        customer_name,
        customer_email,
        customer_region,
        customer_city,
        customer_segment,
        customer_signup_date,
        store_id,
        store_name,
        channel,
        store_region,
        store_city,
        store_state,
        store_country,
        product_id,
        product_name,
        category,
        subcategory,
        item_id,
        quantity,
        unit_price,
        unit_cost,
        discount_percent,
        gross_revenue,
        discount_amount,
        net_revenue,
        total_cogs,
        allocated_shipping_cost,
        gross_profit,
        net_profit,
        net_profit_margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed';
    """
    df = execute_query(query)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['customer_signup_date'] = pd.to_datetime(df['customer_signup_date'])
    return df

@st.cache_data(ttl=3600)
def get_database_status_metadata():
    """Retrieves system status metadata (row counts, last refresh)."""
    conn_query = "SELECT COUNT(*) FROM orders;"
    order_count = execute_query(conn_query).iloc[0, 0]
    return {
        "connected": True,
        "total_orders": order_count,
        "primary_view": "vw_sales_analytics"
    }
