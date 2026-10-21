import glob, csv, pymysql, getpass

src = glob.glob(r"D:\download\**\banking_finance.csv", recursive=True)[0]
print("Using:", src)
pw = getpass.getpass("MySQL root password: ")

conn = pymysql.connect(host="localhost", user=input("MySQL user: "), password=pw, database="Banking_Finance_Dataset")
cur = conn.cursor()
cur.execute("TRUNCATE TABLE transactions")

sql = "INSERT INTO transactions VALUES (" + ",".join(["%s"] * 15) + ")"
with open(src, newline="", encoding="utf-8") as f:
    r = csv.reader(f)
    next(r)
    batch, total = [], 0
    for row in r:
        batch.append(row)
        if len(batch) == 10000:
            cur.executemany(sql, batch)
            conn.commit()
            total += len(batch)
            batch = []
            print(total, "rows")
    if batch:
        cur.executemany(sql, batch)
        conn.commit()
        total += len(batch)
print("Done:", total)
