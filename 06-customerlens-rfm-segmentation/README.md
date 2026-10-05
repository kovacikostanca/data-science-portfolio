# Customer Segmentation & Retention Analytics (RFM on Olist Marketplace)

> An end-to-end customer segmentation project: a validated **PostgreSQL** RFM engine (Recency, Frequency, Monetary) feeding a 3-page **Power BI** dashboard that turns 93,357 marketplace customers into 7 actionable segments.

**Author:** Kostanca · Data Scientist · [Portfolio](https://kostancakovaci.com)

**Stack:** PostgreSQL · pgAdmin · SQL (CTEs, window functions, `NTILE`, `DISTINCT ON`) · Power BI · Power Query (M) · DAX

**Dataset:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle). All amounts are in Brazilian reais (R$).


**Repository contents**

| File | What it is |
|---|---|
| `README.md` | This document: method, all queries, Power Query and DAX code |
| `case_study.md` | The portfolio case study (story, decisions, impact) |
| `insights.md` | The business insights and recommended actions |
| `queries.sql` | The complete runnable SQL script |
| `images/` | Dashboard screenshots |

---

## 1. Business problem

A marketplace usually treats every customer the same. A marketing team needs to know who its best customers are, who is about to leave, and where the next campaign budget should go.

RFM answers this with three behavioural signals per customer:

| Signal | Question | Measured as |
|---|---|---|
| **R**ecency | How recently did they buy? | Days since last delivered order (lower is better) |
| **F**requency | How often do they buy? | Number of distinct delivered orders |
| **M**onetary | How much do they spend? | Total payment value of delivered orders |

---

## 2. Headline results

| Metric | Value |
|---|---|
| Customers analysed (delivered orders only) | **93,357** |
| Delivered orders | 96,477 |
| Total revenue | **R$ 15.42M** |
| Average revenue per customer | R$ 165.20 |
| Average recency | 238.5 days |
| Customers with only one order | **97.0%** |
| Repeat customers (2+ orders) | **3.0%** |
| Revenue from the three one-time-buyer segments | ≈ 97.5% |

**The main finding:** Olist behaves as a one-time-purchase marketplace. Nearly all customers and revenue sit in three segments that differ mainly by *when* the single purchase happened. The largest opportunity is converting first-time buyers into repeat buyers.

---

## 3. Data

Only three of the nine Olist tables are needed:

| Table | Rows | Used for |
|---|---|---|
| `olist_customers_dataset` | 99,441 | Real customer ID (`customer_unique_id`), city, state |
| `olist_orders_dataset` | 99,441 | Order status and purchase date |
| `olist_order_payments_dataset` | 103,886 | Payment value (Monetary) |

---

## 4. Method and design decisions

| # | Decision | Why |
|---|---|---|
| 1 | Group by `customer_unique_id`, not `customer_id` | `customer_id` is generated per order, so grouping by it makes repeat purchases impossible. |
| 2 | Delivered orders only | Canceled or unavailable orders are not realised revenue and add noise. |
| 3 | Collapse payments to one row per order first | An order paid with several methods has several payment rows. Joining them directly would duplicate orders and inflate Frequency. |
| 4 | Snapshot date = last order date + 1 day | The data is historical (2016-2018). Today's date would make every recency about 2,000 days. |
| 5 | R and M scored with `NTILE(5)` | Quintiles put days and currency on one comparable 1-5 scale (5 = best). |
| 6 | F scored with custom thresholds | 97% of customers have one order, so quintiles would split identical customers arbitrarily. |
| 7 | Deterministic tie-breaker in `NTILE` | Many customers share the same recency, so without it scores could change between runs. |
| 8 | One city and state per customer (latest order) | Customers can move, and filters need exactly one value per person. |

### Segment rules (evaluated top to bottom, first match wins)

| Segment | Rule | Meaning | Recommended action |
|---|---|---|---|
| Champions | R ≥ 4 and F ≥ 4 | Recent and frequent | VIP rewards and loyalty offers |
| Loyal Customers | R ≥ 3 and F ≥ 3 | Strong repeat customers | Cross-sell and personalised offers |
| Can't Lose Them | R ≤ 2 and F ≥ 3 | Valuable but declining | Priority retention campaign |
| New Customers | F = 1 and R ≥ 4 | Recent first-time buyers | Welcome journey and second-purchase offer |
| Potential Loyalists | R ≥ 3 (remaining) | Showing potential | Encourage repeat purchase |
| At Risk | F = 2 (remaining) | Previously engaged, becoming inactive | Win-back campaign |
| Hibernating | Everything else | Low engagement over a long period | Low-cost reactivation campaign |

---

## 5. SQL pipeline

The complete script is in `queries.sql`. Each step below was run and checked before moving on.

### 5.1 Create the tables

```sql
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
```

Load each CSV with pgAdmin (right-click the table, Import/Export Data, header ON, delimiter `,`). IDs are `TEXT` because they are hash strings, timestamps are `TIMESTAMP` for date arithmetic, and money is `NUMERIC(10,2)` to avoid floating-point rounding.

### 5.2 Check the load

