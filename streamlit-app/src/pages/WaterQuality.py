import streamlit as st 
from utils.LoadData import data_is_loaded

DEV_STARTED=True

# def data_is_loaded()-> bool: 
#     return 'water quality dataset' in st.session_state
def under_construction_widget():
    st.divider()
    vert_space = '<div style="padding: 20px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)
    main_container = st.container()
    # st.markdown("# Still Under Development :construction:")
    main_container.write("# Still Under Development :construction:")
    st.markdown(vert_space, unsafe_allow_html=True)
    st.divider()
    
if __name__ == "__main__": 
    st.title("Water Quality Dashboard")
    
    # provide an under construction view
    if not DEV_STARTED: 
        under_construction_widget()
    else: 
        if not data_is_loaded(): 
            st.markdown("### Please **upload** the data first")
        else:
            st.markdown("### Loaded Data dataframe")
            st.dataframe(st.session_state.water_quality_data)
            
        