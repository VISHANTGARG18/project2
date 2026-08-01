# Lumina Lifestyle & Living - Tableau Executive Dashboard Specification

This document provides exact technical blueprints, Tableau calculated field code, parameter configurations, layout wireframes, and dashboard action filter specifications for building the **Lumina Executive Retail Analytics Dashboard**.

---

## 1. Executive KPI Cards (Top Container)

| KPI Card Title | Display Format | Tableau Calculation Formula | Business Context |
| :--- | :--- | :--- | :--- |
| **Total Net Revenue** | Currency (`$#,##0`) | `SUM([Net Revenue])` | Total recognized net sales after discounts across completed orders. |
| **Total Net Profit** | Currency (`$#,##0`) | `SUM([Net Profit])` | Bottom-line profit after COGS and shipping allocation. |
| **Net Profit Margin %**| Percentage (`0.0%`) | `SUM([Net Profit]) / SUM([Net Revenue])` | Overall business profitability efficiency. |
| **Total Completed Orders**| Number (`#,##0`) | `COUNTD(IF [Order Status] = 'Completed' THEN [Order Id] END)` | Distinct volume of completed order transactions. |
| **Average Order Value (AOV)**| Currency (`$#,##0.00`)| `SUM([Net Revenue]) / COUNTD([Order Id])` | Average net revenue generated per order transaction. |
| **Repeat Customer Rate %**| Percentage (`0.0%`) | `COUNTD(IF [Customer Order Count] > 1 THEN [Customer Id] END) / COUNTD([Customer Id])` | Ratio of customers with more than 1 completed lifetime order. |

---

## 2. Tableau Calculated Fields Reference Code

### Field 1: `[Net Revenue]`
```tableau
ROUND(([Quantity] * [Unit Price]) * (1.0 - [Discount Percent]), 2)
```

### Field 2: `[Net Profit]`
```tableau
ROUND((([Quantity] * [Unit Price]) * (1.0 - [Discount Percent])) - ([Quantity] * [Unit Cost]) - [Allocated Shipping Cost], 2)
```

### Field 3: `[Net Profit Margin %]`
```tableau
IF SUM([Net Revenue]) > 0 THEN 
    SUM([Net Profit]) / SUM([Net Revenue])
ELSE 
    0.0 
END
```

### Field 4: `[Selected Metric Value]` (Dynamic Metric Toggle Parameter)
```tableau
CASE [Parameters].[Metric Selector]
    WHEN 'Net Revenue' THEN SUM([Net Revenue])
    WHEN 'Net Profit' THEN SUM([Net Profit])
    WHEN 'Total Orders' THEN FLOAT(COUNTD([Order Id]))
    WHEN 'AOV' THEN SUM([Net Revenue]) / COUNTD([Order Id])
END
```

### Field 5: `[RFM Segment Name]`
```tableau
IF [R Score] >= 3 AND [F Score] >= 3 AND [M Score] >= 3 THEN "Champions"
ELSEIF [R Score] >= 3 AND [F Score] >= 2 AND [M Score] >= 2 THEN "Loyal Customers"
ELSEIF [R Score] >= 3 AND [F Score] <= 2 THEN "Promising / Recent"
ELSEIF [R Score] <= 2 AND [F Score] >= 3 AND [M Score] >= 3 THEN "At-Risk (High Value)"
ELSEIF [R Score] <= 2 AND [F Score] <= 2 AND [M Score] <= 2 THEN "Lost / Inactive"
ELSE "Needs Attention"
END
```

---

## 3. Interactive Parameter Setup

### Parameter: `[Metric Selector]`
- **Data Type**: String
- **Allowable Values**: List
- **List Items**:
  1. `Net Revenue` (Default)
  2. `Net Profit`
  3. `Total Orders`
  4. `AOV`

---

## 4. Visual Worksheets & Layout Architecture

```
+-----------------------------------------------------------------------------------+
|                            LUMINA EXECUTIVE DASHBOARD                             |
+-----------------------------------------------------------------------------------+
|  [KPI 1: Revenue]  [KPI 2: Profit]  [KPI 3: Margin %]  [KPI 4: Orders]  [KPI 5: AOV]  |
+-----------------------------------------------------------------------------------+
|  [Parameter: Metric Selector V]               [Filter: Global Date Range Slider V] |
+------------------------------------------+----------------------------------------+
| Sheet 1: Monthly Trend Line (MoM / YoY)  | Sheet 2: Global Regional Sales Map     |
| (Line Chart: Order Month vs Selected Metric)| (Symbol Map: Region & Store Profits)   |
+------------------------------------------+----------------------------------------+
| Sheet 3: Top 10 Product Profit Rank      | Sheet 4: RFM Customer Segment Breakdown|
| (Horizontal Bar Chart: Net Profit)       | (Donut / Treemap: Customer Count & LTV)|
+------------------------------------------+----------------------------------------+
| Sheet 5: Channel Margin Erosion Bar      | Sheet 6: Cohort Retention Heatmap      |
| (Stacked Bar: E-Commerce vs Retail Store)| (Matrix: Signup Month vs Month Offset)  |
+------------------------------------------+----------------------------------------+
```

---

## 5. Dashboard Interactivity & Action Filters

1. **Action Filter 1: `[Map Click -> Filter All Charts]`**
   - **Source Sheet**: Sheet 2 (Global Regional Sales Map)
   - **Target Sheets**: All sheets on dashboard
   - **Trigger**: Select (Clicking North America East or Europe Central filters trends, top products, and RFM segments).

2. **Action Filter 2: `[Product Category Hover -> Highlight Channel]`**
   - **Source Sheet**: Sheet 3 (Top 10 Product Profit Rank)
   - **Target Sheets**: Sheet 5 (Channel Margin Erosion Bar)
   - **Trigger**: Hover

3. **Action Filter 3: `[RFM Segment Click -> Drilldown Cohort Heatmap]`**
   - **Source Sheet**: Sheet 4 (RFM Customer Segment Breakdown)
   - **Target Sheets**: Sheet 6 (Cohort Retention Heatmap)
   - **Trigger**: Select

---

## 6. Publishing to Tableau Public & Embedding

1. Extract data connection in Tableau Desktop (`lumina_retail.hyper` or live SQLite connection).
2. Publish to Tableau Public profile under title: `Lumina Retail Analytics Flagship Dashboard`.
3. Obtain embed URL and iframe snippet.
4. Add live link and preview thumbnail to `README.md`.
