import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Path to Excel file
excel_path = "data/betos-cy-2024.xlsx"
df_preview = pd.read_excel(excel_path, header=None)
print(df_preview.head(10))

# Load BETOS Excel
df = pd.read_excel(excel_path, header=2)

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Debug: show detected columns
print("Detected columns:", df.columns.tolist())

# Rename columns to match your DB table
df = df.rename(columns={
    "BETOS": "betos_group",
    "Allowed Services": "allowed_services",
    "Allowed Charges": "allowed_charges",
    "Payment Amt": "payment_amt"
})

# Keep only relevant columns
df = df[["betos_group", "allowed_services", "allowed_charges", "payment_amt"]]

# Ensure numeric types
numeric_cols = ["allowed_services", "allowed_charges", "payment_amt"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove empty rows
df = df.dropna(subset=["betos_group"])

# Connect to Postgres
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
except psycopg2.OperationalError as e:
    print("Error connecting to the database:", e)
    exit(1)

cur = conn.cursor()

# Insert SQL
insert_sql = """
INSERT INTO public.betos_metrics (betos_group, allowed_services, allowed_charges, payment_amt)
VALUES (%s, %s, %s, %s)
ON CONFLICT (betos_group) DO NOTHING;
"""

# Insert each row
for row in df.itertuples(index=False):
    cur.execute(insert_sql, row)

conn.commit()

cur.execute("SELECT COUNT(*) FROM public.betos_metrics;")
print(cur.fetchone())

cur.close()
conn.close()


print("BETOS codes ingested successfully ✅.")



