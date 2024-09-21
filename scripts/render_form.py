import streamlit as st
from .help_function import DatabaseHelper
from datetime import datetime

def submit_form(table_name, columns, form_inputs, return_id=True):
    """
    Generalized form submission handler.
    
    :param table_name: The name of the table to insert data into.
    :param columns: List of column names corresponding to the form inputs.
    :param form_inputs: List of form inputs (user input data) corresponding to the columns.
    :param return_id: Whether or not to return the last inserted ID.
    :return: Success message or error message after form submission.
    """
    db_helper = DatabaseHelper()
    success, message, inserted_id = db_helper.insert_record(table_name, columns, form_inputs, return_id=return_id)
    db_helper.close_connection()
    
    if success:
        st.success(message)
        if return_id:
            st.write(f"Inserted ID: {inserted_id}")
    else:
        st.error(message)

def submit_type_of_application_form():
    st.title("Submit Type of Application")
    
    with st.form(key='type_of_application_form'):
        title = st.text_input("Title", placeholder="Enter the application title")
        description = st.text_area("Description", placeholder="Enter the description (optional)")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            submit_form(
                table_name='type_of_application', 
                columns=['Title', 'Description'], 
                form_inputs=[title, description]
            )

def submit_raw_water_source_form():
    st.title("Submit Raw Water Source Form")
    
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
            form_inputs = [
                code, RawWaterSource_name, int(availability_year_round), total_abstraction,
                Drawing_RawWater_PumpingStation.read() if Drawing_RawWater_PumpingStation else None,
                Drawing_Water_Transmission_Network.read() if Drawing_Water_Transmission_Network else None,
                Drawing_Water_Treatment_Plant.read() if Drawing_Water_Treatment_Plant else None
            ]
            submit_form(
                table_name='raw_watersource',
                columns=[
                    'code', 'RawWaterSource_name', 'availability_year_round', 'total_abstraction',
                    'Drawing_RawWater_PumpingStation', 'Drawing_Water_Transmission_Network', 'Drawing_Water_Treatment_Plant'
                ],
                form_inputs=form_inputs,
                # return_id=False  # No auto-increment ID to return
            )

def submit_for_of_oficial_user_only_form():
    st.title("Submit Official User Data Form")
    
    with st.form(key='for_of_oficial_user_only_form'):
        safety_mark_number = st.text_input("Safety Mark Number")
        officer_number = st.text_input("Officer Number")
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            submit_form(
                table_name='for_of_oficial_user_only',
                columns=['SafetyMarkNumber', 'OfficerNumber'],
                form_inputs=[safety_mark_number, officer_number]
            )

def submit_company_form():
    st.title("Submit Company Form")
    
    db_helper = DatabaseHelper()
    type_of_application_data = db_helper.fetch_data('type_of_application', ['TypeOfApplicationID', 'Title'])
    db_helper.close_connection()
    
    if type_of_application_data:
        type_of_application_options = {str(row[1]): row[0] for row in type_of_application_data}
    else:
        st.error("No type of applications found.")
        return
    
    with st.form(key='company_form'):
        name = st.text_input("Company Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        phone = st.text_input("Phone")
        location_plan = st.file_uploader("Upload Location Plan", type=["png", "jpg", "jpeg", "pdf"])
        selected_title = st.selectbox("Select Type of Application", options=list(type_of_application_options.keys()))
        type_of_application_id = type_of_application_options[selected_title]
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [name, email, address, phone, location_plan.read() if location_plan else None, type_of_application_id]
            submit_form(
                table_name='company',
                columns=['Name', 'Email', 'Address', 'Phone', 'LocationPlan', 'TypeOfApplicationID'],
                form_inputs=form_inputs
            )

def submit_company_signature_form():
    st.title("Submit Company Signature Form")
    
    db_helper = DatabaseHelper()
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    db_helper.close_connection()
    
    company_options = {company[0]: company[1] for company in company_list}
    
    with st.form(key='company_signature_form'):
        name = st.text_input("Name", placeholder="Enter the name")
        date = st.date_input("Date")
        position = st.text_input("Position", placeholder="Enter the position")
        signature = st.file_uploader("Upload Signature or Fingerprint", type=["png", "jpg", "jpeg"])
        stamp = st.file_uploader("Upload Stamp", type=["png", "jpg", "jpeg"])
        company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [name, date, position, signature.read() if signature else None, stamp.read() if stamp else None, company_id]
            submit_form(
                table_name='company_signatur_and_stamp',
                columns=['Name', 'Date', 'Position', 'SignatureOrFingerprint', 'Stamp', 'CompanyID'],
                form_inputs=form_inputs
            )

def submit_applicant_form():
    st.title("Submit Applicant Form")
    
    db_helper = DatabaseHelper()
    
    # Fetch necessary data for dropdowns
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    type_of_application_data = db_helper.fetch_data('type_of_application', ['TypeOfApplicationID', 'Title'])
    for_official_user_data = db_helper.fetch_data('for_of_oficial_user_only', ['ForOfficialUserOnlyID', 'SafetyMarkNumber'])

    db_helper.close_connection()
    
    # Prepare dropdown options

    company_options = {company[1]: company[0] for company in company_list}
    type_of_application_options = {row[1]: row[0] for row in type_of_application_data}
    official_user_options = {row[1]: row[0] for row in for_official_user_data}  # Ensure ID is selected

    with st.form(key='applicant_form'):
        application_date = st.date_input("Application Date")
        local_rep_name = st.text_input("Local Representative Name")
        local_rep_position = st.text_input("Local Representative Position")
        local_rep_email = st.text_input("Local Representative Email")
        local_rep_phone = st.text_input("Local Representative Phone")
        local_rep_address = st.text_input("Local Representative Address")
        local_rep_company_name = st.text_input("Local Representative Company Name")
        
        # Dropdowns for selecting IDs
        # Selecting company - displaying names, but passing the corresponding ID
        selected_company_name = st.selectbox("Select Company", options=list(company_options.keys()))
        selected_company_id = company_options[selected_company_name]  # Fetch corresponding company ID

        # Selecting type of application - displaying titles, but passing the corresponding ID
        selected_type_of_application_title = st.selectbox("Select Type of Application", options=list(type_of_application_options.keys()))
        type_of_application_id = type_of_application_options[selected_type_of_application_title]  # Fetch corresponding type of application ID

        # Selecting official user - displaying user names, but passing the corresponding ID
        selected_official_user_name = st.selectbox("Select Official User", options=list(official_user_options.keys()))
        selected_official_user_id = official_user_options[selected_official_user_name]  # Fetch corresponding official user ID



        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [application_date, local_rep_name, local_rep_position, local_rep_email, local_rep_phone, local_rep_address,local_rep_company_name,
                           selected_company_id,type_of_application_id,selected_official_user_id]
            submit_form(
                table_name='applicant',
                columns=['Applicationdate', 'LocalRepresentativeName', 'LocalRepresentativePosition', 'LocalRepresentativeEmail',
                 'LocalRepresentativePhone', 'LocalRepresentativeAddress', 'LocalRepresentativeCompanyName',
                 'ForOfficialUserOnlyID','TypeOfApplicationID', 'CompanyID'],
                form_inputs=form_inputs
            )

def submit_personal_info_form():
    st.title("Submit Personal Information for Applicant")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}

    with st.form(key='personal_info_form'):
        khmer_name = st.text_input("Khmer Name")
        latin_name = st.text_input("Latin Name")
        date_of_birth = st.date_input("Date of Birth")
        ethnicity = st.text_input("Ethnicity")
        nationality = st.text_input("Nationality")
        current_occupation = st.text_input("Current Occupation")
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        
        # Dropdown for selecting Applicant ID
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                khmer_name, latin_name, date_of_birth, ethnicity, 
                nationality, current_occupation, gender, selected_applicant_id
            ]
            submit_form(
                table_name='personal_infor_for_applicant',
                columns=[
                    'KhmerName', 'LatinName', 'DateOfBirth', 
                    'Ethnicity', 'Nationality', 'CurrentOccupation', 
                    'Gender', 'ApplicantID'
                ],
                form_inputs=form_inputs
            )  

