import os
import pandas as pd # pandas for reading, cleaning and manipulating data
from sqlalchemy import create_engine # sqlalchemy - used to connect Python to a database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---- ENV VALIDATION ----
required_env_vars = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME"
]

missing = [v for v in required_env_vars if not os.getenv(v)]
if missing:
    raise EnvironmentError(f"Missing required env vars: {missing}")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ---- DATABASE CONNECTION ----
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ---- INGEST MEDICARE PART B DATA ----
def ingest_part_b(csv_path, sample_size=5000):
    print("Loading Medicare Part B data...")
    df = pd.read_csv(csv_path, low_memory=False)

    # Sample to keep MVP manageable
    df = df.sample(sample_size, random_state=42)

    # Rename columns to match schema
    df = df.rename(columns={
        "Rndrng_NPI": "provider_id",
        "Rndrng_Prvdr_Type": "specialty",
        "HCPCS_Cd": "cpt_code",
        "Place_Of_Srvc": "place_of_service",
        "Avg_Sbmtd_Chrg_Amt": "claim_amount"
    })

    # Ensure optional CMS fields exist
    if "claim_amount" not in df.columns:
        print("claim_amount not found - creating synthetic values")
        df["claim_amount"] = 0.0

    if "place_of_service" not in df.columns:
        print("place_of_service not found - creating default values")
        df["place_of_service"] = "UNK"

    # Create synthetic fields
    df["claim_id"] = df.index.astype(str)
    df["patient_id"] = "PAT" + (df.index % 1000).astype(str)
    df["service_date"] = pd.to_datetime("2024-01-01")
    df["icd_code"] = "Z00.00"

    # ---- Providers table ----
    providers = (
        df[["provider_id", "specialty"]]
        .drop_duplicates()
        .dropna(subset=["provider_id"])
    )

    # ---- Claims table ----
    required_claim_cols = [
        "claim_id",
        "provider_id",
        "patient_id",
        "cpt_code",
        "icd_code",
        "service_date",
    ]

    optional_claim_cols = [
        "claim_amount",
        "place_of_service"
    ]

    claims_cols = required_claim_cols + [
        c for c in optional_claim_cols if c in df.columns
    ]

    claims = df[claims_cols]

    print(f"Inserting {len(providers)} providers...")
    providers.to_sql(
        "providers",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"Inserting {len(claims)} claims...")
    claims.to_sql(
        "claims",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Medicare Part B ingestion complete ✅")

# ---- RUN ----
if __name__ == "__main__":
    ingest_part_b("data/MUP_PHY_R25_P05_V20_D23_Prov_Svc.csv")
