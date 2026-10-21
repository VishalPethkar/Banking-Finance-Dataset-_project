import pandas as pd

folder = r"D:\download\Banking_Finance_Dataset"
df = pd.read_excel(folder + r"\banking_finance_dataset_1000000_rows1.xlsx", engine="calamine")
df.to_csv(folder + r"\banking.csv", index=False, date_format="%Y-%m-%d")

print(df.shape)     # should be (1000000, number_of_columns)
print(df.dtypes)    # needed to design the MySQL table
print(df.head())
