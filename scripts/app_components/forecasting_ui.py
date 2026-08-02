"""
Tab 5: Forecasting Studio Component.
Features interactive controls for YoY growth, confidence interval bounds, inflation, and discounts,
displaying Optimistic, Base, and Pessimistic scenario graphs and projection tables.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from utils.forecasting import generate_monthly_forecast
from utils.helpers import fmt_currency, fmt_percent

def render_forecasting_tab(df_filtered: pd.DataFrame):
    """Renders the Tab 5 Forecasting Studio component."""
    st.header("📈 Time-Series Forecasting Studio & Scenario Modeling")
    st.markdown("Project future revenue, net profit, and margin bounds under customizable growth, inflation, and discount scenarios.")

    if df_filtered.empty:
        st.warning("No data available for active filters.")
        return

    # 1. Interactive Forecasting Sliders
    st.subheader("🎛️ Forecasting Controls & Inflation Adjustments")
    
    fc_col1, fc_col2, fc_col3, fc_col4 = st.columns(4)
    
    with fc_col1:
        growth_rate = st.slider("Expected YoY Growth %", -10.0, 30.0, 4.1, step=0.5)
    with fc_col2:
        conf_interval = st.slider("Confidence Interval Bounds ±%", 2.0, 15.0, 5.0, step=0.5)
    with fc_col3:
        inflation = st.slider("Inflation Adjustment %", 0.0, 10.0, 2.0, step=0.5)
    with fc_col4:
        discount_adjust = st.slider("Discount Policy Shift %", -5.0, 10.0, 0.0, step=0.5)

    # Generate Forecast
    monthly_hist, forecast_df = generate_monthly_forecast(
        df_filtered,
        growth_rate_pct=growth_rate,
        confidence_interval_pct=conf_interval,
        inflation_pct=inflation,
        discount_adjust_pct=discount_adjust
    )

    if forecast_df.empty:
        st.info("Insufficient historical monthly data to build projection model.")
        return

    st.markdown("---")

    # 2. Q1 2026 Forecast Summary Metrics
    q1_base_rev = forecast_df['base_revenue'].sum()
    q1_base_prof = forecast_df['base_profit'].sum()
    q1_opt_rev = forecast_df['optimistic_revenue'].sum()
    q1_pess_rev = forecast_df['pessimistic_revenue'].sum()
    q1_margin = (q1_base_prof / q1_base_rev * 100.0) if q1_base_rev > 0 else 0.0

    st.subheader("🔮 Q1 2026 Forecast Projection Summary")
    
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    q_col1.metric("Q1 Base Net Revenue", fmt_currency(q1_base_rev))
    q_col2.metric("Q1 Base Net Profit", fmt_currency(q1_base_prof))
    q_col3.metric("Optimistic Upper Bound", fmt_currency(q1_opt_rev))
    q_col4.metric("Pessimistic Lower Bound", fmt_currency(q1_pess_rev))

    st.markdown("---")

    # 3. Scenario Graph (Historical vs Optimistic / Base / Pessimistic)
    st.subheader("📉 Historical Sales vs. Projected Q1 Scenarios")

    fig_fc = go.Figure()
    
    # Historical Net Revenue
    fig_fc.add_trace(go.Scatter(
        x=monthly_hist['order_year_month'],
        y=monthly_hist['net_revenue'],
        name="Historical Net Revenue",
        mode="lines+markers",
        line=dict(color="#38BDF8", width=3)
    ))

    # Forecast Base Scenario
    fig_fc.add_trace(go.Scatter(
        x=forecast_df['target_month'],
        y=forecast_df['base_revenue'],
        name="Base Scenario",
        mode="lines+markers",
        line=dict(color="#FFB300", width=3, dash='dash')
    ))

    # Forecast Optimistic Bound
    fig_fc.add_trace(go.Scatter(
        x=forecast_df['target_month'],
        y=forecast_df['optimistic_revenue'],
        name="Optimistic Upper Bound",
        mode="lines",
        line=dict(color="#10B981", width=2, dash='dot')
    ))

    # Forecast Pessimistic Bound
    fig_fc.add_trace(go.Scatter(
        x=forecast_df['target_month'],
        y=forecast_df['pessimistic_revenue'],
        name="Pessimistic Lower Bound",
        mode="lines",
        line=dict(color="#EF4444", width=2, dash='dot')
    ))

    fig_fc.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=20, r=20, t=35, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    # 4. Monthly & Quarterly Projection Data Table
    st.subheader("📋 Monthly Q1 2026 Forecast Breakdown Table")
    
    st.dataframe(
        forecast_df[[
            'target_month', 'base_revenue', 'base_profit', 'base_margin_pct', 
            'optimistic_revenue', 'pessimistic_revenue'
        ]].style.format({
            'base_revenue': '${:,.2f}',
            'base_profit': '${:,.2f}',
            'optimistic_revenue': '${:,.2f}',
            'pessimistic_revenue': '${:,.2f}',
            'base_margin_pct': '{:.2f}%'
        }),
        use_container_width=True
    )
