import pandas as pd

from common_utilities.utilities import *
'''
#oracle_conn = create_engine(URL.create(f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"))
# Oracle connection
oracle_url = URL.create(
    drivername="oracle+oracledb",
    username=ORACLE_USER,
    password=ORACLE_PASSWORD,
    host=ORACLE_HOST,
    port=int(ORACLE_PORT),
    query={"service_name": ORACLE_SERVICE}
)
oracle_conn = create_engine(oracle_url, pool_pre_ping=True)
print("Oracle engine created successfully")

# My SQL connection
mysql_url = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=int(MYSQL_PORT),
    database=MYSQL_DATABASE
)

mysql_conn = create_engine(
    mysql_url,
    pool_pre_ping=True
)

print("MySQL engine created successfully")
'''
class DataExtraction:
    def extract_read_product_data_and_write_to_staging(self, file_path, file_type, table_name):
        logger.info("Data extraction process started ......")
        read_from_file_to_sql(file_path, file_type, table_name)
       # df.to_sql(table_name, mysql_conn, index=False, if_exists="replace")
        logger.info("Data extraction process of Product file has completed... ")

    def extract_read_inventory_XML_data_and_write_to_staging(self, file_path, file_type, table_name):
        logger.info("Data extraction process started from Inventory data....")
        read_from_file_to_sql(file_path, file_type, table_name)
        logger.info("Data extraction process of Inventory data has completed... ")

    def extract_read_supplier_json_data_and_write_to_staging(self, file_path, file_type, table_name):
        logger.info("Data extraction process started from supplier_data....")
        read_from_file_to_sql(file_path, file_type, table_name)
        logger.info("Data extraction process of supplier_data has completed... ")
    '''
    def extract_read_sales_data_from_file_and_write_to_staging_mysql(self, bucket_name,file_key):
        print("Data extraction process started from Sales S3 data....")
        read_file_from_s3(bucket_name,file_key)
        print("Data extraction process of sales_data has completed... ")
   '''

    def extract_read_sales_data_and_write_to_staging_staging(self, file_path, file_type, table_name):
        logger.info("Data extraction process started from Sales data....")
        read_from_file_to_sql(file_path, file_type, table_name)
        logger.info("Data extraction process of sales_data has completed... ")

    def extract_read_stores_data_oracle_and_write_to_staging(self, file_path, file_type, table_name):
        logger.info("Data extraction process started from Stores oracle data....")
        read_from_oracle_to_sql(file_path, file_type, table_name)
        logger.info("Data extraction process of stores_data has completed... ")

de1=DataExtraction()
de1.extract_read_product_data_and_write_to_staging("Source_System/product_data.csv", "csv", "stage_product")
de1.extract_read_inventory_XML_data_and_write_to_staging("Source_System/inventory_data.xml", "xml", "stage_inventory")
de1.extract_read_supplier_json_data_and_write_to_staging("Source_System/supplier_data.json", "json", "stage_supplier")
de1.extract_read_stores_data_oracle_and_write_to_staging("Source_System/product_data.csv", "oracle", "stage_stores")
de1.extract_read_sales_data_and_write_to_staging_staging("Source_System/sales_data.csv", "csv", "stage_sales")

