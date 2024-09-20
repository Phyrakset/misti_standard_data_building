import streamlit as st
from .help_function import DatabaseHelper

def submit_type_of_application_form():
    st.title("Submit Type of Application")
    
    with st.form(key='type_of_application_form'):
        title = st.text_input("Title", placeholder="Enter the application title")
        description = st.text_area("Description", placeholder="Enter the description (optional)")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            db_helper = DatabaseHelper()
            success, message, type_of_application_id = db_helper.insert_type_of_application(title, description)
            db_helper.close_connection()

            if success:
                st.success(message)
                st.write(f"TypeOfApplicationID: {type_of_application_id}")
            else:
                st.error(message)
def submit_raw_water_source_form():
    # st.title("Submit Raw Water Source Form")
    
    with st.form(key='raw_water_source_form'):
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
            success, message = db_helper.submit_raw_water_source_form( code, RawWaterSource_name, 
                availability_year_round, total_abstraction,
                Drawing_RawWater_PumpingStation, Drawing_Water_Transmission_Network, 
                Drawing_Water_Treatment_Plant
            )
            db_helper.close_connection()
            st.success(message) if success else st.error(message)

def submit_for_of_oficial_user_only_form():
    st.title("Submit Official User Data Form")
    
    with st.form(key='for_of_oficial_user_only_form'):
        safety_mark_number = st.text_input("Safety Mark Number")
        officer_number = st.text_input("Officer Number")
        applicantid = st.number_input("Applicant ID", min_value=1, step=1)
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            db_helper = DatabaseHelper()
            success, message = db_helper.insert_for_of_oficial_user_only(safety_mark_number, officer_number, applicantid)
            db_helper.close_connection()
            st.success(message) if success else st.error(message)

def submit_company_form():
    st.title("Submit Company Form")
    
    # Initialize database helper
    db_helper = DatabaseHelper()
    
    # Fetch the TypeOfApplicationID and Titles for dropdown
    type_of_application_data = db_helper.fetch_data('type_of_application', ['TypeOfApplicationID', 'Title'])
    db_helper.close_connection()
    
    # Prepare the dropdown options (ID and Title)
    if type_of_application_data:
        type_of_application_options = {str(row[1]): row[0] for row in type_of_application_data}  # {Title: TypeOfApplicationID}
    else:
        st.error("No type of applications found.")
        return
    
    with st.form(key='company_form'):
        name = st.text_input("Company Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        phone = st.text_input("Phone")
        location_plan = st.file_uploader("Upload Location Plan", type=["png", "jpg", "jpeg", "pdf"])

        # Dropdown or Autocomplete for TypeOfApplicationID
        selected_title = st.selectbox("Select Type of Application", options=list(type_of_application_options.keys()))
        type_of_application_id = type_of_application_options[selected_title]  # Map back to the ID

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            db_helper = DatabaseHelper()
            success, message, CompanyID = db_helper.insert_company(name, email, address, phone, location_plan, type_of_application_id)
            db_helper.close_connection()
            if success:
                st.success(message)
                st.write(f"Company ID: {CompanyID}")
            else:
                st.error(message)

def submit_company_signature_form():

    db_helper = DatabaseHelper()
    
    # Fetch company list for the dropdown
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    company_options = {company[0]: company[1] for company in company_list}
    
    with st.form(key='company_signature_form'):
        name = st.text_input("Name", placeholder="Enter the name")
        date = st.date_input("Date")
        position = st.text_input("Position", placeholder="Enter the position")
        
        # Upload SignatureOrFingerprint and Stamp as files
        signature = st.file_uploader("Upload Signature or Fingerprint", type=["png", "jpg", "jpeg"])
        stamp = st.file_uploader("Upload Stamp", type=["png", "jpg", "jpeg"])
        
        # Dropdown for selecting the company
        company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Read the file content for signature and stamp (if provided)
            signature_content = signature.read() if signature else None
            stamp_content = stamp.read() if stamp else None
            
            success, message, company_signature_id = db_helper.insert_company_signature(
                name, date, position, signature_content, stamp_content, company_id
            )
            db_helper.close_connection()

            if success:
                st.success(message)
                st.write(f"CompanySignatureID: {company_signature_id}")
            else:
                st.error(message)