from common_utilities.utilities import *
#from sqlalchemy import text

class DataLoader:
    def load_fact_sales_table(self):
        logger.info("Data loading fact_sales_table started ...")
        loading_fact_sales()
        logger.info("Data loading fact_sales_table completed ...")
    def load_fact_inventory_table(self):
        logger.info("Data loading fact_inventory_table started ...")
        loading_inventory()
        logger.info("Data loading fact_inventory_table completed ...")
    def load_inventory_levels_by_store_table(self):
        logger.info("Data loading inventory_levels_by_store_table started ...")
        loading_inventory_level_by_store()
        logger.info("Data loading inventory_levels_by_store_table completed ...")
    def load_monthly_sales_report_table(self):
        logger.info("Data loading monthly_sales_report table started ...")
        loading_monthly_sales_details()
        logger.info("Data loading monthly_sales_report table completed ...")

if __name__ == "__main__":
dl1 = DataLoader()
dl1.load_fact_sales_table()