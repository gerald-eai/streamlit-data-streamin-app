import streamlit as st 
import pandas as pd 
from pandas import DataFrame
import utils.RequestData as db_requests
import os 
from time import sleep



@st.cache_data
def load_csv_data(f_path: str) -> DataFrame:
    return pd.read_csv(f_path)

@st.cache_data
def get_user_data() -> dict: 
    user_data = db_requests.get_user_info()
    return user_data

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def user_is_captured() -> bool: 
    return 'user_info' in st.session_state

def data_is_loaded()-> bool: 
    return 'water quality dataset' in st.session_state 
    # or 'water pollution dataset' in st.session_state

def databricks_is_loaded()-> bool:
    return 'tank sre df' in st.session_state 

@st.cache_data
def load_databricks_df() -> DataFrame:
    """
        Generates data from a fixed dataset
    """
    # run a job on the Notebook 
    run_id = db_requests.run_single_job()
    sleep(5)
    # Get the last run id from the notebook
    my_df = db_requests.get_last_run_output(run_id)
    return my_df 

# demo data 
@st.cache_data
def read_from_txt_data(): 
    dir = os.getcwd() + ""
    print(f"Current working directory: {dir} ")
    data = None 
    with open('./db/dpsn_wq_tank_sre_dummy.txt') as f: 
        data = f.read()
        # print(f"contents: {contents}")
    dataframe = db_requests.convert_to_df(data)
    print(f"dataframe: {dataframe}")
    # dataframe['sampled_date'] = pd.to_datetime(dataframe['sampled_date'], format="%m/%d/%Y, %H:%M:%S")
    dataframe['sampled_date']= pd.to_datetime(dataframe['sampled_date'], format="%Y-%m-%dT%H:%M:%S.%fZ", utc=True)

    return dataframe


    

if __name__ == '__main__': 
    read_from_txt_data()
    
    
    
    