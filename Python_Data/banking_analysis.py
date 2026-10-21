import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)

# ======================================================
# 1. LOAD DATA
# ======================================================
path = r"D:\download\Banking & Finance Dataset — Power BI Project Guide\banking_finance_dataset_1000000_rows1.xlsx"
df = pd.read_excel(path)
# df = pd.read_pickle("banking_cache.pkl")   # faster, if you already have the cache

df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")
print("Shape:", df.shape)
print(df.head())

# ======================================================
# 2. DATA QUALITY
# ======================================================
print("\n--- Data types ---")
print(df.dtypes)
print("\n--- Missing values ---")
print(df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("Unique customers:", df["Customer_ID"].nunique())
print("Unique accounts :", df["Account_ID"].nunique())
print("Date range:", df["Transaction_Date"].min(), "to", df["Transaction_Date"].max())

# ======================================================
# 3. DESCRIPTIVE STATISTICS (pandas + numpy)
# ======================================================
num_cols = ["Transaction_Amount_INR", "Interest_Rate_Pct",
            "Loan_Amount_INR", "Balance_After_INR"]
print("\n--- Summary statistics ---")
print(df[num_cols].describe().T)

amount = df["Transaction_Amount_INR"].to_numpy()
print("\n--- NumPy statistics: Transaction Amount ---")
print("Mean       :", np.mean(amount))
print("Median     :", np.median(amount))
print("Std dev    :", np.std(amount))
print("90th pct   :", np.percentile(amount, 90))
print("99th pct   :", np.percentile(amount, 99))
print("Max        :", np.max(amount))

# Outliers using the IQR rule
q1, q3 = np.percentile(amount, [25, 75])
iqr = q3 - q1
outliers = ((amount < q1 - 1.5 * iqr) | (amount > q3 + 1.5 * iqr)).sum()
print(f"Outliers: {outliers:,} ({outliers / len(df) * 100:.2f}%)")

# ======================================================
# 4. GROUP ANALYSIS
# ======================================================
def summary_by(col, top=None):
    g = (df.groupby(col)["Transaction_Amount_INR"]
           .agg(transactions="count", total="sum", average="mean")
           .sort_values("total", ascending=False))
    return g.head(top) if top else g

print("\n--- By Channel ---")
print(summary_by("Channel"))
print("\n--- By Transaction Type ---")
print(summary_by("Transaction_Type"))
print("\n--- By Account Type ---")
print(summary_by("Account_Type"))
print("\n--- Top 10 Banks ---")
print(summary_by("Bank_Name", 10))
print("\n--- Top 10 Cities ---")
print(summary_by("Customer_City", 10))
print("\n--- Top 10 Merchant Categories ---")
print(summary_by("Merchant_Category", 10))

status_pct = df["Transaction_Status"].value_counts(normalize=True) * 100
print("\n--- Transaction Status % ---")
print(status_pct.round(2))

# Top 10 customers by total transaction amount
top_customers = (df.groupby("Customer_ID")["Transaction_Amount_INR"]
                   .sum().sort_values(ascending=False).head(10))
print("\n--- Top 10 Customers ---")
print(top_customers)

# ======================================================
# 5. TIME FEATURES
# ======================================================
df["Year"] = df["Transaction_Date"].dt.year
df["Month"] = df["Transaction_Date"].dt.month
df["Weekday"] = df["Transaction_Date"].dt.day_name()

monthly = df.groupby(df["Transaction_Date"].dt.to_period("M"))["Transaction_Amount_INR"].sum()
monthly.index = monthly.index.to_timestamp()

yearly = df.groupby("Year")["Transaction_Amount_INR"].agg(["count", "sum"])
print("\n--- Yearly summary ---")
print(yearly)

# Smaller sample for heavy plots
sample = df.sample(50_000, random_state=42)

# ======================================================
# 6. CHARTS
# ======================================================

# 6.1 Distribution of numeric columns
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for ax, col in zip(axes.ravel(), num_cols):
    sns.histplot(sample[col].dropna(), bins=40, kde=True, ax=ax)
    ax.set_title(f"Distribution of {col}")
plt.tight_layout()
plt.show()

# 6.2 Boxplots
fig, axes = plt.subplots(1, 4, figsize=(16, 5))
for ax, col in zip(axes, num_cols):
    sns.boxplot(y=sample[col], ax=ax)
    ax.set_title(col)
plt.tight_layout()
plt.show()

# 6.3 Channel and transaction type
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(x=summary_by("Channel").index, y=summary_by("Channel")["total"], ax=axes[0])
axes[0].set_title("Total Amount by Channel")
axes[0].tick_params(axis="x", rotation=30)
sns.countplot(data=df, x="Transaction_Type", order=df["Transaction_Type"].value_counts().index, ax=axes[1])
axes[1].set_title("Transactions by Type")
axes[1].tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.show()

# 6.4 Top banks and cities
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
tb = summary_by("Bank_Name", 10)
sns.barplot(x=tb["total"], y=tb.index, ax=axes[0])
axes[0].set_title("Top 10 Banks by Total Amount")
tc = summary_by("Customer_City", 10)
sns.barplot(x=tc["total"], y=tc.index, ax=axes[1])
axes[1].set_title("Top 10 Cities by Total Amount")
plt.tight_layout()
plt.show()

# 6.5 Transaction status (pie chart)
plt.figure(figsize=(7, 7))
plt.pie(status_pct.values, labels=status_pct.index, autopct="%1.1f%%", startangle=90)
plt.title("Transaction Status Share")
plt.show()

# 6.6 Monthly trend
plt.figure(figsize=(14, 5))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Monthly Total Transaction Amount")
plt.xlabel("Month")
plt.ylabel("Amount (INR)")
plt.show()

# 6.7 Weekday pattern
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wk = df.groupby("Weekday")["Transaction_Amount_INR"].count().reindex(order)
plt.figure(figsize=(10, 5))
sns.barplot(x=wk.index, y=wk.values)
plt.title("Transactions by Weekday")
plt.xticks(rotation=30)
plt.show()

# 6.8 Heatmap: average amount, Channel x Transaction Type
pivot = df.pivot_table(index="Channel", columns="Transaction_Type",
                       values="Transaction_Amount_INR", aggfunc="mean")
plt.figure(figsize=(11, 6))
sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlGnBu")
plt.title("Average Transaction Amount: Channel vs Transaction Type")
plt.show()

# 6.9 Average amount by account type (boxplot)
plt.figure(figsize=(10, 5))
sns.boxplot(data=sample, x="Account_Type", y="Transaction_Amount_INR", showfliers=False)
plt.title("Transaction Amount by Account Type")
plt.show()

# 6.10 Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(sample[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.show()

# 6.11 Scatter: amount vs balance
plt.figure(figsize=(9, 6))
sns.scatterplot(data=sample.sample(5000, random_state=1),
                x="Transaction_Amount_INR", y="Balance_After_INR", alpha=0.4)
plt.title("Transaction Amount vs Balance After")
plt.show()

# ======================================================
# 7. KEY SUMMARY
# ======================================================
print("\n" + "=" * 55)
print("KEY FINDINGS")
print("=" * 55)
print(f"Total transactions   : {len(df):,}")
print(f"Total amount (INR)   : {df['Transaction_Amount_INR'].sum():,.0f}")
print(f"Average transaction  : {df['Transaction_Amount_INR'].mean():,.2f}")
print(f"Top channel          : {summary_by('Channel').index[0]}")
print(f"Top bank             : {summary_by('Bank_Name').index[0]}")
print(f"Top city             : {summary_by('Customer_City').index[0]}")
print(f"Most common status   : {status_pct.index[0]} ({status_pct.iloc[0]:.1f}%)")
print("=" * 55)



# Shape: (1000000, 15)
#   Transaction_ID  Customer_ID  Account_ID Transaction_Date Transaction_Type  \
# 0   TXN000000001       180325  9573501481       2025-04-26          Payment   
# 1   TXN000000002       796559  3493244171       2026-09-28           Refund   
# 2   TXN000000003       689113  9793520123       2026-02-05       Withdrawal   
# 3   TXN000000004       494990  5838712654       2024-10-19           Refund   
# 4   TXN000000005       489713  5402426336       2025-08-31       Withdrawal   

#         Account_Type  Transaction_Amount_INR  Balance_After_INR  \
# 0             Salary                  649.56          12,277.06   
# 1  Recurring Deposit                  262.42          51,161.28   
# 2  Recurring Deposit                  843.17          23,774.22   
# 3      Fixed Deposit                2,323.10           3,511.84   
# 4            Current                1,763.15          18,154.46   

#             Channel Transaction_Status Merchant_Category  \
# 0               POS         Successful    Loan Repayment   
# 1               ATM         Successful             Other   
# 2            Branch         Successful         Education   
# 3  Internet Banking         Successful         Groceries   
# 4               ATM         Successful              Rent   

#                 Bank_Name Customer_City  Interest_Rate_Pct  Loan_Amount_INR  
# 0  Summit Commercial Bank         Delhi               1.72             0.00  
# 1            Aarohan Bank        Mumbai               9.47             0.00  
# 2     National Trust Bank       Kolkata              13.68             0.00  
# 3            Aarohan Bank        Mumbai               7.32             0.00  
# 4  Summit Commercial Bank         Delhi              10.55             0.00  

# --- Data types ---
# Transaction_ID                    object
# Customer_ID                        int64
# Account_ID                         int64
# Transaction_Date          datetime64[ns]
# Transaction_Type                  object
# Account_Type                      object
# Transaction_Amount_INR           float64
# Balance_After_INR                float64
# Channel                           object
# Transaction_Status                object
# Merchant_Category                 object
# Bank_Name                         object
# Customer_City                     object
# Interest_Rate_Pct                float64
# Loan_Amount_INR                  float64
# dtype: object

# --- Missing values ---
# Transaction_ID            0
# Customer_ID               0
# Account_ID                0
# Transaction_Date          0
# Transaction_Type          0
# Account_Type              0
# Transaction_Amount_INR    0
# Balance_After_INR         0
# Channel                   0
# Transaction_Status        0
# Merchant_Category         0
# Bank_Name                 0
# Customer_City             0
# Interest_Rate_Pct         0
# Loan_Amount_INR           0
# dtype: int64

# Duplicate rows: 0
# Unique customers: 604054
# Unique accounts : 999941
# Date range: 2023-01-01 00:00:00 to 2026-10-14 00:00:00

# --- Summary statistics ---
#                               count       mean        std    min       25%  \
# Transaction_Amount_INR 1,000,000.00   2,980.58   3,897.29  10.00    921.71   
# Interest_Rate_Pct      1,000,000.00       9.25       5.05   0.50      4.88   
# Loan_Amount_INR        1,000,000.00 225,802.00 569,791.45   0.00      0.00   
# Balance_After_INR      1,000,000.00  37,058.03  35,070.89 420.65 15,702.35   

#                              50%       75%          max  
# Transaction_Amount_INR  1,811.25  3,555.25   366,532.05  
# Interest_Rate_Pct           9.24     13.63        18.00  
# Loan_Amount_INR             0.00      0.00 2,499,982.33  
# Balance_After_INR      26,925.17 46,192.24 1,298,645.61  

# --- NumPy statistics: Transaction Amount ---
# Mean       : 2980.58426708
# Median     : 1811.25
# Std dev    : 3897.283969831241
# 90th pct   : 6523.873
# 99th pct   : 18446.323500000002
# Max        : 366532.05
# Outliers: 77,482 (7.75%)

# --- By Channel ---
#                   transactions          total  average
# Channel                                               
# Internet Banking        167565 501,317,933.66 2,991.78
# UPI                     166833 500,713,242.34 3,001.28
# Branch                  166729 498,679,014.16 2,990.96
# Mobile App              166661 496,202,466.90 2,977.32
# ATM                     166080 492,190,608.46 2,963.58
# POS                     166132 491,481,001.56 2,958.38

# --- By Transaction Type ---
#                   transactions          total  average
# Transaction_Type                                      
# Deposit                 143089 428,624,524.58 2,995.51
# Refund                  142949 426,668,367.88 2,984.76
# Loan EMI                142935 425,805,933.62 2,979.02
# Payment                 142832 425,456,457.35 2,978.72
# Transfer                142995 425,200,907.68 2,973.54
# Withdrawal              142370 424,978,355.39 2,985.03
# Investment              142830 423,849,720.58 2,967.51

# --- By Account Type ---
#                    transactions          total  average
# Account_Type                                           
# Savings                  200416 599,343,243.51 2,990.50
# Salary                   200289 596,726,209.38 2,979.33
# Current                  200010 596,192,272.40 2,980.81
# Recurring Deposit        200200 595,392,458.12 2,973.99
# Fixed Deposit            199085 592,930,083.67 2,978.28

# --- Top 10 Banks ---
#                         transactions          total  average
# Bank_Name                                                   
# Aarohan Bank                  199554 598,357,102.63 2,998.47
# National Trust Bank           200388 596,723,563.01 2,977.84
# Western Finance Bank          200297 595,562,925.26 2,973.40
# Unity Cooperative Bank        199394 595,388,825.38 2,985.99
# Summit Commercial Bank        200367 594,551,850.80 2,967.31

# --- Top 10 Cities ---
#                transactions          total  average
# Customer_City                                      
# Delhi                100186 299,909,624.64 2,993.53
# Solapur              100109 299,272,429.75 2,989.47
# Mumbai               100311 298,946,739.32 2,980.20
# Chennai              100014 298,648,578.37 2,986.07
# Kolkata               99616 298,304,313.89 2,994.54
# Pune                 100073 298,246,879.75 2,980.29
# Nashik               100130 297,916,703.98 2,975.30
# Nagpur                99659 297,255,006.18 2,982.72
# Bengaluru             99991 296,251,767.59 2,962.78
# Hyderabad             99911 295,832,223.61 2,960.96

# --- Top 10 Merchant Categories ---
#                    transactions          total  average
# Merchant_Category                                      
# Investment                83525 249,638,655.90 2,988.79
# Shopping                  83192 249,602,614.23 3,000.32
# Rent                      83888 249,543,189.31 2,974.72
# Travel                    83425 249,543,006.05 2,991.23
# Utilities                 83672 249,231,201.10 2,978.67
# Loan Repayment            83021 249,218,603.48 3,001.87
# Other                     83206 249,022,882.65 2,992.85
# Education                 83374 248,545,629.87 2,981.09
# Healthcare                83245 247,774,261.24 2,976.45
# Fuel                      82728 246,953,405.01 2,985.12

# --- Transaction Status % ---
# Transaction_Status
# Successful   90.98
# Failed        4.01
# Pending       3.51
# Reversed      1.50
# Name: proportion, dtype: float64

# --- Top 10 Customers ---
# Customer_ID
# 668506   367,039.21
# 467174   215,585.18
# 263055   194,659.48
# 458140   186,160.82
# 317819   159,650.65
# 583809   149,129.93
# 520016   144,640.56
# 252861   143,376.75
# 141261   132,948.51
# 197744   132,455.37
# Name: Transaction_Amount_INR, dtype: float64

# --- Yearly summary ---
#        count            sum
# Year                       
# 2023  264635 787,200,340.63
# 2024  264041 787,223,463.72
# 2025  263329 786,998,801.17
# 2026  207995 619,161,661.56

# =======================================================
# KEY FINDINGS
# =======================================================
# Total transactions   : 1,000,000
# Total amount (INR)   : 2,980,584,267
# Average transaction  : 2,980.58
# Top channel          : Internet Banking
# Top bank             : Aarohan Bank
# Top city             : Delhi
# Most common status   : Successful (91.0%)
# =======================================================
# PS D:\download\Banking & Finance Dataset — Power BI Project Guide> 