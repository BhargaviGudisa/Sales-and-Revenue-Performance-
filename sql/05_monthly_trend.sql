-- ============================================================
-- Monthly / quarterly sales trend
-- Used for the revenue-over-time line chart on the dashboard.
-- ============================================================

-- Monthly revenue, profit, and order volume trend
SELECT
    order_year_month,
    ROUND(SUM(sales), 2)     AS total_sales,
    ROUND(SUM(profit), 2)    AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales
GROUP BY order_year_month
ORDER BY order_year_month;

-- Quarterly revenue trend
SELECT
    order_year,
    ((order_month - 1) / 3) + 1        AS quarter,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY order_year, quarter
ORDER BY order_year, quarter;

-- Month-over-month revenue growth rate
WITH monthly AS (
    SELECT order_year_month, SUM(sales) AS total_sales
    FROM sales
    GROUP BY order_year_month
)
SELECT
    order_year_month,
    total_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY order_year_month))
        * 1.0 / LAG(total_sales) OVER (ORDER BY order_year_month),
        4
    ) AS mom_growth_rate
FROM monthly
ORDER BY order_year_month;
