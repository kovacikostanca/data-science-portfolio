---------------------------
-- Clean Customers Table --

UPDATE customers
SET full_name = INITCAP(TRIM(full_name));

UPDATE customers
SET email = LOWER(TRIM(email));

UPDATE customers
SET country = CASE
    WHEN LOWER(country) IN ('usa','us','united states') THEN 'USA'
    WHEN LOWER(country) IN ('uk','u.k') THEN 'UK'
    WHEN LOWER(country) IN ('ireland') THEN 'Ireland'
    WHEN LOWER(country) IN ('mexico','mexiko') THEN 'Mexico'
    WHEN LOWER(country) = 'canada' THEN 'Canada'
    ELSE INITCAP(TRIM(country))
END;

-- Remove invalid emails
DELETE FROM customers
WHERE email NOT LIKE '%_@__%.__%';



--------------------------
-- Clean Products Table --
UPDATE products
SET product_name = INITCAP(TRIM(product_name)),
    category = INITCAP(TRIM(category));

UPDATE products
SET price = 1
WHERE price <= 0;

DELETE FROM products a
USING products b
WHERE a.product_id > b.product_id
  AND a.product_name = b.product_name
  AND a.category = b.category;



------------------------
-- Clean Orders Table --
DELETE FROM order_items
WHERE quantity <= 0 OR price <= 0 OR price IS NULL;

DELETE FROM order_items oi
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = oi.order_id);

DELETE FROM order_items oi
WHERE NOT EXISTS (SELECT 1 FROM products p WHERE p.product_id = oi.product_id);




-----------------------------
-- Recalculate Orders Total --
UPDATE orders o
SET total_amount = sub.total
FROM (
    SELECT order_id, SUM(quantity * price) AS total
    FROM order_items
    GROUP BY order_id
) AS sub
WHERE o.order_id = sub.order_id;
