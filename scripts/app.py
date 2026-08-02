#!/usr/bin/env python3
"""
Lumina Lifestyle & Living - Flagship Executive Analytics Platform
Main Entry Point & Router Application.
Run with: streamlit run scripts/app.py
"""

import time
import os
import sys
import streamlit as st

# Add scripts directory to sys.path for robust imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_components.styling import apply_custom_css
from app_components.sidebar import render_sidebar_filters
from app_components.executive_dashboard import render_executive_dashboard_tab
from app_components.product_studio import render_product_studio_tab
from app_components.customer_intelligence import render_customer_intelligence_tab
from app_components.market_basket_ui import render_market_basket_tab
from app_components.forecasting_ui import render_forecasting_tab
from app_components.sql_sandbox import render_sql_sandbox_tab
from utils.cache import load_all_analytics_data, get_database_status_metadata

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lumina Executive Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DATA LOADING WITH PERFORMANCE CACHING
# ---------------------------------------------------------
start_time = time.time()
df_raw = load_all_analytics_data()
load_time = time.time() - start_time

if df_raw.empty:
    st.error("Error: Failed to load analytics data from database.")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR FILTERS & DYNAMIC THEME SELECTION
# ---------------------------------------------------------
df_filtered, filter_summary = render_sidebar_filters(df_raw)

# Apply dynamic Light/Dark Mode CSS based on sidebar radio button
apply_custom_css(filter_summary.get('theme_mode', 'Dark Mode 🌙'))

# ---------------------------------------------------------
# SYSTEM STATUS PANEL (HEADER)
# ---------------------------------------------------------
status_meta = get_database_status_metadata()

status_html = f"""
<div class='status-panel'>
    🟢 <b>Database Status</b>: Connected (`lumina_retail.db`) &nbsp;|&nbsp; 
    📊 <b>Rows Loaded</b>: {len(df_raw):,} &nbsp;|&nbsp; 
    🎯 <b>Active Filtered Records</b>: {filter_summary['active_records']:,} &nbsp;|&nbsp; 
    ⚡ <b>Query Speed</b>: {load_time:.3f}s &nbsp;|&nbsp; 
    🎨 <b>Theme</b>: {filter_summary.get('theme_mode', 'Dark Mode 🌙')} &nbsp;|&nbsp;
    🌍 <b>Country</b>: {filter_summary['country']} &nbsp;|&nbsp; 
    📡 <b>Channel</b>: {filter_summary['channel']}
</div>
"""
st.markdown(status_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENTERPRISE TAB NAVIGATION
# ---------------------------------------------------------
tab_names = [
    "🏠 Executive Overview",
    "📦 Product Intelligence",
    "👥 Customer Analytics",
    "🛒 Market Basket Explorer",
    "📈 Forecasting Studio",
    "🧠 SQL Analytics Lab"
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_names)

with tab1:
    render_executive_dashboard_tab(df_filtered, df_raw)

with tab2:
    render_product_studio_tab(df_filtered)

with tab3:
    render_customer_intelligence_tab(df_filtered)

with tab4:
    render_market_basket_tab(df_filtered)

with tab5:
    render_forecasting_tab(df_filtered)

with tab6:
    render_sql_sandbox_tab(df_filtered)
