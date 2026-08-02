-- ============================================================================
-- LUMINA LIFESTYLE & LIVING - DATABASE SCHEMA DESIGN (DDL)
-- Target RDBMS: SQLite (Generalized ANSI SQL standard compatible with Postgres/MySQL)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. STORES TABLE
-- Stores physical and online retail locations across global operational regions, states, and countries.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('Online', 'Retail Store')),
    region VARCHAR(50) NOT NULL CHECK (region IN ('North America East', 'North America West', 'Europe Central', 'Asia Pacific')),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    manager_name VARCHAR(100) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. PRODUCTS TABLE
-- Catalog of retail items, cost structures, and price points.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL CHECK (unit_cost >= 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    CONSTRAINT chk_price_above_cost CHECK (unit_price >= unit_cost)
);

-- ----------------------------------------------------------------------------
-- 3. CUSTOMERS TABLE
-- Demographics, global geography, signup date, and tier segmentation.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(30),
    city VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL CHECK (region IN ('North America East', 'North America West', 'Europe Central', 'Asia Pacific')),
    signup_date DATE NOT NULL,
    customer_segment VARCHAR(20) NOT NULL CHECK (customer_segment IN ('Standard', 'Silver', 'Gold', 'VIP'))
);

-- ----------------------------------------------------------------------------
-- 4. ORDERS TABLE
-- Header record for sales transactions, shipping fees, and fulfillment status.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    order_status VARCHAR(20) NOT NULL CHECK (order_status IN ('Completed', 'Returned', 'Cancelled')),
    payment_method VARCHAR(30) NOT NULL CHECK (payment_method IN ('Credit Card', 'PayPal', 'Apple Pay', 'Store Financing', 'Bank Transfer')),
    shipping_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (shipping_cost >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 5. ORDER_ITEMS TABLE
-- Transaction line-item detail recording quantities, price snapshot, and discounts.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    discount_percent DECIMAL(4, 2) NOT NULL DEFAULT 0.00 CHECK (discount_percent BETWEEN 0.00 AND 0.50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);

-- ============================================================================
-- PERFORMANCE INDEXES (WITH BUSINESS JUSTIFICATIONS)
-- ============================================================================

-- Index 1: Optimizes time-series aggregation, MoM/YoY growth trends, and date filtering
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);

-- Index 2: Accelerates customer lifetime value (LTV), cohort analysis, and RFM segment CTE joins
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);

-- Index 3: Speeds up regional and online vs. brick-and-mortar channel margin comparisons
CREATE INDEX IF NOT EXISTS idx_orders_store_id ON orders(store_id);

-- Index 4: Accelerates product performance ranking and category profitability aggregation
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

-- Index 5: Fast foreign key lookups when joining order headers to line items in large report queries
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- Index 6: Optimizes regional customer filtering and signup cohort queries
CREATE INDEX IF NOT EXISTS idx_customers_region_signup ON customers(region, signup_date);
