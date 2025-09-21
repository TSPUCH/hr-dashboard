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
