"""
Metrics & KPI Delta Calculation Helper Utility.
"""

import pandas as pd

def calculate_kpis(df: pd.DataFrame):
    """
    Computes total Net Revenue, Net Profit, Margin %, Total Orders, AOV, 
    Repeat Customer Rate %, Total Customers, and Revenue per Customer.
    """
    if df.empty:
        return {
            "net_revenue": 0.0,
            "net_profit": 0.0,
            "margin_pct": 0.0,
            "total_orders": 0,
            "aov": 0.0,
            "repeat_rate_pct": 0.0,
            "total_customers": 0,
            "rev_per_customer": 0.0
        }

    net_revenue = df['net_revenue'].sum()
    net_profit = df['net_profit'].sum()
    margin_pct = (net_profit / net_revenue * 100.0) if net_revenue > 0 else 0.0
    total_orders = df['order_id'].nunique()
    aov = (net_revenue / total_orders) if total_orders > 0 else 0.0
    
    total_customers = df['customer_id'].nunique()
    rev_per_customer = (net_revenue / total_customers) if total_customers > 0 else 0.0
    
    # Calculate Repeat Buyer Rate
    customer_order_counts = df.groupby('customer_id')['order_id'].nunique()
    repeat_customers = (customer_order_counts > 1).sum()
    repeat_rate_pct = (repeat_customers / total_customers * 100.0) if total_customers > 0 else 0.0

    return {
        "net_revenue": net_revenue,
        "net_profit": net_profit,
        "margin_pct": margin_pct,
        "total_orders": total_orders,
        "aov": aov,
        "repeat_rate_pct": repeat_rate_pct,
        "total_customers": total_customers,
        "rev_per_customer": rev_per_customer
    }

def calculate_kpi_deltas(df_current: pd.DataFrame, df_prior: pd.DataFrame):
    """Calculates percentage deltas between current filtered period and prior period."""
    curr = calculate_kpis(df_current)
    prior = calculate_kpis(df_prior)
    
    deltas = {}
    for key in curr:
        curr_val = curr[key]
        prior_val = prior[key]
        if prior_val > 0:
            pct_change = ((curr_val - prior_val) / prior_val) * 100.0
        else:
            pct_change = 0.0
        deltas[key] = pct_change
    return curr, deltas
