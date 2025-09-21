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

#--------------------------------------------------------------------------#
# 4. DATA LOADING AND INITIAL FILTERING
#--------------------------------------------------------------------------#
try:
    df = run_query("SELECT * FROM employees")
except Exception as e:
    st.error(f"Failed to load data from '{DB_PATH}': {e}")
    st.info("Please ensure you have run 'python src/setup_database.py' to create the database.")
    st.stop()

#--------------------------------------------------------------------------#
# 5. SIDEBAR LAYOUT
#--------------------------------------------------------------------------#
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.info("Add a 'logo.png' to the /images folder to display it here.")

st.sidebar.header("Dashboard Filters & Actions")

department = st.sidebar.selectbox(
    "Select a Department:",
    options=['All'] + sorted(df['Department'].unique().tolist())
)

df_filtered = df[df['Department'] == department] if department != 'All' else df.copy()

# --- Form: Add New Employee ---
with st.sidebar.form("new_employee_form", clear_on_submit=True):
    st.subheader("Add New Employee")
    new_id = st.number_input("Employee ID", min_value=df['EmployeeID'].max() + 1, step=1)
    new_dept = st.selectbox("Department", options=sorted(df['Department'].unique().tolist()))
    
    # NEW: Added more fields to create a complete, valid employee record.
    new_job_role = st.selectbox("Job Role", options=sorted(df['JobRole'].unique().tolist()))
    new_perf_rating = st.selectbox("Performance Rating", options=[1, 2, 3, 4])
    new_overtime = st.selectbox("OverTime", options=['Yes', 'No'])
    
    new_income = st.number_input("Monthly Income", min_value=1000, step=100)

    if st.form_submit_button("Add Employee"):
        try:
            # NEW: Updated INSERT query to include all the new fields.
            # This prevents creating rows with NULL values that can break charts.
            query = """
                INSERT INTO employees 
                (EmployeeID, Department, JobRole, PerformanceRating, OverTime, MonthlyIncome, Attrition) 
                VALUES (?, ?, ?, ?, ?, ?, 'No')
            """
            params = (new_id, new_dept, new_job_role, new_perf_rating, new_overtime, new_income)
            execute_query(query, params)
            st.sidebar.success(f"Employee {new_id} added successfully!")
            st.rerun()
        except sqlite3.IntegrityError:
             st.sidebar.error(f"Employee ID {new_id} already exists.")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")
