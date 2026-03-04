import os
import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
plt.style.use("seaborn-v0_8-darkgrid")


st.set_page_config(page_title="Health Claims Fraud Dashboard", layout="wide")

st.title("Health Claims Fraud & Abuse Analytics Platform")

# --- DATABASE CONNECTION ---
load_dotenv()

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

conn = get_connection()

# --- METRIC SUMMARY ---
col1, col2, col3 = st.columns(3)

risk_summary = pd.read_sql("""
    SELECT risk_tier, COUNT(*) as count
    FROM provider_risk_tier
    GROUP BY risk_tier
""", conn)

high_count = risk_summary.loc[risk_summary['risk_tier']=='High','count'].sum()
medium_count = risk_summary.loc[risk_summary['risk_tier']=='Medium','count'].sum()
low_count = risk_summary.loc[risk_summary['risk_tier']=='Low','count'].sum()

col1.metric("High Risk Providers", int(high_count))
col2.metric("Medium Risk Providers", int(medium_count))
col3.metric("Low Risk Providers", int(low_count))

st.divider()

# --- RISK TIER BAR CHART ---
st.subheader("Provider Risk Tier Distribution")

color_map = {
    "High": "#d62728",
    "Medium": "#ff7f0e",
    "Low": "#2ca02c"
}

colors = [color_map.get(tier, "#1f77b4") for tier in risk_summary["risk_tier"]]

fig1, ax1 = plt.subplots()
ax1.bar(risk_summary["risk_tier"], risk_summary["count"], color=colors)
ax1.set_xlabel("Risk Tier")
ax1.set_ylabel("Number of Providers")
ax1.set_title("Risk Tier Distribution")
st.pyplot(fig1)

st.divider()

# --- PEER Z-SCORE DISTRIBUTION ---
st.subheader("Peer Claims Z-Score Distribution")

peer_df = pd.read_sql("""
    SELECT claims_peer_z
    FROM provider_peer_risk
""", conn)

fig2, ax2 = plt.subplots()
ax2.hist(peer_df["claims_peer_z"].dropna(), bins=30, color="#1f77b4", edgecolor="black", alpha=0.7)
ax2.set_xlabel("Claims Peer Z-Score")
ax2.set_ylabel("Frequency")
ax2.set_title("Peer Z-Score Distribution")
st.pyplot(fig2)

st.divider()

# --- TEMPORAL SPIKE DISTRIBUTION ---
st.subheader("Temporal Spike Risk Distribution")

spike_df = pd.read_sql("""
    SELECT max_spike_risk
    FROM provider_spike_risk_score
""", conn)

fig3, ax3 = plt.subplots()
ax3.hist(spike_df["max_spike_risk"].dropna(), bins=30,
         color="#9467bd", edgecolor="black", alpha=0.7)
ax3.set_xlabel("Max Spike Z-Score")
ax3.set_ylabel("Frequency")
ax3.set_title("Temporal Spike Risk Distribution")
st.pyplot(fig3)

st.divider()

# --- AVERAGE CLAIM BY SPECIALTY ---
st.subheader("Average Claim Amount by Specialty")

spec_df = pd.read_sql("""
    SELECT specialty, AVG(avg_claim_amount) as avg_amount
    FROM provider_summary
    GROUP BY specialty
""", conn)

fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.bar(spec_df["specialty"], spec_df["avg_amount"], color="#17becf")
ax4.set_xticklabels(spec_df["specialty"], rotation=45, ha='right')
ax4.set_ylabel("Average Claim Amount")
ax4.set_title("Average Claim Amount by Spcialty")
plt.tight_layout()
st.pyplot(fig4)

st.divider()

# --- HIGH RISK PROVIDERS TABLE ---
st.subheader("High Risk Providers Detail")

high_risk_df = pd.read_sql("""
    SELECT *
    FROM provider_risk_tier
    WHERE risk_tier = 'High'
    ORDER BY claims_peer_z DESC
""", conn)

st.dataframe(high_risk_df)

conn.close()