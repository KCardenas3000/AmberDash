import sqlite3
import pandas as pd

# Connect to database & query records
conn = sqlite3.connect("data/amberdash.db")
df = pd.read_sql_query("SELECT * FROM raw_disbursements", conn)
conn.close()

# Save to CSV for Power BI
df.to_csv("data/amberdash_clean.csv", index=False)
print("Successfully exported database to data/amberdash_clean.csv!")