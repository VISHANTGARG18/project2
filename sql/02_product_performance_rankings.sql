-- ============================================================================
-- QUERY 02: PRODUCT PERFORMANCE RANKINGS WITHIN CATEGORIES
-- Business Question:
-- "Which specific products generate the highest net profit and revenue within each product 
--  category, and which low-margin or heavily-discounted items drag down category margins?
--  Includes multi-window ranking (DENSE_RANK, RANK, ROW_NUMBER) to provide executive visibility."
-- ============================================================================

WITH product_aggregates AS (
    SELECT 
        category,
        product_id,
        product_name,
        unit_cost,
        unit_price,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(gross_revenue), 2) AS gross_revenue,
        ROUND(SUM(discount_amount), 2) AS total_discounts,
        ROUND(AVG(discount_percent) * 100.0, 2) AS avg_discount_pct,
        ROUND(SUM(net_revenue), 2) AS net_revenue,
        ROUND(SUM(total_cogs), 2) AS total_cogs,
        ROUND(SUM(net_profit), 2) AS net_profit,
        ROUND((SUM(net_profit) / NULLIF(SUM(net_revenue), 0)) * 100.0, 2) AS net_profit_margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed'
    GROUP BY category, product_id, product_name, unit_cost, unit_price
)
SELECT 
    category,
    product_name,
    unit_cost,
    unit_price,
    total_units_sold,
    net_revenue,
    net_profit,
    avg_discount_pct,
    net_profit_margin_pct,
    
    -- Dense Rank by Net Revenue within Category (No gaps in ranking sequence)
    DENSE_RANK() OVER (
        PARTITION BY category 
        ORDER BY net_revenue DESC
    ) AS revenue_rank_dense,

    -- Rank by Net Profit within Category (Allows ties with gap ranking)
    RANK() OVER (
        PARTITION BY category 
        ORDER BY net_profit DESC
    ) AS profit_rank,

    -- Row Number for definitive unique ranking order
    ROW_NUMBER() OVER (
        PARTITION BY category 
        ORDER BY net_profit_margin_pct DESC, net_profit DESC
    ) AS margin_rank_row_num

FROM product_aggregates
ORDER BY category ASC, revenue_rank_dense ASC;
