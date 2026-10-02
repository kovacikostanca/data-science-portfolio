-- 	Create Database Schema --

-- E-commerce Database --
CREATE DATABASE ecommerce;

-- Create Tables --
-- Customers Table --
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50),
    signup_date DATE
);

-- Products Table -- 
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2) NOT NULL CHECK(price > 0)
);

-- Orders Table --
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    payment_method VARCHAR(50),
    order_status VARCHAR(20),
    total_amount NUMERIC(10,2) DEFAULT 0
);

-- Orders Items Table --
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK(quantity > 0),
    price NUMERIC(10,2) NOT NULL CHECK(price > 0)
);
