# Lumina Lifestyle & Living - Technical & Behavioral Interview Q&A Guide

This guide prepares you to defend every architectural decision, SQL window function, schema design tradeoff, and business insight in technical and executive interviews.

---

## Technical & Schema Design Questions

### Q1: "Walk me through how you designed the database schema for this project."
> **Answer**:  
> *"I designed a fully normalized 3NF relational schema in SQLite consisting of 5 core entities: `stores`, `products`, `customers`, `orders`, and `order_items`. Primary keys were enforced on all tables, foreign keys were configured with explicit `ON DELETE RESTRICT` constraints to prevent orphaned records, and `CHECK` constraints were added at the DDL level—for example, enforcing `unit_price > unit_cost`, `discount_percent BETWEEN 0 AND 0.50`, and valid status ENUMs. I also added targeted indexes on high-cardinality join and filter columns, such as `orders(order_date)`, `orders(customer_id)`, and `order_items(product_id)`, with 1-line business comments explaining why each index exists."*

### Q2: "Why did you create the `vw_sales_analytics` view instead of writing raw joins in every query?"
> **Answer**:  
> *"In production retail environments, writing 5-table joins across every ad-hoc query leads to code duplication, inconsistent revenue definitions, and human error. `vw_sales_analytics` acts as a single source of truth analytical layer. It pre-joins all 5 entities and pre-computes line-level financial formulas—including Gross Revenue, Discount Amount, Net Revenue, COGS, line-allocated shipping costs, Net Profit, and Net Profit Margin %. This allows downstream reporting scripts, window functions, and Tableau dashboards to query clean, standardized metrics."*

### Q3: "How did you handle shipping costs in line-item profitability calculations?"
> **Answer**:  
> *"Orders table contains a header-level `shipping_cost`. Attributing the full shipping cost to a single line item would distort product profitability. In `vw_sales_analytics`, I used a CTE (`order_item_counts`) to calculate the total number of line items per order (`COUNT(*)`), and allocated the shipping cost proportionally using `ROUND(o.shipping_cost / total_items_in_order, 2)`. This ensures that line-level Net Profit accurately reflects fulfillment overhead."*

### Q4: "Explain how your MoM and YoY revenue growth query works under the hood."
> **Answer**:  
> *"In `01_monthly_trends_mom_yoy.sql`, I first aggregated completed order revenue and profit by `order_year_month`. In the second CTE, I applied SQL window functions: `LAG(net_revenue, 1) OVER (ORDER BY order_year_month)` to fetch the prior month's revenue for MoM growth, and `LAG(net_revenue, 12) OVER (ORDER BY order_year_month)` to fetch the exact same month from the prior year for YoY growth. I wrapped the percentage calculations in `NULLIF()` to prevent division-by-zero errors."*

### Q5: "What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` in your product ranking query?"
> **Answer**:  
> *"In `02_product_performance_rankings.sql`, I partitioned products by `category` and ranked them. `DENSE_RANK()` assigns sequential rank numbers without skipping sequence values if two products tie in revenue. `RANK()` assigns tied items the same rank but skips subsequent numbers (e.g. 1, 2, 2, 4). `ROW_NUMBER()` assigns a unique, strictly incremental integer to every row regardless of ties. Showing all three demonstrates mastery of window function edge-case behavior."*

### Q6: "Walk me through your multi-step CTE chain for RFM customer segmentation."
> **Answer**:  
> *"Rather than building one giant unreadable query, I broke RFM segmentation into 5 explicit CTE steps:
> 1. `rfm_raw`: Computes Recency (days since last order relative to 2025-12-31), Frequency (distinct order count), and Monetary (total net revenue and profit).
> 2. `rfm_quartiles`: Uses `NTILE(4) OVER (...)` to rank customers into 1–4 scores for R, F, and M.
> 3. `rfm_scores`: Concatenates score strings (e.g., `'444'`) and computes total score sum.
> 4. `rfm_segmented`: Applies conditional CASE logic to classify customers into strategic tiers ('Champions', 'Loyal Customers', 'At-Risk (High Value)', 'Lost').
> 5. Final SELECT: Aggregates total customer counts, revenue share, and net profit margins per segment."*

