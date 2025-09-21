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

# --- Form: Update Employee Income ---
with st.sidebar.form("update_income_form", clear_on_submit=True):
    st.subheader("Update Employee Income")
    emp_to_update = st.selectbox("Select Employee ID", options=sorted(df['EmployeeID'].unique().tolist()))
    new_monthly_income = st.number_input("New Monthly Income", min_value=1000, step=100)

    if st.form_submit_button("Update Income"):
        try:
            query = "UPDATE employees SET MonthlyIncome = ? WHERE EmployeeID = ?"
            params = (new_monthly_income, emp_to_update)
            execute_query(query, params)
            st.sidebar.success(f"Income for Employee ID {emp_to_update} updated!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Failed to update income: {e}")

#--------------------------------------------------------------------------#
# 6. MAIN DASHBOARD LAYOUT
#--------------------------------------------------------------------------#
st.title(f"📊 HR Analytics Dashboard: {department}")

# --- KPIs ---
total_employees = df_filtered.shape[0]
avg_income = int(df_filtered['MonthlyIncome'].mean())
attrition_rate = (df_filtered[df_filtered['Attrition'] == 'Yes'].shape[0] / total_employees * 100) if total_employees > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Total Employees", value=total_employees)
kpi2.metric(label="Average Monthly Income", value=f"${avg_income:,}")
kpi3.metric(label="Attrition Rate", value=f"{attrition_rate:.2f}%")

st.markdown("---")

# --- Tabs for organization ---
tab1, tab2, tab3 = st.tabs(["Department Overview", "Attrition Deep Dive", "Employee Details"])

# --- TAB 1: Department Overview ---
with tab1:
    st.header("Department Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Employee Count by Job Role")
        # Ensure 'JobRole' exists and is not null before processing
        if 'JobRole' in df_filtered.columns:
            role_counts = df_filtered['JobRole'].value_counts().reset_index()
            fig_bar = px.bar(role_counts, x='count', y='JobRole', orientation='h', color_discrete_sequence=['#4F008C'])
            st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.subheader("Performance Rating Distribution")
        # Ensure 'PerformanceRating' exists and is not null before processing
        if 'PerformanceRating' in df_filtered.columns:
            perf_counts = df_filtered['PerformanceRating'].value_counts().reset_index()
            fig_perf = px.bar(perf_counts, x='PerformanceRating', y='count', color_discrete_sequence=['#FF375E'])
            st.plotly_chart(fig_perf, use_container_width=True)

# --- TAB 2: Attrition Deep Dive ---
with tab2:
    st.header("Attrition Deep Dive")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Overall Attrition Breakdown")
        attrition_counts = df_filtered['Attrition'].value_counts().reset_index()
        fig_pie = px.pie(attrition_counts, names='Attrition', values='count', hole=0.4,
                         color='Attrition', color_discrete_map={'Yes': '#FF375E', 'No': '#4F008C'})
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.subheader("Attrition Rate by Overtime")
        # Ensure 'OverTime' exists and is not null before processing
        if 'OverTime' in df_filtered.columns:
            overtime_attrition = df_filtered.groupby('OverTime')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
            if 'Yes' in overtime_attrition.columns:
                overtime_attrition_df = (overtime_attrition['Yes'] * 100).reset_index()
                fig_overtime = px.bar(overtime_attrition_df, x='OverTime', y='Yes',
                                      labels={'Yes': 'Attrition Rate (%)'}, color_discrete_sequence=['#FF375E'])
                st.plotly_chart(fig_overtime, use_container_width=True)

    # --- ADVANCED SQL: Using a Common Table Expression (CTE) ---
    st.subheader("Are We Losing Our Top Performers?")
    cte_query = """
        WITH PerfAttrition AS (
            SELECT PerformanceRating, Attrition, COUNT(EmployeeID) as Count
            FROM employees
            WHERE (:dept = 'All' OR Department = :dept)
            AND PerformanceRating IS NOT NULL
            GROUP BY PerformanceRating, Attrition
        )
        SELECT * FROM PerfAttrition;
    """
    params = {"dept": department}
    perf_attrition_df = run_query(cte_query, params=params)

    if not perf_attrition_df.empty:
        fig_perf_attr = px.bar(
            perf_attrition_df, x='PerformanceRating', y='Count', color='Attrition',
            title='Attrition Count by Performance Rating', barmode='group',
            color_discrete_map={'Yes': '#FF375E', 'No': '#4F008C'}
        )
        st.plotly_chart(fig_perf_attr, use_container_width=True)

# --- TAB 3: Employee Details ---
with tab3:
    st.header("Employee Details")
    display_columns = ['EmployeeID', 'Age', 'Department', 'JobRole', 'MonthlyIncome', 'PerformanceRating', 'YearsAtCompany', 'Attrition', 'OverTime']
    st.dataframe(df_filtered[display_columns], use_container_width=True)

