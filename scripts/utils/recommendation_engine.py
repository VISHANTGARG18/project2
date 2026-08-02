"""
Market Basket Recommendation Engine Utility.
"""

from collections import defaultdict
from itertools import combinations
import pandas as pd

def compute_market_basket_rules(df: pd.DataFrame, min_support: float = 0.005, min_confidence: float = 0.05, min_lift: float = 1.0):
    """
    Computes Support, Confidence, and Lift ratios for item pairs in completed orders.
    """
    if df.empty:
        return pd.DataFrame()

    # Group products by order_id
    order_baskets = df.groupby('order_id')['product_name'].apply(set).to_dict()
    total_orders = len(order_baskets)

    if total_orders == 0:
        return pd.DataFrame()

    item_counts = defaultdict(int)
    pair_counts = defaultdict(int)

    for basket in order_baskets.values():
        for item in basket:
            item_counts[item] += 1
        for item1, item2 in combinations(sorted(basket), 2):
            pair_counts[(item1, item2)] += 1

    rules = []
    for (item_a, item_b), pair_freq in pair_counts.items():
        supp_a_b = pair_freq / total_orders
        if supp_a_b < min_support:
            continue

        supp_a = item_counts[item_a] / total_orders
        supp_b = item_counts[item_b] / total_orders

        # A -> B
        conf_a_b = pair_freq / item_counts[item_a]
        lift_a_b = conf_a_b / supp_b

        if conf_a_b >= min_confidence and lift_a_b >= min_lift:
            rules.append({
                "antecedent": item_a,
                "consequent": item_b,
                "pair_count": pair_freq,
                "support": supp_a_b,
                "confidence": conf_a_b,
                "lift": lift_a_b
            })

        # B -> A
        conf_b_a = pair_freq / item_counts[item_b]
        lift_b_a = conf_b_a / supp_a

        if conf_b_a >= min_confidence and lift_b_a >= min_lift:
            rules.append({
                "antecedent": item_b,
                "consequent": item_a,
                "pair_count": pair_freq,
                "support": supp_a_b,
                "confidence": conf_b_a,
                "lift": lift_b_a
            })

    rules_df = pd.DataFrame(rules)
    if not rules_df.empty:
        rules_df = rules_df.sort_values(by='lift', ascending=False).reset_index(drop=True)
    return rules_df
