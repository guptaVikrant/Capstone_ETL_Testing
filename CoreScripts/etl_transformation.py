from common_utilities.utilities import *


class DataTransformation:
    def transform_filter_sales(self):
        print("Data filter process started ...")
        filter_from_sales()
        print("Data filter process finished")

    def transform_router_sales(self):
        print("Data routing process started ...")
        router_region_based_sales()
        print("Data routing process finished")

    def transform_aggregate_sales(self):
        print("Data aggregate process for sales started ...")
        aggregate_sales()
        print("Data aggregate process for sales finished ...")
    def transform_aggregate_inventory(self):
        print("Data aggregate process for sales started ...")
        aggregate_inventory()
        print("Data aggregate process for sales finished ...")
    def transform_joiner_sales(self):
        print("Data joiner sales process started ...")
        join_sales()
        print("Data joiner sales process finished ...")

dt1=DataTransformation()
dt1.transform_filter_sales()
dt1.transform_router_sales()
dt1.transform_aggregate_sales()
dt1.transform_joiner_sales()
dt1.transform_aggregate_inventory()