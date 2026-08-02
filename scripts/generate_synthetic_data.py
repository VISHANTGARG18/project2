#!/usr/bin/env python3
"""
Synthetic Data Generation Engine for Lumina Lifestyle & Living.
Generates 5 relational tables: customers, products, stores, orders, order_items.
Spans 2 full calendar years (2024-01-01 to 2025-12-31) with realistic real-world noise:
- Seasonal holiday spikes (Nov/Dec)
- Cancelled and returned orders (~6-8%)
- Varied discount percentages (0% to 35%)
- Multiple sales channels (Online E-Commerce vs. Retail Flagship Store)
- Multiple global regions (North America East, North America West, Europe Central, Asia Pacific)
- Mix of single-time, repeat, and churned customers.
"""

import os
import csv
import random
from datetime import datetime, timedelta

# Set deterministic random seed for reproducible realistic data
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE STORES (WITH STATE & COUNTRY COLUMNS)
# ---------------------------------------------------------
stores_data = [
    (101, "Lumina E-Commerce Store", "Online", "North America East", "New York", "New York", "United States", "Sarah Jenkins"),
    (102, "Lumina New York Flagship", "Retail Store", "North America East", "New York", "New York", "United States", "Marcus Vance"),
    (103, "Lumina San Francisco Hub", "Retail Store", "North America West", "San Francisco", "California", "United States", "Elena Rostova"),
    (104, "Lumina Seattle Tech Retail", "Retail Store", "North America West", "Seattle", "Washington", "United States", "David Kim"),
    (105, "Lumina London Concept Store", "Retail Store", "Europe Central", "London", "England", "United Kingdom", "Arthur Pendelton"),
    (106, "Lumina Berlin Design Center", "Retail Store", "Europe Central", "Berlin", "Berlin", "Germany", "Greta Weber"),
    (107, "Lumina Tokyo Ginza Outlet", "Retail Store", "Asia Pacific", "Tokyo", "Tokyo", "Japan", "Kenji Sato"),
    (108, "Lumina Sydney Harbour Retail", "Retail Store", "Asia Pacific", "Sydney", "New South Wales", "Australia", "Chloe Bennett")
]

stores_file = os.path.join(DATA_DIR, "stores.csv")
with open(stores_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["store_id", "store_name", "channel", "region", "city", "state", "country", "manager_name"])
    writer.writerows(stores_data)

print(f"Generated {len(stores_data)} stores in stores.csv")

# ---------------------------------------------------------
# 2. GENERATE PRODUCTS
# ---------------------------------------------------------
products_catalog = [
    # Premium Home Goods
    ("Lumina Ergonomic Executive Chair", "Premium Home Goods", "Furniture", 180.00, 450.00),
    ("Lumina Standing Desk Pro", "Premium Home Goods", "Furniture", 290.00, 680.00),
    ("Aura Ambient LED Desk Lamp", "Premium Home Goods", "Lighting", 25.00, 89.00),
    ("Minimalist Bamboo Bookshelf", "Premium Home Goods", "Furniture", 65.00, 160.00),
    ("Artisan Ceramic Coffee Set", "Premium Home Goods", "Kitchenware", 18.00, 55.00),
    ("Cast Iron Dutch Oven 5Qt", "Premium Home Goods", "Kitchenware", 42.00, 130.00),
    ("Luxury Memory Foam Pillow Pair", "Premium Home Goods", "Bedding", 22.00, 75.00),
    
    # Smart Electronics
    ("Lumina Noise-Cancelling Headphones", "Smart Electronics", "Audio", 85.00, 240.00),
    ("Lumina Wireless Soundbar 5.1", "Smart Electronics", "Audio", 110.00, 320.00),
    ("Smart Climate Controller Hub", "Smart Electronics", "Home Automation", 40.00, 119.00),
    ("Ultra-HD 4K Smart Monitor 32\"", "Smart Electronics", "Displays", 210.00, 520.00),
    ("Ergonomic Wireless Trackball Mouse", "Smart Electronics", "Accessories", 18.00, 49.00),
    ("Mechanical Backlit Keyboard", "Smart Electronics", "Accessories", 32.00, 95.00),
    ("Smart Security Camera 2-Pack", "Smart Electronics", "Home Automation", 55.00, 149.00),
    
    # Outdoor Living
    ("Lumina All-Weather Patio Set (4-pc)", "Outdoor Living", "Patio Furniture", 340.00, 890.00),
    ("Portable Stainless Steel Smokeless Grill", "Outdoor Living", "Cooking & Grilling", 75.00, 210.00),
    ("Solar Power Bank & Lantern 20,000mAh", "Outdoor Living", "Gear & Tech", 15.00, 45.00),
    ("Insulated Stainless Steel Cooler 45L", "Outdoor Living", "Gear & Tech", 60.00, 175.00),
    ("Waterproof Canvas Camping Tent 4-Person", "Outdoor Living", "Gear & Tech", 95.00, 260.00),
    ("Teak Wood Garden Bench", "Outdoor Living", "Patio Furniture", 120.00, 310.00)
]

