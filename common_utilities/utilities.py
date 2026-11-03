import pandas as pd

import oracledb
import pymysql
from sqlalchemy import create_engine, URL

from project_config.etlConfig import *
mysql_conn = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
# Oracle connection
oracle_url = URL.create(
    drivername="oracle+oracledb",
    username=ORACLE_USER,
    password=ORACLE_PASSWORD,
    host=ORACLE_HOST,
    port=int(ORACLE_PORT),
    query={"service_name": ORACLE_SERVICE}
)

def read_from_file_to_sql(file_path, file_type, table_name):
    file_type = file_type.strip().lower()
    if file_type == "csv":
        df= pd.read_csv(file_path)
    elif file_type == "json":
        df= pd.read_json(file_path)
    elif file_type == "xml":
        df= pd.read_xml(file_path, xpath=".//item")
    else :
        raise ValueError(f"{file_type} is not supported.")
    #return df
    df.to_sql(table_name, con=mysql_conn, if_exists='replace', index=False)
    print(f"{file_type} File Data has been moved to staging ....")

def read_from_oracle_to_sql(file_path, file_type, table_name):
    oracle_conn = create_engine(oracle_url, pool_pre_ping=True)
    print("Oracle engine created successfully")
    #file_type = file_type.strip().lower()
    oracle_query="""
    select * 
    from stores 
    """
    df = pd.read_sql(oracle_query, oracle_conn)
    df.to_sql(table_name, con=mysql_conn, if_exists='replace', index=False)
    print("Oracle Data has been moved to staging for Stores....")