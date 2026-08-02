"""
Tab 2: Product Intelligence Studio Component.
Features searchable product matrix, Profit vs Revenue scatter plot, Pareto 80/20 analysis,
ABC product classification, and Discount Scenario Simulator with Plotly gauges.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import fmt_currency, fmt_percent, fmt_number

def render_product_studio_tab(df_filtered: pd.DataFrame):
    """Renders the Tab 2 Product Intelligence Studio."""
    st.header("📦 Product Intelligence Studio")
    st.markdown("Catalog performance metrics, Pareto 80/20 classification, and Discount Scenario Simulator.")

    if df_filtered.empty:
        st.warning("No data available for active filters.")
        return

    # 1. Product Aggregation Matrix
    prod_agg = df_filtered.groupby(['product_name', 'category', 'subcategory']).agg(
        total_units_sold=('quantity', 'sum'),
        total_orders=('order_id', 'nunique'),
        gross_revenue=('gross_revenue', 'sum'),
        total_discounts=('discount_amount', 'sum'),
        net_revenue=('net_revenue', 'sum'),
        total_cogs=('total_cogs', 'sum'),
        net_profit=('net_profit', 'sum'),
        avg_discount_pct=('discount_percent', lambda x: x.mean() * 100.0),
        avg_selling_price=('unit_price', 'mean')
    ).reset_index()

    prod_agg['net_profit_margin_pct'] = (prod_agg['net_profit'] / prod_agg['net_revenue'] * 100.0).round(2)
    prod_agg = prod_agg.sort_values(by='net_revenue', ascending=False).reset_index(drop=True)

    # Pareto 80/20 & ABC Classification
    total_rev = prod_agg['net_revenue'].sum()
    prod_agg['cum_revenue'] = prod_agg['net_revenue'].cumsum()
    prod_agg['cum_revenue_pct'] = (prod_agg['cum_revenue'] / total_rev * 100.0)

    def classify_abc(cum_pct):
        if cum_pct <= 80.0:
            return 'Class A (Top 80% Rev)'
        elif cum_pct <= 95.0:
            return 'Class B (Next 15% Rev)'
        else:
            return 'Class C (Remaining 5%)'

    prod_agg['abc_class'] = prod_agg['cum_revenue_pct'].apply(classify_abc)

    # 2. Searchable Product Table
    st.subheader("📋 Product Performance Catalog")
    
    st.dataframe(
        prod_agg[[
            'product_name', 'category', 'abc_class', 'total_units_sold', 
            'net_revenue', 'net_profit', 'net_profit_margin_pct', 'avg_discount_pct', 'avg_selling_price'
        ]].style.format({
            'net_revenue': '${:,.2f}',
            'net_profit': '${:,.2f}',
            'net_profit_margin_pct': '{:.2f}%',
            'avg_discount_pct': '{:.2f}%',
            'avg_selling_price': '${:,.2f}',
            'total_units_sold': '{:,}'
        }),
        use_container_width=True
    )

    st.markdown("---")

    # 3. Profit vs Revenue Scatter Plot & Pareto Analysis
    col_scatter, col_pareto = st.columns([1.2, 1])

    with col_scatter:
        st.subheader("🎯 Profit vs. Revenue Scatter Analysis")
        fig_scatter = px.scatter(
            prod_agg,
            x="net_revenue",
            y="net_profit",
            size="total_units_sold",
            color="category",
            hover_name="product_name",
            text="product_name",
            color_discrete_sequence=px.colors.qualitative.Bold,
            title="Product Revenue vs. Net Profit (Bubble Size = Units Sold)"
        )
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_pareto:
        st.subheader("📊 Pareto 80/20 & ABC Distribution")
        abc_counts = prod_agg.groupby('abc_class')['product_name'].count().reset_index()
        fig_pareto = px.bar(
            abc_counts,
            x="abc_class",
            y="product_name",
            color="abc_class",
            title="ABC Category Product Counts",
            color_discrete_sequence=["#10B981", "#F59E0B", "#EF4444"]
        )
        fig_pareto.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_pareto, use_container_width=True)

    st.markdown("---")

    # 4. Discount & Pricing Scenario Simulator
    st.subheader("🎛️ Discount & Pricing Scenario Simulator")
    st.markdown("Adjust promotional rules and price increases to simulate real-time profit recovery.")

    sim_col1, sim_col2 = st.columns(2)

    with sim_col1:
        max_discount_cap = st.slider("Maximum Online Discount Cap %", 5, 30, 15, help="Cap online promotional discounts at this percentage.")
        free_shipping_min = st.slider("Minimum Free Shipping Threshold ($)", 0, 200, 150, help="Orders below this amount incur shipping fees.")
        
    with sim_col2:
        price_increase_pct = st.slider("List Price Increase %", 0.0, 15.0, 2.5, step=0.5, help="Simulate a minor catalog price adjustment.")
        volume_elasticity = st.slider("Expected Sales Volume Impact %", -15.0, 5.0, -2.0, step=0.5, help="Expected elasticity volume response.")

    # Recalculate Scenario Impact
    sim_df = df_filtered.copy()
    
    # Cap discount
    sim_df['sim_discount'] = sim_df['discount_percent'].clip(upper=max_discount_cap / 100.0)
    
    # Price adjustment
    sim_df['sim_unit_price'] = sim_df['unit_price'] * (1.0 + price_increase_pct / 100.0)
    sim_df['sim_quantity'] = (sim_df['quantity'] * (1.0 + volume_elasticity / 100.0)).round().clip(lower=1)
    
    # Compute simulated revenue & profit
    sim_df['sim_gross'] = sim_df['sim_quantity'] * sim_df['sim_unit_price']
    sim_df['sim_net_rev'] = sim_df['sim_gross'] * (1.0 - sim_df['sim_discount'])
    sim_df['sim_cogs'] = sim_df['sim_quantity'] * sim_df['unit_cost']
    sim_df['sim_net_profit'] = sim_df['sim_net_rev'] - sim_df['sim_cogs'] - sim_df['allocated_shipping_cost']

    base_profit = df_filtered['net_profit'].sum()
    sim_profit = sim_df['sim_net_profit'].sum()
    profit_recovery = sim_profit - base_profit
    sim_margin = (sim_profit / sim_df['sim_net_rev'].sum() * 100.0) if sim_df['sim_net_rev'].sum() > 0 else 0.0

    st.markdown("#### Scenario Impact Results")
    
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Simulated Net Revenue", fmt_currency(sim_df['sim_net_rev'].sum()))
    res_col2.metric("Simulated Net Profit", fmt_currency(sim_profit), f"+{fmt_currency(profit_recovery)}" if profit_recovery >= 0 else fmt_currency(profit_recovery))
    res_col3.metric("Simulated Profit Margin", fmt_percent(sim_margin))
    res_col4.metric("Annual Profit Recovery", fmt_currency(profit_recovery))

    # Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sim_margin,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Simulated Margin Efficiency (%)"},
        delta={'reference': (base_profit / total_rev * 100.0)},
        gauge={
            'axis': {'range': [0, 75]},
            'bar': {'color': "#10B981"},
            'steps': [
                {'range': [0, 50], 'color': "#EF4444"},
                {'range': [50, 60], 'color': "#F59E0B"},
                {'range': [60, 75], 'color': "#311B92"}
            ]
        }
    ))
    fig_gauge.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)
