#!/usr/bin/env python3
"""
Automated ETL Ingestion & Database Assembly Script for Lumina Lifestyle & Living.
Reads raw CSV datasets from data/, initializes the SQLite database database/lumina_retail.db,
applies database/schema.sql and database/views.sql, loads data with constraint verification,
and executes database/data_validation.sql.
"""

import os
import csv
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "lumina_retail.db")

SCHEMA_SQL_PATH = os.path.join(DB_DIR, "schema.sql")
VIEWS_SQL_PATH = os.path.join(DB_DIR, "views.sql")
VALIDATION_SQL_PATH = os.path.join(DB_DIR, "data_validation.sql")

def run_etl():
    print(f"Initializing ETL Ingestion Pipeline -> Database: {DB_PATH}")
    
    # Remove existing db file if recreating
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing SQLite database file.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Apply Schema DDL
    print("Applying database schema DDL...")
    with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()

    # 2. Ingest Stores
    stores_csv = os.path.join(DATA_DIR, "stores.csv")
    with open(stores_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        stores_rows = [(row["store_id"], row["store_name"], row["channel"], row["region"], row["city"], row["manager_name"]) for row in reader]
    cursor.executemany("INSERT INTO stores VALUES (?, ?, ?, ?, ?, ?);", stores_rows)
    print(f"Loaded {len(stores_rows)} rows into 'stores'")

    # 3. Ingest Products
    products_csv = os.path.join(DATA_DIR, "products.csv")
    with open(products_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        products_rows = [(row["product_id"], row["product_name"], row["category"], row["subcategory"], row["unit_cost"], row["unit_price"], row["is_active"]) for row in reader]
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?);", products_rows)
    print(f"Loaded {len(products_rows)} rows into 'products'")

    # 4. Ingest Customers
    customers_csv = os.path.join(DATA_DIR, "customers.csv")
    with open(customers_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        customers_rows = [(row["customer_id"], row["first_name"], row["last_name"], row["email"], row["phone"], row["city"], row["region"], row["signup_date"], row["customer_segment"]) for row in reader]
    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", customers_rows)
    print(f"Loaded {len(customers_rows)} rows into 'customers'")

    # 5. Ingest Orders
    orders_csv = os.path.join(DATA_DIR, "orders.csv")
    with open(orders_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        orders_rows = [(row["order_id"], row["customer_id"], row["store_id"], row["order_date"], row["order_status"], row["payment_method"], row["shipping_cost"]) for row in reader]
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?);", orders_rows)
    print(f"Loaded {len(orders_rows)} rows into 'orders'")

    # 6. Ingest Order Items
    order_items_csv = os.path.join(DATA_DIR, "order_items.csv")
    with open(order_items_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        items_rows = [(row["item_id"], row["order_id"], row["product_id"], row["quantity"], row["unit_price"], row["discount_percent"]) for row in reader]
    cursor.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?);", items_rows)
    print(f"Loaded {len(items_rows)} rows into 'order_items'")

    conn.commit()

    # 7. Apply Views
    print("Creating analytical view 'vw_sales_analytics'...")
    with open(VIEWS_SQL_PATH, "r", encoding="utf-8") as f:
        views_sql = f.read()
    cursor.executescript(views_sql)
    conn.commit()

    # 8. Run Validation Suite
    print("\n--- RUNNING DATA VALIDATION CHECKS ---")
    with open(VALIDATION_SQL_PATH, "r", encoding="utf-8") as f:
        val_sql = f.read()
    
    statements = [s.strip() for s in val_sql.split(";") if s.strip()]
    for stmt in statements:
        if stmt.startswith("--"):
            continue
        cursor.execute(stmt)
        results = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        print(f"Query: {stmt[:40]}...")
        for r in results:
            print(f"  {col_names}: {r}")

    conn.close()
    print("\nETL Pipeline completed successfully! Database is ready for queries.")

if __name__ == "__main__":
    run_etl()
