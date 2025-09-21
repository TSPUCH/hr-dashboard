# HR Analytics & Employee Attrition Dashboard
### 1. Project Overview & Pitch

This project is more than just a report; it's an analytical tool designed to empower HR departments. It transforms raw employee data into an interactive dashboard, enabling managers to move beyond simple metrics and proactively identify the root causes of attrition.
By visualizing key factors like overtime, job satisfaction, and performance, this tool helps facilitate data-driven strategies to improve employee retention and workplace morale.
<img width="1885" height="1002" alt="Screenshot 2025-09-21 212548" src="https://github.com/user-attachments/assets/883fdf31-aa45-4935-aaa9-9def7a7e4c5d" />

### Table of Contents

Project Overview & Pitch

Key Features

Technology Stack

Data Source & Acknowledgments

Setup and Local Installation

How to Run the Application

Author

### 2.  Key Features

Interactive Visualizations: A suite of charts that dynamically update based on user selections.
KPI Dashboard: A high-level overview of critical metrics, including total employees, average income, and attrition rate.
Dynamic Filtering: The entire dashboard can be filtered by department for targeted analysis.
Data Management: Integrated forms allow for adding new employees and updating existing records.
Insightful Analysis: A dedicated "Attrition Deep Dive" tab explores potential causes of attrition.

### 3. Technology Stack

Python: The core programming language for all data processing and application logic.

Streamlit: The web framework used to build and serve the interactive dashboard.

Pandas: The primary library for data loading, cleaning, and manipulation.

Plotly: The library used for creating rich, interactive data visualizations.

SQLAlchemy: The library that acts as the engine, allowing Pandas to communicate efficiently with the SQL database.

SQLite: The lightweight, file-based database used to store the cleaned employee data (via Python's built-in sqlite3 module).

### 4. Data Source & Acknowledgments

Source

Dataset: IBM HR Analytics Employee Attrition & Performance

Provider: Kaggle

Author/Publisher: pavansubhash

Direct Link: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

Data Dictionary

A brief description of key columns used in the analysis:

Attrition: (Yes/No) Whether the employee has left the company.

Department: The department the employee works in (e.g., Sales, R&D).

JobSatisfaction: A rating from 1 (Low) to 4 (High).

MonthlyIncome: The employee's monthly salary in dollars.

OverTime: (Yes/No) Whether the employee works overtime.

PerformanceRating: A rating from 1 (Low) to 4 (Excellent).

### 5. Setup and Local Installation

Follow these steps to set up the project and run the dashboard locally.

Prerequisites:

Python 3.9+

Conda package manager

Step 1: Clone the Repository

    git clone (https://github.com/TSPUCH/hr-dashboard.git)

    cd hr-dashboard


Step 2: Create and Activate the Conda Environment
This command creates a new, isolated environment for the project.
    
        conda create --name hr_env python=3.9 -y
  
        conda activate hr_env


Step 3: Install Required Libraries
This command installs all necessary packages from the requirements.txt file.
    
        pip install -r requirements.txt


### 6. How to Run the Application
The application requires a two-step launch process.
Step 1: Create the Database
Run the setup script once to process the raw data and create the SQLite database.

        python src/setup_database.py


Step 2: Launch the Streamlit Dashboard
Start the Streamlit web server to launch the interactive dashboard.
   
        streamlit run src/app.py


The application will open in a new tab in your web browser.
### 7. Author
alhanouf alqarawi
