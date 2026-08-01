-- ============================================================================
-- QUERY 05: REGIONAL & CHANNEL MARGIN COMPARISON
-- Business Question:
-- "How do sales volume, gross revenue, net revenue, discount rates, and net profit margins 
--  compare across online vs. retail flagship store channels in each global region? 
--  Identifies region-channel combinations suffering from excessive discount erosion."
-- ============================================================================

SELECT 
    store_region,
    channel,
    COUNT(DISTINCT store_id) AS total_stores,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    
    -- Revenue Breakdown
    ROUND(SUM(gross_revenue), 2) AS gross_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discounts,
    ROUND((SUM(discount_amount) / NULLIF(SUM(gross_revenue), 0)) * 100.0, 2) AS discount_rate_pct,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    
    -- Cost Structure
    ROUND(SUM(total_cogs), 2) AS total_cogs,
    ROUND((SUM(total_cogs) / NULLIF(SUM(net_revenue), 0)) * 100.0, 2) AS cogs_to_net_revenue_pct,
    ROUND(SUM(allocated_shipping_cost), 2) AS total_shipping_cost,
    
    -- Bottom-Line Profitability
    ROUND(SUM(net_profit), 2) AS net_profit,
    ROUND((SUM(net_profit) / NULLIF(SUM(net_revenue), 0)) * 100.0, 2) AS net_profit_margin_pct,
    
    -- Average Metrics per Order
    ROUND(SUM(net_revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_order_value_aov,
    ROUND(SUM(net_profit) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_profit_per_order

FROM vw_sales_analytics
WHERE order_status = 'Completed'
GROUP BY store_region, channel
ORDER BY store_region ASC, net_profit_margin_pct DESC;
