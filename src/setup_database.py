# =====================================================================================
#
#  Database Setup Script
#
#  Purpose: This script is designed to be run only ONCE. Its job is to:
#           1. Read the raw employee data from the CSV file.
#           2. Clean up the column names and any missing data.
#           3. Create a new, clean SQLite database file in the /data folder.
#           4. Load the cleaned data into a table inside that database.
#
# =====================================================================================

#--------------------------------------------------------------------------#
# 1. IMPORTS AND CONFIGURATION
#--------------------------------------------------------------------------#
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import re
import os

# --- Configuration Settings ---
# We build robust file paths that work on any computer.
# This script is in /src, so we go up one level ('..') to the project root,
# then down into the /data folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
CSV_FILE_PATH = os.path.join(DATA_DIR, 'WA_Fn-UseC_-HR-Employee-Attrition.csv')
DB_FILE_PATH = os.path.join(DATA_DIR, 'hr_database.db')
TABLE_NAME = 'employees'

#--------------------------------------------------------------------------#
# 2. HELPER FUNCTION FOR CLEANING
#--------------------------------------------------------------------------#
def clean_col_names(df):
    """Cleans the column names of a pandas DataFrame to be safe for a database."""
    cols = df.columns
    new_cols = []
    for col in cols:
        new_col = re.sub(r'[^0-9a-zA-Z_]', '', col)
        if new_col:
            new_cols.append(new_col)
    df.columns = new_cols
    return df

#--------------------------------------------------------------------------#
# 3. MAIN DATABASE SETUP FUNCTION
#--------------------------------------------------------------------------#
def setup_database():
    """
    Main function to read, clean, and load data into a new SQLite database.
    """
    try:
        # --- Task 1: Load Data ---
        print(f"Loading data from '{CSV_FILE_PATH}'...")
        df = pd.read_csv(CSV_FILE_PATH)
        print("Data loaded successfully.")

        # --- Task 2: Data Cleaning and Preparation ---
        if 'EmployeeID' not in df.columns:
            df.insert(0, 'EmployeeID', range(1, 1 + len(df)))

        # FIX: Handle missing Department values at the source.
        # We drop rows where 'Department' is NaN, as they are not useful for analysis.
        initial_rows = len(df)
        df.dropna(subset=['Department'], inplace=True)
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            print(f"Data Cleaning: Removed {rows_dropped} rows with missing Department information.")

        if 'YearsAtCompany' in df.columns and df['YearsAtCompany'].isnull().any():
            median_years = df['YearsAtCompany'].median()
            df['YearsAtCompany'].fillna(median_years, inplace=True)
            print(f"Data Cleaning: Missing 'YearsAtCompany' values filled with median value: {median_years}")

        df = clean_col_names(df)
        print("Column names cleaned.")

        # --- Task 3: Create Database and Insert Data ---
        os.makedirs(DATA_DIR, exist_ok=True)
        engine = create_engine(f'sqlite:///{DB_FILE_PATH}')
        print(f"Connecting to database at '{DB_FILE_PATH}'...")

        df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
        print(f"Data successfully inserted into '{TABLE_NAME}' table.")

        # --- Task 4: Verification ---
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"Verification: Found {count} records in '{TABLE_NAME}' table.")
        print("\nDatabase setup is complete! You can now run the main application.")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        print("Please ensure the /data folder exists and the CSV file is inside it.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
#--------------------------------------------------------------------------#
# 4. SCRIPT EXECUTION
#--------------------------------------------------------------------------#
if __name__ == '__main__':
    setup_database()
