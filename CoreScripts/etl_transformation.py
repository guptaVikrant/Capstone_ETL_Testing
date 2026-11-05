from common_utilities.utilities import *


class DataTransformation:
    def transform_filter_sales(self):
        logger.info("Data filter process started ...")
        filter_from_sales()
        logger.info("Data filter process finished")

    def transform_router_sales(self):
        logger.info("Data routing process started ...")
        router_region_based_sales()
        logger.info("Data routing process finished")

    def transform_aggregate_sales(self):
        logger.info("Data aggregate process for sales started ...")
        aggregate_sales()
        logger.info("Data aggregate process for sales finished ...")
    def transform_aggregate_inventory(self):
        logger.info("Data aggregate process for sales started ...")
        aggregate_inventory()
        logger.info("Data aggregate process for sales finished ...")
    def transform_joiner_sales(self):
        logger.info("Data joiner sales process started ...")
        join_sales()
        logger.info("Data joiner sales process finished ...")

dt1=DataTransformation()
dt1.transform_filter_sales()
dt1.transform_router_sales()
dt1.transform_aggregate_sales()
dt1.transform_joiner_sales()
dt1.transform_aggregate_inventory()