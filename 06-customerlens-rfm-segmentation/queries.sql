-- =====================================================================
-- CustomerLens: complete SQL script (PostgreSQL)
-- Olist Brazilian E-Commerce dataset. Amounts are in Brazilian reais.
-- Run the sections in order. Each section ends with a check.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Create the tables (load the CSVs afterwards with pgAdmin:
--    right-click table > Import/Export Data > Import, header ON, delimiter ',')
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    customer_id               TEXT PRIMARY KEY,
    customer_unique_id        TEXT,
    customer_zip_code_prefix  TEXT,
    customer_city             TEXT,
    customer_state            TEXT
);

CREATE TABLE orders (
    order_id                       TEXT PRIMARY KEY,
    customer_id                    TEXT,
    order_status                   TEXT,
    order_purchase_timestamp       TIMESTAMP,
    order_approved_at              TIMESTAMP,
    order_delivered_carrier_date   TIMESTAMP,
    order_delivered_customer_date  TIMESTAMP,
    order_estimated_delivery_date  TIMESTAMP
);

CREATE TABLE order_payments (
    order_id              TEXT,
    payment_sequential    INT,
    payment_type          TEXT,
    payment_installments  INT,
    payment_value         NUMERIC(10,2)
);

-- ---------------------------------------------------------------------
-- 2. Check the load. Expected: 99,441 / 99,441 / 103,886
-- ---------------------------------------------------------------------
SELECT 'customers' AS tbl, COUNT(*) FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments;

-- ---------------------------------------------------------------------
-- 3. Payments collapse to one row per order. Both values must be equal
--    (99,440), which proves later joins cannot duplicate orders.
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS rows, COUNT(DISTINCT order_id) AS orders
FROM (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
) t;

-- ---------------------------------------------------------------------
-- 4. Delivered orders joined to the real customer.
--    Expected: 96,477 delivered orders, 93,357 real customers.
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS delivered_orders,
       COUNT(DISTINCT customer_unique_id) AS real_customers
FROM (
    SELECT c.customer_unique_id, o.order_id, v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN (
        SELECT order_id, SUM(payment_value) AS order_value
        FROM order_payments
        GROUP BY order_id
    ) v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
) delivered;

-- ---------------------------------------------------------------------
-- 5. Frequency distribution (explains why F uses custom thresholds)
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date)) AS recency_days,
           COUNT(DISTINCT d.order_id)            AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2) AS monetary
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
)
SELECT frequency,
       COUNT(*) AS customers,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM rfm_raw
GROUP BY frequency
ORDER BY frequency;

-- ---------------------------------------------------------------------
-- 6a. Score check: Recency (about 18,671 customers per score;
--     score 5 must have the smallest number of days)
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date)) AS recency_days,
           COUNT(DISTINCT d.order_id)            AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2) AS monetary
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
),
scored AS (
    SELECT
        r.*,
        NTILE(5) OVER (ORDER BY recency_days DESC, customer_unique_id) AS r_score,
        CASE
            WHEN frequency >= 5 THEN 5
            WHEN frequency  = 4 THEN 4
            WHEN frequency  = 3 THEN 3
            WHEN frequency  = 2 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, customer_unique_id) AS m_score
    FROM rfm_raw r
)
SELECT r_score, COUNT(*) AS customers,
       MIN(recency_days) AS min_days, MAX(recency_days) AS max_days
FROM scored
GROUP BY r_score
ORDER BY r_score;

-- ---------------------------------------------------------------------
-- 6b. Score check: Monetary (score 5 must reach 13,664.08)
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date)) AS recency_days,
           COUNT(DISTINCT d.order_id)            AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2) AS monetary
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
),
scored AS (
    SELECT
        r.*,
        NTILE(5) OVER (ORDER BY recency_days DESC, customer_unique_id) AS r_score,
        CASE
            WHEN frequency >= 5 THEN 5
            WHEN frequency  = 4 THEN 4
            WHEN frequency  = 3 THEN 3
            WHEN frequency  = 2 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, customer_unique_id) AS m_score
    FROM rfm_raw r
)
SELECT m_score, COUNT(*) AS customers,
       MIN(monetary) AS min_value, MAX(monetary) AS max_value
FROM scored
GROUP BY m_score
ORDER BY m_score;

-- ---------------------------------------------------------------------
-- 6c. Score check: Frequency (expected 90,556 / 2,573 / 181 / 28 / 19)
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date)) AS recency_days,
           COUNT(DISTINCT d.order_id)            AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2) AS monetary
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
),
scored AS (
    SELECT
        r.*,
        NTILE(5) OVER (ORDER BY recency_days DESC, customer_unique_id) AS r_score,
        CASE
            WHEN frequency >= 5 THEN 5
            WHEN frequency  = 4 THEN 4
            WHEN frequency  = 3 THEN 3
            WHEN frequency  = 2 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, customer_unique_id) AS m_score
    FROM rfm_raw r
)
SELECT f_score, COUNT(*) AS customers
FROM scored
GROUP BY f_score
ORDER BY f_score;

