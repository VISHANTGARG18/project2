"""
Tab 1: Executive Overview Command Center Component.
Features Groww / Stripe inspired high-aesthetic KPI cards, Plotly smooth-curved trend graphs,
interactive maps, and AI insights cards.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.metrics import calculate_kpis, calculate_kpi_deltas
from utils.helpers import fmt_currency, fmt_currency_exact, fmt_percent, fmt_number
from .executive_alerts import render_executive_alerts
from .ai_insights import render_ai_executive_insights

def render_executive_dashboard_tab(df_filtered: pd.DataFrame, df_raw: pd.DataFrame):
    """Renders the Tab 1 Executive Command Center."""
    st.header("⚡ Executive Command Center")
    st.markdown("Real-time omnichannel sales performance, operational alerts, and profitability metrics.")

    if df_filtered.empty or df_filtered['order_date'].isnull().all():
        st.warning("⚠️ No sales transactions found matching the current global filter selection. Please adjust your date range or sidebar filters.")
        return

    plotly_template = st.session_state.get('plotly_template', 'plotly_dark')

    # 1. Executive Alert Banners
    render_executive_alerts(df_filtered)

    # 2. Compute KPIs & Prior Period Deltas safely
    max_d = df_filtered['order_date'].max()
    min_d = df_filtered['order_date'].min()
    
    if pd.isna(min_d) or pd.isna(max_d):
        st.warning("⚠️ Invalid date range in filtered records.")
        return

    days_span = max(int((max_d - min_d).days), 1)
    
    prior_start = min_d - pd.Timedelta(days=days_span + 1)
    prior_end = min_d - pd.Timedelta(days=1)
    
    df_prior = df_raw[(df_raw['order_date'] >= prior_start) & (df_raw['order_date'] <= prior_end)]
    
    curr_kpis, deltas = calculate_kpi_deltas(df_filtered, df_prior)

    # 3. Render 8 High-Aesthetic Groww-Style KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    def render_groww_kpi(container, title, value_str, delta_val):
        arrow = "▲" if delta_val >= 0 else "▼"
        badge_class = "groww-badge-pos" if delta_val >= 0 else "groww-badge-neg"
        delta_str = f"{arrow} {abs(delta_val):.1f}% vs prior"
        
        container.markdown(f"""
        <div class='groww-card'>
            <div class='groww-title'>{title}</div>
            <div class='groww-value'>{value_str}</div>
            <div><span class='{badge_class}'>{delta_str}</span></div>
        </div>
        """, unsafe_allow_html=True)

    render_groww_kpi(col1, "Net Revenue", fmt_currency(curr_kpis['net_revenue']), deltas['net_revenue'])
    render_groww_kpi(col2, "Net Profit", fmt_currency(curr_kpis['net_profit']), deltas['net_profit'])
    render_groww_kpi(col3, "Profit Margin", fmt_percent(curr_kpis['margin_pct']), deltas['margin_pct'])
    render_groww_kpi(col4, "Completed Orders", fmt_number(curr_kpis['total_orders']), deltas['total_orders'])

    render_groww_kpi(col5, "Avg Order Value (AOV)", fmt_currency_exact(curr_kpis['aov']), deltas['aov'])
    render_groww_kpi(col6, "Repeat Buyer Rate", fmt_percent(curr_kpis['repeat_rate_pct']), deltas['repeat_rate_pct'])
    render_groww_kpi(col7, "Total Customers", fmt_number(curr_kpis['total_customers']), deltas['total_customers'])
    render_groww_kpi(col8, "Rev per Customer", fmt_currency_exact(curr_kpis['rev_per_customer']), deltas['rev_per_customer'])

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. High-Aesthetic Smooth Spline Plotly Chart
    st.subheader("📈 Revenue & Net Profit Growth Trends")
    
    monthly = df_filtered.set_index('order_date').resample('ME')[['net_revenue', 'net_profit']].sum().reset_index()
    monthly['order_year_month'] = monthly['order_date'].dt.strftime('%Y-%m')

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly['order_year_month'],
        y=monthly['net_revenue'],
        name="Net Revenue ($)",
        mode="lines+markers",
        line=dict(color="#00D09C", width=3.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 208, 156, 0.08)'
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly['order_year_month'],
        y=monthly['net_profit'],
        name="Net Profit ($)",
        mode="lines+markers",
        line=dict(color="#00B8D9", width=3.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 184, 217, 0.08)'
    ))
    fig_trend.update_layout(
        template=plotly_template,
        height=390,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # 5. Maps & Geographic Breakdown
    st.subheader("🌍 Regional & Channel Performance Matrix")
    
    map_col, channel_col = st.columns([1.6, 1])

    with map_col:
        map_style_opt = st.radio("Map Style", ["Choropleth Map", "Bubble Map"], horizontal=True)
        country_agg = df_filtered.groupby(['store_country', 'store_region']).agg(
            net_revenue=('net_revenue', 'sum'),
            net_profit=('net_profit', 'sum')
        ).reset_index()

        if map_style_opt == "Choropleth Map":
            fig_map = px.choropleth(
                country_agg,
                locations="store_country",
                locationmode="country names",
                color="net_revenue",
                hover_name="store_country",
                hover_data=["store_region", "net_revenue", "net_profit"],
                color_continuous_scale="tealgrn",
                title="Global Revenue Distribution by Country"
            )
        else:
            fig_map = px.scatter_geo(
                country_agg,
                locations="store_country",
                locationmode="country names",
                size="net_revenue",
                color="net_profit",
                hover_name="store_country",
                color_continuous_scale="emrld",
                title="Global Profitability Bubble Map"
            )

        fig_map.update_layout(template=plotly_template, height=380, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_map, use_container_width=True)

    with channel_col:
        st.markdown("#### Profitability by Channel")
        chan_agg = df_filtered.groupby('channel')[['net_revenue', 'net_profit']].sum().reset_index()
        fig_chan = px.bar(
            chan_agg,
            x="channel",
            y=["net_revenue", "net_profit"],
            barmode="group",
            color_discrete_sequence=["#00D09C", "#00B8D9"],
            title="Online vs Retail Store Net Revenue & Profit"
        )
        fig_chan.update_layout(template=plotly_template, height=380, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_chan, use_container_width=True)

    # 6. Category Contribution & Top Performers
    col_cat, col_store, col_prod = st.columns(3)

    with col_cat:
        st.markdown("#### Category Contribution")
        cat_agg = df_filtered.groupby('category')['net_revenue'].sum().reset_index()
        fig_cat = px.pie(
            cat_agg,
            values="net_revenue",
            names="category",
            color_discrete_sequence=["#00D09C", "#00B8D9", "#FFB300"],
            hole=0.5
        )
        fig_cat.update_layout(template=plotly_template, height=300, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_store:
        st.markdown("#### Top Stores by Profit")
        store_agg = df_filtered.groupby('store_name')['net_profit'].sum().reset_index().sort_values(by='net_profit', ascending=True).tail(5)
        fig_store = px.bar(
            store_agg,
            x="net_profit",
            y="store_name",
            orientation="h",
            color_discrete_sequence=["#00D09C"]
        )
        fig_store.update_layout(template=plotly_template, height=300, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_store, use_container_width=True)

    with col_prod:
        st.markdown("#### Top Products by Revenue")
        prod_agg = df_filtered.groupby('product_name')['net_revenue'].sum().reset_index().sort_values(by='net_revenue', ascending=True).tail(5)
        fig_prod = px.bar(
            prod_agg,
            x="net_revenue",
            y="product_name",
            orientation="h",
            color_discrete_sequence=["#00B8D9"]
        )
        fig_prod.update_layout(template=plotly_template, height=300, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_prod, use_container_width=True)

    st.markdown("---")

    # 7. AI Executive Insights Component
    render_ai_executive_insights(df_filtered)
