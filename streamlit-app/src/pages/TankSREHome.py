#:TODO: implement a streamlit page that will act as a mock dashboard from table dpsn_wq.tank_sre_cl_res 
import streamlit as st 
import utils.LoadData as data_loader
import altair as alt 
import pandas as pd 
import numpy as np
import time 
# import matplotlib.pyplot as plt 

@st.cache_data
def load_df(): 
    st.session_state['tank sre df'] = data_loader.load_databricks_df()
    
def init_page(): 
    print("Init the Tank SRE Dashboard Page")
    # load the user information into the state
    # st.session_state['user_info'] = data_loader.get_user_data()
    st.session_state['fake tank sre df'] = data_loader.read_from_txt_data()

def calc_avg_value(dataframe): 
    avg_value = dataframe['value'].mean()
    print(avg_value)
    return avg_value

def calc_top_group_id(dataframe):
    top_group = dataframe['group_id'].mode()
    print("Top Group: ",str(top_group[0]))
    return str(top_group[0])

def get_value_by_date_chart(dataframe): 
    # TODO: implement this
    hover = alt.selection_single(
        fields=["sampled_date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    
    lines = (
        alt.Chart(dataframe, title="WQ Value of Date")
        .mark_line()
        .encode(
            x="sampled_date",
            y="value",
        )
    )
    
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(dataframe)
        .mark_rule()
        .encode(
            x="sampled_date",
            y="value",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("sampled_date", title="Date Sampled"),
                alt.Tooltip("value", title="WQ Value (mg/l)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()
    
    # pass

def group_id_pie_chart(dataframe): 
    unique_data = dataframe['group_id'].value_counts()
    group_ids = dataframe['group_id'].unique()
    source_data = pd.DataFrame(columns=['GroupID', 'Count'])
    total = unique_data.sum()

    for id_ in group_ids: 
        tmp_df = pd.DataFrame({"GroupID":[id_], "CountPercentage":[round(100.0*(unique_data[id_]/total),4)]})
        source_data = source_data.append(tmp_df, ignore_index=True)

    fig_category_percent=alt.Chart(source_data).mark_arc().encode(
        theta=alt.Theta(field="CountPercentage", type="quantitative"),
        color=alt.Color(field="GroupID", type="nominal"))
    
    return fig_category_percent
    
def plot_value_by_group_id(dataframe): 
    chart = alt.Chart(dataframe).mark_circle().encode(
        x='sampled_date',
        y='value',
        color='group_id',
        ).interactive()

    # tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
    return chart 

def clear_df_data(): 
    if data_loader.databricks_is_loaded(): 
        del st.session_state['tank sre df']
        
def display_dashboard(): 
    #########################
        """ Show the Dataframe data"""
        st.dataframe(st.session_state['tank sre df'], use_container_width=True)
        
        csv = data_loader.convert_df(st.session_state['tank sre df'])
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='tank_sre_df.csv',
            mime='text/csv',
        )
        st.divider()        
        #########################
        """ Show averages of the Tank Data """
        
        # show breakdown of the 
        col1, col2 = st.columns(2)
        avg_value = calc_avg_value(st.session_state['tank sre df'])
        top_group_id = calc_top_group_id(st.session_state['tank sre df'])    
        col1.metric("Average Water Value", f"{str(round(avg_value,3))} mg/l")
        col2.metric("Most Frequent Group ID", f"{top_group_id}")
        
        #########################
        """ Display an interactive chart of the values over a time interval """
        value_chart = get_value_by_date_chart(st.session_state['tank sre df'])
        st.altair_chart(value_chart, use_container_width=True)
        
        ################
        """Display interactive chart of sampled values based on group ID"""
        circle_chart = plot_value_by_group_id(st.session_state['tank sre df'])
        st.altair_chart(circle_chart, use_container_width=True, theme="streamlit")
        
        ################
        """Display a pie chart of the group id"""
        fig_category_percent = group_id_pie_chart(st.session_state['tank sre df'])
        st.altair_chart(fig_category_percent)
        
if __name__ == "__main__":
    init_page() # initialise data required for the page
    st.title("Tank SRE Dashboard")
    st.markdown("Showcase some of the KPIs that are responsible for the Tank SRE Table found in dpsn_wq")
    data_loaded = data_loader.databricks_is_loaded()
    if not data_loaded: 
        # have button asking user to request the data 
        button_result = st.button('Request Tank SRE Data')
        st.caption("Press the button to request data from Databricks.")
        
        if button_result:
            # load the data
            # st.session_state['tank sre df'] = data_loader.load_databricks_df()
            st.session_state['tank sre df'] = data_loader.load_databricks_df()
            # st.success("Success loading data from Databricks")
            st.success("Success loading data from Databricks")
            # time.sleep(5)
            if st.session_state['tank sre df'] is not None:
                clear_data = st.button("Clear the Data from Databricks")   
                st.caption("Press the button to clear the data from Databricks.")   
                if clear_data: 
                    # st.experimental_rerun()
                    clear_df_data()
                else: 
                    display_dashboard()
                
            # display_dashboard()
            # st.dataframe(st.session_state['tank sre df'])
            # continue 
    # else: 
    #     clear_data = st.button("Clear the Data from Databricks")   
    #     st.caption("Press the button to clear the data from Databricks.")  
    #     if clear_data: 
    #         clear_df_data()
    #         st.success("Clear the data from Databricks")
    #         button_result = st.button('Request Tank SRE Data', on_click=load_df)
    #         st.caption("Press the button to request data from Databricks.")
    #         time.sleep(8)
    #         if st.session_state['tank sre df'] is not None: 
    #             display_dashboard()
    #     else:
    #         display_dashboard()
    
    
    
    

