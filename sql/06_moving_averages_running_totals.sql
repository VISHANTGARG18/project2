-- ============================================================================
-- QUERY 06: RUNNING TOTALS & MOVING AVERAGES
-- Business Question:
-- "What is the 7-day and 30-day moving average of daily net revenue to smooth out 
--  short-term weekday volatility, and how does cumulative year-to-date (YTD) net revenue 
--  and profit build over the course of each fiscal year?"
-- ============================================================================

WITH daily_aggregates AS (
    SELECT 
        order_date,
        STRFTIME('%Y', order_date) AS order_year,
        COUNT(DISTINCT order_id) AS daily_orders,
        SUM(quantity) AS daily_units_sold,
        ROUND(SUM(net_revenue), 2) AS daily_net_revenue,
        ROUND(SUM(net_profit), 2) AS daily_net_profit
    FROM vw_sales_analytics
    WHERE order_status = 'Completed'
    GROUP BY order_date
)
SELECT 
    order_date,
    order_year,
    daily_orders,
    daily_units_sold,
    daily_net_revenue,
    daily_net_profit,

    -- 7-Day Moving Average Net Revenue (Smoothes out weekend vs weekday fluctuations)
    ROUND(
        AVG(daily_net_revenue) OVER (
            ORDER BY order_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS mavg_7day_net_revenue,

    -- 30-Day Moving Average Net Revenue (Highlights medium-term seasonal trend line)
    ROUND(
        AVG(daily_net_revenue) OVER (
            ORDER BY order_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ), 2
    ) AS mavg_30day_net_revenue,

    -- Cumulative Year-To-Date (YTD) Net Revenue Running Total
    ROUND(
        SUM(daily_net_revenue) OVER (
            PARTITION BY order_year 
            ORDER BY order_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 2
    ) AS ytd_running_net_revenue,

    -- Cumulative Year-To-Date (YTD) Net Profit Running Total
    ROUND(
        SUM(daily_net_profit) OVER (
            PARTITION BY order_year 
            ORDER BY order_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 2
    ) AS ytd_running_net_profit

FROM daily_aggregates
ORDER BY order_date ASC;
