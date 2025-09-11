-- ===============================================
-- Step 1: Create Database and Table
-- ===============================================

CREATE DATABASE sql_project_sales;
USE sql_project_sales;

CREATE TABLE sales_store (
    transaction_id VARCHAR(15),
    customer_id VARCHAR(15),
    customer_name VARCHAR(30),
    customer_age INT,
    gender VARCHAR(15),
    product_id VARCHAR(15),
    product_name VARCHAR(15),
    product_category VARCHAR(15),
    quantity INT,
    price FLOAT,
    payment_mode VARCHAR(15),
    purchase_date DATE,
    time_of_purchase TIME,
    status VARCHAR(15)
);
-- ===============================================
-- Step 2: Loading data 
-- ===============================================
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sales.csv'
INTO TABLE sales_store
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
    transaction_id,
    customer_id,
    customer_name,
    @customer_age,
    gender,
    product_id,
    product_name,
    product_category,
    @quantity,
    @price,
    payment_mode,
    @purchase_date,
    time_of_purchase,
    status
)
SET 
    customer_age = NULLIF(@customer_age, ''),
    quantity = NULLIF(@quantity, ''),
    price = NULLIF(@price, ''),
    purchase_date = STR_TO_DATE(NULLIF(@purchase_date,''), '%d-%m-%Y');
select purchase_date from sales_store;



-- Step 4:  cleaning and  copying and removing  duplicates
-- ===============================================
CREATE TABLE sales AS
SELECT * FROM sales_store;
# copying the table
-- Create new table and copy data
CREATE TABLE sales AS
SELECT * FROM sales_store;
#-----------------------------------------------------------------------------------------------------------------------------------------
#----------- FINDING THE TOTAL NULL VALUES IN EACH COLUMN------------------
SELECT 'transaction_id' AS column_name, COUNT(*) AS null_count
FROM sales WHERE transaction_id IS NULL
UNION ALL
SELECT 'customer_id', COUNT(*) FROM sales WHERE customer_id IS NULL
UNION ALL
SELECT 'customer_name', COUNT(*) FROM sales WHERE customer_name IS NULL
UNION ALL
SELECT 'customer_age', COUNT(*) FROM sales WHERE customer_age IS NULL
UNION ALL
SELECT 'gender', COUNT(*) FROM sales WHERE gender IS NULL
UNION ALL
SELECT 'product_id', COUNT(*) FROM sales WHERE product_id IS NULL
UNION ALL
SELECT 'product_name', COUNT(*) FROM sales WHERE product_name IS NULL
UNION ALL
SELECT 'product_category', COUNT(*) FROM sales WHERE product_category IS NULL
UNION ALL
SELECT 'quantity', COUNT(*) FROM sales WHERE quantity IS NULL
UNION ALL
SELECT 'price', COUNT(*) FROM sales WHERE price IS NULL
UNION ALL
SELECT 'payment_mode', COUNT(*) FROM sales WHERE payment_mode IS NULL
UNION ALL
SELECT 'purchase_date', COUNT(*) FROM sales WHERE purchase_date IS NULL
UNION ALL
SELECT 'time_of_purchase', COUNT(*) FROM sales WHERE time_of_purchase IS NULL
UNION ALL
SELECT 'status', COUNT(*) FROM sales WHERE status IS NULL;
#-------------------------------------------------------------------------------------------------------



SELECT transaction_id,COUNT(*)
FROM sales 
GROUP BY transaction_id
HAVING COUNT(transaction_id) >1;
WITH CTE AS (
    SELECT 
        transaction_id,
        ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY transaction_id) AS row_num
    FROM sales
)
SELECT *
FROM CTE
WHERE transaction_id IN ('TXN240646','TXN342128','TXN855235','TXN981773')
  AND row_num > 1;
DELETE s
FROM sales s
JOIN (
    SELECT 
        transaction_id,
        ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY transaction_id) AS row_num
    FROM sales
) t
ON s.transaction_id = t.transaction_id
WHERE t.row_num > 1
  AND s.transaction_id IN ('TXN240646','TXN342128','TXN855235','TXN981773');

