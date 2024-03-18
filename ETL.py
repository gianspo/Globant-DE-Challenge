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

# SQLAlchemy Conection
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted_conn_str))

def csv_to_db(file_table_mapping, custom_headers=None, batch_size=1000):
    if custom_headers is None:
        custom_headers = {}

    # Iterar sobre los archivos y tablas
    for file_path, table_name in file_table_mapping:
        df = pd.read_csv(file_path)

        if table_name in custom_headers:
            headers = custom_headers[table_name]
            df.columns = headers

        # Dividir el DataFrame en lotes y cargarlos en la base de datos
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            batch_df.to_sql(table_name, engine, if_exists='append', index=False, schema='ing')

    return True

# CSV Paths
file_table_mapping = [
    (r'C:\Users\gians\Documents\DE-Challenge Globant\source\departments.csv', 'departments'),
    (r'C:\Users\gians\Documents\DE-Challenge Globant\source\hired_employees.csv', 'hired_employees'),
    (r'C:\Users\gians\Documents\DE-Challenge Globant\source\jobs.csv', 'jobs')
]

# Header Definition
custom_headers = {
    'departments': ['ID', 'Department'],  
    'hired_employees': ['ID', 'Name', 'Datetime', 'Department_id','Job_id'],  
    'jobs': ['ID', 'Job']  
}

# Load CSV to DB
csv_to_db(file_table_mapping, custom_headers)

# Load from ing to dim
def load_ing_to_dim_departments(db_config):
    sql_query = """ SELECT DISTINCT * FROM ing.departments """
    result_df = pd.read_sql_query(sql_query, engine)
    result_df.to_sql('departments', engine, if_exists='replace', index=False, schema='dim')
    return result_df

load_ing_to_dim_departments(db_config)

def load_ing_to_dim_hired_employees(db_config):
    sql_query = """ SELECT DISTINCT * FROM ing.hired_employees """
    result_df = pd.read_sql_query(sql_query, engine)
    result_df.to_sql('hired_employees', engine, if_exists='replace', index=False, schema='dim')
    return result_df

load_ing_to_dim_hired_employees(db_config)

def load_ing_to_dim_jobs(db_config):
    sql_query = """ SELECT DISTINCT * FROM ing.JOBS """
    result_df = pd.read_sql_query(sql_query, engine)
    result_df.to_sql('jobs', engine, if_exists='replace', index=False, schema='dim')
    return result_df

load_ing_to_dim_jobs(db_config)



