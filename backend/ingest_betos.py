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
    "Allowed Services": "betos_description"
})

# Keep only relevant columns
df = df[["betos_group", "betos_description"]]

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
INSERT INTO betos_codes (betos_group, betos_description)
VALUES (%s, %s)
ON CONFLICT (betos_group) DO NOTHING;
"""

# Insert each row
for row in df.itertuples(index=False):
    cur.execute(insert_sql, row)

conn.commit()
cur.close()
conn.close()

print("BETOS codes ingested successfully ✅.")
