import streamlit as st
from .help_function import DatabaseHelper

def submit_type_of_application_form():
    st.title("Submit Type of Application Form")
    
    with st.form(key='type_of_application_form'):
        title = st.text_input("Title")
        description = st.text_area("Description")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            db_helper = DatabaseHelper()
            success, message = db_helper.insert_type_of_application(title, description)
            db_helper.close_connection()
            st.success(message) if success else st.error(message)

def submit_raw_water_source_form():
    st.title("Submit Raw Water Source Form")
    
    with st.form(key='raw_water_source_form'):
        idRawWaterSource = st.number_input("ID Raw Water Source", min_value=1)
        code = st.number_input("Code", min_value=1)
        RawWaterSource_name = st.text_input("Raw Water Source Name")
        availability_year_round = st.selectbox("Availability Year Round", [0, 1])
        total_abstraction = st.number_input("Total Abstraction", format="%.2f")
        
        Drawing_RawWater_PumpingStation = st.file_uploader("Upload Drawing Raw Water Pumping Station", type=["png", "jpg", "jpeg"])
        Drawing_Water_Transmission_Network = st.file_uploader("Upload Drawing Water Transmission Network", type=["png", "jpg", "jpeg"])
        Drawing_Water_Treatment_Plant = st.file_uploader("Upload Drawing Water Treatment Plant", type=["png", "jpg", "jpeg"])
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            db_helper = DatabaseHelper()
            success, message = db_helper.submit_raw_water_source_form(
                idRawWaterSource, code, RawWaterSource_name, 
                availability_year_round, total_abstraction,
                Drawing_RawWater_PumpingStation, Drawing_Water_Transmission_Network, 
                Drawing_Water_Treatment_Plant
            )
            db_helper.close_connection()
            st.success(message) if success else st.error(message)