import glob, pandas as pd

src = glob.glob(r"D:\download\Banking*\banking_finance_dataset_1000000_rows1.xlsx")[0]
dst = r"D:\download\banking_finance.csv"

print("Source:", src)
print("Reading Excel...")
df = pd.read_excel(src, engine="calamine")
print("Rows read:", len(df))

df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"]).dt.strftime("%Y-%m-%d")
df.to_csv(dst, index=False)
print("Saved:", dst)