#------------Switch off the safety option--------
SET SQL_SAFE_UPDATES=0;
#-----------------------------------------------
#-----------------filling null ---------------------------
select * from sales
where customer_id='CUST1003';

UPDATE sales 
set customer_name="Mahika Saini",customer_age=35,gender="Male"
where customer_id='CUST1003';
#--------------------------------------------------------------
# deleted null values
delete  from sales
where customer_age is NULL ;

#--------------------------------------------


-- ===============================================
-- Step 5: Data Cleaning
-- ===============================================
-- Clean Gender
UPDATE sales SET gender='M' WHERE gender='Male';
UPDATE sales SET gender='F' WHERE gender='Female';
select distinct gender from sales; 

-- Clean Payment Mode
UPDATE sales SET payment_mode='Credit Card' WHERE payment_mode='CC';

describe sales;
select * from sales
where transaction_id is null;
-- ===============================================
-- Step 6: Data Analysis Queries
-- ===============================================

-- 1️⃣ Top 5 most selling products by quantity
SELECT product_name, SUM(quantity) AS total_quantity_sold
FROM sales
WHERE status='delivered'
GROUP BY product_name
ORDER BY total_quantity_sold DESC
LIMIT 5;

-- 2️⃣ Top 5 most frequently cancelled products
SELECT product_name, COUNT(*) AS total_cancelled
FROM sales
WHERE status='cancelled'
GROUP BY product_name
ORDER BY total_cancelled DESC
LIMIT 5;

-- 3️⃣ Peak purchase time of day
SELECT 
    CASE 
        WHEN HOUR(time_of_purchase) BETWEEN 0 AND 5 THEN 'NIGHT'
        WHEN HOUR(time_of_purchase) BETWEEN 6 AND 11 THEN 'MORNING'
        WHEN HOUR(time_of_purchase) BETWEEN 12 AND 17 THEN 'AFTERNOON'
        WHEN HOUR(time_of_purchase) BETWEEN 18 AND 23 THEN 'EVENING'
    END AS time_of_day,
    COUNT(*) AS total_orders
FROM sales
GROUP BY time_of_day
ORDER BY total_orders DESC;

-- 4️⃣ Top 5 highest spending customers
SELECT customer_name, SUM(price * quantity) AS total_spend
FROM sales
GROUP BY customer_name
ORDER BY SUM(price * quantity) DESC
LIMIT 5;

-- 5️⃣ Revenue by product category
SELECT product_category, round(SUM(price * quantity)/10000000,2) AS revenue
FROM sales
GROUP BY product_category
ORDER BY revenue DESC;

-- 6️⃣ Cancellation / Return rate per category
SELECT product_category,
       ROUND(SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END)*100/COUNT(*),2) AS cancelled_percent,
       ROUND(SUM(CASE WHEN status='returned' THEN 1 ELSE 0 END)*100/COUNT(*),2) AS returned_percent
FROM sales
GROUP BY product_category
ORDER BY cancelled_percent DESC;

-- 7️⃣ Preferred payment mode
SELECT payment_mode, COUNT(*) AS total_count
FROM sales
GROUP BY payment_mode
ORDER BY total_count DESC;

-- 8️⃣ Age group purchase behavior
SELECT 
    CASE    
        WHEN customer_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN customer_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN customer_age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END AS age_group,
    round(SUM(price * quantity)/10000000,2) AS total_purchase
FROM sales
GROUP BY age_group
ORDER BY total_purchase DESC;

-- 9️⃣ Monthly sales trend
SELECT DATE_FORMAT(purchase_date,'%Y-%m') AS Month_Year,
       round(SUM(price * quantity)/10000000,2) AS total_sales,
       SUM(quantity) AS total_quantity
FROM sales
GROUP BY Month_Year
ORDER BY Month_Year ASC;

-- 10️⃣ Gender vs Product Category
SELECT gender, product_category, COUNT(*) AS total_purchase
FROM sales
GROUP BY gender,product_category
ORDER BY  gender;