```sql
SELECT 'customers' AS tbl, COUNT(*) FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments;
```

Expected: 99,441 / 99,441 / 103,886. Payments have more rows than orders because one order can be split across several payment methods.

### 5.3 Prove payments collapse to one row per order

```sql
SELECT COUNT(*) AS rows, COUNT(DISTINCT order_id) AS orders
FROM (
    SELECT order_id, SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id
) t;
```

Both values are 99,440 (one order has no payment row), so later joins cannot duplicate orders.

### 5.4 Delivered orders joined to the real customer

```sql
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
```

Result: **96,477 delivered orders from 93,357 real customers**. The 3,120 extra orders are repeat purchases.

### 5.5 Frequency distribution (why F needs custom thresholds)

```sql
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
```

| Orders | Customers | Share |
|---|---|---|
| 1 | 90,556 | 97.00% |
| 2 | 2,573 | 2.76% |
| 3 | 181 | 0.19% |
| 4 | 28 | 0.03% |
| 5 or more | 19 | 0.02% |

### 5.6 Score checks (R, F, M)

The query below checks the Recency score. To check the others, change only the final `SELECT`: for M use `m_score` with `MIN(monetary)` and `MAX(monetary)`, and for F use `f_score` with `COUNT(*)`.

```sql
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
```

Recency is sorted `DESC` so the oldest customers get 1 and the most recent get 5. Monetary is sorted `ASC` so the biggest spenders get 5. Each group holds about 18,671 customers, and Frequency scores split as 90,556 / 2,573 / 181 / 28 / 19.

### 5.7 Final table: `customer_rfm_final`

```sql
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
```

### 5.8 Validate the final table

```sql
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
```

Result: **93,357 rows, 93,357 unique customers, 0 invalid values, monetary range 9.59 to 13,664.08.**

### 5.9 Segment summary (the dashboard's reference table)

```sql
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
```

| Segment | Customers | % | Avg recency (days) | Avg orders | Avg spend (R$) | Revenue (R$) |
|---|---|---|---|---|---|---|
| New Customers | 36,141 | 38.7 | 91.0 | 1.00 | 164.29 | 5.94M |
| Hibernating | 36,352 | 38.9 | 395.4 | 1.00 | 161.85 | 5.88M |
| Potential Loyalists | 19,714 | 21.1 | 213.2 | 1.08 | 163.47 | 3.22M |
| At Risk | 922 | 1.0 | 381.7 | 2.00 | 285.25 | 0.26M |
| Loyal Customers | 126 | 0.1 | 128.1 | 3.14 | 459.68 | 0.06M |
| Can't Lose Them | 70 | 0.1 | 391.8 | 3.14 | 423.90 | 0.03M |
| Champions | 32 | 0.0 | 83.6 | 4.97 | 873.64 | 0.03M |

---

## 6. Power BI layer

### 6.1 Loading the data

`customer_rfm_final` is exported from pgAdmin (Import/Export Data, Export, CSV, header ON, UTF8) and loaded in Power BI, because a direct PostgreSQL connection was not available. The Power Query code below also creates the helper columns used by the Recency and Frequency distribution charts.

```
let
    Source = Csv.Document(File.Contents("C:\Users\kwnst\Downloads\oilist_dataset\oilist_customer_rfm_final.csv"),[Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_unique_id", type text}, {"customer_city", type text}, {"customer_state", type text}, {"recency_days", Int64.Type}, {"frequency", Int64.Type}, {"monetary", type number}, {"avg_order_value", type number}, {"last_order_date", type date}, {"r_score", Int64.Type}, {"f_score", Int64.Type}, {"m_score", Int64.Type}, {"segment", type text}}, "en-US"),
    #"Added Conditional Column" = Table.AddColumn(#"Changed Type", "Bucket Order", each if [recency_days] <= 30 then 1 else if [recency_days] <= 60 then 2 else if [recency_days] <= 90 then 3 else if [recency_days] <= 180 then 4 else if [recency_days] <= 365 then 5 else 6),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Conditional Column",{{"Bucket Order", Int64.Type}}),
    #"Added Conditional Column2" = Table.AddColumn(#"Changed Type1", "Frequency Bucket", each if [frequency] = 1 then 1 else if [frequency] = 2 then 2 else if [frequency] = 3 then 3 else if [frequency] = 4 then 4 else if [frequency] = 5 then 5 else if [frequency] <= 10 then "6 to 10" else if [frequency] <= 20 then "11 to 20" else 21),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Conditional Column2",{{"Frequency Bucket", type text}}),
    #"Added Conditional Column3" = Table.AddColumn(#"Changed Type3", "Frequency Order", each if [frequency] = 1 then 1 else if [frequency] = 2 then 2 else if [frequency] = 3 then 3 else if [frequency] = 4 then 4 else if [frequency] = 5 then 5 else if [frequency] <= 10 then 6 else if [frequency] <= 20 then 7 else 8),
    #"Changed Type4" = Table.TransformColumnTypes(#"Added Conditional Column3",{{"Frequency Order", Int64.Type}})
in
    #"Changed Type4"
```

