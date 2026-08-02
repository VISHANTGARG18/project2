#!/usr/bin/env python3
"""
Market Basket & Product Co-Purchasing Association Analysis Engine.
Analyzes multi-item order transactions from database/lumina_retail.db,
computes Support, Confidence, and Lift metrics for product pairs,
and outputs strategic cross-selling recommendations for retail merchandising.
"""

import os
import sqlite3
from collections import defaultdict
from itertools import combinations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "lumina_retail.db")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
OUTPUT_MD_PATH = os.path.join(DOCS_DIR, "market_basket_analysis.md")

def run_market_basket_analysis():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query completed order line items
    query = """
    SELECT 
        oi.order_id,
        p.product_name,
        p.category
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_status = 'Completed'
    ORDER BY oi.order_id ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Group products by order_id
    order_baskets = defaultdict(set)
    for order_id, product_name, category in rows:
        order_baskets[order_id].add(product_name)

    total_orders = len(order_baskets)
    multi_item_baskets = [basket for basket in order_baskets.values() if len(basket) > 1]
    total_multi_item_orders = len(multi_item_baskets)

    # Count individual product frequencies
    item_counts = defaultdict(int)
    # Count pair frequencies
    pair_counts = defaultdict(int)

    for basket in order_baskets.values():
        for item in basket:
            item_counts[item] += 1
        for item1, item2 in combinations(sorted(basket), 2):
            pair_counts[(item1, item2)] += 1

    # Calculate Association Rules (Support, Confidence, Lift)
    rules = []
    for (item_a, item_b), pair_freq in pair_counts.items():
        support_a_b = pair_freq / total_orders
        support_a = item_counts[item_a] / total_orders
        support_b = item_counts[item_b] / total_orders

        # Rule 1: A -> B
        confidence_a_b = pair_freq / item_counts[item_a]
        lift_a_b = confidence_a_b / support_b

        # Rule 2: B -> A
        confidence_b_a = pair_freq / item_counts[item_b]
        lift_b_a = confidence_b_a / support_a

        rules.append({
            "antecedent": item_a,
            "consequent": item_b,
            "pair_freq": pair_freq,
            "support": support_a_b,
            "confidence": confidence_a_b,
            "lift": lift_a_b
        })
        rules.append({
            "antecedent": item_b,
            "consequent": item_a,
            "pair_freq": pair_freq,
            "support": support_a_b,
            "confidence": confidence_b_a,
            "lift": lift_b_a
        })

    # Sort rules by Lift descending
    rules.sort(key=lambda x: x["lift"], reverse=True)

    print("==========================================================================")
    print("  LUMINA LIFESTYLE & LIVING - MARKET BASKET ASSOCIATION ANALYSIS")
    print("==========================================================================")
    print(f"Total Completed Orders Analyzed: {total_orders:,}")
    print(f"Multi-Item Basket Transactions:  {total_multi_item_orders:,} ({total_multi_item_orders/total_orders*100:.1f}% of total)\n")

    top_rules = rules[:10]
    print(f"{'Base Product (Antecedent)':<38} -> {'Recommended Cross-Sell (Consequent)':<38} | {'Pairs':<5} | {'Confidence':<10} | {'Lift':<6}")
    print("-" * 105)
    for r in top_rules:
        print(f"{r['antecedent'][:37]:<38} -> {r['consequent'][:37]:<38} | {r['pair_freq']:<5} | {r['confidence']*100:>8.2f}% | {r['lift']:>5.2f}x")

    # Generate Markdown documentation file
    md_content = f"""# Market Basket Association & Product Cross-Sell Analysis

This analysis applies Market Basket Mining to **{total_orders:,} completed orders** ({total_multi_item_orders:,} multi-item baskets) to discover product co-purchasing patterns, calculate **Support**, **Confidence**, and **Lift** ratios, and optimize checkout cross-selling bundles.

---

## 1. Executive Metrics & Methodology

- **Support**: $P(A \\cap B)$ - Percentage of overall orders containing both Product A and Product B.
- **Confidence**: $P(B \\mid A)$ - Likelihood that a customer buying Product A also purchases Product B.
- **Lift**: $\\frac{{P(B \\mid A)}}{{P(B)}}$ - Magnitude of purchasing power increase compared to random chance ($>1.0$ indicates positive association).

---

## 2. Top Product Co-Purchasing Association Rules

| Base Product (Antecedent) | Recommended Cross-Sell (Consequent) | Co-Purchased Orders | Confidence % | Lift Ratio | Strategic Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for r in top_rules:
        action = "Bundle at Checkout" if r['lift'] > 1.1 else "Promote Cross-Sell"
        md_content += f"| **{r['antecedent']}** | {r['consequent']} | {r['pair_freq']} | {r['confidence']*100:.2f}% | **{r['lift']:.2f}x** | {action} |\n"

    md_content += """
---

## 3. Merchandising Strategy Recommendations

1. **Smart Electronics Bundles**: Pair high-volume *Ultra-HD 4K Smart Monitors* with *Mechanical Backlit Keyboards* or *Wireless Trackball Mice* at checkout with a 5% bundle incentive.
2. **Outdoor Living Patio Packages**: Cross-sell *Insulated Coolers* alongside *All-Weather Patio Sets* during Q2/Q3 checkout flows.
3. **Home Office Ergonomic Sets**: Offer automatic add-on discounts for *Aura LED Desk Lamps* when customers purchase *Lumina Standing Desk Pros*.
"""

    with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nSaved Market Basket Analysis report to: {OUTPUT_MD_PATH}")

if __name__ == "__main__":
    run_market_basket_analysis()
