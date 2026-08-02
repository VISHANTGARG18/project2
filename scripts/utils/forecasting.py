"""
Time-Series Forecasting Engine & Scenario Bounds Utility.
"""

import pandas as pd
import numpy as np

def generate_monthly_forecast(df: pd.DataFrame, growth_rate_pct: float = 4.0, confidence_interval_pct: float = 5.0, inflation_pct: float = 0.0, discount_adjust_pct: float = 0.0):
    """
    Computes monthly historical net revenue and projects 3 scenarios:
    - Base Scenario
    - Optimistic Scenario (+Confidence Interval)
    - Pessimistic Scenario (-Confidence Interval)
    """
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    monthly = df.set_index('order_date').resample('ME')[['net_revenue', 'net_profit']].sum().reset_index()
    monthly['order_year_month'] = monthly['order_date'].dt.strftime('%Y-%m')

    # Effective annual growth factor adjusted by sliders
    effective_growth = (growth_rate_pct + inflation_pct - (discount_adjust_pct * 0.5)) / 100.0
    growth_multiplier = 1.0 + effective_growth

    # Forecast Q1 2026 months (2026-01, 2026-02, 2026-03)
    last_year_q1 = monthly[monthly['order_year_month'].isin(['2025-01', '2025-02', '2025-03'])].copy()
    
    if last_year_q1.empty:
        last_year_q1 = monthly.tail(3).copy()

    forecast_rows = []
    month_names = ['2026-01 (Jan)', '2026-02 (Feb)', '2026-03 (Mar)']
    
    for idx, row in enumerate(last_year_q1.itertuples()):
        if idx >= 3:
            break
        base_rev = row.net_revenue * growth_multiplier
        base_profit = row.net_profit * (growth_multiplier * 1.01)
        
        ci_factor = confidence_interval_pct / 100.0
        
        forecast_rows.append({
            "target_month": month_names[idx],
            "base_revenue": base_rev,
            "base_profit": base_profit,
            "optimistic_revenue": base_rev * (1.0 + ci_factor),
            "optimistic_profit": base_profit * (1.0 + ci_factor),
            "pessimistic_revenue": base_rev * (1.0 - ci_factor),
            "pessimistic_profit": base_profit * (1.0 - ci_factor),
            "base_margin_pct": (base_profit / base_rev * 100.0) if base_rev > 0 else 0.0
        })

    forecast_df = pd.DataFrame(forecast_rows)
    return monthly, forecast_df
