from io import StringIO
from project_config.etlConfig import *
#import boto3
import pandas as pd
import oracledb
import pymysql
from sqlalchemy import create_engine, URL, text
import logging

# loger configuration
logging.basicConfig(
    filename='application_log/etl_process.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initiate a session with s3
#s3 = boto3.client('s3')

# -------------------------Query for transformation-------------------------------

filter_query = """select * from stage_sales where sale_date>01-09-2026"""
router1_query="""select * from stage_sales where region='high'"""
router2_query="""select * from stage_sales where region='low'"""
aggr_query="""select product_id, year(sale_date) as SalesYear, month(sale_date) as SalesMonth, 
                sum(quantity*price) as Total_Sales from filtered_sales group by product_id, year(sale_date), month(sale_date)"""
joiner_query="""select  fs.sales_id,fs.quantity,fs.price,fs.quantity * fs.price as sales_amount,fs.sale_date,
                sp.product_id,sp.product_name, ss.store_id,ss.store_name 
                from filtered_sales fs inner join stage_product sp on fs.product_id=sp.product_id 
                inner join stage_stores ss on fs.store_id=ss.store_id"""
inventory_aggr_query="""select store_id, sum(quantity_on_hand) as total_product from stage_inventory group by store_id """

# -------------------------Query for Loading--------------------------------

factSalesQuery=text("""INSERT INTO fact_sales (sales_id,product_id,store_id,quantity,total_sales, sale_date)
                  SELECT sales_id,product_id,store_id, quantity,sales_amount,STR_TO_DATE(sale_date, '%d-%m-%Y') 
                   FROM sales_with_details""")
factInventoryQuery=text("""insert into fact_inventory(product_id,  store_id, quantity_on_hand, last_updated)
select product_id,  store_id, quantity_on_hand, last_updated from stage_inventory""")
monthlySalesQuery=text("""insert into fact_inventory(product_id,  store_id, quantity_on_hand, last_updated)
select product_id,  store_id, quantity_on_hand, last_updated from stage_inventory""")
inventoryByStoreQuery=text("""insert into fact_inventory(product_id,  store_id, quantity_on_hand, last_updated)
select product_id,  store_id, quantity_on_hand, last_updated from stage_inventory""")
# -------------------------Loading--------------------------------
def loading_fact_sales():
    with mysql_conn.connect() as conn:
        logger.info(factSalesQuery)
        conn.execute(factSalesQuery)
        conn.commit()
    logger.info("table has been loaded successfully....")

def loading_monthly_sales_details():
    with mysql_conn.connect() as conn:
        logger.info(monthlySalesQuery)
        conn.execute(monthlySalesQuery)
        conn.commit()
    logger.info("table has been loaded successfully....")

def loading_inventory():
    with mysql_conn.connect() as conn:
        logger.info(factInventoryQuery)
        conn.execute(factInventoryQuery)
        conn.commit()
    logger.info("table has been loaded successfully....")

def loading_inventory_level_by_store():
    with mysql_conn.connect() as conn:
        logger.info(inventoryByStoreQuery)
        conn.execute(inventoryByStoreQuery)
        conn.commit()
    logger.info("table has been loaded successfully....")
# -------------------------Transformation--------------------------------
def filter_from_sales():
    df= pd.read_sql(filter_query, con=mysql_conn)
    df.to_sql("filtered_sales", con=mysql_conn, if_exists='replace', index=False)
    logger.info(f"Filtered table has been created successfully....")

def router_region_based_sales():
    df1= pd.read_sql(router1_query, con=mysql_conn)
    df1.to_sql("high_sales", con=mysql_conn, if_exists='replace', index=False)
    df2= pd.read_sql(router2_query, con=mysql_conn)
    df2.to_sql("low_sales", con=mysql_conn, if_exists='replace', index=False)
    logger.info(f"Routed tables have been created successfully....")

def aggregate_sales():
    df= pd.read_sql(aggr_query, con=mysql_conn)
    df.to_sql("monthly_sales_summary", con=mysql_conn, if_exists='replace', index=False)
    logger.info(f"Aggregated tables for sales have been created successfully....")

def join_sales():
    df= pd.read_sql(joiner_query, con=mysql_conn)
    df.to_sql("sales_with_details", con=mysql_conn, if_exists='replace', index=False)
    logger.info(f"Joined sales detail tables have been created successfully....")

def aggregate_inventory():
    df= pd.read_sql(inventory_aggr_query, con=mysql_conn)
    df.to_sql("inventory_level", con=mysql_conn, if_exists='replace', index=False)
    logger.info(f"Aggregated inventory levels have been created successfully....")

# MySql connection
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
# -------------------------Extraction--------------------------------
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
    logger.info(f"{file_type} File Data has been moved to staging ....")

def read_from_oracle_to_sql(file_path, file_type, table_name):
    oracle_conn = create_engine(oracle_url, pool_pre_ping=True)
    logger.info("Oracle engine created successfully")
    #file_type = file_type.strip().lower()
    oracle_query="""
    select * 
    from stores 
    """
    df = pd.read_sql(oracle_query, oracle_conn)
    df.to_sql(table_name, con=mysql_conn, if_exists='replace', index=False)
    logger.info("Oracle Data has been moved to staging for Stores....")

def read_file_from_s3(bucket_name,file_key):
# fetch the csv file from s3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    print("response is :", response)
    csv_content = response['Body'].read().decode('utf-8')
    data = StringIO(csv_content)
    df = pd.read_csv(data)
    #print("Data frame: ", df)
    return df
