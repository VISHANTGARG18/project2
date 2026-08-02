# Lumina Lifestyle & Living - Comprehensive Data Dictionary

This document details the data architecture, table schemas, field definitions, data types, constraints, and sample values for the **Lumina Lifestyle & Living** database (`lumina_retail.db`).

---

## 1. Table: `stores`
Stores operational records for physical retail flagships and e-commerce digital channels across global operational regions, states/provinces, and countries.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `store_id` | `INTEGER` | `PRIMARY KEY` | Unique surrogate key for each store location. | `101` |
| `store_name` | `VARCHAR(100)`| `NOT NULL` | Operational name of the store or website. | `Lumina New York Flagship` |
| `channel` | `VARCHAR(20)` | `NOT NULL, CHECK ('Online', 'Retail Store')` | Sales fulfillment channel type. | `Retail Store` |
| `region` | `VARCHAR(50)` | `NOT NULL, CHECK ('North America East', 'North America West', 'Europe Central', 'Asia Pacific')` | Global operational territory. | `North America East` |
| `city` | `VARCHAR(50)` | `NOT NULL` | City where physical store or regional hub is based. | `New York` |
| `state` | `VARCHAR(50)` | `NOT NULL` | State or province where store operates. | `New York` |
| `country` | `VARCHAR(50)` | `NOT NULL` | Country where physical store or regional hub operates. | `United States` |
| `manager_name` | `VARCHAR(100)`| `NOT NULL` | General Manager responsible for store performance. | `Marcus Vance` |

---

## 2. Table: `products`
Catalog of merchandise, category hierarchies, production costs, and retail prices.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | `INTEGER` | `PRIMARY KEY` | Unique product identifier. | `1001` |
| `product_name` | `VARCHAR(150)`| `NOT NULL` | Full commercial product title. | `Lumina Ergonomic Executive Chair` |
| `category` | `VARCHAR(50)` | `NOT NULL` | Top-level product category grouping. | `Premium Home Goods` |
| `subcategory` | `VARCHAR(50)` | `NOT NULL` | Secondary product grouping. | `Furniture` |
| `unit_cost` | `DECIMAL(10,2)`| `NOT NULL, CHECK (>= 0)` | Wholesale unit cost incurred by retailer (COGS baseline). | `180.00` |
| `unit_price` | `DECIMAL(10,2)`| `NOT NULL, CHECK (> 0, >= unit_cost)` | Standard retail price before line-level discounts. | `450.00` |
| `is_active` | `INTEGER` | `NOT NULL, DEFAULT 1, CHECK (0, 1)` | Active product status flag (1 = Active, 0 = Discontinued). | `1` |

---

## 3. Table: `customers`
Customer demographic profiles, global geography, signup dates, and tier segments.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `INTEGER` | `PRIMARY KEY` | Unique customer account identifier. | `5001` |
| `first_name` | `VARCHAR(50)` | `NOT NULL` | Customer's first name. | `Alexander` |
| `last_name` | `VARCHAR(50)` | `NOT NULL` | Customer's family name. | `Smith` |
| `email` | `VARCHAR(100)`| `NOT NULL, UNIQUE` | Customer's verified primary email address. | `alexander.smith5001@example-lumina.com` |
| `phone` | `VARCHAR(30)` | `NULLABLE` | Primary contact phone number. | `+1-415-555-0192` |
| `city` | `VARCHAR(50)` | `NOT NULL` | City of customer primary address. | `San Francisco` |
| `region` | `VARCHAR(50)` | `NOT NULL, CHECK (Valid Regions)` | Regional geographic territory. | `North America West` |
| `signup_date` | `DATE` | `NOT NULL` | Account registration date (`YYYY-MM-DD`). | `2023-11-14` |
| `customer_segment`| `VARCHAR(20)` | `NOT NULL, CHECK ('Standard', 'Silver', 'Gold', 'VIP')` | Baseline customer loyalty tier. | `Gold` |

---

## 4. Table: `orders`
Header transaction records detailing customer orders, store channels, order dates, and shipping fees.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `INTEGER` | `PRIMARY KEY` | Unique order transaction identifier. | `10001` |
| `customer_id` | `INTEGER` | `NOT NULL, FK -> customers(customer_id)` | Account ID of customer placing order. | `5001` |
| `store_id` | `INTEGER` | `NOT NULL, FK -> stores(store_id)` | Fulfillment store or online portal ID. | `101` |
| `order_date` | `DATE` | `NOT NULL` | Date order was placed (`YYYY-MM-DD`). | `2024-01-15` |
| `order_status` | `VARCHAR(20)` | `NOT NULL, CHECK ('Completed', 'Returned', 'Cancelled')` | Final order fulfillment status. | `Completed` |
| `payment_method` | `VARCHAR(30)` | `NOT NULL, CHECK (Valid Methods)` | Payment processing channel. | `Credit Card` |
| `shipping_cost` | `DECIMAL(10,2)`| `NOT NULL, DEFAULT 0.00, CHECK (>= 0)` | Outbound shipping fee charged to customer/absorbed. | `9.99` |

---

## 5. Table: `order_items`
Granular line-item breakdown specifying items purchased, quantities, unit prices, and applied discounts.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `item_id` | `INTEGER` | `PRIMARY KEY` | Unique transaction line item ID. | `50001` |
| `order_id` | `INTEGER` | `NOT NULL, FK -> orders(order_id)` | Parent order header reference ID. | `10001` |
| `product_id` | `INTEGER` | `NOT NULL, FK -> products(product_id)`| Catalog product ID purchased. | `1001` |
| `quantity` | `INTEGER` | `NOT NULL, CHECK (> 0)` | Units of product ordered. | `2` |
| `unit_price` | `DECIMAL(10,2)`| `NOT NULL, CHECK (> 0)` | Transaction unit price snapshot at order time. | `450.00` |
| `discount_percent`| `DECIMAL(4,2)` | `NOT NULL, DEFAULT 0.00, CHECK (0.00 to 0.50)` | Promotional discount rate applied (e.g. 0.15 = 15%). | `0.10` |

---

## 6. Analytical View: `vw_sales_analytics`
Pre-calculated analytical reporting layer joining all 5 relational tables.

| Computed Field Name | Calculation Formula / SQL Definition | Business Meaning |
| :--- | :--- | :--- |
| `gross_revenue` | `ROUND(quantity * unit_price, 2)` | Revenue prior to promotional discounts. |
| `discount_amount` | `ROUND(quantity * unit_price * discount_percent, 2)` | Dollar magnitude of promotional discount. |
| `net_revenue` | `ROUND(gross_revenue - discount_amount, 2)` | Top-line net sales recognized by business. |
| `total_cogs` | `ROUND(quantity * unit_cost, 2)` | Direct cost of goods sold. |
| `allocated_shipping_cost` | `ROUND(shipping_cost / total_items_in_order, 2)` | Line-allocated shipping overhead. |
| `gross_profit` | `ROUND(net_revenue - total_cogs, 2)` | Direct margin before fulfillment fees. |
| `net_profit` | `ROUND(gross_profit - allocated_shipping_cost, 2)` | True bottom-line profit generated by line item. |
| `net_profit_margin_pct` | `ROUND((net_profit / net_revenue) * 100.0, 2)` | Percentage profit efficiency per dollar earned. |
