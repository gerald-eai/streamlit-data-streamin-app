from databricks import sql 
import os 

databricks_instance = str(os.getenv("AZ_DB_INSTANCE"))
databricks_token = str(os.getenv("AZ_DB_TOKEN"))
databricks_cluster_id = str(os.getenv("AZ_DB_CLUSTER_ID"))
databricks_notebook_path = str(os.getenv("AZ_DB_NOTEBOOK_PATH"))
databricks_http_path = str(os.getenv("AZ_CLUSTER_HTTP_PATH"))


def main(): 
    with sql.connect(server_hostname=databricks_instance, 
                     access_token=databricks_token, 
                     http_path=databricks_http_path) as connection:
        with connection.cursor() as cursor:
            # cursor.execute("SHOW DATABASES")
            # cursor.execute("SELECT * FROM dpsn_wq.tank_sre_last_cl_res")
            cursor.columns(schema_name="dpsn_wq", table_name="tank_sre_last_cl_res")
            rows = cursor.fetchall()
            print(rows)
            
if __name__ == "__main__":
    print('Try out SQL Connector')
    main()
    
    