import requests
from dotenv import load_dotenv
import os
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.clusters.api import ClusterApi
from databricks_cli.jobs.api import JobsApi
from databricks_cli.runs.api import RunsApi
from databricks_cli.workspace.api import WorkspaceApi
from time import time
from datetime import datetime
import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SparkSession
import json
import ast
from pandas import DataFrame

# init env variables
load_dotenv()

databricks_instance = "https://"+str(os.getenv("AZ_DB_INSTANCE"))
databricks_token = str(os.getenv("AZ_DB_TOKEN"))
databricks_cluster_id = str(os.getenv("AZ_DB_CLUSTER_ID"))
databricks_notebook_path = str(os.getenv("AZ_DB_NOTEBOOK_PATH"))

# def get_user_status(user):


def list_workspace_objects_sdk(workspace: str, api_client: ApiClient):
    # api_client = ApiClient(host=databricks_instance, token=databricks_token)
    workspace_api = WorkspaceApi(api_client)
    workspace_list_objs = workspace_api.list_objects(workspace)
    return workspace_list_objs


def gen_job_id(base: str) -> str:
    """_summary_
    Returns a custom id for the given job, based on a give date and time
    Args:
        base (str): _description_

    Returns:
        str: _description_
    """
    # get the current date time
    curr_time = datetime.now()      # in date time format
    ct_string = curr_time.strftime("%d%m%Y_%HH%MM%SS")
    # print(f"Current Time: {ct_string} \ntype:{type(ct_string)}")
    return base + ct_string


def run_single_job() -> str:
    """
        Run a single job in the specified Notebook and directory path 
        Returns the run id of the job 
    """
    timeout_seconds = 60
    # Run a Job with the desired notebook
    job_name = gen_job_id("ssdb_job_")
    task_key = gen_job_id("gen_tank_sre_df_")
    run_response = requests.post(f"{databricks_instance}api/2.0/jobs/runs/submit",
                                 headers={
                                     "Authorization": f"Bearer {databricks_token}"},
                                 json={
                                     "run_name": job_name,
                                     "tags": {"App": "SSDB App"},
                                     "timeout_seconds": timeout_seconds,
                                     "tasks": [
                                         {
                                             "task_key": task_key,
                                             "existing_cluster_id": databricks_cluster_id,
                                             "description": "Generate output for SSDB_Notebook_001 cell.",
                                             "notebook_task": {"notebook_path": databricks_notebook_path+"SSDB_Notebook_001",
                                                               "source": "WORKSPACE"},
                                             "timeout_seconds": timeout_seconds
                                         }
                                     ]
                                 })
    print(f"Run ID: {run_response.json()['run_id']}")
    return run_response.json()['run_id']
    # pass


def convert_to_df(data) -> DataFrame:
    """
        Convert the json data to a dataframe
    """
    empty_list = []
    dict_output = ast.literal_eval(data)
    # print(f"Number of dict output entries: {len(dict_output)}")

    for entry in dict_output:
        json_entry = json.loads(entry)
        empty_list.append(json_entry)

    # print(f"Length of entries: {len(empty_list)}")
    df = pd.DataFrame.from_dict(empty_list)
    return df


def get_user_info() -> dict:
    auth_response = requests.get(f"{databricks_instance}api/2.0/preview/scim/v2/Me",
                                 headers={"Authorization": f"Bearer {databricks_token}"})

    # print(auth_response.json())
    # get user details from the response
    user_info = {}
    user_info["username"] = auth_response.json()["userName"]
    user_info["user_id"] = auth_response.json()["id"]

    # print(user_info)
    return user_info


def get_last_run_output(run_id: str) -> DataFrame:
    """
        Returns a dataframe that was created with the last notebook run for SSDB_Notebook001

    """
    # get the id of the task that was run
    # print(f"Status Response: \n {status_response.json()}")

    # print(status_response.json()["state"]["life_cycle_state"])
    # print(status_response.json()["state"]["result_state"])")

    status_response = requests.get(f"{databricks_instance}api/2.0/jobs/runs/get-output",
                                   headers={
                                       "Authorization": f"Bearer {databricks_token}"},
                                   params={"run_id": run_id}) 
    
    while status_response.json()['metadata']["state"]["life_cycle_state"] not in {"TERMINATED", "SKIPPED", "INTERNAL_ERROR"}:
        status_response = requests.get(
            f"{databricks_instance}api/2.0/jobs/runs/get-output",
            headers={"Authorization": f"Bearer {databricks_token}"},
            params={"run_id": run_id}
        )
        # time.sleep(1)
        # time.

    
    print(status_response.json())
    if status_response.json()['metadata']["state"]["result_state"] == "SUCCESS":
        output = status_response.json()["notebook_output"]["result"]
    else:
        raise RuntimeError("Notebook execution failed")
    my_df = convert_to_df(output)
    return my_df


def get_notebook_id():
    """
        Get Notebook id based on the path and name of the notebook. 
        Returns the notebook id of the notebook. 

        Raises:
            ValueError: If no notebook is found at the given path. 

        Returns:
            str: notebook id of the notebook.
    """
    list_workspace_response = requests.get(f"{databricks_instance}api/2.0/workspace/list",
                                           headers={
                                               "Authorization": f"Bearer {databricks_token}"},
                                           params={"path": databricks_notebook_path})
    notebook_id = None
    for item in list_workspace_response.json()["objects"]:
        print(item)
        if item["object_type"] == "NOTEBOOK" and item["path"] == databricks_notebook_path+"SSDB_Notebook_001":
            notebook_id = item["object_id"]
            print(f"Object ID: {notebook_id}")
            break

    if notebook_id is None:
        raise ValueError(
            f"No notebook found at path {databricks_notebook_path}")

    return notebook_id


def main():
    # get user information based on the auth token
    get_user_info()
    # get notebook information
    nb_id = get_notebook_id()
    run_id = run_single_job()
    # Get the last run id from the notebook
    my_df = get_last_run_output(run_id)
    # print(f"My DF {type(my_df)} ")
    # print(f"DF Head {my_df.head()}")
    # print(f"My DF Schema {my_df.schema()}")


if __name__ == "__main__":
    print(f"Instance: {databricks_instance} \nToken: {databricks_token}")
    main()
    get_user_info()
