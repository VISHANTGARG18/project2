"""
Tab 4: Market Basket Explorer Component.
Features interactive Support, Confidence, and Lift sliders, product bundle recommender,
and association rule matrix.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from utils.recommendation_engine import compute_market_basket_rules
from utils.helpers import fmt_currency, fmt_percent

def render_market_basket_tab(df_filtered: pd.DataFrame):
    """Renders the Tab 4 Market Basket Explorer component."""
    st.header("🛒 Market Basket Explorer & Cross-Sell Recommender")
    st.markdown("Association rule mining (Support, Confidence, Lift) for automated product bundle cross-selling.")

    if df_filtered.empty:
        st.warning("No data available for active filters.")
        return

    # 1. Interactive Sliders
    st.subheader("🎛️ Association Rule Parameters")
    
    col_supp, col_conf, col_lift = st.columns(3)
    
    with col_supp:
        min_supp = st.slider("Minimum Support %", 0.1, 5.0, 0.5, step=0.1) / 100.0
    with col_conf:
        min_conf = st.slider("Minimum Confidence %", 1.0, 50.0, 5.0, step=1.0) / 100.0
    with col_lift:
        min_lift = st.slider("Minimum Lift Ratio", 0.5, 3.0, 1.0, step=0.1)

    # Compute Rules
    rules_df = compute_market_basket_rules(df_filtered, min_support=min_supp, min_confidence=min_conf, min_lift=min_lift)

    if rules_df.empty:
        st.info("No association rules found for the selected parameters. Try lowering Minimum Support or Confidence.")
        return

    st.markdown("---")

    # 2. Choose any product to get recommended bundles
    st.subheader("🛍️ Interactive Product Bundle Recommender")
    
    all_products = sorted(list(df_filtered['product_name'].unique()))
    selected_prod = st.selectbox("Select a Base Product to View Cross-Sell Bundles", all_products)

    prod_rules = rules_df[rules_df['antecedent'] == selected_prod]

    if not prod_rules.empty:
        st.markdown(f"#### Top Recommended Cross-Sells for **{selected_prod}**")
        
        for r in prod_rules.head(3).itertuples():
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            col_b1.metric("Recommended Cross-Sell", r.consequent)
            col_b2.metric("Confidence %", fmt_percent(r.confidence * 100.0))
            col_b3.metric("Lift Ratio", f"{r.lift:.2f}x")
            col_b4.metric("Co-Purchased Orders", f"{r.pair_count:,}")
    else:
        st.info(f"No strong cross-sell rules found specifically for {selected_prod}. View all global rules below.")

    st.markdown("---")

    # 3. Association Rules Matrix Table & Scatter Plot
    st.subheader("📋 Top Global Association Rules Table")
    
    col_rule_table, col_rule_chart = st.columns([1.3, 1])

    with col_rule_table:
        st.dataframe(
            rules_df[['antecedent', 'consequent', 'pair_count', 'support', 'confidence', 'lift']].style.format({
                'support': '{:.2%}',
                'confidence': '{:.2%}',
                'lift': '{:.2f}x',
                'pair_count': '{:,}'
            }),
            use_container_width=True
        )

    with col_rule_chart:
        st.markdown("#### Confidence vs. Lift Scatter")
        fig_rules = px.scatter(
            rules_df,
            x="confidence",
            y="lift",
            size="pair_count",
            hover_name="antecedent",
            hover_data=["consequent"],
            color="lift",
            color_continuous_scale="Viridis",
            title="Rules Scatter (Confidence vs. Lift)"
        )
        fig_rules.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_rules, use_container_width=True)
