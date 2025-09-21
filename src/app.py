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
