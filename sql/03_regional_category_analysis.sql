-- ============================================================
-- Regional & category performance
-- Used for the regional comparison and category breakdown
-- visuals on the dashboard.
-- ============================================================

-- Revenue, profit, and margin by region
SELECT
    region,
    ROUND(SUM(sales), 2)                     AS total_sales,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(SUM(profit) * 1.0 / SUM(sales), 4) AS profit_margin,
    COUNT(DISTINCT order_id)                 AS total_orders
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- Revenue, profit, and margin by category / sub-category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)                     AS total_sales,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(SUM(profit) * 1.0 / SUM(sales), 4) AS profit_margin,
    SUM(quantity)                            AS units_sold
FROM sales
GROUP BY category, sub_category
ORDER BY total_sales DESC;

-- Region x Category cross-tab (revenue only)
SELECT
    region,
    category,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY region, category
ORDER BY region, total_sales DESC;