products_data = []
for idx, p in enumerate(products_catalog, start=1001):
    products_data.append((idx, p[0], p[1], p[2], p[3], p[4], 1))

products_file = os.path.join(DATA_DIR, "products.csv")
with open(products_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "product_name", "category", "subcategory", "unit_cost", "unit_price", "is_active"])
    writer.writerows(products_data)

print(f"Generated {len(products_data)} products in products.csv")

# ---------------------------------------------------------
# 3. GENERATE CUSTOMERS
# ---------------------------------------------------------
FIRST_NAMES = ["Alexander", "Emily", "Michael", "Sophia", "Daniel", "Olivia", "James", "Ava", "William", "Isabella",
               "Benjamin", "Mia", "Lucas", "Charlotte", "Henry", "Amelia", "Mason", "Harper", "Ethan", "Evelyn",
               "Sebastian", "Abigail", "Logan", "Emily", "Jackson", "Elizabeth", "Levi", "Mila", "Oliver", "Ella"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]

REGIONS_CITIES = [
    ("North America East", ["New York", "Boston", "Toronto", "Philadelphia", "Atlanta"]),
    ("North America West", ["San Francisco", "Seattle", "Los Angeles", "Vancouver", "Denver"]),
    ("Europe Central", ["London", "Berlin", "Paris", "Amsterdam", "Zurich"]),
    ("Asia Pacific", ["Tokyo", "Sydney", "Singapore", "Melbourne", "Hong Kong"])
]

CUSTOMERS_COUNT = 1500
customers_data = []

start_signup = datetime(2023, 6, 1)  # Some signed up prior to 2024
end_signup = datetime(2025, 12, 15)
signup_span = (end_signup - start_signup).days

for cid in range(5001, 5001 + CUSTOMERS_COUNT):
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    email = f"{fn.lower()}.{ln.lower()}{cid}@example-lumina.com"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    region_info = random.choice(REGIONS_CITIES)
    region = region_info[0]
    city = random.choice(region_info[1])
    
    # Signup date
    signup_dt = start_signup + timedelta(days=random.randint(0, signup_span))
    signup_date_str = signup_dt.strftime("%Y-%m-%d")
    
    # Base tier
    tier = random.choices(["Standard", "Silver", "Gold", "VIP"], weights=[0.55, 0.25, 0.15, 0.05])[0]
    
    customers_data.append((cid, fn, ln, email, phone, city, region, signup_date_str, tier))

customers_file = os.path.join(DATA_DIR, "customers.csv")
with open(customers_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "first_name", "last_name", "email", "phone", "city", "region", "signup_date", "customer_segment"])
    writer.writerows(customers_data)

print(f"Generated {len(customers_data)} customers in customers.csv")

# ---------------------------------------------------------
# 4. GENERATE ORDERS & ORDER ITEMS (2024 - 2025)
# ---------------------------------------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
total_days = (end_date - start_date).days + 1

PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Store Financing", "Bank Transfer"]

orders_data = []
order_items_data = []

order_id_counter = 10001
item_id_counter = 50001