-- ---------------------------------------------------------------------
-- 7. Segment preview before saving the table
-- ---------------------------------------------------------------------
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date)) AS recency_days,
           COUNT(DISTINCT d.order_id)            AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2) AS monetary
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
),
scored AS (
    SELECT
        r.*,
        NTILE(5) OVER (ORDER BY recency_days DESC, customer_unique_id) AS r_score,
        CASE
            WHEN frequency >= 5 THEN 5
            WHEN frequency  = 4 THEN 4
            WHEN frequency  = 3 THEN 3
            WHEN frequency  = 2 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, customer_unique_id) AS m_score
    FROM rfm_raw r
),
segmented AS (
    SELECT
        s.*,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'Can''t Lose Them'
            WHEN f_score = 1  AND r_score >= 4 THEN 'New Customers'
            WHEN r_score >= 3                  THEN 'Potential Loyalists'
            WHEN f_score = 2                   THEN 'At Risk'
            ELSE                                    'Hibernating'
        END AS segment
    FROM scored s
)
SELECT
    segment,
    COUNT(*)                                            AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)  AS pct_customers,
    ROUND(AVG(recency_days), 1)                         AS avg_recency,
    ROUND(AVG(frequency), 2)                            AS avg_frequency,
    ROUND(AVG(monetary), 2)                             AS avg_monetary,
    ROUND(SUM(monetary), 2)                             AS total_revenue
FROM segmented
GROUP BY segment
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------
-- 8. Final table: customer_rfm_final (one row per real customer)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS customer_rfm_final;

CREATE TABLE customer_rfm_final AS
WITH order_value AS (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
),
delivered AS (
    SELECT c.customer_unique_id, c.customer_city, c.customer_state,
           o.order_id,
           o.order_purchase_timestamp::date AS order_date,
           v.order_value
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN order_value v ON v.order_id = o.order_id
    WHERE o.order_status = 'delivered'
),
snapshot AS (
    SELECT (MAX(order_date) + 1) AS snapshot_date FROM delivered
),
latest_location AS (
    SELECT DISTINCT ON (customer_unique_id)
           customer_unique_id, customer_city, customer_state
    FROM delivered
    ORDER BY customer_unique_id, order_date DESC, order_id
),
rfm_raw AS (
    SELECT d.customer_unique_id,
           (s.snapshot_date - MAX(d.order_date))          AS recency_days,
           COUNT(DISTINCT d.order_id)                     AS frequency,
           ROUND(SUM(d.order_value)::numeric, 2)          AS monetary,
           ROUND((SUM(d.order_value) / COUNT(DISTINCT d.order_id))::numeric, 2)
                                                          AS avg_order_value,
           MAX(d.order_date)                              AS last_order_date
    FROM delivered d
    CROSS JOIN snapshot s
    GROUP BY d.customer_unique_id, s.snapshot_date
),
scored AS (
    SELECT
        r.*,
        NTILE(5) OVER (ORDER BY recency_days DESC, customer_unique_id) AS r_score,
        CASE
            WHEN frequency >= 5 THEN 5
            WHEN frequency  = 4 THEN 4
            WHEN frequency  = 3 THEN 3
            WHEN frequency  = 2 THEN 2
            ELSE 1
        END AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC, customer_unique_id) AS m_score
    FROM rfm_raw r
)
SELECT
    s.customer_unique_id,
    l.customer_city,
    l.customer_state,
    s.recency_days,
    s.frequency,
    s.monetary,
    s.avg_order_value,
    s.last_order_date,
    s.r_score,
    s.f_score,
    s.m_score,
    CASE
        WHEN s.r_score >= 4 AND s.f_score >= 4 THEN 'Champions'
        WHEN s.r_score >= 3 AND s.f_score >= 3 THEN 'Loyal Customers'
        WHEN s.r_score <= 2 AND s.f_score >= 3 THEN 'Can''t Lose Them'
        WHEN s.f_score = 1  AND s.r_score >= 4 THEN 'New Customers'
        WHEN s.r_score >= 3                    THEN 'Potential Loyalists'
        WHEN s.f_score = 2                     THEN 'At Risk'
        ELSE                                        'Hibernating'
    END AS segment
FROM scored s
JOIN latest_location l USING (customer_unique_id);

-- ---------------------------------------------------------------------
-- 9. Validate the final table.
--    Expected: 93,357 / 93,357 / zeros / 9.59 / 13,664.08
-- ---------------------------------------------------------------------
SELECT
    COUNT(*)                                                          AS total_rows,
    COUNT(DISTINCT customer_unique_id)                                AS unique_customers,
    COUNT(*) FILTER (WHERE recency_days IS NULL OR recency_days < 1)  AS bad_recency,
    COUNT(*) FILTER (WHERE frequency < 1)                             AS bad_frequency,
    COUNT(*) FILTER (WHERE monetary IS NULL OR monetary <= 0)         AS bad_monetary,
    COUNT(*) FILTER (WHERE segment IS NULL)                           AS no_segment,
    COUNT(*) FILTER (WHERE customer_state IS NULL)                    AS no_state,
    MIN(monetary)                                                     AS min_value,
    MAX(monetary)                                                     AS max_value
FROM customer_rfm_final;

-- ---------------------------------------------------------------------
-- 10. Segment summary from the final table (matches the dashboard)
-- ---------------------------------------------------------------------
SELECT
    segment,
    COUNT(*)                                            AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)  AS pct_customers,
    ROUND(AVG(recency_days), 1)                         AS avg_recency,
    ROUND(AVG(frequency), 2)                            AS avg_frequency,
    ROUND(AVG(monetary), 2)                             AS avg_monetary,
    ROUND(SUM(monetary), 2)                             AS total_revenue
FROM customer_rfm_final
GROUP BY segment
ORDER BY total_revenue DESC;

-- ---------------------------------------------------------------------
-- 11. Export for Power BI:
--     pgAdmin > right-click customer_rfm_final > Import/Export Data >
--     Export, format CSV, header ON, delimiter ',', encoding UTF8.
-- ---------------------------------------------------------------------
