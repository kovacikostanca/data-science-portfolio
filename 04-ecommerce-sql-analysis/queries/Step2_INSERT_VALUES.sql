-- Insert Values to Tables --

-- Customer Table --
INSERT INTO customers (full_name, email, country, signup_date) VALUES
('John Smith', 'john.smith@gmail.com', 'USA', '2022-01-03'),
('Sarah Connor', 'sarahc@gmail.com', 'UK', '2022-02-11'),
('Alice Johnson', 'alice.j@example.com', 'USA', '2022-01-05'),
('Bob Smith', 'bob.s@example.com', 'Canada', '2022-02-12'),
('Charlie Lee', 'charlie.l@example.com', 'UK', '2022-03-15'),
('Chris O''Neil', 'chris.oneil@mail.com', 'Ireland', '2022-02-09'),
('Samantha Green', 'samantha.green@gmail.com', 'USA', '2022-03-15'),
('Robert Miles', 'rob.miles@outlook.com', 'UK', '2022-02-28'),
('Linda Ray', 'linda.ray@hotmail.com', 'Canada', '2022-03-12'),
('Carlos Vega', 'c.vega@gmail.com', 'Mexico', '2022-01-09');

-- Products Table --
INSERT INTO products (product_name, category, price) VALUES
('Wireless Mouse', 'Electronics', 25.99),
('Gaming Keyboard', 'Electronics', 79.49),
('Office Chair', 'Furniture', 199.00),
('Desk Lamp', 'Furniture', 35.00),
('Laptop Stand', 'Accessories', 27.50),
('Noise Cancelling Headphones', 'Electronics', 199.99),
('Monitor 24"', 'Electronics', 149.99),
('Webcam HD', 'Electronics', 49.99),
('Notebook', 'Stationery', 3.50),
('Pen', 'Stationery', 1.50),
('Water Bottle', 'Home & Kitchen', 15.50),
('Travel Backpack', 'Accessories', 49.95),
('Smart Watch', 'Electronics', 199.00),
('Phone Case', 'Electronics', 12.00),
('Charging Brick', 'Electronics', 29.99);


-- Orders Table --
INSERT INTO orders (customer_id, order_date, payment_method, order_status, total_amount) VALUES
(1, '2022-01-05', 'Credit Card', 'completed', 0),
(2, '2022-02-12', 'PayPal', 'completed', 0),
(3, '2022-03-15', 'Credit Card', 'completed', 0),
(4, '2022-04-01', 'Credit Card', 'cancelled', 0),
(5, '2022-01-22', 'Debit Card', 'completed', 0),
(6, '2022-06-20', 'PayPal', 'completed', 0),
(7, '2022-07-02', 'Apple Pay', 'completed', 0),
(8, '2022-05-26', 'Credit Card', 'completed', 0),
(9, '2022-04-15', 'Debit Card', 'completed', 0),
(10, '2022-03-30', 'Credit Card', 'completed', 0),
(1, '2022-03-07', 'Credit Card', 'completed', 0),
(2, '2022-03-10', 'Credit Card', 'completed', 0),
(3, '2022-08-05', 'PayPal', 'completed', 0),
(4, '2022-12-05', 'Credit Card', 'completed', 0),
(5, '2022-09-15', 'Credit Card', 'completed', 0);



-- Order Items Table --
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 25.99),
(1, 2, 2, 79.49),
(2, 3, 1, 199.00),
(2, 4, 1, 35.00),
(3, 5, 2, 27.50),
(3, 6, 1, 199.99),
(4, 7, 1, 149.99),
(4, 8, 1, 49.99),
(5, 9, 3, 3.50),
(5, 10, 5, 1.50),
(6, 11, 1, 15.50),
(6, 12, 1, 49.95),
(7, 13, 1, 199.00),
(7, 14, 1, 12.00),
(8, 15, 1, 29.99),
(8, 1, 2, 25.99),
(9, 2, 1, 79.49),
(9, 3, 1, 199.00),
(10, 4, 2, 35.00),
(10, 5, 1, 27.50),
(11, 6, 1, 199.99),
(11, 7, 1, 149.99),
(12, 8, 1, 49.99),
(12, 9, 3, 3.50),
(13, 10, 2, 1.50),
(13, 11, 1, 15.50),
(14, 12, 1, 49.95),
(14, 13, 1, 199.00),
(15, 14, 2, 12.00),
(15, 15, 1, 29.99);



