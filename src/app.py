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
