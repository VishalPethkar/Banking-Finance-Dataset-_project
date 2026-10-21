USE Banking_Finance_Dataset;

-- 1. Data check
SELECT COUNT(*) AS total_rows,
       MIN(Transaction_Date) AS first_date,
       MAX(Transaction_Date) AS last_date
FROM transactions;

-- 2. Total transaction value, average, count
SELECT COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount,
       ROUND(AVG(Transaction_Amount_INR),2) AS avg_amount
FROM transactions;

-- 3. Transaction type wise
SELECT Transaction_Type, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Transaction_Type
ORDER BY total_amount DESC;

-- 4. Status wise (success / failed split)
SELECT Transaction_Status, COUNT(*) AS txns,
       ROUND(COUNT(*) * 100 / SUM(COUNT(*)) OVER (), 2) AS pct
FROM transactions
GROUP BY Transaction_Status;

-- 5. Channel wise
SELECT Channel, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Channel
ORDER BY txns DESC;

-- 6. Bank wise
SELECT Bank_Name, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount,
       ROUND(AVG(Transaction_Amount_INR),2) AS avg_amount
FROM transactions
GROUP BY Bank_Name
ORDER BY total_amount DESC;

-- 7. City wise
SELECT Customer_City, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Customer_City
ORDER BY total_amount DESC;

-- 8. Merchant category wise
SELECT Merchant_Category, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Merchant_Category
ORDER BY total_amount DESC;

-- 9. Account type wise
SELECT Account_Type, COUNT(*) AS txns,
       ROUND(AVG(Balance_After_INR),2) AS avg_balance
FROM transactions
GROUP BY Account_Type
ORDER BY txns DESC;

-- 10. Monthly trend
SELECT DATE_FORMAT(Transaction_Date,'%Y-%m') AS month,
       COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY month
ORDER BY month;

-- 11. Yearly trend with growth over previous year
WITH y AS (
  SELECT YEAR(Transaction_Date) AS yr,
         SUM(Transaction_Amount_INR) AS total_amount
  FROM transactions GROUP BY yr
)
SELECT yr, ROUND(total_amount,2) AS total_amount,
       ROUND((total_amount - LAG(total_amount) OVER (ORDER BY yr))
             * 100 / LAG(total_amount) OVER (ORDER BY yr), 2) AS growth_pct
FROM y ORDER BY yr;

-- 12. Top 10 customers by value
SELECT Customer_ID, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Customer_ID
ORDER BY total_amount DESC
LIMIT 10;

-- 13. Top 10 largest single transactions
SELECT Transaction_ID, Customer_ID, Transaction_Date, Transaction_Type,
       Transaction_Amount_INR, Bank_Name
FROM transactions
ORDER BY Transaction_Amount_INR DESC
LIMIT 10;

-- 14. Loan analysis (loan wale rows)
SELECT Bank_Name, COUNT(*) AS loan_rows,
       ROUND(SUM(Loan_Amount_INR),2) AS total_loan,
       ROUND(AVG(Interest_Rate_Pct),2) AS avg_interest
FROM transactions
WHERE Loan_Amount_INR > 0
GROUP BY Bank_Name
ORDER BY total_loan DESC;

-- 15. Bank x Channel (kis bank me kaunsa channel zyada)
SELECT Bank_Name, Channel, COUNT(*) AS txns
FROM transactions
GROUP BY Bank_Name, Channel
ORDER BY Bank_Name, txns DESC;

-- 16. Customers jinke kayi cities/accounts hain (data quality check)
SELECT Customer_ID, COUNT(DISTINCT Account_ID) AS accounts
FROM transactions
GROUP BY Customer_ID
HAVING accounts > 1
ORDER BY accounts DESC
LIMIT 20;