---

## Data Validation & Engineering Questions

### Q7: "How did you ensure the synthetic dataset was clean and realistic?"
> **Answer**:  
> *"I built a Python data generation engine (`generate_synthetic_data.py`) with a fixed seed (`random.seed(42)`). I intentionally injected real-world business dynamics: Q4 holiday spikes (1.85x volume weight), realistic return/cancellation rates (~6-8%), channel-specific discount variances, and customer activity weighting. To prove data health, I wrote `data_validation.sql` which executes automated checks for zero orphaned foreign keys, non-negative unit prices/costs, valid discount ranges, zero duplicate emails, and valid date sequences."*

### Q8: "How would you scale this pipeline if data volume grew from thousands to millions of rows?"
> **Answer**:  
> *"While SQLite is ideal for localized desktop analysis and embedded apps, for multi-million row scale I would migrate the storage engine to PostgreSQL or Snowflake. I would partition the `orders` and `order_items` tables by `order_date` (monthly or yearly partitions), replace the Python CSV script with a PySpark or DuckDB ETL pipeline, and convert `vw_sales_analytics` into a materialized view refreshed incrementally."*

---

## Behavioral & Strategic Project Questions

### Q9: "Walk me through this project from start to finish."
> **Answer (STAR Method)**:  
> - **Situation**: *"Executive leadership at Lumina Lifestyle & Living lacked visibility into why profit margins varied across global regions and online vs. store channels, needing to know which products and customer segments truly drive net profitability rather than just top-line gross sales."*  
> - **Task**: *"As the Data Analyst, I owned the project end-to-end—from generating a realistic 2-year transactional dataset and designing a normalized database schema, to writing advanced SQL analytics queries, building a forecasting model, and crafting executive recommendations."*  
> - **Action**: *"I built an automated ETL ingestion pipeline in Python, authored 6 deep SQL scripts using window functions and 5-stage CTEs, created a pre-computed profitability view (`vw_sales_analytics`), and analyzed margin erosion across channels."*  
> - **Result**: *"I identified that the Online E-Commerce channel suffered a 3.96% margin drag due to uncontrolled 8.62% discount rates and absorbed shipping, and that 28.98% of customers ('Champions') drive 61.3% of net profits. My recommendations provide actionable strategies to reclaim ~$85,000 in annual profit."*

### Q10: "What was the most surprising insight you uncovered in the data?"
> **Answer**:  
> *"I was surprised to discover that North America East Online E-Commerce sales generated the highest gross revenue ($3.10M), yet had the lowest net profit margin (56.53%) among all channel-region pairs. Physical retail stores achieved 60.5%–60.8% net margins. Diving deeper into line-level data revealed that high promotional discount rates (up to 30%) combined with small cart sizes absorbing shipping costs severely eroded online margins."*

### Q11: "How would you defend your recommendation to cap online discounts to a skeptical VP of Marketing?"
> **Answer**:  
> *"I would ground the discussion in data rather than opinion. I'd show that while aggressive discounting drove volume, it produced a 3.96% margin penalty on $2.8M in online revenue—effectively giving away $267,000 in discounts. I'd present a compromise model: capping open discount codes at 15%, but offering higher tiered discounts (20-25%) exclusively to Gold and VIP loyalty members who maintain an Average Order Value above $150. This protects top-line volume while preserving margin."*

### Q12: "If you had 2 more weeks on this project, what stretch features would you build?"
> **Answer**:  
> *"I would extend the Python stretch scripts by building an automated market basket analysis (Apriori algorithm) to identify product co-purchase patterns for checkout cross-selling. I would also write a Streamlit or Dash web app wrapped around the SQLite database so non-technical stakeholders could run custom date range queries dynamically."*
