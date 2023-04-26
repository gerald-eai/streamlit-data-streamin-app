import streamlit as st

DEV_STARTED= False

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
    st.title("Water Pollution Dashboard")
    
    if not DEV_STARTED: 
        under_construction_widget()