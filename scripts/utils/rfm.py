"""
RFM (Recency, Frequency, Monetary) Scoring & Customer Segmentation Utility.
"""

import pandas as pd
import numpy as np

def compute_rfm_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes RFM raw metrics and maps customers into strategic segments:
    - Champions
    - Loyalists
    - Potential Loyalists
    - At Risk
    - Lost
    """
    if df.empty:
        return pd.DataFrame()

    ref_date = df['order_date'].max()

    rfm = df.groupby('customer_id').agg(
        customer_name=('customer_name', 'first'),
        customer_email=('customer_email', 'first'),
        customer_segment=('customer_segment', 'first'),
        region=('customer_region', 'first'),
        recency_days=('order_date', lambda dates: (ref_date - dates.max()).days),
        frequency_orders=('order_id', 'nunique'),
        monetary_net_revenue=('net_revenue', 'sum'),
        monetary_net_profit=('net_profit', 'sum'),
        last_order_date=('order_date', 'max'),
        favorite_category=('category', lambda cats: cats.mode()[0] if not cats.empty else 'N/A')
    ).reset_index()

    if len(rfm) < 4:
        rfm['r_score'] = 3
        rfm['f_score'] = 3
        rfm['m_score'] = 3
    else:
        # Quartile scoring (4 is best, 1 is worst)
        rfm['r_score'] = pd.qcut(rfm['recency_days'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['f_score'] = pd.qcut(rfm['frequency_orders'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
        rfm['m_score'] = pd.qcut(rfm['monetary_net_revenue'], q=4, labels=[1, 2, 3, 4], duplicates='drop')

    # Convert to int
    rfm['r_score'] = rfm['r_score'].astype(int)
    rfm['f_score'] = rfm['f_score'].astype(int)
    rfm['m_score'] = rfm['m_score'].astype(int)

    def map_rfm_segment(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']
        if r >= 3 and f >= 3 and m >= 3:
            return 'Champions'
        elif r >= 3 and f >= 2:
            return 'Loyalists'
        elif r >= 3 and f <= 2:
            return 'Potential Loyalists'
        elif r <= 2 and f >= 2:
            return 'At Risk'
        else:
            return 'Lost'

    rfm['rfm_segment'] = rfm.apply(map_rfm_segment, axis=1)
    
    # Loyalty Score (1 to 100)
    rfm['loyalty_score'] = np.round(((rfm['r_score'] + rfm['f_score'] + rfm['m_score']) / 12.0) * 100.0, 1)

    return rfm
