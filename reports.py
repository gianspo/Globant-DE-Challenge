import pandas as pd
from sqlalchemy import create_engine
import urllib

# DB Config
db_config = {
    'Server': 'LAPTOP-4IKA5I7P',
    'Database': 'DE_GLOBANT',
    'Trusted_Connection': 'yes'
}

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    rf'SERVER={db_config["Server"]};'
    rf'DATABASE={db_config["Database"]};'
    rf'Trusted_Connection={db_config["Trusted_Connection"]};'
)

quoted_conn_str = urllib.parse.quote_plus(conn_str)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted_conn_str))

def hired_employees_per_department(db_config):
    sql_query = """
            WITH DEPARTMENT_BY_Q AS (
            SELECT 
            department_id, 
            job_id, 
            CONCAT('Q',DATEPART(QUARTER, datetime)) as Quarter, 
            COUNT(*) as count 
            FROM dim.hired_employees 
            WHERE year(datetime) = 2021  
            GROUP BY  department_id, job_id, concat('Q',DATEPART(QUARTER, datetime)) 
            )

            SELECT 
            D.DEPARTMENT, 
            J.JOB,
            SUM(CASE WHEN Quarter='Q1' THEN COUNT ELSE 0 END) as Q1,
            SUM(CASE WHEN Quarter='Q2' THEN COUNT ELSE 0 END) as Q2,
            SUM(CASE WHEN Quarter='Q3' THEN COUNT ELSE 0 END) as Q3,
            SUM(CASE WHEN Quarter='Q4' THEN COUNT ELSE 0 END) as Q4 
            FROM DEPARTMENT_BY_Q A 
            INNER JOIN dim.jobs J 
            ON J.id = A.job_id 
            INNER JOIN dim.departments D 
            ON D.id = A.department_id 
            GROUP BY D.department, J.job 
            ORDER BY D.department ASC, J.job ASC"""
    result_df = pd.read_sql_query(sql_query, engine)
    result_df.to_sql('hired_employees_per_department', engine, if_exists='replace', index=False, schema='rep')

    return result_df

summary_df = hired_employees_per_department(db_config)

print(summary_df)

def top_hiring_departments(db_config):
    sql_query = """
            WITH HIRED_COUNT AS (
            SELECT department_id,  count(*) as HIRED 
            FROM dim.hired_employees  
            WHERE YEAR(datetime) = 2021  
            GROUP BY department_id),
            HIRED_MEAN AS (
            SELECT AVG(HIRED) as MEAN 
            FROM HIRED_COUNT )
            SELECT H.department_id as ID, D.department as DEPARTMENT, H.HIRED
            FROM HIRED_COUNT H
            INNER JOIN dim.departments D 
            ON D.id = H.department_id 
            INNER JOIN HIRED_MEAN M
            ON H.HIRED > M.MEAN
            ORDER BY H.HIRED DESC"""
    result_df = pd.read_sql_query(sql_query, engine)
    result_df.to_sql('top_hiring_departments', engine, if_exists='replace', index=False, schema='rep')

    return result_df

summary_df = top_hiring_departments(db_config)

print(summary_df)