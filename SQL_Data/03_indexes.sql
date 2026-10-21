USE Banking_Finance_Dataset;

SELECT COUNT(*) AS total_rows FROM transactions;
SELECT * FROM transactions LIMIT 5;

ANALYZE TABLE transactions;
SHOW INDEX FROM transactions;



SELECT Transaction_Type, COUNT(*) AS txns,
       ROUND(SUM(Transaction_Amount_INR),2) AS total_amount
FROM transactions
GROUP BY Transaction_Type
ORDER BY total_amount DESC;