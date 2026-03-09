import os
import streamlit as st
import psycopg2 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Health Claims Fraud Dashboard", layout="wide")

## DB connection
def get_data(query):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("Health Claims Fraud & Abuse Analytics")


# BETOS Risk Distribution 
# - Shows immediate risk stratification
# - High-rik BETOS = abuse-prone services
st.header("BETOS Risk Overview")

query = """
SELECT betos_group, complexity_score
FROM betos_complexity
ORDER BY complexity_score DESC;
"""

df_betos = get_data(query)

fig, ax = plt.subplots()
sns.barplot(data=df_betos, x="betos_group", y="complexity_score", ax=ax)
ax.set_title("BETOS Complexity Scores")
ax.set_xlabel("BETOS Group")
ax.set_ylabel("Complexity Score")
plt.xticks(rotation=90)

st.pyplot(fig)

# BETOS Cost vs Volume (Fraud Signal)
# - Low volume + high cost - classic abuse risk. 
# - A real CMS fraud detection heuristic

st.header("BETOS Cost vs Volume")

query = """
SELECT betos_group,
allowed_services,
payment_amt,
(payment_amt / allowed_services) AS avg_cost_per_service
FROM betos_metrics
ORDER BY avg_cost_per_service DESC;
"""

df_cost = get_data(query)

fig, ax = plt.subplots()
sns.scatterplot(
    data=df_cost,
    x="allowed_services",
    y="avg_cost_per_service",
    size="payment_amt",
    sizes=(20, 50),
    alpha=0.7,
    ax=ax
)

ax.set_xscale("log")
ax.set_title("Cost vs Volume (Fraud Lens)")
ax.set_xlabel("Allowed Services (log scale)")
ax.set_ylabel("Avg Cost per Service")

st.pyplot(fig)

# Provider Risk View
# - Identifies providers with abnormally expensive behavior
# - Foundation for fraud flags

st.header("High-Risk Providers")

query = """
SELECT
p.provider_id,
p.specialty,
COUNT(*) AS total_claims,
AVG(c.claim_amount) AS avg_claim
FROM claims c
JOIN providers p USING (provider_id)
GROUP BY p.provider_id, p.specialty
ORDER BY avg_claim DESC
LIMIT 20;
"""

df_providers = get_data(query)
st.dataframe(df_providers)
