#--------------------------------------------------------------------------#
# 1. IMPORTS AND PAGE CONFIGURATION
#--------------------------------------------------------------------------#
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#--------------------------------------------------------------------------#
# 2. CUSTOM STYLING & FILE PATHS
#--------------------------------------------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "images")
LOGO_PATH = os.path.join(IMAGE_DIR, "logo.svg")
DB_PATH = os.path.join(BASE_DIR, "..", "data", "hr_database.db")

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-image: linear-gradient(to bottom, #000, #4F008C);
    }
</style>
""", unsafe_allow_html=True)

#--------------------------------------------------------------------------#
# 3. DATABASE UTILITY FUNCTIONS
#--------------------------------------------------------------------------#
def get_connection():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def run_query(query, params=None):
    """Runs a SQL SELECT query and returns the result as a DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_query(query, params=None):
    """Executes a non-select SQL query (INSERT, UPDATE)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()
