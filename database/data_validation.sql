-- ============================================================================
-- LUMINA LIFESTYLE & LIVING - DATA INTEGRITY & VALIDATION SUITE
-- Executes automated assertion queries to prove data clean property & trustworthiness.
-- Returns 0 rows for all anomaly checks when data is valid.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Check 1: Orphaned Foreign Keys in Orders (Missing Customer or Store)
-- Expected Result: 0 rows
-- ----------------------------------------------------------------------------
SELECT 
    'Orphaned Orders' AS check_name,
    COUNT(*) AS anomaly_count
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN stores s ON o.store_id = s.store_id
WHERE c.customer_id IS NULL OR s.store_id IS NULL;

-- ----------------------------------------------------------------------------
-- Check 2: Orphaned Foreign Keys in Order Items (Missing Order or Product)
-- Expected Result: 0 rows
-- ----------------------------------------------------------------------------
SELECT 
    'Orphaned Order Items' AS check_name,
    COUNT(*) AS anomaly_count
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.order_id IS NULL OR p.product_id IS NULL;

-- ----------------------------------------------------------------------------
-- Check 3: Invalid Price, Cost, Quantity, or Shipping Values
-- Expected Result: 0 rows
-- ----------------------------------------------------------------------------
SELECT 
    'Invalid Monetary/Quantity Values' AS check_name,
    COUNT(*) AS anomaly_count
FROM (
    SELECT item_id FROM order_items WHERE unit_price <= 0 OR quantity <= 0 OR discount_percent < 0 OR discount_percent > 0.50
    UNION ALL
    SELECT product_id FROM products WHERE unit_cost < 0 OR unit_price <= 0 OR unit_cost > unit_price
    UNION ALL
    SELECT order_id FROM orders WHERE shipping_cost < 0
);

-- ----------------------------------------------------------------------------
-- Check 4: Duplicate Customer Email Addresses
-- Expected Result: 0 rows
-- ----------------------------------------------------------------------------
SELECT 
    'Duplicate Customer Emails' AS check_name,
    COUNT(*) - COUNT(DISTINCT email) AS anomaly_count
FROM customers;

-- ----------------------------------------------------------------------------
-- Check 5: Date Sequence Anomaly (Order Date before Customer Signup Date)
-- Expected Result: 0 rows
-- ----------------------------------------------------------------------------
SELECT 
    'Order Date Prior to Signup Date' AS check_name,
    COUNT(*) AS anomaly_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date < c.signup_date;

-- ----------------------------------------------------------------------------
-- Summary: Record Counts across All 5 Tables
-- ----------------------------------------------------------------------------
SELECT 'stores' AS table_name, COUNT(*) AS total_records FROM stores
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;
