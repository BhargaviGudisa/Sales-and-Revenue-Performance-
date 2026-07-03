-- ============================================================
-- Top products & customers
-- Used for the "Top 10 Products" and customer-value visuals.
-- ============================================================

-- Top 10 products by revenue
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)  AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity)          AS units_sold
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 10;

-- Products with high sales but low (or negative) profit margin
-- -> candidates for discount policy review
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)                     AS total_sales,
    ROUND(SUM(profit), 2)                    AS total_profit,
    ROUND(SUM(profit) * 1.0 / SUM(sales), 4) AS profit_margin
FROM sales
GROUP BY product_name, category, sub_category
HAVING total_sales > (SELECT AVG(sales) * 20 FROM sales)  -- above-average-volume products
   AND profit_margin < 0.05
ORDER BY total_sales DESC;

-- Top 10 customers by lifetime revenue
SELECT
    customer_id,
    customer_name,
    segment,
    ROUND(SUM(sales), 2)     AS lifetime_sales,
    ROUND(SUM(profit), 2)    AS lifetime_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales
GROUP BY customer_id, customer_name, segment
ORDER BY lifetime_sales DESC
LIMIT 10;
