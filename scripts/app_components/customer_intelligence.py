"""
Tab 3: Customer Analytics & Customer 360 Profile Component.
Features Customer 360 lookup, RFM segment distribution, order timeline, and Cohort Retention Heatmap.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from utils.rfm import compute_rfm_segments
from utils.helpers import fmt_currency, fmt_percent, fmt_number
from .styling import get_plotly_theme_dict

def render_customer_intelligence_tab(df_filtered: pd.DataFrame):
    """Renders the Tab 3 Customer Analytics component."""
    st.header("👥 Customer Analytics & 360° Profile")
    st.markdown("Individual customer lookup, RFM behavioral segmentation, and 24-month cohort retention heatmaps.")

    if df_filtered.empty:
        st.warning("No data available for active filters.")
        return

    theme_mode = st.session_state.get('theme_mode', 'Dark Mode 🌙')
    theme_kwargs = get_plotly_theme_dict(theme_mode)

    # Compute RFM Segments
    rfm_df = compute_rfm_segments(df_filtered)

    # 1. Customer Segment Distribution
    st.subheader("📊 Customer Segment Distribution (RFM Segmentation)")
    
    col_rfm_chart, col_rfm_table = st.columns([1.2, 1])

    with col_rfm_chart:
        segment_counts = rfm_df.groupby('rfm_segment').agg(
            customer_count=('customer_id', 'count'),
            total_net_revenue=('monetary_net_revenue', 'sum'),
            total_net_profit=('monetary_net_profit', 'sum')
        ).reset_index()

        fig_rfm = px.bar(
            segment_counts,
            x="rfm_segment",
            y="total_net_revenue",
            color="rfm_segment",
            text="customer_count",
            title="Net Revenue by RFM Segment (Bar height = Revenue, Label = Customers)",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_rfm.update_layout(height=350, margin=dict(l=10, r=10, t=35, b=10), **theme_kwargs)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col_rfm_table:
        st.markdown("#### Segment Performance Summary")
        segment_counts['margin_pct'] = (segment_counts['total_net_profit'] / segment_counts['total_net_revenue'] * 100.0).round(2)
        st.dataframe(
            segment_counts.style.format({
                'total_net_revenue': '${:,.2f}',
                'total_net_profit': '${:,.2f}',
                'margin_pct': '{:.2f}%',
                'customer_count': '{:,}'
            }),
            use_container_width=True
        )

    st.markdown("---")

    # 2. Customer 360 Profile Lookup Tool
    st.subheader("👤 Customer 360° Individual Lookup")
    st.markdown("Search any account by name, email, or customer ID to inspect full spend history and timeline.")

    search_input = st.text_input("🔎 Search Customer Name, Email, or ID", "Alexander Smith")

    matching_customers = rfm_df[
        rfm_df['customer_name'].str.contains(search_input, case=False, na=False) |
        rfm_df['customer_email'].str.contains(search_input, case=False, na=False) |
        rfm_df['customer_id'].astype(str).str.contains(search_input, case=False, na=False)
    ]

    if not matching_customers.empty:
        selected_cid = st.selectbox(
            "Select Customer Account",
            matching_customers['customer_id'].unique(),
            format_func=lambda cid: f"{matching_customers[matching_customers['customer_id'] == cid]['customer_name'].values[0]} ({matching_customers[matching_customers['customer_id'] == cid]['customer_email'].values[0]})"
        )

        cust_profile = rfm_df[rfm_df['customer_id'] == selected_cid].iloc[0]
        cust_orders = df_filtered[df_filtered['customer_id'] == selected_cid].sort_values(by='order_date', ascending=False)

        # Profile Cards
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Lifetime Spend", fmt_currency(cust_profile['monetary_net_revenue']))
        c2.metric("Total Orders", fmt_number(cust_profile['frequency_orders']))
        c3.metric("Loyalty Score", f"{cust_profile['loyalty_score']} / 100")
        c4.metric("RFM Segment", cust_profile['rfm_segment'])
        c5.metric("Favorite Category", cust_profile['favorite_category'])

        col_trend, col_timeline = st.columns([1, 1.2])

        with col_trend:
            st.markdown("#### Monthly Spend History")
            cust_monthly = cust_orders.set_index('order_date').resample('ME')['net_revenue'].sum().reset_index()
            cust_monthly['order_date'] = cust_monthly['order_date'].dt.strftime('%Y-%m')
            fig_cust_trend = px.line(cust_monthly, x='order_date', y='net_revenue', markers=True, title="Customer Spend Timeline")
            fig_cust_trend.update_layout(height=280, margin=dict(l=10, r=10, t=30, b=10), **theme_kwargs)
            st.plotly_chart(fig_cust_trend, use_container_width=True)

        with col_timeline:
            st.markdown("#### Order Transactions Timeline")
            st.dataframe(
                cust_orders[['order_id', 'order_date', 'store_name', 'product_name', 'quantity', 'unit_price', 'net_revenue']].style.format({
                    'unit_price': '${:,.2f}',
                    'net_revenue': '${:,.2f}',
                    'quantity': '{:,}'
                }),
                use_container_width=True
            )

    else:
        st.info("No matching customer found. Try searching for 'Alexander' or 'Smith'.")

    st.markdown("---")

    # 3. Interactive Cohort Retention Heatmap
    st.subheader("📅 24-Month Signup Cohort Retention Heatmap")
    
    df_cohort = df_filtered.copy()
    df_cohort['cohort_month'] = df_cohort['customer_signup_date'].dt.strftime('%Y-%m')
    df_cohort['order_month'] = df_cohort['order_date'].dt.strftime('%Y-%m')

    cohort_pivot = df_cohort.pivot_table(
        index='cohort_month',
        columns='order_month',
        values='customer_id',
        aggfunc='nunique'
    ).fillna(0)

    if not cohort_pivot.empty:
        fig_heatmap = px.imshow(
            cohort_pivot,
            labels=dict(x="Order Month", y="Signup Cohort Month", color="Active Buyers"),
            x=cohort_pivot.columns,
            y=cohort_pivot.index,
            color_continuous_scale="Tealgrn",
            title="Monthly Active Buyers by Signup Cohort"
        )
        fig_heatmap.update_layout(height=450, margin=dict(l=10, r=10, t=35, b=10), **theme_kwargs)
        st.plotly_chart(fig_heatmap, use_container_width=True)
