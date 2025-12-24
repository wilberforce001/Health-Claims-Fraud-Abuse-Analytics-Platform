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