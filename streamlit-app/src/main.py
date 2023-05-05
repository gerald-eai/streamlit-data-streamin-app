import streamlit as st 
from utils.LoadData import load_csv_data

if __name__ == '__main__':
    st.title("Streamlit App")
    # load the data as a user input/file
    water_pollution_data = load_csv_data('db/water_pollution.csv')
    st.markdown("## Water Pollution Dataset :test_tube:")
    st.dataframe(water_pollution_data)
    st.divider()
    water_quality_data = load_csv_data('db/water_quality_1.csv')
    st.markdown("## Water Quality Dataset :droplet:")
    st.dataframe(water_quality_data)
    # upload csv file streamlit
    st.markdown("## :arrow_up: Upload a Water Quality Dataset :droplet:")
    wq_csv = st.file_uploader("Upload a Water Quality Dataset", type=["csv"])
    st.markdown("## :arrow_up: Upload a Water Pollution Dataset :test_tube:")
    wp_csv = st.file_uploader("Upload a Water Pollution Dataset", type=["csv"])
    
    # todo: code is duplicated here, try unduplicate it
    if wq_csv is not None:
        # fix the data to our session state
        st.write(wq_csv)
        st.session_state['water quality dataset'] = load_csv_data(wq_csv)
    if wp_csv is not None:
        # fix the data to our session state
        st.write(wp_csv)
        st.session_state['water pollution dataset'] = load_csv_data(wp_csv)