# Pre-determine customer order tendencies (some frequent, some churned/one-time)
customer_weights = {}
for c in customers_data:
    cid = c[0]
    signup_dt = datetime.strptime(c[7], "%Y-%m-%d")
    # Higher activity if signup was earlier
    activity_multiplier = random.choices([1, 2, 4, 8, 12], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
    customer_weights[cid] = (signup_dt, activity_multiplier)

for day_offset in range(total_days):
    curr_date = start_date + timedelta(days=day_offset)
    month = curr_date.month
    day_of_week = curr_date.weekday()
    
    # Seasonal weight: Nov/Dec holiday spike (Black Friday / Xmas), summer bump in July
    seasonal_factor = 1.0
    if month in (11, 12):
        seasonal_factor = 1.85
    elif month in (6, 7):
        seasonal_factor = 1.25
    elif month == 1:
        seasonal_factor = 0.85
        
    # Weekend bump
    if day_of_week in (5, 6):
        seasonal_factor *= 1.2
        
    # Orders per day
    num_orders_today = int(random.randint(6, 14) * seasonal_factor)
    
    # Pick active eligible customers
    eligible_cids = [cid for cid, (s_dt, mult) in customer_weights.items() if s_dt <= curr_date]
    if not eligible_cids:
        continue
        
    # Select customers for today's orders
    selected_cids = random.choices(
        eligible_cids, 
        weights=[customer_weights[cid][1] for cid in eligible_cids],
        k=num_orders_today
    )
    
    for cid in selected_cids:
        order_id = order_id_counter
        order_id_counter += 1
        
        # Get customer region to align store matching
        c_info = next(c for c in customers_data if c[0] == cid)
        c_region = c_info[6]
        
        # 60% chance to buy online, 40% in retail store in their region
        if random.random() < 0.60:
            store_id = 101 # Online store
        else:
            regional_stores = [s[0] for s in stores_data if s[3] == c_region and s[1] != "Lumina E-Commerce Store"]
            if regional_stores:
                store_id = random.choice(regional_stores)
            else:
                store_id = 101
                
        # Status: 92% Completed, 5% Returned, 3% Cancelled
        order_status = random.choices(["Completed", "Returned", "Cancelled"], weights=[0.92, 0.05, 0.03])[0]
        payment_method = random.choice(PAYMENT_METHODS)
        shipping_cost = round(random.choice([0.00, 9.99, 14.99, 24.99]), 2) if store_id == 101 else 0.00
        
        orders_data.append((order_id, cid, store_id, curr_date.strftime("%Y-%m-%d"), order_status, payment_method, shipping_cost))
        
        # Generate 1 to 5 line items per order
        num_items = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.07, 0.03])[0]
        chosen_products = random.sample(products_data, num_items)
        
        for p in chosen_products:
            p_id = p[0]
            unit_price = p[5]
            qty = random.choices([1, 2, 3, 4], weights=[0.75, 0.18, 0.05, 0.02])[0]
            
            # Discounts: 0% to 30%, slightly higher discounts in Europe Central / Online channel
            if store_id == 101 or c_region == "Europe Central":
                discount = random.choices([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], weights=[0.35, 0.15, 0.20, 0.15, 0.10, 0.03, 0.02])[0]
            else:
                discount = random.choices([0.00, 0.05, 0.10, 0.15, 0.20], weights=[0.60, 0.20, 0.10, 0.07, 0.03])[0]
                
            order_items_data.append((item_id_counter, order_id, p_id, qty, unit_price, discount))
            item_id_counter += 1

# Write Orders CSV
orders_file = os.path.join(DATA_DIR, "orders.csv")
with open(orders_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_id", "store_id", "order_date", "order_status", "payment_method", "shipping_cost"])
    writer.writerows(orders_data)

print(f"Generated {len(orders_data)} orders in orders.csv")

# Write Order Items CSV
order_items_file = os.path.join(DATA_DIR, "order_items.csv")
with open(order_items_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"])
    writer.writerows(order_items_data)

print(f"Generated {len(order_items_data)} order items in order_items.csv")
print("Synthetic Dataset Generation Complete!")