def submit_id_card_or_passport_form():
    st.title("Submit ID Card or Passport Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID', 'KhmerName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    personal_info_options = {row[0]: row[1] for row in personal_info_data}

    with st.form(key='id_card_passport_form'):
        id_card_or_passport_number = st.text_input("ID Card or Passport Number")
        issued_date = st.date_input("Issued Date")
        expiration_date = st.date_input("Expiration Date")
        
        # Dropdown for selecting Personal Information ID
        selected_personal_info_id = st.selectbox("Select Personal Information", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                id_card_or_passport_number, issued_date, expiration_date, selected_personal_info_id
            ]
            submit_form(
                table_name='idcardorpaassport',
                columns=[
                    'IDCardOrPassportNumber', 'IssuedDate', 'ExpirationDate', 
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_address_form():
    st.title("Submit Address Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID', 'KhmerName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    personal_info_options = {row[0]: row[1] for row in personal_info_data}

    with st.form(key='address_form'):
        house_number = st.text_input("House Number")
        street = st.text_input("Street")
        village = st.text_input("Village")
        commune = st.text_input("Commune")
        district = st.text_input("District")
        province = st.text_input("Province")
        office_address = st.text_input("Office Address")
        currently_location = st.text_input("Currently Location")
        
        # Dropdown for selecting Personal Information ID
        selected_personal_info_id = st.selectbox("Select Personal Information", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                house_number, street, village, commune, district, 
                province, office_address, currently_location, selected_personal_info_id
            ]
            submit_form(
                table_name='address',
                columns=[
                    'HouseNumber', 'Street', 'Village', 'Commune', 
                    'District', 'Province', 'OfficeAddress', 
                    'Currently_location', 'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_human_resources_form():
    st.title("Submit Human Resources Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    raw_water_sources = db_helper.fetch_data('raw_watersource', ['idRawWaterSource', 'RawWaterSource_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    raw_water_options = {row[0]: row[1] for row in raw_water_sources}

    with st.form(key='human_resources_form'):
        code = st.number_input("Code", min_value=0, step=1)
        human_resources_name = st.text_input("Human Resources Name")
        total_staff = st.number_input("Total Staff", min_value=0, step=1)
        staff_per_1000_subscribers = st.number_input("Staff per 1000 Subscribers", format="%.2f")
        training_sessions = st.number_input("Training Sessions", min_value=0, step=1)
        organization_chart = st.file_uploader("Upload Organization Chart", type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"])

        # Dropdowns for selecting foreign key IDs
        selected_raw_water_source_id = st.selectbox("Select Raw Water Source", options=list(raw_water_options.keys()), format_func=lambda x: raw_water_options[x])
    
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            # Handle the uploaded file (blob)
            if organization_chart is not None:
                organization_chart_blob = organization_chart.read()
            else:
                organization_chart_blob = None
            
            form_inputs = [
                code, human_resources_name, total_staff, staff_per_1000_subscribers,
                training_sessions, organization_chart_blob, 
                selected_raw_water_source_id
            ]
            submit_form(
                table_name='human_resources',
                columns=[
                    'code', 'Humanresources_name', 'total_staff', 'staff_per_1000_subscribers', 
                    'training_sessions', 'organization_chart', 
                    'idRawWaterSource'
                ],
                form_inputs=form_inputs
            )

def submit_treatment_plant_form():
    st.title("Submit Treatment Plant Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    raw_water_sources = db_helper.fetch_data('raw_watersource', ['idRawWaterSource', 'RawWaterSource_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    raw_water_options = {row[0]: row[1] for row in raw_water_sources}

    with st.form(key='treatment_plant_form'):
        code = st.number_input("Code", min_value=0, step=1)
        treatment_plant_name = st.text_input("Treatment Plant Name")
        treatment_losses = st.number_input("Treatment Losses", format="%.2f")
        pac_consumption = st.number_input("PAC Consumption", format="%.2f")
        pac_per_m3_produced = st.number_input("PAC per m³ Produced", format="%.2f")
        alum_consumption = st.number_input("Alum Consumption", format="%.2f")
        alum_per_m3_produced = st.number_input("Alum per m³ Produced", format="%.2f")
        chlorine_consumption = st.number_input("Chlorine Consumption", format="%.2f")
        chlorine_per_m3_produced = st.number_input("Chlorine per m³ Produced", format="%.2f")
        electricity_consumption = st.number_input("Electricity Consumption", format="%.2f")
        electricity_per_m3_produced = st.number_input("Electricity per m³ Produced", format="%.2f")
        lime_consumption = st.number_input("Lime Consumption", format="%.2f")
        lime_per_m3_produced = st.number_input("Lime per m³ Produced", format="%.2f")
        fuel_consumption = st.number_input("Fuel Consumption", format="%.2f")
        fuel_per_m3_produced = st.number_input("Fuel per m³ Produced", format="%.2f")
        production_capacity = st.number_input("Production Capacity", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_raw_water_source_id = st.selectbox("Select Raw Water Source", options=list(raw_water_options.keys()), format_func=lambda x: raw_water_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                code, treatment_plant_name, treatment_losses, pac_consumption,
                pac_per_m3_produced, alum_consumption, alum_per_m3_produced,
                chlorine_consumption, chlorine_per_m3_produced, electricity_consumption,
                electricity_per_m3_produced, lime_consumption, lime_per_m3_produced,
                fuel_consumption, fuel_per_m3_produced, production_capacity,
                selected_raw_water_source_id
            ]
            submit_form(
                table_name='treatment_plant',
                columns=[
                    'code', 'TreatmentPlant_name', 'treatment_losses', 'pac_consumption',
                    'pac_per_m3_produced', 'alum_consumption', 'alum_per_m3_produced',
                    'chlorine_consumption', 'chlorine_per_m3_produced', 'electricity_consumption',
                    'electricity_per_m3_produced', 'lime_consumption', 'lime_per_m3_produced',
                    'fuel_consumption', 'fuel_per_m3_produced', 'production_capacity',
                    'idRawWaterSource'
                ],
                form_inputs=form_inputs
            )

def submit_water_quality_form():
    st.title("Submit Water Quality Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    treatment_plants = db_helper.fetch_data('treatment_plant', ['idTreatmentPlant', 'TreatmentPlant_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    treatment_plant_options = {row[0]: row[1] for row in treatment_plants}

    with st.form(key='water_quality_form'):
        code = st.number_input("Code", min_value=0, step=1)
        water_quality_name = st.text_input("Water Quality Name")
        color = st.number_input("Color", format="%.2f")
        turbidity = st.number_input("Turbidity", format="%.2f")
        ph_level = st.number_input("pH Level", format="%.2f")
        arsenic_level = st.number_input("Arsenic Level", format="%.2f")
        total_dissolved_solids = st.number_input("Total Dissolved Solids", format="%.2f")
        manganese_level = st.number_input("Manganese Level", format="%.2f")
        zinc_level = st.number_input("Zinc Level", format="%.2f")
        sulfate_level = st.number_input("Sulfate Level", format="%.2f")
        copper_level = st.number_input("Copper Level", format="%.2f")
        hydrogen_sulfide = st.number_input("Hydrogen Sulfide", format="%.2f")
        hardness = st.number_input("Hardness", format="%.2f")
        aluminum_level = st.number_input("Aluminum Level", format="%.2f")
        chloride_level = st.number_input("Chloride Level", format="%.2f")
        iron_level = st.number_input("Iron Level", format="%.2f")
        ammonia_level = st.number_input("Ammonia Level", format="%.2f")
        barium_level = st.number_input("Barium Level", format="%.2f")
        cadmium_level = st.number_input("Cadmium Level", format="%.2f")
        chromium_level = st.number_input("Chromium Level", format="%.2f")
        fluoride_level = st.number_input("Fluoride Level", format="%.2f")
        lead_level = st.number_input("Lead Level", format="%.2f")
        mercury_level = st.number_input("Mercury Level", format="%.2f")
        nitrate_level = st.number_input("Nitrate Level", format="%.2f")
        nitrite_level = st.number_input("Nitrite Level", format="%.2f")
        sodium_level = st.number_input("Sodium Level", format="%.2f")
        residual_chlorine = st.number_input("Residual Chlorine", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_treatment_plant_id = st.selectbox("Select Treatment Plant", options=list(treatment_plant_options.keys()), format_func=lambda x: treatment_plant_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                code, water_quality_name, color, turbidity, ph_level, arsenic_level,
                total_dissolved_solids, manganese_level, zinc_level, sulfate_level,
                copper_level, hydrogen_sulfide, hardness, aluminum_level, chloride_level,
                iron_level, ammonia_level, barium_level, cadmium_level, chromium_level,
                fluoride_level, lead_level, mercury_level, nitrate_level, nitrite_level,
                sodium_level, residual_chlorine, selected_treatment_plant_id
            ]
            submit_form(
                table_name='water_quality',
                columns=[
                    'code', 'WaterQuality_name', 'color', 'turbidity', 'ph_level', 
                    'arsenic_level', 'total_dissolved_solids', 'manganese_level',
                    'zinc_level', 'sulfate_level', 'copper_level', 'hydrogen_sulfide',
                    'hardness', 'aluminum_level', 'chloride_level', 'iron_level',
                    'ammonia_level', 'barium_level', 'cadmium_level', 'chromium_level',
                    'fluoride_level', 'lead_level', 'mercury_level', 'nitrate_level',
                    'nitrite_level', 'sodium_level', 'residual_chlorine', 'idTreatmentPlant'
                ],
                form_inputs=form_inputs
            )

def submit_commercial_form():
    st.title("Submit Commercial Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    treatment_plants = db_helper.fetch_data('treatment_plant', ['idTreatmentPlant', 'TreatmentPlant_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    treatment_plant_options = {row[0]: row[1] for row in treatment_plants}

    with st.form(key='commercial_form'):
        code = st.number_input("Code", min_value=0, step=1)
        commercial_name = st.text_input("Commercial Name")
        population_served = st.number_input("Population Served", min_value=0)
        service_coverage_license_area = st.number_input("Service Coverage License Area (sq km)", format="%.2f")
        service_coverage_network_area = st.number_input("Service Coverage Network Area (sq km)", format="%.2f")
        water_production = st.number_input("Water Production (m³)", format="%.2f")
        water_sold = st.number_input("Water Sold (m³)", format="%.2f")
        water_supplied_without_charge = st.number_input("Water Supplied Without Charge (m³)", format="%.2f")
        total_water_consumption = st.number_input("Total Water Consumption (m³)", format="%.2f")
        water_losses = st.number_input("Water Losses (m³)", format="%.2f")
        non_revenue_water = st.number_input("Non-Revenue Water (m³)", format="%.2f")
        average_daily_consumption = st.number_input("Average Daily Consumption (m³)", format="%.2f")
        average_consumption_per_connection = st.number_input("Average Consumption Per Connection (m³)", format="%.2f")
        average_consumption_per_capita = st.number_input("Average Consumption Per Capita (m³)", format="%.2f")
        total_water_connections = st.number_input("Total Water Connections", min_value=0)
        residential_connections = st.number_input("Residential Connections", min_value=0)
        commercial_connections = st.number_input("Commercial Connections", min_value=0)
        public_entity_connections = st.number_input("Public Entity Connections", min_value=0)
        factory_connections = st.number_input("Factory Connections", min_value=0)
        sme_connections = st.number_input("SME Connections", min_value=0)
        poor_connections = st.number_input("Poor Connections", min_value=0)
        poor_household_ratio = st.number_input("Poor Household Ratio (%)", format="%.2f")
        customer_complaints = st.number_input("Customer Complaints", min_value=0)
        complaints_per_1000_connections = st.number_input("Complaints Per 1000 Connections", format="%.2f")
        license_area_profile = st.text_input("License Area Profile")
        network_area_population = st.number_input("Network Area Population", min_value=0)
        network_area_houses = st.number_input("Network Area Houses", min_value=0)
        licensed_area_population = st.number_input("Licensed Area Population", min_value=0)
        licensed_area_houses = st.number_input("Licensed Area Houses", min_value=0)

        # Dropdown for selecting foreign key ID
        selected_treatment_plant_id = st.selectbox("Select Treatment Plant", options=list(treatment_plant_options.keys()), format_func=lambda x: treatment_plant_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                code, commercial_name, population_served, service_coverage_license_area,
                service_coverage_network_area, water_production, water_sold,
                water_supplied_without_charge, total_water_consumption, water_losses,
                non_revenue_water, average_daily_consumption, average_consumption_per_connection,
                average_consumption_per_capita, total_water_connections, residential_connections,
                commercial_connections, public_entity_connections, factory_connections,
                sme_connections, poor_connections, poor_household_ratio, customer_complaints,
                complaints_per_1000_connections, license_area_profile, network_area_population,
                network_area_houses, licensed_area_population, licensed_area_houses,
                selected_treatment_plant_id
            ]
            submit_form(
                table_name='commercial',
                columns=[
                    'code', 'Commercial_name', 'population_served', 'service_coverage_license_area',
                    'service_coverage_network_area', 'Water_Production', 'water_sold',
                    'water_supplied_without_charge', 'total_water_consumption', 'water_losses',
                    'non_revenue_water', 'average_daily_consumption', 'average_consumption_per_connection',
                    'average_consumption_per_capita', 'total_water_connections', 'residential_connections',
                    'commercial_connections', 'public_entity_connections', 'factory_connections',
                    'sme_connections', 'poor_connections', 'poor_household_ratio', 'customer_complaints',
                    'complaints_per_1000_connections', 'license_area_profile', 'network_area_population',
                    'network_area_houses', 'licensed_area_population', 'licensed_area_houses',
                    'idTreatmentPlant'
                ],
                form_inputs=form_inputs
            )
    
def submit_financial_form():
    st.title("Submit Financial Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    commercial_list = db_helper.fetch_data('commercial', ['idCommercial', 'Commercial_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    commercial_options = {row[0]: row[1] for row in commercial_list}

    with st.form(key='financial_form'):
        code = st.number_input("Code", min_value=0, step=1)
        financial_name = st.text_input("Financial Name")
        cash_from_water_sales = st.number_input("Cash From Water Sales", format="%.2f")
        other_cash = st.number_input("Other Cash", format="%.2f")
        amount_billed_for_water_sales = st.number_input("Amount Billed for Water Sales", format="%.2f")
        amount_billed_for_other_services = st.number_input("Amount Billed for Other Services", format="%.2f")
        accounts_receivable = st.number_input("Accounts Receivable", format="%.2f")
        average_tariff = st.number_input("Average Tariff", format="%.2f")
        bill_collection_ratio = st.number_input("Bill Collection Ratio (%)", format="%.2f")
        total_operating_expenses = st.number_input("Total Operating Expenses", format="%.2f")
        operating_ratio = st.number_input("Operating Ratio (%)", format="%.2f")
        production_expenses = st.number_input("Production Expenses", format="%.2f")
        unit_production_cost = st.number_input("Unit Production Cost", format="%.2f")
        net_income = st.number_input("Net Income", format="%.2f")
        net_profit_margin = st.number_input("Net Profit Margin (%)", format="%.2f")
        investment_expenditures = st.number_input("Investment Expenditures", format="%.2f")
        loans = st.number_input("Loans", format="%.2f")
        accounts_payable = st.number_input("Accounts Payable", format="%.2f")
        total_assets = st.number_input("Total Assets", format="%.2f")
        owner_equity = st.number_input("Owner Equity", format="%.2f")
        debt_to_equity_ratio = st.number_input("Debt to Equity Ratio", format="%.2f")
        return_on_assets = st.number_input("Return on Assets (%)", format="%.2f")
        return_on_equity = st.number_input("Return on Equity (%)", format="%.2f")
        interest_expense = st.number_input("Interest Expense", format="%.2f")
        depreciation_expense = st.number_input("Depreciation Expense", format="%.2f")
        other_expense = st.number_input("Other Expense", format="%.2f")
        residential_tariff = st.number_input("Residential Tariff", format="%.2f")
        commercial_tariff = st.number_input("Commercial Tariff", format="%.2f")
        government_tariff = st.number_input("Government Tariff", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_commercial_id = st.selectbox("Select Commercial", options=list(commercial_options.keys()), format_func=lambda x: commercial_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                code, financial_name, cash_from_water_sales, other_cash,
                amount_billed_for_water_sales, amount_billed_for_other_services,
                accounts_receivable, average_tariff, bill_collection_ratio,
                total_operating_expenses, operating_ratio, production_expenses,
                unit_production_cost, net_income, net_profit_margin,
                investment_expenditures, loans, accounts_payable,
                total_assets, owner_equity, debt_to_equity_ratio,
                return_on_assets, return_on_equity, interest_expense,
                depreciation_expense, other_expense, residential_tariff,
                commercial_tariff, government_tariff, selected_commercial_id
            ]
            submit_form(
                table_name='financial',
                columns=[
                    'code', 'Financial_name', 'cash_from_water_sales', 'other_cash',
                    'amount_billed_for_water_sales', 'amount_billed_for_other_services',
                    'accounts_receivable', 'average_tariff', 'bill_collection_ratio',
                    'total_operating_expenses', 'operating_ratio', 'production_expenses',
                    'unit_production_cost', 'net_income', 'net_profit_margin',
                    'investment_expenditures', 'loans', 'accounts_payable',
                    'total_assets', 'owner_equity', 'debt_to_equity_ratio',
                    'return_on_assets', 'return_on_equity', 'interest_expense',
                    'depreciation_expense', 'other_expense', 'residential_tariff',
                    'commercial_tariff', 'government_tariff', 'idCommercial'
                ],
                form_inputs=form_inputs
            )

def submit_distribution_network_form():
    st.title("Submit Distribution Network Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    commercial_list = db_helper.fetch_data('commercial', ['idCommercial', 'Commercial_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    commercial_options = {row[0]: row[1] for row in commercial_list}

    with st.form(key='distribution_network_form'):
        code = st.number_input("Code", min_value=0, step=1)
        distribution_network_name = st.text_input("Distribution Network Name")
        supply_pressure_end_connection = st.number_input("Supply Pressure at End Connection", format="%.2f")
        number_of_leaks_repaired = st.number_input("Number of Leaks Repaired", format="%.2f")
        total_length = st.number_input("Total Length (m)", format="%.2f")
        transmission_length = st.number_input("Transmission Length (m)", format="%.2f")
        distribution_length = st.number_input("Distribution Length (m)", format="%.2f")
        storage_capacity = st.number_input("Storage Capacity (m³)", format="%.2f")
        supply_duration = st.number_input("Supply Duration (hours)", min_value=0, step=1)

        # Dropdown for selecting foreign key ID
        selected_commercial_id = st.selectbox("Select Commercial", options=list(commercial_options.keys()), format_func=lambda x: commercial_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                code, distribution_network_name, supply_pressure_end_connection,
                number_of_leaks_repaired, total_length, transmission_length,
                distribution_length, storage_capacity, supply_duration,
                selected_commercial_id
            ]
            submit_form(
                table_name='distribution_network',
                columns=[
                    'code', 'DistributionNetwork_name', 'Supply_Pressure_end_connection',
                    'Number_leak_repaired', 'total_length', 'transmission_length',
                    'distribution_length', 'Storagecapacity', 'Supply_duration',
                    'idCommercial'
                ],
                form_inputs=form_inputs
            )

def submit_office_contact_form():
    st.title("Submit Office Contact Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_list = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_list}
    company_options = {row[0]: row[1] for row in company_list}

    with st.form(key='office_contact_form'):
        office_phone = st.text_input("Office Phone")
        fax_number = st.text_input("Fax Number")
        mobile_phone = st.text_input("Mobile Phone")
        email = st.text_input("Email")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                office_phone, fax_number, mobile_phone, email,
                selected_applicant_id, selected_company_id
            ]
            submit_form(
                table_name='office_contact',
                columns=[
                    'OfficePhone', 'FaxNumber', 'MobilePhone', 'Email',
                    'ApplicantID', 'CompanyID'
                ],
                form_inputs=form_inputs
            )

def submit_factory_form():
    st.title("Submit Factory Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdown
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_list}

    with st.form(key='factory_form'):
        factory_name = st.text_input("Factory Name")
        country = st.text_input("Country")
        address = st.text_input("Address")

        # Dropdown for selecting foreign key (CompanyID)
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                factory_name, country, address, selected_company_id
            ]
            submit_form(
                table_name='factory',
                columns=['Name', 'Country', 'Address', 'CompanyID'],
                form_inputs=form_inputs
            )

def submit_product_form():
    st.title("Submit Product Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_list = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    factory_list = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_list}
    factory_options = {row[0]: row[1] for row in factory_list}

    with st.form(key='product_form'):
        product_name = st.text_input("Product Name")
        trade_name = st.text_input("Trade Name")
        model_number = st.text_input("Model Number")
        referred_standard = st.file_uploader("Referred Standard", type=['pdf', 'docx', 'jpg', 'png'])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                product_name, trade_name, model_number, referred_standard.read() if referred_standard else None, 
                selected_applicant_id, selected_factory_id
            ]
            submit_form(
                table_name='product',
                columns=['ProductName', 'TradeName', 'ModelNumber', 'ReferredStandard', 'ApplicantID', 'FactoryID'],
                form_inputs=form_inputs
            )

def submit_license_form():
    st.title("Submit License Information")
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_list = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_list}
    product_options = {row[0]: row[1] for row in product_list}

    with st.form(key='license_form'):
        license_number = st.text_input("License Number")
        license_issued_date = st.date_input("License Issued Date")
        license_expiry_date = st.date_input("License Expiry Date")
        license_type = st.text_input("License Type")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            form_inputs = [
                license_number, license_issued_date, license_expiry_date, license_type, 
                selected_company_id, selected_product_id
            ]
            submit_form(
                table_name='license',
                columns=['LicenseNumber', 'LicenseIssuedDate', 'LicenseExpiryDate', 'LicenseType', 'CompanyID', 'ProductID'],
                form_inputs=form_inputs
            )

def submit_factory_inspection_report_form():
    st.title("Submit Factory Inspection Report")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_list = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    product_list = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_list}
    product_options = {row[0]: row[1] for row in product_list}

    with st.form(key='factory_inspection_report_form'):
        certification_number = st.text_input("System Certification Number")
        issued_date = st.date_input("Issued Date")
        certification_body_name = st.text_input("Certification Body Name")

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                certification_number, issued_date, certification_body_name,
                selected_factory_id, selected_product_id
            ]
            submit_form(
                table_name='factory_inspection_report',
                columns=['SystemCertificationNumber', 'IssuedDate', 'CertificationBodyName', 'FactoryID', 'ProductID'],
                form_inputs=form_inputs
            )

def submit_certificate_of_conformity_form():
    st.title("Submit Certificate of Conformity Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    factory_inspection_report_data = db_helper.fetch_data('factory_inspection_report', ['FactoryInspectionReportID', 'SystemCertificationNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    factory_inspection_report_options = {report[0]: report[1] for report in factory_inspection_report_data}

    with st.form(key='certificate_of_conformity_form'):
        certificate_number = st.text_input("Certificate Number")
        issued_date = st.date_input("Issued Date")
        certification_body_name = st.text_input("Certification Body Name")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_factory_inspection_report_id = st.selectbox("Select Factory Inspection Report", options=list(factory_inspection_report_options.keys()), format_func=lambda x: factory_inspection_report_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                certificate_number, issued_date, certification_body_name,
                selected_product_id, selected_factory_inspection_report_id
            ]
            submit_form(
                table_name='certificate_of_conformity',
                columns=[
                    'CertificateNumber', 'IssuedDate', 'CertificationBodyName', 
                    'ProductID', 'FactoryInspectionReportID'
                ],
                form_inputs=form_inputs
            )

def submit_test_report_form():
    st.title("Submit Test Report Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    certificate_of_conformity_data = db_helper.fetch_data('certificate_of_conformity', ['CertificateOfConformityID', 'CertificateNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    certificate_of_conformity_options = {cert[0]: cert[1] for cert in certificate_of_conformity_data}

    with st.form(key='test_report_form'):
        report_number = st.text_input("Report Number")
        test_laboratory_name = st.text_input("Test Laboratory Name")
        issued_date = st.date_input("Issued Date"
                                    ,min_value=datetime(1900, 1, 1))

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_certificate_of_conformity_id = st.selectbox("Select Certificate of Conformity", options=list(certificate_of_conformity_options.keys()), format_func=lambda x: certificate_of_conformity_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                report_number, test_laboratory_name, issued_date,
                selected_product_id, selected_certificate_of_conformity_id
            ]
            submit_form(
                table_name='test_report',
                columns=[
                    'ReportNumber', 'TestLaboratoryName', 'IssuedDate', 
                    'ProductID', 'CertificateOfConformityID'
                ],
                form_inputs=form_inputs,
                return_id=False

            )

def submit_patent_card_form():
    st.title("Submit Patent Card Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    company_options = {company[0]: company[1] for company in company_data}

    with st.form(key='patent_card_form'):
        number = st.text_input("Patent Number")
        patent_issued_date = st.date_input("Patent Issued Date",min_value=datetime(1900, 1, 1))
        tax_unit = st.text_input("Tax Unit")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                number, patent_issued_date, tax_unit,
                selected_product_id, selected_company_id
            ]
            submit_form(
                table_name='patent_card',
                columns=[
                    'Number', 'PatentIssuedDate', 'TaxUnit',
                    'ProductID', 'CompanyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_pro_or_spare_part_pro_registration_form():
    st.title("Submit Document for Product or Spare Part Registration Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    certificate_of_conformity_data = db_helper.fetch_data('certificate_of_conformity', ['CertificateOfConformityID', 'CertificateNumber'])
    factory_inspection_report_data = db_helper.fetch_data('factory_inspection_report', ['FactoryInspectionReportID', 'SystemCertificationNumber'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    certificate_of_conformity_options = {row[0]: row[1] for row in certificate_of_conformity_data}
    factory_inspection_report_options = {row[0]: row[1] for row in factory_inspection_report_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='doc_pro_or_spare_part_pro_registration_form'):
        description = st.text_input("Description")
        certificate_conformity_in_english = st.file_uploader("Upload Certificate Conformity in English", type=["pdf", "jpg", "png"])
        factory_inspection_report = st.file_uploader("Upload Factory Inspection Report", type=["pdf", "jpg", "png"])
        label = st.file_uploader("Upload Label", type=["pdf", "jpg", "png"])
        users_instruction_manual = st.file_uploader("Upload Users Instruction Manual", type=["pdf", "jpg", "png"])
        record_of_modification = st.file_uploader("Upload Record of Modification", type=["pdf", "jpg", "png"])
        product_color_photographs = st.file_uploader("Upload Product Color Photographs", type=["pdf", "jpg", "png"])
        test_report_conformity_in_english = st.file_uploader("Upload Test Report Conformity in English", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_certificate_of_conformity_id = st.selectbox("Select Certificate of Conformity", options=list(certificate_of_conformity_options.keys()), format_func=lambda x: certificate_of_conformity_options[x])
        selected_factory_inspection_report_id = st.selectbox("Select Factory Inspection Report", options=list(factory_inspection_report_options.keys()), format_func=lambda x: factory_inspection_report_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                description,
                certificate_conformity_in_english.read() if certificate_conformity_in_english else None,
                factory_inspection_report.read() if factory_inspection_report else None,
                label.read() if label else None,
                users_instruction_manual.read() if users_instruction_manual else None,
                record_of_modification.read() if record_of_modification else None,
                product_color_photographs.read() if product_color_photographs else None,
                test_report_conformity_in_english.read() if test_report_conformity_in_english else None,
                selected_certificate_of_conformity_id,
                selected_factory_inspection_report_id,
                selected_product_id
            ]
            submit_form(
                table_name='doc_pro_or_spare_part_pro_registration',
                columns=[
                    'Description', 'CertificateConformityInEnglish', 'FactoryInspectionReport', 
                    'Label', 'UsersInstructionManual', 'RecordOfModification', 
                    'ProductColorPhotographs', 'TestReportConformityInEnglish', 
                    'CertificateOfConformityID', 'FactoryInspectionReportID', 
                    'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_electri_and_electro_pro_registration_form():
    st.title("Submit Document for Electrical and Electronic Product Registration Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    documents_data = db_helper.fetch_data('doc_pro_or_spare_part_pro_registration', ['DocumentsID', 'Description'])
    
    db_helper.close_connection()

    # Prepare dropdown options
    documents_options = {row[0]: row[1] for row in documents_data}

    with st.form(key='doc_electri_and_electro_pro_registration_form'):
        full_electrical_wiring_circuit_diagrams = st.file_uploader("Upload Full Electrical Wiring Circuit Diagrams", type=["pdf", "jpg", "png"])

        # Dropdown for selecting foreign keys
        selected_documents_id = st.selectbox("Select Document ID", options=list(documents_options.keys()), format_func=lambda x: documents_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                full_electrical_wiring_circuit_diagrams.read() if full_electrical_wiring_circuit_diagrams else None,
                selected_documents_id
            ]
            submit_form(
                table_name='doc_electri_and_electro_pro_registration',
                columns=[
                    'FullElectricalWiringCircuitDiagrams', 'DocumentsID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_detail_of_modification_form():
    st.title("Submit Information Detail of Modification for Part or Electrical and Electronic Product")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    applicant_options = {row[0]: row[1] for row in applicant_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='infor_detail_of_modification_form'):
        item_number = st.text_input("Item Number")
        description_item = st.text_input("Description of Item")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                item_number,
                description_item,
                selected_company_id,
                selected_applicant_id,
                selected_product_id
            ]
            submit_form(
                table_name='infor_detail_of_modification_part_or_electri_and_electro_pro',
                columns=[
                    'ItemNumber', 'DescriptionItem', 'CompanyID', 'ApplicantID', 'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_of_modification_part_pro_form():
    st.title("Submit Document of Modification for Part Product")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    infor_detail_of_modification_data = db_helper.fetch_data('infor_detail_of_modification_part_or_electri_and_electro_pro', ['InforDetailOfModificationID', 'ItemNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    product_options = {row[0]: row[1] for row in product_data}
    infor_detail_options = {row[0]: row[1] for row in infor_detail_of_modification_data}

    with st.form(key='doc_of_modification_part_pro_form'):
        industrial_announcement_letter = st.file_uploader("Upload Industrial Announcement Letter", type=["pdf", "jpg", "png"])
        certificate_of_operation_company_local = st.file_uploader("Upload Certificate of Operation Company Local", type=["pdf", "jpg", "png"])
        company_establishment_statute = st.file_uploader("Upload Company Establishment Statute", type=["pdf", "jpg", "png"])
        commercial_registration_certificate = st.file_uploader("Upload Commercial Registration Certificate", type=["pdf", "jpg", "png"])
        patent_certificate = st.file_uploader("Upload Patent Certificate", type=["pdf", "jpg", "png"])
        equivalent_legal_documents = st.file_uploader("Upload Equivalent Legal Documents", type=["pdf", "jpg", "png"])
        letter_of_recognition = st.file_uploader("Upload Letter of Recognition", type=["pdf", "jpg", "png"])
        national_id_card_or_passport = st.file_uploader("Upload National ID Card or Passport", type=["pdf", "jpg", "png"])
        analysis_certificate = st.file_uploader("Upload Analysis Certificate", type=["pdf", "jpg", "png"])
        compliance_evaluation_certificate = st.file_uploader("Upload Compliance Evaluation Certificate", type=["pdf", "jpg", "png"])
        license_using_vehicle_safety_mark = st.file_uploader("Upload License Using Vehicle Safety Mark", type=["pdf", "jpg", "png"])
        other_related_documents = st.file_uploader("Upload Other Related Documents", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_infor_detail_id = st.selectbox("Select Information Detail of Modification", options=list(infor_detail_options.keys()), format_func=lambda x: infor_detail_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                industrial_announcement_letter.read() if industrial_announcement_letter else None,
                certificate_of_operation_company_local.read() if certificate_of_operation_company_local else None,
                company_establishment_statute.read() if company_establishment_statute else None,
                commercial_registration_certificate.read() if commercial_registration_certificate else None,
                patent_certificate.read() if patent_certificate else None,
                equivalent_legal_documents.read() if equivalent_legal_documents else None,
                letter_of_recognition.read() if letter_of_recognition else None,
                national_id_card_or_passport.read() if national_id_card_or_passport else None,
                analysis_certificate.read() if analysis_certificate else None,
                compliance_evaluation_certificate.read() if compliance_evaluation_certificate else None,
                license_using_vehicle_safety_mark.read() if license_using_vehicle_safety_mark else None,
                other_related_documents.read() if other_related_documents else None,
                selected_applicant_id,
                selected_company_id,
                selected_product_id,
                selected_infor_detail_id
            ]
            submit_form(
                table_name='doc_of_modification_part_pro',
                columns=[
                    'IndustrialAnouncementLatter', 'CertificateOfOpperationCompanyLocal', 
                    'Companyestablishmentstatute', 'commercialregistrationcertificate', 
                    'patentCertificate', 'equivalentlegaldocuments', 'Letterofrecognition', 
                    'NationalIDCardorPassport', 'Analysiscertificate', 
                    'complianceevaluationcertificate', 'Licenseusingvehiclsafetymark', 
                    'Otherrelateddocuments', 'ApplicantID', 'CompanyID', 
                    'ProductID', 'InforDetailOfModificationID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_of_modification_electri_electro_part_pro_form():
    st.title("Submit Document of Modification for Electrical and Electro Part Product")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    infor_detail_of_modification_data = db_helper.fetch_data('infor_detail_of_modification_part_or_electri_and_electro_pro', ['InforDetailOfModificationID', 'ItemNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    product_options = {row[0]: row[1] for row in product_data}
    infor_detail_options = {row[0]: row[1] for row in infor_detail_of_modification_data}

    with st.form(key='doc_of_modification_electri_electro_part_pro_form'):
        test_report_in_english = st.file_uploader("Upload Test Report in English", type=["pdf", "jpg", "png"])
        certificate_of_conformity_in_english = st.file_uploader("Upload Certificate of Conformity in English", type=["pdf", "jpg", "png"])
        product_safety_license = st.file_uploader("Upload Product Safety License", type=["pdf", "jpg", "png"])
        confirmed_letter = st.file_uploader("Upload Confirmed Letter", type=["pdf", "jpg", "png"])
        document_related_regulated_products = st.file_uploader("Upload Document Related to Regulated Products", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_infor_detail_id = st.selectbox("Select Information Detail of Modification", options=list(infor_detail_options.keys()), format_func=lambda x: infor_detail_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                test_report_in_english.read() if test_report_in_english else None,
                certificate_of_conformity_in_english.read() if certificate_of_conformity_in_english else None,
                product_safety_license.read() if product_safety_license else None,
                confirmed_letter.read() if confirmed_letter else None,
                document_related_regulated_products.read() if document_related_regulated_products else None,
                selected_company_id,
                selected_applicant_id,
                selected_infor_detail_id,
                selected_product_id
            ]
            submit_form(
                table_name='doc_of_modification_electri_electro_part_pro',
                columns=[
                    'TestReportInEnglish', 'CertificateOfConformityInEnglish', 
                    'ProductSafetyLicense', 'ConfirmedLetter', 
                    'DocumentRelatedRegulatedProducts', 'CompanyID', 
                    'ApplicantID', 'InforDetailOfModificationID', 'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_list_chemical_substance_form():
    st.title("Submit Chemical Substance Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    company_signature_data = db_helper.fetch_data('company_signatur_and_stamp', ['CompanySignatureID', 'Name'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    company_signature_options = {row[0]: row[1] for row in company_signature_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='list_chemical_substance_form'):
        chemical_name = st.text_input("Chemical Name")
        commercial_name = st.text_input("Commercial Name")
        recognition = st.text_input("Recognition")
        quantity = st.text_input("Quantity")
        standard_of_usage = st.text_input("Standard of Usage")
        reference_chemical = st.text_input("Reference Chemical")
        support_purpose = st.text_input("Support Purpose")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_company_signature_id = st.selectbox("Select Company Signature", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                chemical_name,
                commercial_name,
                recognition,
                quantity,
                standard_of_usage,
                reference_chemical,
                support_purpose,
                selected_applicant_id,
                selected_company_id,
                selected_company_signature_id,
                selected_product_id
            ]
            submit_form(
                table_name='list_chemical_substance',
                columns=[
                    'ChemicalName', 'CommercialName', 'Recognition', 
                    'Quantity', 'StandardOfUsage', 'ReferenceChemical', 
                    'SupportPurpose', 'ApplicantID', 'CompanyID', 
                    'CompanySignatureID', 'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_previous_chemical_usage_form():
    st.title("Submit Previous Chemical Usage Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='previous_chemical_usage_form'):
        chemical_name = st.text_input("Chemical Name")
        previous_quantity = st.text_input("Previous Quantity")
        previous_import_license_number = st.text_input("Previous Import License Number")
        previous_import_date = st.date_input("Previous Import Date")

        # Dropdown for selecting foreign key
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                chemical_name,
                previous_quantity,
                previous_import_license_number,
                previous_import_date,
                selected_chemical_substance_id
            ]
            submit_form(
                table_name='previous_chemical_usage',
                columns=[
                    'ChemicalName', 'PreviousQuantity', 'PreviousImportLicenseNumber', 
                    'PreviousImportDate', 'ChemicalSubstanceID'
                ],
                form_inputs=form_inputs
            )

def submit_appli_details_chemical_form():
    st.title("Submit Application Details for Chemical Substance")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='appli_details_chemical_form'):
        port_to_port = st.text_input("Port to Port")
        port_to_applicant_storage_premise = st.text_input("Port to Applicant Storage Premise")
        port_to_job_site_for_immediate_use = st.text_input("Port to Job Site for Immediate Use")
        port_to_customer_storage_premise = st.text_input("Port to Customer Storage Premise")
        other = st.text_input("Other Details")
        name_of_premise = st.text_input("Name of Premise")
        kind_of_premise = st.text_input("Kind of Premise")
        size_capacity = st.text_input("Size Capacity")
        emergency_action_plan = st.checkbox("Emergency Action Plan", value=False)
        date = st.date_input("Date")

        # Dropdown for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                port_to_port,
                port_to_applicant_storage_premise,
                port_to_job_site_for_immediate_use,
                port_to_customer_storage_premise,
                other,
                name_of_premise,
                kind_of_premise,
                size_capacity,
                int(emergency_action_plan),
                date,
                selected_company_id,
                selected_chemical_substance_id
            ]
            submit_form(
                table_name='appli_details_chemical',
                columns=[
                    'PortToPort', 'PortToApplicantStoragePremise', 'PortToJobSiteForImmediateUse', 
                    'PortToCustomerStoragePremise', 'Other', 'NameOfPremise', 'KindOfPremise', 
                    'SizeCapacity', 'EmergencyActionPlan', 'Date', 'CompanyID', 'ChemicalSubstanceID'
                ],
                form_inputs=form_inputs
            )

def submit_chemical_pro_plan_annual_form():
    st.title("Submit Chemical Production Plan Annual")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='chemical_pro_plan_annual_form'):
        production_quantity = st.text_input("Production Quantity")
        recognition = st.text_input("Recognition")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        # Dropdown for selecting foreign key (CompanyID)
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                production_quantity,
                recognition,
                start_date,
                end_date,
                selected_company_id
            ]
            submit_form(
                table_name='chemical_pro_plan_annual',
                columns=[
                    'ProductionQuantity', 'Recognition', 'StartDate', 'EndDate', 'CompanyID'
                ],
                form_inputs=form_inputs
            )

def submit_declaration_buyer_importer_form():
    st.title("Submit Declaration for Buyer/Importer")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='declaration_buyer_importer_form'):
        usage_purpose = st.text_input("Usage Purpose")
        name = st.text_input("Name")
        position = st.text_input("Position")
        stand_for_company = st.text_input("Stand For Company")
        address = st.text_area("Address")
        phone = st.text_input("Phone")
        fax_number = st.text_input("Fax Number")
        email = st.text_input("Email")
        date = st.date_input("Date")

        # Dropdowns for foreign keys
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                usage_purpose,
                name,
                position,
                stand_for_company,
                address,
                phone,
                fax_number,
                email,
                date,
                selected_chemical_substance_id,
                selected_company_id
            ]
            submit_form(
                table_name='declaration_buyer_importer',
                columns=[
                    'UsagePurpose', 'Name', 'Position', 'StandForCompany', 'Address', 'Phone', 
                    'FaxNumber', 'Email', 'Date', 'ChemicalSubstanceID', 'CompanyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_recog_standard_chemical_substance_form():
    st.title("Submit Document for Recognition of Standard Chemical Substance")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='doc_recog_standard_chemical_substance_form'):
        company_characteristics = st.file_uploader("Upload Company Characteristics", type=["pdf", "jpg", "png"])
        company_certification_letter = st.file_uploader("Upload Company Certification Letter", type=["pdf", "jpg", "png"])
        company_registration_certificate = st.file_uploader("Upload Company Registration Certificate", type=["pdf", "jpg", "png"])
        value_added_tax_registration_certificate = st.file_uploader("Upload Value Added Tax Registration Certificate", type=["pdf", "jpg", "png"])
        valid_patents_copies = st.file_uploader("Upload Valid Patents Copies", type=["pdf", "jpg", "png"])
        factory_permit_and_certificate = st.file_uploader("Upload Factory Permit and Certificate", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("Upload Rights Transfer Letter", type=["pdf", "jpg", "png"])
        chemical_substances_list_and_values = st.file_uploader("Upload Chemical Substances List and Values", type=["pdf", "jpg", "png"])
        applicant_id_or_passport_copy = st.file_uploader("Upload Applicant ID or Passport Copy", type=["pdf", "jpg", "png"])
        material_safety_data_sheet = st.file_uploader("Upload Material Safety Data Sheet", type=["pdf", "jpg", "png"])
        analysis_certificate_or_sample = st.file_uploader("Upload Analysis Certificate or Sample", type=["pdf", "jpg", "png"])
        previous_importation_and_usage_report = st.file_uploader("Upload Previous Importation and Usage Report", type=["pdf", "jpg", "png"])
        other_documents_if_required = st.file_uploader("Upload Other Documents if Required", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                company_characteristics.read() if company_characteristics else None,
                company_certification_letter.read() if company_certification_letter else None,
                company_registration_certificate.read() if company_registration_certificate else None,
                value_added_tax_registration_certificate.read() if value_added_tax_registration_certificate else None,
                valid_patents_copies.read() if valid_patents_copies else None,
                factory_permit_and_certificate.read() if factory_permit_and_certificate else None,
                rights_transfer_letter.read() if rights_transfer_letter else None,
                chemical_substances_list_and_values.read() if chemical_substances_list_and_values else None,
                applicant_id_or_passport_copy.read() if applicant_id_or_passport_copy else None,
                material_safety_data_sheet.read() if material_safety_data_sheet else None,
                analysis_certificate_or_sample.read() if analysis_certificate_or_sample else None,
                previous_importation_and_usage_report.read() if previous_importation_and_usage_report else None,
                other_documents_if_required.read() if other_documents_if_required else None,
                selected_company_id,
                selected_chemical_substance_id
            ]

            submit_form(
                table_name='doc_recog_standard_chemical_substance',
                columns=[
                    'CompanyCharacteristics', 'CompanyCertificationLetter', 'CompanyRegistrationCertificate', 
                    'ValueAddedTaxRegistrationCertificate', 'ValidPatentsCopies', 'FactoryPermitAndCertificate', 
                    'RightsTransferLetter', 'ChemicalSubstancesListAndValues', 'ApplicantIDOrPassportCopy', 
                    'MaterialSafetyDataSheet', 'AnalysisCertificateOrSample', 'PreviousImportationAndUsageReport', 
                    'OtherDocumentsIfRequired', 'CompanyID', 'ChemicalSubstanceID'
                ],
                form_inputs=form_inputs
            )

def submit_pro_registration_license_form():
    st.title("Submit Product Registration License Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['AddressID', 'officeAddress'])  # Assuming AddressID is the primary key
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    applicant_options = {row[0]: row[1] for row in applicant_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='pro_registration_license_form'):
        license_type = st.text_input("License Type")
        old_license_number_if_renewal = st.text_input("Old License Number (if Renewal)")
        product_name = st.text_input("Product Name")
        capacity_weight = st.text_input("Capacity/Weight")
        trademark = st.text_input("Trademark")
        standard_reference = st.text_input("Standard Reference")
        related_terms_conditions = st.text_area("Related Terms and Conditions")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                license_type,
                old_license_number_if_renewal,
                product_name,
                capacity_weight,
                trademark,
                standard_reference,
                related_terms_conditions,
                selected_company_id,
                selected_address_id,
                selected_applicant_id,
                selected_product_id
            ]

            submit_form(
                table_name='pro_registration_license',
                columns=[
                    'license_type', 'old_license_number_if_renewal', 'product_name', 
                    'capacity_weight', 'trademark', 'standard_reference', 
                    'related_terms_conditions', 'CompanyID', 'CurrentAddressForApplicantID', 
                    'ApplicantID', 'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_machinery_equipment_in_factory_form():
    st.title("Submit Machinery Equipment in Factory Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['AddressID', 'officeAddress'])  # Assuming AddressID is the primary key
    product_registration_license_data = db_helper.fetch_data('pro_registration_license', ['ProductRegistrationLicenseID', 'product_name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    product_registration_license_options = {row[0]: row[1] for row in product_registration_license_data}

    with st.form(key='machinery_equipment_in_factory_form'):
        machinery_name = st.text_input("Machinery Name")
        inspection_date = st.date_input("Inspection Date")
        additional_information = st.text_area("Additional Information")

        # Dropdowns for selecting foreign keys
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("Select Product Registration License", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                inspection_date,
                additional_information,
                machinery_name,
                selected_address_id,
                selected_company_id,
                selected_product_registration_license_id
            ]

            submit_form(
                table_name='machinery_equipment_in_factory',
                columns=[
                    'inspection_date', 'additional_information', 'machinery_name',
                    'addressID', 'CompanyID', 'ProductRegistrationLicenseID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_pro_regis_license_form():
    st.title("Submit Document for Product Registration License Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_registration_license_data = db_helper.fetch_data('pro_registration_license', ['ProductRegistrationLicenseID', 'product_name'])
    company_signature_data = db_helper.fetch_data('company_signatur_and_stamp', ['CompanySignatureID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    product_registration_license_options = {row[0]: row[1] for row in product_registration_license_data}
    company_signature_options = {row[0]: row[1] for row in company_signature_data}

    with st.form(key='doc_pro_regis_license_form'):
        # File upload inputs
        declaration_of_factory = st.file_uploader("Upload Declaration of Factory", type=["pdf", "jpg", "png"])
        product_label_compliance = st.file_uploader("Upload Product Label Compliance (CS001:2000)", type=["pdf", "jpg", "png"])
        product_analysis_certificate = st.file_uploader("Upload Product Analysis Certificate", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("Upload Rights Transfer Letter", type=["pdf", "jpg", "png"])
        other_documents = st.file_uploader("Upload Other Documents", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("Select Product Registration License", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])
        selected_company_signature_id = st.selectbox("Select Company Signature", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                declaration_of_factory.read() if declaration_of_factory else None,
                product_label_compliance.read() if product_label_compliance else None,
                product_analysis_certificate.read() if product_analysis_certificate else None,
                rights_transfer_letter.read() if rights_transfer_letter else None,
                other_documents.read() if other_documents else None,
                selected_company_id,
                selected_product_registration_license_id,
                selected_company_signature_id
            ]

            submit_form(
                table_name='doc_pro_regis_license',
                columns=[
                    'declaration_of_factory', 'product_label_compliance_cs001_2000', 
                    'product_analysis_certificate', 'rights_transfer_letter', 
                    'other_documents', 'CompanyID', 'ProductRegistrationLicenseID', 'CompanySignatureID'
                ],
                form_inputs=form_inputs
            )

def submit_production_chain_form():
    st.title("Submit Production Chain Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['addressID', 'officeAddress'])  # Assuming there's an 'address' table
    product_registration_license_data = db_helper.fetch_data('pro_registration_license', ['ProductRegistrationLicenseID', 'product_name'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    product_registration_license_options = {row[0]: row[1] for row in product_registration_license_data}

    with st.form(key='production_chain_form'):
        production_chain_diagram = st.file_uploader("Upload Production Chain Diagram", type=["pdf", "jpg", "png"])
        date_of_diagram = st.date_input("Date of Diagram")
        product_purpose = st.text_input("Production Purpose")
        issued_date = st.date_input("Issued Date")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_product_registration_license_id = st.selectbox("Select Product Registration License", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                production_chain_diagram.read() if production_chain_diagram else None,
                date_of_diagram,
                product_purpose,
                issued_date,
                selected_applicant_id,
                selected_company_id,
                selected_address_id,
                selected_product_registration_license_id
            ]

            submit_form(
                table_name='production_chain',
                columns=[
                    'production_chain_diagram', 'date_of_diagram', 
                    'ProducPorpuse', 'IssuedDate', 
                    'ApplicantID', 'CompanyID', 'addressID', 
                    'ProductRegistrationLicenseID'
                ],
                form_inputs=form_inputs
            )

def submit_raw_materials_form():
    st.title("Submit Raw Materials Form")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address', ['addressID', 'officeAddress'])  # Assuming there's an 'address' table
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_registration_license_data = db_helper.fetch_data('pro_registration_license', ['ProductRegistrationLicenseID', 'product_name'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]: row[1] for row in address_data}
    company_options = {row[0]: row[1] for row in company_data}
    product_registration_license_options = {row[0]: row[1] for row in product_registration_license_data}

    with st.form(key='raw_materials_form'):
        material_name = st.text_input("Material Name")
        trademark_used = st.text_input("Trademark Used")
        percentage_used_in_final_product = st.text_input("Percentage Used in Final Product")
        additional_information = st.text_input("Additional Information")

        # Dropdowns for selecting foreign keys
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("Select Product Registration License", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                material_name,
                trademark_used,
                percentage_used_in_final_product,
                additional_information,
                selected_address_id,
                selected_company_id,
                selected_product_registration_license_id
            ]

            submit_form(
                table_name='raw_materials',
                columns=[
                    'material_name', 'trademark_used', 
                    'percentage_used_in_final_product', 'additional_information', 
                    'addressID', 'CompanyID', 'ProductRegistrationLicenseID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_restricted_chemicals_form():
    st.title("Submit Document for Restricted Chemicals")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])  # Assuming there's an 'applicant' table
    company_signature_data = db_helper.fetch_data('company_signatur_and_stamp', ['CompanySignatureID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_signature_options = {row[0]: row[1] for row in company_signature_data}

    with st.form(key='doc_restricted_chemicals_form'):
        company_statute = st.file_uploader("Upload Company Statute", type=["pdf", "jpg", "png"])
        company_verification_letter = st.file_uploader("Upload Company Verification Letter", type=["pdf", "jpg", "png"])
        company_registration_certificate = st.file_uploader("Upload Company Registration Certificate", type=["pdf", "jpg", "png"])
        vat_registration_certificate = st.file_uploader("Upload VAT Registration Certificate", type=["pdf", "jpg", "png"])
        patent_card = st.file_uploader("Upload Patent Card", type=["pdf", "jpg", "png"])
        previous_compliance_status = st.file_uploader("Upload Previous Compliance Status", type=["pdf", "jpg", "png"])
        other_documents = st.file_uploader("Upload Other Documents", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("Upload Rights Transfer Letter", type=["pdf", "jpg", "png"])
        factory_establishment_permission = st.file_uploader("Upload Factory Establishment Permission", type=["pdf", "jpg", "png"])
        craft_establishment_permission = st.file_uploader("Upload Craft Establishment Permission", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_company_signature_id = st.selectbox("Select Company Signature", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                company_statute.read() if company_statute else None,
                company_verification_letter.read() if company_verification_letter else None,
                company_registration_certificate.read() if company_registration_certificate else None,
                vat_registration_certificate.read() if vat_registration_certificate else None,
                patent_card.read() if patent_card else None,
                previous_compliance_status.read() if previous_compliance_status else None,
                other_documents.read() if other_documents else None,
                rights_transfer_letter.read() if rights_transfer_letter else None,
                factory_establishment_permission.read() if factory_establishment_permission else None,
                craft_establishment_permission.read() if craft_establishment_permission else None,
                selected_applicant_id,
                selected_company_id,
                selected_company_signature_id
            ]

            submit_form(
                table_name='doc_restricted_chemicals',
                columns=[
                    'company_statute', 'company_verification_letter', 
                    'company_registration_certificate', 'vat_registration_certificate', 
                    'patent_card', 'previous_compliance_status', 
                    'OtherDocuments', 'rights_transfer_letter', 
                    'factory_establishment_permission', 'craft_establishment_permission', 
                    'ApplicantID', 'CompanyID', 'CompanySignatureID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_represent_company_form():
    st.title("Submit Document for Representative Companies (Electri, Electro, or Spare Part)")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])  # Assuming there's an 'applicant' table
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    company_signature_data = db_helper.fetch_data('company_signatur_and_stamp', ['CompanySignatureID', 'Name'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    company_signature_options = {row[0]: row[1] for row in company_signature_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='doc_represent_company_form'):
        industrial_announcement_letter = st.file_uploader("Upload Industrial Announcement Letter", type=["pdf", "jpg", "png"])
        certi_commercial_registration_or_equivalent_legal_doc = st.file_uploader("Upload Commercial Registration or Equivalent Legal Document", type=["pdf", "jpg", "png"])
        national_id_card_or_passport = st.file_uploader("Upload National ID Card or Passport", type=["pdf", "jpg", "png"])
        other_related_documents = st.file_uploader("Upload Other Related Documents", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_company_signature_id = st.selectbox("Select Company Signature", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                industrial_announcement_letter.read() if industrial_announcement_letter else None,
                certi_commercial_registration_or_equivalent_legal_doc.read() if certi_commercial_registration_or_equivalent_legal_doc else None,
                national_id_card_or_passport.read() if national_id_card_or_passport else None,
                other_related_documents.read() if other_related_documents else None,
                selected_applicant_id,
                selected_company_id,
                selected_product_id,
                selected_company_signature_id
            ]

            submit_form(
                table_name='doc_represent_company_electri_electro_or_spare_part_pro',
                columns=[
                    'IndustrialAnouncementLatter', 'CertiComercialRegisOrequivalentlegaldoc', 
                    'NationalIDCardorPassport', 'Otherrelateddocuments', 
                    'ApplicantID', 'CompanyID', 'ProductID', 'CompanySignatureID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_establishment_factory_form():
    st.title("Submit Document for Establishment of Factory")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])  # Assuming there's an 'applicant' table
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_options = {row[0]: row[1] for row in company_data}
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='doc_establishment_factory_form'):
        photo_of_factory_owner = st.file_uploader("Upload 4x6 Photo of Factory Owner", type=["jpg", "png"])
        national_id_card_or_passport = st.file_uploader("Upload National ID Card or Passport", type=["pdf", "jpg", "png"])
        copy_of_corporate_statute = st.file_uploader("Upload Copy of Corporate Statute", type=["pdf", "jpg", "png"])
        copy_letter_of_commercial_registration = st.file_uploader("Upload Copy Letter of Commercial Registration", type=["pdf", "jpg", "png"])
        construction_permit = st.file_uploader("Upload Construction Permit from Authority", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                photo_of_factory_owner.read() if photo_of_factory_owner else None,
                national_id_card_or_passport.read() if national_id_card_or_passport else None,
                copy_of_corporate_statute.read() if copy_of_corporate_statute else None,
                copy_letter_of_commercial_registration.read() if copy_letter_of_commercial_registration else None,
                construction_permit.read() if construction_permit else None,
                selected_applicant_id,
                selected_company_id,
                selected_factory_id
            ]

            submit_form(
                table_name='doc_establishment_factory',
                columns=[
                    '3photoOfFactoryOwner4x6', 'NationalIDCardorPassport', 
                    'Copyofcorporatestatute', 'CopyLatterOfcomercialRigisteration', 
                    'ConstructionPermitFromAuthority', 
                    'ApplicantID', 'CompanyID', 'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_raw_material_form():
    st.title("Submit Information for Raw Material")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='infor_raw_material_form'):
        description_raw_material = st.text_input("Description of Raw Material")
        unit = st.text_input("Unit")
        domestic_quantity = st.text_input("Domestic Quantity")
        domestic_amount = st.text_input("Domestic Amount")
        import_quantity = st.text_input("Import Quantity")
        import_amount = st.text_input("Import Amount")

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                description_raw_material,
                unit,
                domestic_quantity,
                domestic_amount,
                import_quantity,
                import_amount,
                selected_factory_id,
                selected_chemical_substance_id
            ]

            submit_form(
                table_name='infor_raw_material',
                columns=[
                    'Description_RawMaterialcol', 'Unit', 
                    'Domstic_Quantity', 'Domstic_Amount', 
                    'Import_Quantity', 'Import_Amount', 
                    'FactoryID', 'ChemicalSubstanceID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_invest_pro_safety_and_sanitary_system_form():
    st.title("Submit Information for Investment Production Safety and Sanitary System")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_invest_pro_safety_and_sanitary_system_form'):
        total_surface_area = st.text_input("Total Surface Area")
        description_surrounding_environment = st.text_input("Description of Surrounding Environment")

        # Dropdown for selecting foreign key
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                total_surface_area,
                description_surrounding_environment,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_invest_pro_safety_and_sanitary_system',
                columns=[
                    'Totalsurfacearea', 'Descriptionsurroundingenvironment', 
                    'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_for_inves_project_pro_safety_form():
    st.title("Submit Document for Investment Project Production Safety")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='doc_for_inves_project_pro_safety_form'):
        application_form = st.file_uploader("Upload Application Form", type=["pdf", "jpg", "png"])
        factory_permit_authority = st.file_uploader("Upload Factory Permit from Authority", type=["pdf", "jpg", "png"])
        lease_agreement = st.file_uploader("Upload Lease Agreement", type=["pdf", "jpg", "png"])
        land_title = st.file_uploader("Upload Land Title", type=["pdf", "jpg", "png"])
        commercial_registration = st.file_uploader("Upload Commercial Registration", type=["pdf", "jpg", "png"])
        statute = st.file_uploader("Upload Statute", type=["pdf", "jpg", "png"])
        feasibility_study = st.file_uploader("Upload Feasibility Study", type=["pdf", "jpg", "png"])
        factory_signed_board = st.file_uploader("Upload Factory Signed Board", type=["pdf", "jpg", "png"])
        id_or_passport = st.file_uploader("Upload ID or Passport", type=["pdf", "jpg", "png"])
        owner_factory_photo = st.file_uploader("Upload Owner Factory Photo (3x4)", type=["pdf", "jpg", "png"])
        lab_test = st.file_uploader("Upload Lab Test", type=["pdf", "jpg", "png"])
        criminal_police_record = st.file_uploader("Upload Criminal Police Record", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                application_form.read() if application_form else None,
                factory_permit_authority.read() if factory_permit_authority else None,
                lease_agreement.read() if lease_agreement else None,
                land_title.read() if land_title else None,
                commercial_registration.read() if commercial_registration else None,
                statute.read() if statute else None,
                feasibility_study.read() if feasibility_study else None,
                factory_signed_board.read() if factory_signed_board else None,
                id_or_passport.read() if id_or_passport else None,
                owner_factory_photo.read() if owner_factory_photo else None,
                lab_test.read() if lab_test else None,
                criminal_police_record.read() if criminal_police_record else None,
                selected_company_id,
                selected_factory_id
            ]

            submit_form(
                table_name='doc_for_inves_project_pro_safety',
                columns=[
                    'ApplicationForm', 'Factory_permit_Authority', 
                    'LeaseAgreement', 'LandTitle', 
                    'Comercial_RegisterationMoc', 'Statute', 
                    'FeasibilityStudy', 'Factory_Signed_Board', 
                    'IDOrPassport', 'Owner_Factory_photo3_4x6', 
                    'Lab_Test', 'Criminal_Police_Record', 
                    'CompanyID', 'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_permit_small_medium_enterprises_handicraft_form():
    st.title("Submit Document for Small Medium Enterprises Handicraft Permit")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    applicant_options = {row[0]: row[1] for row in applicant_data}

    with st.form(key='doc_permit_small_medium_enterprises_handicraft_form'):
        id_or_passport = st.file_uploader("Upload ID or Passport", type=["pdf", "jpg", "png"])
        location_map_architecture = st.file_uploader("Upload Location Map/Architecture Layouts/Process Flow", type=["pdf", "jpg", "png"])
        letter_local_authority = st.file_uploader("Upload Letter from Local Authority", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                id_or_passport.read() if id_or_passport else None,
                location_map_architecture.read() if location_map_architecture else None,
                letter_local_authority.read() if letter_local_authority else None,
                selected_applicant_id,
                selected_company_id,
                selected_factory_id
            ]

            submit_form(
                table_name='doc_permit_smallmediumenterprices_handicraft',
                columns=[
                    'ID_Or_passport', 'LocationMap_Architecture_layouts_process_flow',
                    'Latter_local_Authority', 'ApplicantID', 
                    'CompanyID', 'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_factory_manager_form():
    st.title("Submit Information for Factory Manager")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_factory_manager_form'):
        name = st.text_input("Name")
        nationality = st.text_input("Nationality")
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        age = st.text_input("Age")
        phone = st.text_input("Phone")
        professional = st.text_input("Professional")
        expertise_working_experience = st.text_area("Expertise/Working Experience Related to Proposed Works")
        number_employee_production = st.text_input("Number of Employees in Production Section")
        number_employee_service = st.text_input("Number of Employees in Service Section")
        number_employee_other = st.text_input("Number of Employees in Other Section")
        total_employees = st.text_input("Total Employees")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                name,
                nationality,
                gender,
                age,
                phone,
                professional,
                expertise_working_experience,
                number_employee_production,
                number_employee_service,
                number_employee_other,
                total_employees,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_factory_manager',
                columns=[
                    'name', 'Nationality', 'gender', 'age', 'phone', 'professional',
                    'expertiseworkingexperience_related_proposed_works',
                    'Number_employee_production_section',
                    'Number_employee_service_section',
                    'Number_employee_other_section', 'Total_employees', 'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_quality_controlprogram_form():
    st.title("Submit Information for Quality Control Program")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_quality_controlprogram_form'):
        describe_processing_flow = st.text_area("Describe Processing Flow")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                describe_processing_flow,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_quality_controlprogram',
                columns=['DescribeprocessingFlow', 'FactoryID'],
                form_inputs=form_inputs
            )

def submit_infor_investment_asset_form():
    st.title("Submit Information for Investment Asset")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_investment_asset_form'):
        total_values_machinery_facilities = st.text_input("Total Estimated Values of Machinery & Facilities")
        total_values_vehicle_transportation = st.text_input("Total Estimated Values of Vehicle & Transportation")
        total_values_building = st.text_input("Total Estimated Values of Building")
        total_values_other_fixed_assets = st.text_input("Total Estimated Values of Other Fixed Assets")
        total_values_working_capital = st.text_input("Total Estimated Values of Working Capital")
        total_values_investment = st.text_input("Total Estimated Values of Investment")
        source_investment = st.text_input("Source of Investment")
        estimated_percentage = st.text_input("Estimated Percentage")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                total_values_machinery_facilities,
                total_values_vehicle_transportation,
                total_values_building,
                total_values_other_fixed_assets,
                total_values_working_capital,
                total_values_investment,
                source_investment,
                estimated_percentage,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_investment_asset',
                columns=[
                    'Total_Estimated_values_machinery_facilities',
                    'Total_Estimated_values_vehicle_transpotation',
                    'Total_estimated_values_building',
                    'Total_estimate_values_other_fixed_assets',
                    'Total_estimated_values_working_capital',
                    'Total_estimated_values_investment',
                    'Souce_Investment',
                    'Estimated_percentage',
                    'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_machinery_facilities_form():
    st.title("Submit Information for Machinery Facilities")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_machinery_facilities_form'):
        list_machinery_facilities = st.text_input("List of Machinery Facilities")
        unit = st.text_input("Unit")
        quantity = st.text_input("Quantity")
        amount = st.text_input("Amount")
        domestic = st.text_input("Domestic")
        import_from = st.text_input("Import From")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                list_machinery_facilities,
                unit,
                quantity,
                amount,
                domestic,
                import_from,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_machinery_facilities',
                columns=[
                    'List_Machinery_facilities',
                    'Unit',
                    'Quatity',
                    'Amount',
                    'Domestic',
                    'ImportFrom',
                    'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_planed_product_output_form():
    st.title("Submit Planned Product Output Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_planed_product_output_form'):
        description_products = st.text_input("Description of Products")
        unit = st.text_input("Unit")
        quantity_first_year = st.text_input("Quantity for First Year")
        amount_first_year = st.text_input("Amount for First Year")
        domestic_percentage_market = st.text_input("Domestic Market Percentage")
        export_percentage_market = st.text_input("Export Market Percentage")
        quantity_full_capacity = st.text_input("Quantity at Full Capacity")
        amount_full_capacity = st.text_input("Amount at Full Capacity")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                description_products,
                unit,
                quantity_first_year,
                amount_first_year,
                domestic_percentage_market,
                export_percentage_market,
                quantity_full_capacity,
                amount_full_capacity,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_planed_product_output',
                columns=[
                    'Description_Products', 'Unit', 'Quantity_firs_year', 'Amount_first_year',
                    'Domestic_percentage_market', 'Export_percentage_market', 'Quantity_full_capacity',
                    'Amount_full_capacity', 'FactoryID'
                ],
                form_inputs=form_inputs
            )

def submit_infor_product_waste_form():
    st.title("Submit Product Waste Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_product_waste_form'):
        solid_waste = st.text_input("Solid Waste")
        liquid_waste = st.text_input("Liquid Waste")
        emission_waste = st.text_input("Emission Waste")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                solid_waste,
                liquid_waste,
                emission_waste,
                selected_factory_id
            ]

            submit_form(
                table_name='infor_product_waste',
                columns=['Solid_waste', 'Liquid_waste', 'Emission_waste', 'FactoryID'],
                form_inputs=form_inputs
            )

def submit_applic_calibration_metrology_form():
    st.title("Submit Calibration Metrology Application Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address', ['AddressID', 'officeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID', 'KhmerName'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]: row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: row[1] for row in personal_info_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='applic_calibration_metrology_form'):
        request_details = st.text_area("Request Details")

        # Dropdown for selecting AddressID, FactoryID, CompanyID, PersonalInforForApplicantID, ProductID
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant's Personal Information", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_address_id,
                selected_factory_id,
                selected_company_id,
                selected_personal_info_id,
                selected_product_id
            ]

            submit_form(
                table_name='applic_calibration_metrology',
                columns=[
                    'RequestDetails',
                    'addresstID',
                    'FactoryID',
                    'CompanyID',
                    'PersonalInforForApplicantID',
                    'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metrology_calibration_form():
    st.title("Submit Metrology Calibration Application Documents")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_metrology_calibration_form'):
        statute_technical = st.file_uploader("Upload Technical Statute", type=["pdf", "jpg", "jpeg", "png"])
        transfer_letter = st.file_uploader("Upload Transfer Letter", type=["pdf", "jpg", "jpeg", "png"])
        id_passport_card = st.file_uploader("Upload ID or Passport Card", type=["pdf", "jpg", "jpeg", "png"])

        # Dropdown for selecting ApplicationMetrologyID
        selected_application_id = st.selectbox("Select Application Metrology ID", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Convert uploaded files to bytes
            statute_technical_blob = statute_technical.getvalue() if statute_technical else None
            transfer_letter_blob = transfer_letter.getvalue() if transfer_letter else None
            id_passport_card_blob = id_passport_card.getvalue() if id_passport_card else None

            form_inputs = [
                statute_technical_blob,
                transfer_letter_blob,
                id_passport_card_blob,
                selected_application_id
            ]

            submit_form(
                table_name='doc_applic_metrology_calibration',
                columns=[
                    'Statute_technical',
                    'Transfer_latter',
                    'ID_passport_card',
                    'ApplicationMetrologyID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_license_repair_metrology_form():
    st.title("Submit License Repair Metrology Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    adddress_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='applic_license_repair_metrology_form'):
        request_details = st.text_area("Request Details")

        # Dropdown for selecting AddressID, FactoryID, CompanyID, PersonalInforForApplicantID, ProductID
        selected_address_id = st.selectbox("Select Address", options=list(adddress_options.keys()), format_func=lambda x: adddress_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_address_id,
                selected_factory_id,
                selected_company_id,
                selected_personal_info_id,
                selected_product_id
            ]

            submit_form(
                table_name='applic_license_repair_metrology',
                columns=[
                    'RequestDetails',
                    'addresstID',
                    'FactoryID',
                    'CompanyID',
                    'PersonalInforForApplicantID',
                    'ProductID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_metro_verify_form():
    st.title("Submit Metrology Verification Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    adddress_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_metro_verify_form'):
        request_details = st.text_area("Request Details")

        # Dropdowns for selecting addressID, FactoryID, CompanyID, PersonalInforForApplicantID
        selected_address_id = st.selectbox("Select Address", options=list(adddress_options.keys()), format_func=lambda x: adddress_options[x])
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_address_id,
                selected_factory_id,
                selected_company_id,
                selected_personal_info_id
            ]

            submit_form(
                table_name='applic_metro_verify',
                columns=[
                    'RequestDetails',
                    'addressID',
                    'FactoryID',
                    'CompanyID',
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_certific_recog_metro_expertise_form():
    st.title("Submit Application for Certificate Recognition in Metrology Expertise")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    adddress_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}
    with st.form(key='applic_certific_recog_metro_expertise_form'):
        # File uploader for Photo Application
        photo_application = st.file_uploader("Upload Photo Application", type=["jpg", "png", "jpeg"])

        request_details = st.text_area("Request Details")
        foreign_languages = st.text_input("Foreign Languages")
        general_education_level = st.text_input("General Education Level")
        work_history = st.text_area("Work History")

        # Dropdowns for selecting FactoryID, CompanyID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(adddress_options.keys()), format_func=lambda x: adddress_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Process the photo upload
            if photo_application:
                photo_data = photo_application.read()

            form_inputs = [
                photo_data if photo_application else None,
                request_details,
                selected_factory_id,
                selected_company_id,
                selected_address_id,
                foreign_languages,
                general_education_level,
                work_history,
                selected_personal_info_id
            ]

            submit_form(
                table_name='applic_certific_recog_metro_expertise',
                columns=[
                    'Photo_application',
                    'RequestDetails',
                    'FactoryID',
                    'CompanyID',
                    'addressID',
                    'ForeignLanguages',
                    'GeneralEducationLevel',
                    'WorkHistory',
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_checking_importpermmetro_equipment_form():
    st.title("Submit Application for Checking Import Permission of Metrology Equipment")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['addressID', 'officeAddress'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_checking_importpermmetro_equipment_form'):
        request_details = st.text_area("Request Details")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_factory_id,
                selected_company_id,
                selected_address_id,
                selected_personal_info_id
            ]

            submit_form(
                table_name='applic_checking_importpermmetro_equipment',
                columns=[
                    'RequestDetails',
                    'FactoryID',
                    'CompanyID',
                    'addressID',
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_prototype_approval_certificate_form():
    st.title("Submit Application for Prototype Approval Certificate")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['addressID', 'officeAddress'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_prototype_approval_certificate_form'):
        request_details = st.text_area("Request Details")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_factory_id,
                selected_company_id,
                selected_address_id,
                selected_personal_info_id
            ]

            submit_form(
                table_name='applic_prototype_approval_certificate',
                columns=[
                    'RequestDetails',
                    'FactoryID',
                    'CompanyID',
                    'addressID',
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_applic_certific_recognition_internal_indu_form():
    st.title("Submit Application for Internal Industry Certification Recognition")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    address_data = db_helper.fetch_data('address', ['addressID', 'officeAddress'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    address_options = {row[0]: row[1] for row in address_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_certific_recognition_internal_indu_form'):
        request_details = st.text_area("Request Details")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("Select Factory", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("Select Applicant", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                request_details,
                selected_factory_id,
                selected_company_id,
                selected_address_id,
                selected_personal_info_id
            ]

            submit_form(
                table_name='applic_certific_recognition_internal_indu',
                columns=[
                    'RequestDetails',
                    'FactoryID',
                    'CompanyID',
                    'addressID',
                    'PersonalInforForApplicantID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_licese_cam_metrotrand_form():
    st.title("Submit Application License for Cambodia Metrology and Standards")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_licese_cam_metrotrand_form'):
        # File uploader for each document
        metrology_registration_certificate = st.file_uploader("Metrology Registration Certificate", type=['pdf', 'jpg', 'png'])
        statute_company = st.file_uploader("Statute Company", type=['pdf', 'jpg', 'png'])
        expired_license = st.file_uploader("Expired License Use Cambodia Metrology", type=['pdf', 'jpg', 'png'])
        inspection_certificate = st.file_uploader("Inspection Verification Certificate", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting ApplicationMetrologyID
        selected_application_id = st.selectbox("Select Application Metrology", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
           
            form_inputs = [

                metrology_registration_certificate.read() if metrology_registration_certificate else None,
                statute_company.read() if statute_company else None,
                expired_license.read() if expired_license else None,
                inspection_certificate.read() if inspection_certificate else None,
                selected_application_id
            ]

            # Submit form using the helper function
            submit_form(
                table_name='doc_applic_licese_cam_metrotrand',
                columns=[
                    'Metrology_Registration_certificate',
                    'Statute_campany',
                    'Expired_License_use_Cambodia_metrology',
                    'Inspection_Verification_Certificate',
                    'ApplicationMetrologyID'
                ],
                form_inputs=form_inputs
            )

def submit_metrology_instrument_form():
    st.title("Submit Metrology Instrument Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])
    prototype_approval_data = db_helper.fetch_data('applic_prototype_approval_certificate', ['Applicatio_Prototype_Approval_CertificateID'])
    recognition_internal_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])
    doc_license_data = db_helper.fetch_data('doc_applic_licese_cam_metrotrand', ['DocAppliLiceUseCamMetroTrandID'])
    import_permision_equipment= db_helper.fetch_data('applic_checking_importpermmetro_equipment',['ApplicationImportPermissionMetrologyEquipmentID'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {row[0]: row[1] for row in product_data}
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}
    repair_options = {row[0]: f"Application License Repair Metrology ID: {row[0]}" for row in license_repair_data}
    prototype_options = {row[0]: f"Application Prototype Approval Certificate ID: {row[0]} " for row in prototype_approval_data}
    recognition_options = {row[0]: f"Application Certificate Recognition Internal Industry ID: {row[0]} "for row in recognition_internal_data}
    license_in_cambodia_options = {row[0]: f"Document Application License Metrology Using in Cambodia ID: {row[0]}" for row in doc_license_data}
    application_permision_import_options = {row[0]: f"Application Checking Import Permision Metrology Equipment ID: {row[0]}" for row in import_permision_equipment}

    with st.form(key='metrology_instrument_form'):
        instrument_name = st.text_input("Instrument Name")
        serial_number = st.text_input("Serial Number")
        calibration_level = st.text_input("Calibration Level")
        calibration_number = st.text_input("Calibration Number")
        other = st.text_area("Other Information")
        calibration_certificate_number = st.text_input("Calibration Certificate Number")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_application_id = st.selectbox("Select Application Metrology", options=list(application_options.keys()), format_func=lambda x: application_options[x])
        selected_Repair_License_id= st.selectbox("Select License Repair Metrology", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])
        selected_Prototype_Approval_id = st.selectbox("Select Prototype Approval", options=list(prototype_options.keys()), format_func=lambda x: prototype_options[x])
        selected_recognition_id = st.selectbox("Select Recognition Internal", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])
        selected_License_Metrology_Cambodia_id = st.selectbox("Select License Metrology Using in Cambodia", options=list(license_in_cambodia_options.keys()), format_func=lambda x: license_in_cambodia_options[x])
        selected_permision_import_id = st.selectbox("Select License", options=list(application_permision_import_options.keys()), format_func=lambda x: application_permision_import_options[x])
        
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                instrument_name,
                serial_number,
                calibration_level,
                calibration_number,
                other,
                calibration_certificate_number,
                selected_product_id,
                selected_application_id,
                selected_Repair_License_id,
                selected_Prototype_Approval_id,
                selected_recognition_id,
                selected_License_Metrology_Cambodia_id,
                selected_permision_import_id,
            ]

            submit_form(
                table_name='metrology_intrument',
                columns=[
                    'Intrument_name',
                    'Serial_number',
                    'Calibratio_level',
                    'Calibration_Number',
                    'Other',
                    'Calibration_certificate_number',
                    'ProductID',
                    'ApplicationMetrologyID',
                    'licenserepair_metrologyId',
                    'Applicatio_Prototype_Approval_CertificateID',
                    'idApplicationCertificateRecognitionInternal',
                    'DocAppliLiceUseCamMetroTrandID',
                    'ApplicationImportPermissionMetrologyEquipmentID'
                ],
                form_inputs=form_inputs
            )

def submit_certificate_calibration_form():
    st.title("Submit Calibration Certificate Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    calibration_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    calibration_options = {row[0]: f"Application Metrology ID: {row[0]}" for row in calibration_data}
    repair_options = {row[0]: f"Repair License ID: {row[0]}" for row in repair_data}

    with st.form(key='certificate_calibration_form'):
        result_calibration_no = st.number_input("Result Calibration Number", min_value=0, step=1)

        # Dropdowns for selecting foreign keys
        selected_calibration_id = st.selectbox("Select Application Metrology", options=list(calibration_options.keys()), format_func=lambda x: calibration_options[x])
        selected_repair_id = st.selectbox("Select Repair License", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                result_calibration_no,
                selected_repair_id,
                selected_calibration_id,
            ]

            submit_form(
                table_name='certificate_calibration',
                columns=[
                    'Result_Calibration_No',
                    'licenserepair_metrologyId',
                    'ApplicationMetrologyID'
                ],
                form_inputs=form_inputs
            )

def submit_instrument_infor_form():
    st.title("Submit Instrument Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    metrology_instrument_data = db_helper.fetch_data('metrology_intrument', ['idMetrologyIntrument'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_options = {row[0]: f"Instrument ID: {row[0]}" for row in metrology_instrument_data}

    with st.form(key='instrument_infor_form'):
        product_capability = st.text_input("Product Capability")
        produce_country = st.text_input("Country of Production")
        location_using = st.text_input("Location of Use")

        # Dropdown for selecting Metrology Instrument ID
        selected_instrument_id = st.selectbox("Select Metrology Instrument", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                product_capability,
                produce_country,
                location_using,
                selected_instrument_id,
            ]

            submit_form(
                table_name='intrument_infor',
                columns=[
                    'Product_capability',
                    'Produce_Country',
                    'Location_using',
                    'idMetrologyIntrument'
                ],
                form_inputs=form_inputs
            )

def submit_instrument_detail_repair_form():
    st.title("Submit Instrument Detail for Repair")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    metrology_instrument_data = db_helper.fetch_data('metrology_intrument', ['idMetrologyIntrument'])
    repair_license_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_options = {row[0]: f"Instrument ID: {row[0]}" for row in metrology_instrument_data}
    repair_options = {row[0]: f"Repair License ID: {row[0]}" for row in repair_license_data}

    with st.form(key='instrument_detail_repair_form'):
        name_metrology_list = st.text_input("Name of Metrology List")
        quantity = st.text_input("Quantity")
        code_number = st.text_input("Code Number")
        condition = st.text_input("Condition")
        description_technical_specifications = st.text_area("Technical Specifications Description")

        # Dropdowns for selecting foreign keys
        selected_repair_id = st.selectbox("Select Repair License", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])
        selected_instrument_id = st.selectbox("Select Metrology Instrument", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                name_metrology_list,
                quantity,
                code_number,
                condition,
                description_technical_specifications,
                selected_repair_id,
                selected_instrument_id
            ]

            submit_form(
                table_name='intrument_detail_repair',
                columns=[
                    'NameMetrologylist',
                    'Quantity',
                    'Code_number',
                    'Condition_Company',
                    'Description_Technical',
                    'licenserepair_metrologyId',
                    'idMetrologyIntrument'
                ],
                form_inputs=form_inputs
            )

def submit_result_of_calibration_form():
    st.title("Submit Result of Calibration")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    metrology_instrument_data = db_helper.fetch_data('metrology_intrument', ['idMetrologyIntrument'])
    instrument_detail_repair_data = db_helper.fetch_data('intrument_detail_repair', ['idIntrumentDetailforRepair'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {row[0]: row[1] for row in product_data}
    instrument_options = {row[0]: f"Instrument ID: {row[0]}" for row in metrology_instrument_data}
    detail_repair_options = {row[0]: f"Repair Detail ID: {row[0]}" for row in instrument_detail_repair_data}

    with st.form(key='result_of_calibration_form'):
        model = st.text_input("Model")
        method_calibration = st.text_input("Method of Calibration")
        accept_date = st.date_input("Accept Date")
        date_calibration = st.date_input("Date of Calibration",min_value=datetime(1990,1,1))
        date_recalibration = st.date_input("Date of Recalibration",min_value=datetime(1990,1,1))

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_instrument_id = st.selectbox("Select Metrology Instrument", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])
        selected_detail_repair_id = st.selectbox("Select Instrument Detail for Repair", options=list(detail_repair_options.keys()), format_func=lambda x: detail_repair_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                model,
                method_calibration,
                accept_date,
                date_calibration,
                date_recalibration,
                selected_product_id,
                selected_instrument_id,
                selected_detail_repair_id
            ]

            submit_form(
                table_name='result_of_calibration',
                columns=[
                    'Model',
                    'Method_calibration',
                    'accept_date',
                    'date_calibration',
                    'date_recalibration',
                    'ProductID',
                    'idMetrologyIntrument',
                    'idIntrumentDetailforRepair'
                ],
                form_inputs=form_inputs
            )

def submit_business_infor_form():
    st.title("Submit Business Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    instrument_infor_data = db_helper.fetch_data('intrument_infor', ['idIntrumentInfor'])
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_infor_options = {row[0]: f"Instrument Information ID: {row[0]}" for row in instrument_infor_data}
    license_repair_options = {row[0]: f"License Repair ID: {row[0]}" for row in license_repair_data}

    with st.form(key='business_infor_form'):
        type_business = st.text_input("Type of Business")
        business_characteristics = st.text_area("Business Characteristics")
        initial_capital = st.text_input("Initial Capital")
        business_location_size = st.text_input("Business Location Size")

        # Dropdowns for selecting foreign keys
        selected_instrument_infor_id = st.selectbox("Select Instrument Information", options=list(instrument_infor_options.keys()), format_func=lambda x: instrument_infor_options[x])
        selected_license_repair_id = st.selectbox("Select License Repair", options=list(license_repair_options.keys()), format_func=lambda x: license_repair_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                type_business,
                business_characteristics,
                initial_capital,
                business_location_size,
                selected_instrument_infor_id,
                selected_license_repair_id
            ]

            submit_form(
                table_name='business_infor',
                columns=[
                    'Type_Business',
                    'Business_Characteristics',
                    'Initial_Capital',
                    'Business_Location_size',
                    'idIntrumentInfor',
                    'licenserepair_metrologyId'
                ],
                form_inputs=form_inputs
            )

def submit_workforce_form():
    st.title("Submit Workforce Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    business_infor_data = db_helper.fetch_data('business_infor', ['idBusinessInfor'])

    db_helper.close_connection()

    # Prepare dropdown options
    business_infor_options = {row[0]: f"Business Information ID: {row[0]}" for row in business_infor_data}

    with st.form(key='workforce_form'):
        technicians = st.text_input("Technicians")
        total_workforce = st.text_input("Total Workforce")

        # Dropdown for selecting Business Information ID
        selected_business_infor_id = st.selectbox("Select Business Information", options=list(business_infor_options.keys()), format_func=lambda x: business_infor_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                technicians,
                total_workforce,
                selected_business_infor_id
            ]

            submit_form(
                table_name='workforce',
                columns=[
                    'Techniicians',
                    'Total_workforce',
                    'idBusinessInfor'
                ],
                form_inputs=form_inputs
            )

def submit_family_infor_form():
    st.title("Submit Family Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address', ['addressID', 'OfficeAddress'])
    certificate_recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]: f"Address ID: {row[0]} - {row[1]}" for row in address_data}
    certificate_recognition_options = {row[0]: f"Certificate Recognition Internal ID: {row[0]}" for row in certificate_recognition_data}

    with st.form(key='family_infor_form'):
        name_of_spouse = st.text_input("Name of Husband or Wife")
        date_of_birth = st.date_input("Date of Birth",min_value=datetime(1990,1,1))
        number_of_children = st.number_input("Number of Daughters and Sons", min_value=0, step=1)
        occupation = st.text_input("Occupation")

        # Dropdown for selecting Address ID and Application Certificate Recognition Internal ID
        selected_address_id = st.selectbox("Select Address", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_certificate_recognition_id = st.selectbox("Select Application Certificate Recognition Internal", options=list(certificate_recognition_options.keys()), format_func=lambda x: certificate_recognition_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                name_of_spouse,
                date_of_birth,
                number_of_children,
                occupation,
                selected_address_id,
                selected_certificate_recognition_id
            ]

            submit_form(
                table_name='family_infor',
                columns=[
                    'name_of_husband_or_wife',
                    'bod',
                    'number_of_daughter_and_son',
                    'occupation',
                    'addressID',
                    'idApplicationCertificateRecognitionInternal'
                ],
                form_inputs=form_inputs
            )

def submit_background_application_form():
    st.title("Submit Background Application Information")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    family_info_data = db_helper.fetch_data('family_infor', ['idfamilyInfor', 'name_of_husband_or_wife'])

    db_helper.close_connection()

    # Prepare dropdown options
    family_info_options = {row[0]: f"Family Info ID: {row[0]} - {row[1]}" for row in family_info_data}

    with st.form(key='background_application_form'):
        language = st.text_input("Language")
        education_level = st.text_input("Education Level")
        any_training = st.text_input("Any Training")
        work_experience = st.text_area("Work Experience")
        background_application_col = st.text_area("Additional Background Information")

        # Dropdown for selecting Family Information ID
        selected_family_info_id = st.selectbox("Select Family Information", options=list(family_info_options.keys()), format_func=lambda x: family_info_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                language,
                education_level,
                any_training,
                work_experience,
                background_application_col,
                selected_family_info_id
            ]

            submit_form(
                table_name='background_application',
                columns=[
                    'language',
                    'education_level',
                    'any_training',
                    'work_experience',
                    'background_applicationcol',
                    'idfamilyInfor'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metrology_calibration_form():
    st.title("Submit Metrology Calibration Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_metrology_calibration_form'):
        # File uploaders for each document
        statute_technical = st.file_uploader("Statute Technical", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology ID
        selected_application_id = st.selectbox("Select Application Metrology", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                statute_technical.read() if statute_technical else None,
                transfer_letter.read() if transfer_letter else None,
                id_passport_card.read() if id_passport_card else None,
                selected_application_id
            ]

            submit_form(
                table_name='doc_applic_metrology_calibration',
                columns=[
                    'Statute_technical',
                    'Transfer_latter',
                    'ID_passport_card',
                    'ApplicationMetrologyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metro_calibra_second_form():
    st.title("Submit Second Metrology Calibration Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_metro_calibra_second_form'):
        # File uploaders for each document
        expired_metrology_certificate = st.file_uploader("Expired Metrology Certificate", type=['pdf', 'jpg', 'png'])
        photograph_4x6cm = st.file_uploader("4x6 cm Photograph", type=['jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology ID
        selected_application_id = st.selectbox("Select Application Metrology", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                expired_metrology_certificate.read() if expired_metrology_certificate else None,
                photograph_4x6cm.read() if photograph_4x6cm else None,
                id_passport_card.read() if id_passport_card else None,
                selected_application_id
            ]

            submit_form(
                table_name='doc_applic_metro_calibra_second',
                columns=[
                    'Expired_metrology_certificate',
                    'Photograph4x6cm',
                    'ID_passport_card',
                    'ApplicationMetrologyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_license_repair_metrology_form():
    st.title("Submit License Repair Metrology Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    repair_license_options = {row[0]: f"License Repair ID: {row[0]}" for row in license_repair_data}

    with st.form(key='doc_applic_license_repair_metrology_form'):
        # File uploaders for each document
        expired_license_repair = st.file_uploader("Expired License Repair Metrology Equipment", type=['pdf', 'jpg', 'png'])
        metrology_registration_certificate = st.file_uploader("Metrology Registration Certificate", type=['pdf', 'jpg', 'png'])
        specialization_certificate = st.file_uploader("Certificate or Proof of Specialization of Applicant", type=['pdf', 'jpg', 'png'])
        technical_drawings = st.file_uploader("Technical Drawings of Requested Metrology Equipment", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card", type=['pdf', 'jpg', 'png'])
        transfer_rights_letter = st.file_uploader("Transfer Rights Letter", type=['pdf', 'jpg', 'png'])
        statute_company = st.file_uploader("Statute Company", type=['pdf', 'jpg', 'png'])
        photograph_4x6 = st.file_uploader("4x6 Photograph", type=['jpg', 'png'])

        # Dropdown for selecting License Repair ID
        selected_license_repair_id = st.selectbox("Select License Repair", options=list(repair_license_options.keys()), format_func=lambda x: repair_license_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                expired_license_repair.read() if expired_license_repair else None,
                metrology_registration_certificate.read() if metrology_registration_certificate else None,
                specialization_certificate.read() if specialization_certificate else None,
                technical_drawings.read() if technical_drawings else None,
                identification_card.read() if identification_card else None,
                transfer_rights_letter.read() if transfer_rights_letter else None,
                statute_company.read() if statute_company else None,
                photograph_4x6.read() if photograph_4x6 else None,
                selected_license_repair_id
            ]

            submit_form(
                table_name='doc_applic_license_repair_metrology',
                columns=[
                    'ExpiredLicenseRepairMetrologyEquipment',
                    'MetrologyRegistrationCertificate',
                    'CertificateOrProofSpecializationofApplicant',
                    'TechnicalDrawingsfRequestedMetrologyEquipment',
                    'IdentificationCard',
                    'TransferRightsLetter',
                    'Statute_company',
                    'Photograph4x6',
                    'licenserepair_metrologyId'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metrology_verify_form():
    st.title("Submit Metrology Verification Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]}" for row in verification_data}

    with st.form(key='doc_applic_metrology_verify_form'):
        # File uploaders for each document
        transfer_letter = st.file_uploader("Transfer Letter", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                transfer_letter.read() if transfer_letter else None,
                id_passport_card.read() if id_passport_card else None,
                selected_verification_id
            ]

            submit_form(
                table_name='doc_applic_metrology_verify',
                columns=[
                    'Transfer_latter',
                    'ID_passport_card',
                    'ApplicationMetrologyVerifyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metro_verify_second_form():
    st.title("Submit Second Metrology Verification Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]}" for row in verification_data}

    with st.form(key='doc_applic_metro_verify_second_form'):
        # File uploader for initial verification document
        initial_verification = st.file_uploader("Initial Verification Previous Usage", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                initial_verification.read() if initial_verification else None,
                selected_verification_id
            ]

            submit_form(
                table_name='doc_applic_metro_verify_second',
                columns=[
                    'Initial_verification_previous_usage',
                    'ApplicationMetrologyVerifyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_metro_verify_third_form():
    st.title("Submit Third Metrology Verification Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]}" for row in verification_data}

    with st.form(key='doc_applic_metro_verify_third_form'):
        # File uploaders for documents
        info_image_imported = st.file_uploader("Information Image of Imported Package", type=['pdf', 'jpg', 'png'])
        technical_doc_imported = st.file_uploader("Technical Document of Imported Package", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                info_image_imported.read() if info_image_imported else None,
                technical_doc_imported.read() if technical_doc_imported else None,
                selected_verification_id
            ]

            submit_form(
                table_name='doc_applic_metro_verifythird',
                columns=[
                    'Infor_image_imported_packaged',
                    'Doc_technical_imported_packaged',
                    'ApplicationMetrologyVerifyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_appli_metro_verify_import_forth_form():
    st.title("Submit Fourth Metrology Verification Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]}" for row in verification_data}

    with st.form(key='doc_appli_metro_verify_import_forth_form'):
        # File uploader for technical document
        technical_doc_imported = st.file_uploader("Technical Document of Imported Package", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                technical_doc_imported.read() if technical_doc_imported else None,
                selected_verification_id
            ]

            submit_form(
                table_name='doc_appli_metro_verify_importforth',
                columns=[
                    'Doc_technical_imported_packaged',
                    'ApplicationMetrologyVerifyID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applc_certific_recogin_form():
    st.title("Submit Certificate Recognition Document Application")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    recognition_options = {row[0]: f"Recognition Application ID: {row[0]}" for row in recognition_data}

    with st.form(key='doc_applc_certific_recogin_form'):
        # File uploaders for each document
        transfer_letter = st.file_uploader("Transfer Letter", type=['pdf', 'jpg', 'png'])
        passport_card = st.file_uploader("ID Passport Card", type=['pdf', 'jpg', 'png'])
        certificate_recognition = st.file_uploader("Certificate of Metrology Expertise Recognition", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Certificate Recognition Internal ID
        selected_recognition_id = st.selectbox("Select Application Certificate Recognition Internal", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                transfer_letter.read() if transfer_letter else None,
                passport_card.read() if passport_card else None,
                certificate_recognition.read() if certificate_recognition else None,
                selected_recognition_id
            ]

            submit_form(
                table_name='doc_applc_certific_recogin',
                columns=[
                    'Transfer_latter',
                    'ID_passport_card',
                    'Certificate_metrology_expertise_recognition',
                    'idApplicationCertificateRecognitionInternal'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_certif_recog_expertise_form():
    st.title("Submit Document for Certification Recognition Expertise")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    recognition_options = {row[0]: f"Recognition ID: {row[0]}" for row in recognition_data}

    with st.form(key='doc_applic_certif_recog_expertise_form'):
        training_certificate = st.file_uploader("Training Certificate", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card", type=['pdf', 'jpg', 'png'])
        photo_4x6 = st.file_uploader("4x6 Photo", type=['jpg', 'png'])

        # Dropdown for selecting Application Certificate Recognition Internal ID
        selected_recognition_id = st.selectbox("Select Recognition Application", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                training_certificate.read() if training_certificate else None,
                identification_card.read() if identification_card else None,
                photo_4x6.read() if photo_4x6 else None,
                selected_recognition_id
            ]

            submit_form(
                table_name='doc_applic_certif_recog_expertise',
                columns=[
                    'TrainingCertificate',
                    'IdentificationCard',
                    'Photo4x6',
                    'idApplicationCertificateRecognitionInternal'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_protoapprove_certificate_form():
    st.title("Submit Document for Prototype Approval Certificate")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    prototype_data = db_helper.fetch_data('applic_prototype_approval_certificate', ['Applicatio_Prototype_Approval_CertificateID'])

    db_helper.close_connection()

    # Prepare dropdown options
    prototype_options = {row[0]: f"Prototype Approval ID: {row[0]}" for row in prototype_data}

    with st.form(key='doc_applic_protoapprove_certificate_form'):
        statute_technical = st.file_uploader("Statute Technical", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Prototype Approval Certificate ID
        selected_prototype_id = st.selectbox("Select Prototype Approval", options=list(prototype_options.keys()), format_func=lambda x: prototype_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                statute_technical.read() if statute_technical else None,
                transfer_letter.read() if transfer_letter else None,
                id_passport_card.read() if id_passport_card else None,
                selected_prototype_id
            ]

            submit_form(
                table_name='doc_applic_protoapprove_certificate',
                columns=[
                    'Statute_technical',
                    'Transfer_latter',
                    'ID_passport_card',
                    'Applicatio_Prototype_Approval_CertificateID'
                ],
                form_inputs=form_inputs
            )

def submit_doc_applic_importper_metroequi_form():
    st.title("Submit Document for Import Permission of Metrology Equipment")

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    import_permission_data = db_helper.fetch_data('applic_checking_importpermmetro_equipment', ['ApplicationImportPermissionMetrologyEquipmentID'])

    db_helper.close_connection()

    # Prepare dropdown options
    import_permission_options = {row[0]: f"Import Permission ID: {row[0]}" for row in import_permission_data}

    with st.form(key='doc_applic_importper_metroequi_form'):
        extract_of_information_picture = st.file_uploader("Extract of Information Picture", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Import Permission ID
        selected_import_permission_id = st.selectbox("Select Import Permission", options=list(import_permission_options.keys()), format_func=lambda x: import_permission_options[x])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            form_inputs = [
                extract_of_information_picture.read() if extract_of_information_picture else None,
                identification_card.read() if identification_card else None,
                transfer_letter.read() if transfer_letter else None,
                selected_import_permission_id
            ]

            submit_form(
                table_name='doc_applic_importper_metroequi',
                columns=[
                    'Extract_of_Information_Picture',
                    'Identification_Card',
                    'Transfer_latter',
                    'ApplicationImportPermissionMetrologyEquipmentID'
                ],
                form_inputs=form_inputs
            )