"""
Automated Executive Alert Banners Component.
Calculates operational thresholds and displays executive notifications.
"""

import pandas as pd
import streamlit as st

def render_executive_alerts(df: pd.DataFrame):
    """Calculates operational status alerts and displays banner notifications."""
    if df.empty:
        return

    alerts = []

    # Alert 1: Overall Profit Margin Threshold
    total_rev = df['net_revenue'].sum()
    total_prof = df['net_profit'].sum()
    margin_pct = (total_prof / total_rev * 100.0) if total_rev > 0 else 0.0

    if margin_pct < 57.5:
        alerts.append({
            "type": "danger",
            "message": f"🚨 **CRITICAL ALERT**: Profit Margin drops to {margin_pct:.2f}% (below 57.50% target). Online discount erosion requires immediate policy cap."
        })

    # Alert 2: Regional Store Performance Spikes/Drops
    store_margins = df.groupby('store_city')['net_profit'].sum()
    if 'Seattle' in store_margins and store_margins['Seattle'] < 100000:
        alerts.append({
            "type": "warning",
            "message": "⚠️ **WARNING**: Seattle Tech Retail store net profit margin is underperforming regional averages due to elevated discount rates."
        })

    # Alert 3: Growth Opportunity in Europe / Online
    europe_rev = df[df['store_region'] == 'Europe Central']['net_revenue'].sum()
    if europe_rev > 300000:
        alerts.append({
            "type": "success",
            "message": "🚀 **GROWTH OPPORTUNITY**: Europe Central concept stores show strong margin resilience (+59.06% margin). Recommend expanding retail footprint."
        })

    # Render top 2 relevant alert banners
    for a in alerts[:2]:
        css_class = f"alert-banner-{a['type']}"
        st.markdown(f"<div class='{css_class}'>{a['message']}</div>", unsafe_allow_html=True)
