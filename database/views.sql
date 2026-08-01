-- ============================================================================
-- LUMINA LIFESTYLE & LIVING - ANALYTICAL VIEWS
-- View: vw_sales_analytics
-- Purpose: Pre-joins all 5 core entity tables and pre-computes line-level
-- revenue, discount, cost, gross profit, net profit, and profit margin metrics.
-- ============================================================================

DROP VIEW IF EXISTS vw_sales_analytics;

CREATE VIEW vw_sales_analytics AS
WITH order_item_counts AS (
    -- Pre-aggregate line item count per order to allocate shipping cost accurately
    SELECT 
        order_id, 
        COUNT(*) AS total_items_in_order
    FROM order_items
    GROUP BY order_id
)
SELECT 
    -- Order Metadata
    o.order_id,
    o.order_date,
    STRFTIME('%Y-%m', o.order_date) AS order_year_month,
    STRFTIME('%Y', o.order_date) AS order_year,
    STRFTIME('%m', o.order_date) AS order_month,
    o.order_status,
    o.payment_method,
    
    -- Customer Attributes
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email AS customer_email,
    c.region AS customer_region,
    c.city AS customer_city,
    c.customer_segment,
    c.signup_date AS customer_signup_date,

    -- Store & Channel Attributes
    s.store_id,
    s.store_name,
    s.channel,
    s.region AS store_region,
    s.city AS store_city,

    -- Product Attributes
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,

    -- Financial Measures (Line-Item Level)
    oi.item_id,
    oi.quantity,
    oi.unit_price,
    p.unit_cost,
    oi.discount_percent,

    -- Computed Revenue & Cost Formulas
    ROUND(oi.quantity * oi.unit_price, 2) AS gross_revenue,
    ROUND(oi.quantity * oi.unit_price * oi.discount_percent, 2) AS discount_amount,
    ROUND((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent), 2) AS net_revenue,
    ROUND(oi.quantity * p.unit_cost, 2) AS total_cogs,
    
    -- Allocated Shipping Cost per Item Line
    ROUND(o.shipping_cost / ic.total_items_in_order, 2) AS allocated_shipping_cost,

    -- Gross Profit = Net Revenue - Total COGS
    ROUND(((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent)) - (oi.quantity * p.unit_cost), 2) AS gross_profit,

    -- Net Profit = Gross Profit - Allocated Shipping Cost
    ROUND((((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent)) - (oi.quantity * p.unit_cost)) - (o.shipping_cost / ic.total_items_in_order), 2) AS net_profit,

    -- Net Profit Margin %
    CASE 
        WHEN ((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent)) > 0 
        THEN ROUND(
            (((((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent)) - (oi.quantity * p.unit_cost)) - (o.shipping_cost / ic.total_items_in_order)) 
            / ((oi.quantity * oi.unit_price) * (1.0 - oi.discount_percent))) * 100.0, 2)
        ELSE 0.00 
    END AS net_profit_margin_pct

FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN stores s ON o.store_id = s.store_id
JOIN products p ON oi.product_id = p.product_id
JOIN order_item_counts ic ON o.order_id = ic.order_id;
