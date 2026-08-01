-- ============================================================================
-- QUERY 03: COHORT RETENTION & REPEAT PURCHASE ANALYSIS
-- Business Question:
-- "What percentage of customers acquired in a given month return to place repeat purchases 
--  in subsequent months, and what is the cumulative revenue and repeat purchase rate per cohort?"
-- ============================================================================

WITH customer_cohorts AS (
    -- Step 1: Assign each customer to their original signup cohort month
    SELECT 
        customer_id,
        STRFTIME('%Y-%m', signup_date) AS cohort_month
    FROM customers
),
cohort_sizes AS (
    -- Step 2: Calculate the total base size of each signup cohort
    SELECT 
        cohort_month,
        COUNT(customer_id) AS total_cohort_customers
    FROM customer_cohorts
    GROUP BY cohort_month
),
customer_orders AS (
    -- Step 3: Map completed customer orders to order month and compute month index offset
    SELECT 
        o.customer_id,
        c.cohort_month,
        STRFTIME('%Y-%m', o.order_date) AS order_month,
        ROUND((JULIANDAY(STRFTIME('%Y-%m-01', o.order_date)) - JULIANDAY(c.cohort_month || '-01')) / 30.4375) AS month_number,
        o.order_id
    FROM orders o
    JOIN customer_cohorts c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'Completed'
),
cohort_activity AS (
    -- Step 4: Aggregate active unique buyers and total orders per cohort month offset
    SELECT 
        co.cohort_month,
        cs.total_cohort_customers,
        CAST(co.month_number AS INT) AS months_since_signup,
        COUNT(DISTINCT co.customer_id) AS active_buyers,
        COUNT(DISTINCT co.order_id) AS total_orders
    FROM customer_orders co
    JOIN cohort_sizes cs ON co.cohort_month = cs.cohort_month
    WHERE co.month_number >= 0 AND co.month_number <= 12
    GROUP BY co.cohort_month, cs.total_cohort_customers, CAST(co.month_number AS INT)
),
repeat_purchaser_summary AS (
    -- Step 5: Calculate overall repeat customer rate (>1 lifetime order)
    SELECT 
        COUNT(DISTINCT customer_id) AS total_customers,
        COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_id END) AS repeat_customers
    FROM (
        SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
        FROM orders
        WHERE order_status = 'Completed'
        GROUP BY customer_id
    )
)
SELECT 
    ca.cohort_month,
    ca.total_cohort_customers,
    ca.months_since_signup,
    ca.active_buyers,
    ca.total_orders,
    ROUND((ca.active_buyers * 100.0) / ca.total_cohort_customers, 2) AS retention_rate_pct,
    rps.repeat_customers AS global_repeat_customers_count,
    ROUND((rps.repeat_customers * 100.0) / rps.total_customers, 2) AS global_repeat_customer_rate_pct
FROM cohort_activity ca
CROSS JOIN repeat_purchaser_summary rps
ORDER BY ca.cohort_month ASC, ca.months_since_signup ASC;
