import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = "data/RBCS_Taxonomy_RY2025.csv"

def ingest_rbcs():
    df = pd.read_csv(CSV_PATH)

    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "hcpcs_cd": "hcpcs_cd",
        "rbcs_id": "rbcs_id",
        "rbcs_cat": "rbcs_cat",
        "rbcs_cat_desc": "rbcs_cat_desc",
        "rbcs_cat_subcat": "rbcs_subcat",
        "rbcs_subcat_desc": "rbcs_subcat_desc",
        "rbcs_family_desc": "rbcs_family_desc",
        "rbcs_major_ind": "rbcs_major_ind"
    })

    df = df[[
        "hcpcs_cd",
        "rbcs_id",
        "rbcs_cat",
        "rbcs_cat_desc",
        "rbcs_subcat",
        "rbcs_subcat_desc",
        "rbcs_family_desc",
        "rbcs_major_ind"
    ]].drop_duplicates()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO rbcs_taxonomy (
                hcpcs_cd,
                rbcs_id,
                rbcs_cat,
                rbcs_cat_desc,
                rbcs_subcat,
                rbcs_subcat_desc,
                rbcs_family_desc,
                rbcs_major_ind
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (hcpcs_cd) DO NOTHING;
        """, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

    print(f"RBCS ingest complete: {len(df)} rows processed")

if __name__ == "__main__":
    ingest_rbcs()
