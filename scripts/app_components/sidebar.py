"""
Global Multi-Filter Sidebar Controller Component.
Controls every visualization across all 6 platform tabs.
"""

import pandas as pd
import streamlit as st

def render_sidebar_filters(df: pd.DataFrame):
    """Renders the global sidebar filter controls and returns filtered DataFrame."""
    st.sidebar.title("💎 Lumina Control Center")
    st.sidebar.markdown("*Omnichannel Filter Matrix*")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Global Filters")

    # 1. Date Range Filter
    min_d = df['order_date'].min().date()
    max_d = df['order_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d
    )

    # 2. Country Filter
    countries = ["All Countries"] + sorted(list(df['store_country'].dropna().unique()))
    selected_country = st.sidebar.selectbox("🌍 Country", countries)

    # 3. Region Filter
    if selected_country != "All Countries":
        avail_regions = df[df['store_country'] == selected_country]['store_region'].unique()
    else:
        avail_regions = df['store_region'].unique()
    regions = ["All Regions"] + sorted(list(avail_regions))
    selected_region = st.sidebar.selectbox("🗺️ Region", regions)

    # 4. Store Filter
    if selected_region != "All Regions":
        avail_stores = df[df['store_region'] == selected_region]['store_name'].unique()
    else:
        avail_stores = df['store_name'].unique()
    stores = ["All Stores"] + sorted(list(avail_stores))
    selected_store = st.sidebar.selectbox("🏪 Store Location", stores)

    # 5. Sales Channel Filter
    channels = ["All Channels"] + sorted(list(df['channel'].unique()))
    selected_channel = st.sidebar.selectbox("📡 Sales Channel", channels)

    # 6. Product Category Filter
    categories = ["All Categories"] + sorted(list(df['category'].unique()))
    selected_category = st.sidebar.selectbox("📦 Product Category", categories)

    # 7. Customer Segment Filter
    segments = ["All Segments"] + sorted(list(df['customer_segment'].unique()))
    selected_segment = st.sidebar.selectbox("👥 Loyalty Segment", segments)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Quick Search")

    # 8. Product Search
    search_product = st.sidebar.text_input("🔍 Product Name", "")

    # 9. Customer Search
    search_customer = st.sidebar.text_input("👤 Customer Name / Email", "")

    # Apply Filtering Logic
    filtered_df = df.copy()

    if len(date_range) == 2:
        s_date, e_date = date_range
        filtered_df = filtered_df[(filtered_df['order_date'].dt.date >= s_date) & (filtered_df['order_date'].dt.date <= e_date)]

    if selected_country != "All Countries":
        filtered_df = filtered_df[filtered_df['store_country'] == selected_country]

    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df['store_region'] == selected_region]

    if selected_store != "All Stores":
        filtered_df = filtered_df[filtered_df['store_name'] == selected_store]

    if selected_channel != "All Channels":
        filtered_df = filtered_df[filtered_df['channel'] == selected_channel]

    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    if selected_segment != "All Segments":
        filtered_df = filtered_df[filtered_df['customer_segment'] == selected_segment]

    if search_product:
        filtered_df = filtered_df[filtered_df['product_name'].str.contains(search_product, case=False, na=False)]

    if search_customer:
        filtered_df = filtered_df[
            filtered_df['customer_name'].str.contains(search_customer, case=False, na=False) |
            filtered_df['customer_email'].str.contains(search_customer, case=False, na=False)
        ]

    # Store active filter state
    filter_summary = {
        "date_range": date_range,
        "country": selected_country,
        "region": selected_region,
        "store": selected_store,
        "channel": selected_channel,
        "category": selected_category,
        "segment": selected_segment,
        "search_product": search_product,
        "search_customer": search_customer,
        "active_records": len(filtered_df),
        "theme_mode": "Dark Mode 🌙"
    }

    return filtered_df, filter_summary
