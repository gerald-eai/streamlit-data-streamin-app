# Databricks Overview Page for testing the API 

import streamlit as st 
# from utils.LoadData import get_user_data, user_is_captured, databricks_is_loaded
import utils.LoadData as data_loader

def under_construction_widget():
    st.divider()
    vert_space = '<div style="padding: 20px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)
    main_container = st.container()
    # st.markdown("# Still Under Development :construction:")
    main_container.write("# Still Under Development :construction:")
    st.markdown(vert_space, unsafe_allow_html=True)
    st.divider()

def clear_df_data(): 
    if data_loader.databricks_is_loaded(): 
        del st.session_state['tank sre df']
    
if __name__ == "__main__": 
    st.title("DataBricks Overview")
    # check if the user is loaded, else load user data 
    if not data_loader.user_is_captured(): 
        st.session_state['user_info'] = data_loader.get_user_data()
    
    if not data_loader.databricks_is_loaded(): 
        # have button asking user to request the data 
        button_result = st.button('Request Tank SRE Data')
        st.caption("Press the button to request data from Databricks.")
        
        if button_result:
            # load the data
            st.session_state['tank sre df'] = data_loader.load_databricks_df()
            st.success("Success loading data from Databricks")
            st.dataframe(st.session_state['tank sre df'])
            
    if data_loader.databricks_is_loaded(): 
        delete_data_button = st.button('Clear Session State Data', on_click=clear_df_data)
        if delete_data_button: 
            button_result = st.button('Request Tank SRE Data')
            st.caption("Press the button to request data from Databricks.")
        else: 
            st.dataframe(st.session_state['tank sre df'])
            csv = data_loader.convert_df(st.session_state['tank sre df'])

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='tank_sre_df.csv',
                mime='text/csv',
            )
    # else: 
    st.write(st.session_state['user_info'])
    