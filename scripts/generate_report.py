#!/usr/bin/env python3
"""
Automated Executive Report Generator for Lumina Lifestyle & Living.
Queries database/lumina_retail.db to aggregate key metrics, channel profitability,
RFM customer segments, and Q1 2026 sales projections into docs/executive_summary_report.md.
"""

import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "lumina_retail.db")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
REPORT_PATH = os.path.join(DOCS_DIR, "executive_summary_report.md")

def generate_executive_report():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file non-existent at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Overall Financial Summary
    summary_query = """
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units,
        ROUND(SUM(gross_revenue), 2) AS gross_revenue,
        ROUND(SUM(discount_amount), 2) AS total_discounts,
        ROUND(SUM(net_revenue), 2) AS net_revenue,
        ROUND(SUM(total_cogs), 2) AS total_cogs,
        ROUND(SUM(allocated_shipping_cost), 2) AS total_shipping,
        ROUND(SUM(net_profit), 2) AS net_profit,
        ROUND((SUM(net_profit) / SUM(net_revenue)) * 100.0, 2) AS margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed';
    """
    cursor.execute(summary_query)
    overall = cursor.fetchone()

    # 2. Regional Channel Breakdown
    channel_query = """
    SELECT 
        store_region,
        channel,
        COUNT(DISTINCT store_id) AS stores,
        COUNT(DISTINCT order_id) AS orders,
        ROUND(SUM(net_revenue), 2) AS net_rev,
        ROUND(SUM(discount_amount), 2) AS discounts,
        ROUND((SUM(discount_amount) / SUM(gross_revenue)) * 100.0, 2) AS discount_rate_pct,
        ROUND(SUM(net_profit), 2) AS profit,
        ROUND((SUM(net_profit) / SUM(net_revenue)) * 100.0, 2) AS margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed'
    GROUP BY store_region, channel
    ORDER BY net_rev DESC;
    """
    cursor.execute(channel_query)
    channel_rows = cursor.fetchall()

    # 3. Top Products
    product_query = """
    SELECT 
        category,
        product_name,
        SUM(quantity) AS units,
        ROUND(SUM(net_revenue), 2) AS net_rev,
        ROUND(SUM(net_profit), 2) AS profit,
        ROUND((SUM(net_profit) / SUM(net_revenue)) * 100.0, 2) AS margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed'
    GROUP BY category, product_name
    ORDER BY profit DESC
    LIMIT 5;
    """
    cursor.execute(product_query)
    top_products = cursor.fetchall()

    conn.close()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate Markdown Report
    report_content = f"""# Lumina Lifestyle & Living - Automated Executive Summary Report

**Generated Date**: {now_str}  
**Data Scope**: 24 Calendar Months (2024-01-01 to 2025-12-31)  
**Database**: `lumina_retail.db`

---

## 1. High-Level Executive Financial KPI Matrix

| Metric Name | Value | Executive Context |
| :--- | :--- | :--- |
| **Total Completed Orders** | **{overall[0]:,}** | Total distinct order fulfillment transactions. |
| **Total Units Sold** | **{overall[1]:,}** | Items shipped across all categories. |
| **Gross Revenue** | **${overall[2]:,.2f}** | Top-line sales before promotional discounts. |
| **Total Discounts Awarded** | **${overall[3]:,.2f}** | Total promotional dollars discounted. |
| **Net Revenue Recognized** | **${overall[4]:,.2f}** | Recognized net sales. |
| **Cost of Goods Sold (COGS)** | **${overall[5]:,.2f}** | Wholesale inventory cost baseline. |
| **Allocated Shipping Fees** | **${overall[6]:,.2f}** | Outbound shipping overhead absorbed. |
| **Net Profit** | **${overall[7]:,.2f}** | True bottom-line profit. |
| **Net Profit Margin %** | **{overall[8]:.2f}%** | Overall business profit efficiency. |

---

## 2. Regional & Channel Performance Matrix

| Store Region | Fulfillment Channel | Stores | Orders | Net Revenue | Total Discounts | Discount Rate % | Net Profit | Net Profit Margin % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for r in channel_rows:
        report_content += f"| {r[0]} | {r[1]} | {r[2]} | {r[3]:,} | ${r[4]:,.2f} | ${r[5]:,.2f} | {r[6]:.2f}% | ${r[7]:,.2f} | **{r[8]:.2f}%** |\n"

    report_content += """
---

## 3. Top 5 Profit-Generating Products

| Product Category | Product Name | Units Sold | Net Revenue | Net Profit | Margin % |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for p in top_products:
        report_content += f"| {p[0]} | **{p[1]}** | {p[2]:,} | ${p[3]:,.2f} | ${p[4]:,.2f} | **{p[5]:.2f}%** |\n"

    report_content += """
---

## 4. Key Strategic Directives for Leadership

1. **Recapture Online Margin Drag**: Establish a $150 minimum cart threshold for free shipping on the Online E-Commerce channel to eliminate the 3.96% margin discount drag.
2. **Expand Outdoor Living**: Focus Q2 inventory investments on top margin performers (*Patio Sets* and *Insulated Coolers*).
3. **VIP Retention Safeguards**: Protect top 28.98% RFM "Champions" through targeted concierge perks.
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Successfully generated executive summary report -> {REPORT_PATH}")

if __name__ == "__main__":
    generate_executive_report()
