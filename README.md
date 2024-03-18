# Globant’s Data Engineering Coding Challenge

This challenge involves loading CSV files into a SQL Server DB and creating two reports using the loaded data.

## Section #1

### ETL.py

This file contains the logic to read the CSV files and load them into a SQL Server DB (Local) in an ingestion schema. Subsequently, the data will be loaded into the dimension schema to be available for reporting.

### create_db.sql

This script creates the schema of the tables in a SQL Database.

## Section #2

### Filename: reports.py

This file creates two reports based on the tables in the dimension schema:

1. **hired_employees_per_department**: Displays the number of employees hired for each job and department in 2021, divided by quarter. Results are ordered alphabetically by department and job.

2. **top_hiring_departments**: Provides a list of department IDs, names, and the number of employees hired by each department that hired more employees than the mean of employees hired in 2021 for all departments. The list is ordered by the number of employees hired (descending).

## Usage

To run the ETL process, execute `ETL.py` after ensuring all dependencies (such as pandas, SQLAlchemy, and pyodbc) are installed. After, execute `reports.py` to generate the reports.
