-- ============================================================================
-- QUERY 01: MONTHLY REVENUE & PROFIT TRENDS WITH MOM & YOY GROWTH
-- Business Question:
-- "Leadership needs to evaluate whether business growth is accelerating or decelerating 
--  on a month-over-month (MoM) and year-over-year (YoY) basis, and whether top-line 
--  net revenue growth translates into bottom-line net profit expansion."
-- ============================================================================

WITH monthly_summary AS (
    SELECT 
        order_year_month,
        order_year,
        order_month,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(gross_revenue), 2) AS gross_revenue,
        ROUND(SUM(discount_amount), 2) AS total_discounts,
        ROUND(SUM(net_revenue), 2) AS net_revenue,
        ROUND(SUM(total_cogs), 2) AS total_cogs,
        ROUND(SUM(net_profit), 2) AS net_profit,
        ROUND((SUM(net_profit) / NULLIF(SUM(net_revenue), 0)) * 100.0, 2) AS net_profit_margin_pct
    FROM vw_sales_analytics
    WHERE order_status = 'Completed'
    GROUP BY order_year_month, order_year, order_month
),
windowed_trends AS (
    SELECT 
        order_year_month,
        total_orders,
        total_units_sold,
        net_revenue,
        net_profit,
        net_profit_margin_pct,
        
        -- Prior Month Net Revenue (MoM)
        LAG(net_revenue, 1) OVER (ORDER BY order_year_month) AS prior_month_net_revenue,
        
        -- Prior Month Net Profit (MoM)
        LAG(net_profit, 1) OVER (ORDER BY order_year_month) AS prior_month_net_profit,

        -- Same Month Prior Year Net Revenue (YoY)
        LAG(net_revenue, 12) OVER (ORDER BY order_year_month) AS prior_year_net_revenue,
        
        -- Same Month Prior Year Net Profit (YoY)
        LAG(net_profit, 12) OVER (ORDER BY order_year_month) AS prior_year_net_profit
    FROM monthly_summary
)
SELECT 
    order_year_month,
    total_orders,
    total_units_sold,
    net_revenue,
    net_profit,
    net_profit_margin_pct,
    
    -- MoM Growth Calculations
    ROUND(((net_revenue - prior_month_net_revenue) / NULLIF(prior_month_net_revenue, 0)) * 100.0, 2) AS mom_net_revenue_growth_pct,
    ROUND(((net_profit - prior_month_net_profit) / NULLIF(prior_month_net_profit, 0)) * 100.0, 2) AS mom_net_profit_growth_pct,

    -- YoY Growth Calculations
    ROUND(((net_revenue - prior_year_net_revenue) / NULLIF(prior_year_net_revenue, 0)) * 100.0, 2) AS yoy_net_revenue_growth_pct,
    ROUND(((net_profit - prior_year_net_profit) / NULLIF(prior_year_net_profit, 0)) * 100.0, 2) AS yoy_net_profit_growth_pct
FROM windowed_trends
ORDER BY order_year_month ASC;
