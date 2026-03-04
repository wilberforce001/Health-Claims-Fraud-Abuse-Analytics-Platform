import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# 1. Load variables from .env
load_dotenv()

# 2. Assign the environment variables to names the script can use
# Note: I used DB_PASSWORD to match your psycopg2 block above
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD") 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# 3. Create engine using the variables defined above
# Added the port to ensure it connects to the right instance
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 4. Fetch and Plot
try:
    # 1. Risk Tier Distribution
    risk_df = pd.read_sql("SELECT risk_tier, COUNT(*) AS count FROM provider_risk_tier GROUP BY risk_tier", engine)

    plt.figure()
    plt.bar(risk_df["risk_tier"], risk_df["count"])
    plt.title("Provider Risk Tier Distribution")
    plt.xlabel("Risk Tier")
    plt.ylabel("Number of Providers")
    plt.tight_layout()
    plt.show(block=False)

    # 2. Peer Claims Z-Score Distribution
    peer_df = pd.read_sql("SELECT claims_peer_z FROM provider_peer_risk", engine)

    plt.figure()
    plt.hist(peer_df["claims_peer_z"].dropna(), bins=30)
    plt.title("Distribution of Peer Claims Z-Scores")
    plt.xlabel("Claims Peer Z-Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show(block=False)

    # 3. Temporal Spike Distribution
    spike_df = pd.read_sql("SELECT max_spike_risk FROM provider_spike_risk_score", engine)

    plt.figure()
    plt.hist(spike_df["max_spike_risk"].dropna(), bins=30)
    plt.title("Distribution of Maximum Temporal Spike Z-Scores")
    plt.xlabel("Max Spike Z-Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show(block=False)

    # 4. Average Claim Amount by Specialty
    spec_df = pd.read_sql("SELECT specialty, AVG(avg_claim_amount) as avg_amount From provider_summary GROUP BY specialty", engine)

    plt.figure()
    plt.bar(spec_df["specialty"], spec_df["avg_amount"])
    plt.xticks(rotation=45)
    plt.title("Average Claim Amount by Specialty")
    plt.xlabel("Specialty")
    plt.ylabel("Average Claim Amount")
    plt.tight_layout()
    plt.show()

    # engine.close()
except Exception as e:
    print(f"Error occurred: {e}")
