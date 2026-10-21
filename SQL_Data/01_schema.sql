
CREATE DATABASE IF NOT EXISTS Banking_Finance_Dataset;
USE Banking_Finance_Dataset;

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
  Transaction_ID         VARCHAR(15)   NOT NULL,
  Customer_ID            INT           NOT NULL,
  Account_ID             BIGINT        NOT NULL,
  Transaction_Date       DATE          NOT NULL,
  Transaction_Type       VARCHAR(30)   NOT NULL,
  Account_Type           VARCHAR(30)   NOT NULL,
  Transaction_Amount_INR DECIMAL(15,2) NOT NULL,
  Balance_After_INR      DECIMAL(15,2) NOT NULL,
  Channel                VARCHAR(30)   NOT NULL,
  Transaction_Status     VARCHAR(20)   NOT NULL,
  Merchant_Category      VARCHAR(40)   NOT NULL,
  Bank_Name              VARCHAR(50)   NOT NULL,
  Customer_City          VARCHAR(40)   NOT NULL,
  Interest_Rate_Pct      DECIMAL(5,2)  NULL,
  Loan_Amount_INR        DECIMAL(15,2) NULL
);