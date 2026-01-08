-- Query 1: Monthly Sales Drill-Down
-- Business Scenario: The CEO wants to see sales performance broken down by time periods. Start with yearly total, then quarterly, then monthly sales for 2024.
-- Demonstrates: Drill-down from Year to Quarter to Month

SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.total_amount) AS total_sales,
    SUM(f.quantity_sold) AS total_quantity
FROM
    fact_sales f
INNER JOIN
    dim_date d ON f.date_key = d.date_key
WHERE
    d.year = 2024
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.quarter,
    d.month;

-- Query 2: Top 10 Products by Revenue
-- Business Scenario: The product manager needs to identify top-performing products. Show the top 10 products by revenue, along with their category, total units sold, and revenue contribution percentage.
-- Includes: Revenue percentage calculation

WITH product_sales AS (
    SELECT
        p.product_name,
        p.category,
        SUM(f.quantity_sold) AS total_units_sold,
        SUM(f.total_amount) AS total_revenue
    FROM
        fact_sales f
    JOIN
        dim_product p ON f.product_key = p.product_key
    GROUP BY
        p.product_name, p.category
),
total_company_revenue AS (
    SELECT SUM(total_amount) AS grand_total FROM fact_sales
)
SELECT
    ps.product_name,
    ps.category,
    ps.total_units_sold,
    ps.total_revenue,
    ROUND((ps.total_revenue / tcr.grand_total) * 100, 2) AS revenue_contribution_percentage
FROM
    product_sales ps,
    total_company_revenue tcr
ORDER BY
    ps.total_revenue DESC
LIMIT 10;

-- Query 3: Customer Segmentation
-- Business Scenario: Marketing wants to target high-value customers. Segment customers into 'High Value' (>₹50,000 spent), 'Medium Value' (₹20,000-₹50,000), and 'Low Value' (<₹20,000). Show count of customers and total revenue in each segment.
-- Segments: High/Medium/Low value customers

WITH customer_spending AS (
    SELECT
        customer_key,
        SUM(total_amount) AS total_spent
    FROM
        fact_sales
    GROUP BY
        customer_key
),
customer_segments AS (
    SELECT
        customer_key,
        total_spent,
        CASE
            WHEN total_spent > 50000 THEN 'High Value'
            WHEN total_spent BETWEEN 20000 AND 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS segment
    FROM
        customer_spending
)
SELECT
    segment AS customer_segment,
    COUNT(customer_key) AS customer_count,
    SUM(total_spent) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_revenue
FROM
    customer_segments
GROUP BY
    segment
ORDER BY
    total_revenue DESC;