Lessons from loading: `Columns=12` must match the file (an old `Columns=8` hid the score columns and caused a "column not found" error), `Encoding=65001` keeps accented city names intact, and the `"en-US"` culture stops decimal points from being misread on systems with different regional settings.

### 6.2 Dashboard pages

1. **Executive Overview:** KPI cards (customers, revenue, average customer value, average recency, repeat-customer rate), segment distribution, average spend by segment, revenue contribution by segment, a Key Insights box, and frequency and recency distributions.
2. **RFM Segmentation:** average recency, frequency and monetary cards, an RFM scatter plot, the segment summary table, and the R, F and M score distributions.
3. **Customer Explorer and Action Center:** filters (segment, R, F, M scores), a customer detail table, a selected-customer card, and an action table with the business meaning and recommended action for each segment.

*[Add screenshots: `images/executive-overview.png`, `images/rfm-segmentation.png`, `images/customer-explorer.png`]*

### 6.3 DAX measures for the Key Insights box

These update automatically with the data.

```
Insight 1 =
VAR total = COUNTROWS('oilist_customer_rfm_final')
VAR oneTime = CALCULATE(COUNTROWS('oilist_customer_rfm_final'), 'oilist_customer_rfm_final'[frequency] = 1)
RETURN FORMAT(DIVIDE(oneTime, total), "0.0%") & " of customers have placed only one order."
```

```
Insight 2 =
VAR total = COUNTROWS('oilist_customer_rfm_final')
VAR inactive = CALCULATE(COUNTROWS('oilist_customer_rfm_final'), 'oilist_customer_rfm_final'[recency_days] > 180)
RETURN FORMAT(DIVIDE(inactive, total), "0%") & " of customers have not bought in over 180 days."
```

```
Insight 3 =
VAR repeatAvg = CALCULATE(AVERAGE('oilist_customer_rfm_final'[monetary]), 'oilist_customer_rfm_final'[frequency] >= 2)
VAR oneAvg = CALCULATE(AVERAGE('oilist_customer_rfm_final'[monetary]), 'oilist_customer_rfm_final'[frequency] = 1)
RETURN "Repeat buyers spend " & FORMAT(DIVIDE(repeatAvg, oneAvg), "0.0") & "x more per customer (" & FORMAT(repeatAvg, "#,0") & " vs " & FORMAT(oneAvg, "#,0") & ")."
```

```
Insight 4 =
VAR rev = SUM('oilist_customer_rfm_final'[monetary])
VAR oneTimeSegs = CALCULATE(SUM('oilist_customer_rfm_final'[monetary]), 'oilist_customer_rfm_final'[segment] IN {"New Customers", "Hibernating", "Potential Loyalists"})
RETURN FORMAT(DIVIDE(oneTimeSegs, rev), "0.0%") & " of revenue comes from New, Hibernating and Potential Loyalists."
```

### 6.4 DAX measures for the selected-customer card

They show one customer after a row is clicked in the detail table, and a prompt before that.

```
Selected Customer = SELECTEDVALUE('oilist_customer_rfm_final'[customer_unique_id], "Select a customer in the table")
```

```
Selected Orders = IF(HASONEVALUE('oilist_customer_rfm_final'[customer_unique_id]), SUM('oilist_customer_rfm_final'[frequency]), BLANK())
```

```
Selected Spent = IF(HASONEVALUE('oilist_customer_rfm_final'[customer_unique_id]), SUM('oilist_customer_rfm_final'[monetary]), BLANK())
```

```
Selected Days Since Purchase = IF(HASONEVALUE('oilist_customer_rfm_final'[customer_unique_id]), SUM('oilist_customer_rfm_final'[recency_days]), BLANK())
```

### 6.5 Updating the data

Re-export the table from pgAdmin with the same file name into the same folder, then click **Refresh** in Power BI. To point to a different file, go to Transform data, click the gear next to **Source**, and browse to it.

---

## 7. Limitations

- **Thresholds are a business choice.** The Champions rule (R ≥ 4 and F ≥ 4) yields only 32 customers because repeat buying is so rare. A client may prefer F ≥ 3.
- **Snapshot date.** Recency is relative to the last order in the dataset (2018), not today's date.
- **No time trend.** The table is one snapshot per customer, so it cannot show revenue over time.
- **Monetary is payment value, not profit.** Payment value includes freight and is not margin.
- **Single-marketplace view.** Customers who bought elsewhere are not visible.

## 8. Next steps

- Add a customer state and city filter to the Customer Explorer.
- Add a cohort retention view to show how quickly first-time buyers drop off.
- Test K-means clustering against the rule-based segments.
- Add a "Data as of" card based on `MAX(last_order_date)`.

## 9. Reproduce

1. Download the Olist dataset and keep the three CSVs listed in section 3.
2. Create a PostgreSQL database and run `queries.sql` (or sections 5.1 to 5.8 in order).
3. Export `customer_rfm_final` to CSV.
4. Load it in Power BI with the Power Query code in 6.1, then add the measures in 6.3 and 6.4.

## 10. Contact

**Kostanca** · MSc Data Science (Distinction), BSc Physics · [GrowInData](https://growindata.com)
[LinkedIn / email: add yours here]
