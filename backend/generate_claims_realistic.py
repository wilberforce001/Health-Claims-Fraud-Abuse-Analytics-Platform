import os
import random
import uuid
from datetime import datetime, timedelta
import psycopg2
import numpy as np
from dotenv import load_dotenv

# CONFIG
NUM_PROVIDERS = 500
CPT_CODES = ["99213", "99214", "99203", "20610", "93000", "77066", "96372"]
ICD_CODES = ["I10", "E11.9", "M54.5", "J06.9", "R51"]
PLACES = ["Office", "Hospital", "Clinic"]

SPECIALTIES = [
    "Family Medicine",
    "Internal Medicine",
    "Cardiology",
    "Dermatology",
    "Orthopedics",
    "Neurology",
    "General Surgery",
    "Endocrinology"
]

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# --------------------------------------------------
# STEP 1: Generate Providers First
# --------------------------------------------------

providers = []

for _ in range(NUM_PROVIDERS):
    provider_id = random.randint(1000000000, 1999999999)
    specialty = random.choice(SPECIALTIES)
    providers.append((provider_id, specialty))

insert_providers = """
INSERT INTO providers (provider_id, specialty)
VALUES (%s, %s)
"""

cur.executemany(insert_providers, providers)
conn.commit()

# --------------------------------------------------
# STEP 2: Generate Claims Using Those Providers
# --------------------------------------------------

def random_date():
    return datetime.now() - timedelta(days=random.randint(0, 365))

claims_to_insert = []

for provider_id, specialty in providers:

    base_claims = np.random.poisson(lam=40)

    # 5% fraud injection
    is_fraud = random.random() < 0.05
    if is_fraud:
        base_claims *= random.randint(5, 15)

    for _ in range(base_claims):

        cpt = random.choice(CPT_CODES)
        icd = random.choice(ICD_CODES)

        base_amount = {
            "99213": 75,
            "99214": 110,
            "99203": 125,
            "20610": 200,
            "93000": 50,
            "77066": 180,
            "96372": 30,
        }[cpt]

        claim_amount = round(
            np.random.normal(base_amount, base_amount * 0.15), 2
        )

        # Fraud providers inflate payment
        if is_fraud:
            claim_amount *= random.uniform(1.5, 3.0)

        claims_to_insert.append((
            str(uuid.uuid4()),
            provider_id,
            str(uuid.uuid4()),
            cpt,
            icd,
            random_date(),
            claim_amount,
            random.choice(PLACES)
        ))

insert_claims = """
INSERT INTO claims (
    claim_id, provider_id, patient_id,
    cpt_code, icd_code, service_date,
    claim_amount, place_of_service
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

cur.executemany(insert_claims, claims_to_insert)
conn.commit()

print(f"Inserted {len(claims_to_insert)} claims.")

cur.close()
conn.close()