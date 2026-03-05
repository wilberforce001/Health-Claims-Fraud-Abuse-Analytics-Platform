import os
import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

plt.style.use("seaborn-v0_8-darkgrid")

st.set_page_config(page_title="Health Claims Fraud Dashboard", layout="wide")

# PAGE STYLE
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1, h2, h3, h4 {color: #ffffff}
    </style>
""", unsafe_allow_html=True)

st.title("🚨 Health Claims Fraud & Abuse Analytics Platform")
st.caption("Advanced Risk Intelligence Dashboard")

# DATABASE CONNECTION
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


# LOAD DATA
risk_summary = pd.read_sql("""
    SELECT risk_tier, COUNT(*) as count
    FROM provider_risk_tier
    GROUP BY risk_tier
""", conn)

peer_df = pd.read_sql("SELECT claims_peer_z FROM provider_peer_risk", conn)
spike_df = pd.read_sql("SELECT max_spike_risk FROM provider_spike_risk_score", conn)

spec_df = pd.read_sql("""
    SELECT specialty, AVG(avg_claim_amount) as avg_amount
    FROM provider_summary
    GROUP BY specialty
""", conn)

# LOAD PROVIDER LIST
provider_list = pd.read_sql("""
    SELECT DISTINCT provider_id
    FROM provider_risk_tier ORDER BY provider_id
""", conn)

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

risk_filter = st.sidebar.multiselect(
    "Select Risk Tier",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

# PROVIDER SEARCH
provider_search = st.sidebar.selectbox(
    "Search Provider ID",
    options=["All Providers"] + provider_list["provider_id"].astype(str).tolist()
)

# KPI METRICS
col1, col2, col3 = st.columns(3)

high_count = risk_summary.loc[risk_summary['risk_tier']=='High','count'].sum()
medium_count = risk_summary.loc[risk_summary['risk_tier']=='Medium','count'].sum()
low_count = risk_summary.loc[risk_summary['risk_tier']=='Low','count'].sum()

col1.metric("🔴 High Risk Providers", int(high_count))
col2.metric("🟠 Medium Risk Providers", int(medium_count))
col3.metric("🟢 Low Risk Providers", int(low_count))

st.divider()

# RISK TIER BAR CHART
st.subheader("Provider Risk Tier Distribution")

order = ["High", "Medium", "Low"]
risk_summary["risk_tier"] = pd.Categorical(
    risk_summary["risk_tier"],
    categories=order,
    ordered=True
)
risk_summary = risk_summary.sort_values("risk_tier")

color_map = {
    "High": "#d62728",
    "Medium": "#ff7f0e",
    "Low": "#2ca02c"
}

colors = [color_map[t] for t in risk_summary["risk_tier"]]

fig1, ax1 = plt.subplots(figsize=(6,4))
bars = ax1.bar(risk_summary["risk_tier"], risk_summary["count"], color=colors)

for bar in bars:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{int(height)}",
        ha='center',
        va='bottom',
        fontweight='bold'
    )

ax1.set_xlabel("Risk Tier")
ax1.set_ylabel("Number of Providers")
ax1.set_title("Risk Tier Distribution", fontweight='bold')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig1)

st.divider()

# PEER Z-SCORE DISTRIBUTION
st.subheader("Peer Claims Z-Score Distribution")

fig2, ax2 = plt.subplots(figsize=(7,4))
ax2.hist(
    peer_df["claims_peer_z"].dropna(),
    bins=30,
    color="#1f77b4",
    edgecolor="black",
    alpha=0.75
)

# Threshold line (Z = 3)
ax2.axvline(3, color="red", linestyle="--", linewidth=2)
ax2.text(3, ax2.get_ylim()[1]*0.9, "Anomaly Threshold (Z=3)", color="red")

ax2.set_xlabel("Claims Peer Z-Score")
ax2.set_ylabel("Frequency")
ax2.set_title("Peer Z-Score Distribution", fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig2)

st.divider()

# TEMPORAL SPIKE DISTRIBUTION
st.subheader("Temporal Spike Risk Distribution")

fig3, ax3 = plt.subplots(figsize=(7,4))
ax3.hist(
    spike_df["max_spike_risk"].dropna(),
    bins=30,
    color="#9467bd",
    edgecolor="black",
    alpha=0.75
)

ax3.axvline(3, color="red", linestyle="--", linewidth=2)
ax3.text(3, ax3.get_ylim()[1]*0.9, "Anomaly Threshold (Z=3)", color="red")

ax3.set_xlabel("Max Spike Z-Score")
ax3.set_ylabel("Frequency")
ax3.set_title("Temporal Spike Risk Distribution", fontweight='bold')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig3)

st.divider()

# AVG CLAIM BY SPECIALTY
st.subheader("Average Claim Amount by Specialty")

spec_df = spec_df.sort_values("avg_amount", ascending=False)

fig4, ax4 = plt.subplots(figsize=(10,5))
bars = ax4.bar(spec_df["specialty"], spec_df["avg_amount"], color="#17becf")

ax4.set_ylabel("Average Claim Amount")
ax4.set_title("Average Claim Amount by Specialty", fontweight='bold')
ax4.set_xticks(range(len(spec_df["specialty"])))
ax4.set_xticklabels(spec_df["specialty"], rotation=45, ha='right')

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig4)

st.divider()

# HIGH RISK TABLE
st.subheader("🔴 High Risk Providers Detail")

query = """
    SELECT *
    FROM provider_risk_tier
    WHERE risk_tier = 'High'
"""

if provider_search != "All Providers":
    query += f" AND provider_id = '{provider_search}'"

query += " ORDER BY claims_peer_z DESC"

high_risk_df = pd.read_sql(query, conn)

st.dataframe(high_risk_df, use_container_width=True)

conn.close()