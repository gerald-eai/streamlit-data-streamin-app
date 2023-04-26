import streamlit as st 
import pandas as pd 
from pandas import DataFrame


@st.cache_data
def load_csv_data(f_path: str) -> DataFrame:
    return pd.read_csv(f_path)


def data_is_loaded()-> bool: 
    return 'water quality dataset' in st.session_state 
    # or 'water pollution dataset' in st.session_state