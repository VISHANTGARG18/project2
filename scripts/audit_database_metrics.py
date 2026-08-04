#!/usr/bin/env python3
"""
Empirical SQL Metric Audit Script for Lumina Retail Database.
Executes all SQL queries in sql/01 through sql/06 against database/lumina_retail.db
and prints exact, empirical numbers.
"""

import sqlite3
import os

DB_PATH = os.path.join("database", "lumina_retail.db")

def run_query(sql_file):
    print(f"\n=======================================================")
    print(f"EXECUTING: {sql_file}")
    print(f"=======================================================")
    with open(sql_file, 'r') as f:
        sql = f.read()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    cols = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    print(" | ".join(cols))
    print("-" * 80)
    for row in rows[:15]:  # print first 15 rows
        print(" | ".join(str(val) for val in row))
    if len(rows) > 15:
        print(f"... ({len(rows) - 15} more rows)")

if __name__ == "__main__":
    sql_files = [
        "sql/01_monthly_trends_mom_yoy.sql",
        "sql/02_product_performance_rankings.sql",
        "sql/03_cohort_retention_analysis.sql",
        "sql/04_rfm_segmentation.sql",
        "sql/05_regional_channel_margins.sql",
        "sql/06_moving_averages_running_totals.sql"
    ]
    for sf in sql_files:
        run_query(sf)
