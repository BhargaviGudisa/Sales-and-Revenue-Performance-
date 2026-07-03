-- ============================================================
-- KPI Summary: headline business metrics
-- Used to populate the top KPI cards on the dashboard.
-- ============================================================

SELECT
    ROUND(SUM(sales), 2)                              AS total_sales,
    ROUND(SUM(profit), 2)                             AS total_profit,
    ROUND(SUM(profit) * 1.0 / SUM(sales), 4)          AS overall_profit_margin,
    COUNT(DISTINCT order_id)                          AS total_orders,
    ROUND(SUM(sales) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value,
    COUNT(DISTINCT customer_id)                       AS total_customers,
    SUM(quantity)                                     AS total_units_sold
FROM sales;
