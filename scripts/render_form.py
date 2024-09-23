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


    with st.form(key='type_of_application_form'):
        title = st.text_input("Title / ចំណងជើង", placeholder="Enter the application title / បញ្ចូលចំណងជើងនៃពាក្យសុំ")
        description = st.text_area("Description / ការពិពណ៌នា", placeholder="Enter the description (optional) / បញ្ចូលការពិពណ៌នា (ស្រេចចិត្ត)")
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            submit_form(
                table_name='type_of_application', 
                columns=['Title', 'Description'], 
                form_inputs=[title, description]
            )

def submit_raw_water_source_form():
    
    with st.form(key='raw_water_source_form'):
        code = st.number_input("Code / លេខកូដ", min_value=1)
        RawWaterSource_name = st.text_input("Raw Water Source Name / ឈ្មោះប្រភពទឹកឆៅ")
        availability_year_round = st.selectbox("Availability Year Round / មានទឹកគ្រប់ឆ្នាំ", [0, 1])
        total_abstraction = st.number_input("Total Abstraction / បរិមាណទឹកសរុប", format="%.2f")
        Drawing_RawWater_PumpingStation = st.file_uploader("Upload Drawing Raw Water Pumping Station / ផ្ទុករូបភាពស្ថានីយបូមទឹកឆៅ", type=["png", "jpg", "jpeg"])
        Drawing_Water_Transmission_Network = st.file_uploader("Upload Drawing Water Transmission Network / ផ្ទុករូបភាពបណ្តាញបញ្ជូនទឹក", type=["png", "jpg", "jpeg"])
        Drawing_Water_Treatment_Plant = st.file_uploader("Upload Drawing Water Treatment Plant / ផ្ទុករូបភាពរោងចក្រកែច្នៃទឹក", type=["png", "jpg", "jpeg"])
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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

    with st.form(key='for_of_oficial_user_only_form'):
        safety_mark_number = st.text_input("Safety Mark Number / លេខសម្គាល់សុវត្ថិភាព")
        officer_number = st.text_input("Officer Number / លេខមន្រ្តី")
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            submit_form(
                table_name='for_of_oficial_user_only',
                columns=['SafetyMarkNumber', 'OfficerNumber'],
                form_inputs=[safety_mark_number, officer_number]
            )

def submit_company_form():

    db_helper = DatabaseHelper()
    type_of_application_data = db_helper.fetch_data('type_of_application', ['TypeOfApplicationID', 'Title'])
    db_helper.close_connection()
    
    if type_of_application_data:
        type_of_application_options = {str(row[1]): row[0] for row in type_of_application_data}
    else:
        st.error("No type of applications found. / មិនមានប្រភេទនៃពាក្យសុំត្រូវបានរកឃើញទេ។")
        return
    
    with st.form(key='company_form'):
        name = st.text_input("Company Name / ឈ្មោះក្រុមហ៊ុន")
        email = st.text_input("Email / អ៊ីមែល")
        address = st.text_input("Address / អាសយដ្ឋាន")
        phone = st.text_input("Phone / លេខទូរស័ព្ទ")
        location_plan = st.file_uploader("Upload Location Plan / ផ្ទុកផែនទីទីតាំង", type=["png", "jpg", "jpeg", "pdf"])
        selected_title = st.selectbox("Select Type of Application / ជ្រើសរើសប្រភេទនៃពាក្យសុំ", options=list(type_of_application_options.keys()))
        type_of_application_id = type_of_application_options[selected_title]
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            form_inputs = [name, email, address, phone, location_plan.read() if location_plan else None, type_of_application_id]
            submit_form(
                table_name='company',
                columns=['Name', 'Email', 'Address', 'Phone', 'LocationPlan', 'TypeOfApplicationID'],
                form_inputs=form_inputs
            )

def submit_company_signature_form():

    db_helper = DatabaseHelper()
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    db_helper.close_connection()
    
    company_options = {company[0]: company[1] for company in company_list}
    
    with st.form(key='company_signature_form'):
        name = st.text_input("Name / ឈ្មោះ", placeholder="Enter the name / បញ្ចូលឈ្មោះ")
        date = st.date_input("Date / កាលបរិច្ឆេទ")
        position = st.text_input("Position / មុខតំណែង", placeholder="Enter the position / បញ្ចូលមុខតំណែង")
        signature = st.file_uploader("Upload Signature or Fingerprint / ផ្ទុកហត្ថលេខា ឬ ក្រយ៉ៅដៃ", type=["png", "jpg", "jpeg"])
        stamp = st.file_uploader("Upload Stamp / ផ្ទុកត្រា", type=["png", "jpg", "jpeg"])
        company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            form_inputs = [name, date, position, signature.read() if signature else None, stamp.read() if stamp else None, company_id]
            submit_form(
                table_name='company_signatur_and_stamp',
                columns=['Name', 'Date', 'Position', 'SignatureOrFingerprint', 'Stamp', 'CompanyID'],
                form_inputs=form_inputs
            )

def submit_applicant_form():
  
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
        application_date = st.date_input("Application Date / កាលបរិច្ឆេទនៃពាក្យសុំ")
        local_rep_name = st.text_input("Local Representative Name / ឈ្មោះតំណាងក្នុងស្រុក")
        local_rep_position = st.text_input("Local Representative Position / មុខតំណែងតំណាងក្នុងស្រុក")
        local_rep_email = st.text_input("Local Representative Email / អ៊ីមែលតំណាងក្នុងស្រុក")
        local_rep_phone = st.text_input("Local Representative Phone / លេខទូរស័ព្ទតំណាងក្នុងស្រុក")
        local_rep_address = st.text_input("Local Representative Address / អាសយដ្ឋានតំណាងក្នុងស្រុក")
        local_rep_company_name = st.text_input("Local Representative Company Name / ឈ្មោះក្រុមហ៊ុនតំណាងក្នុងស្រុក")
        
        # Dropdowns for selecting IDs
        selected_company_name = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()))
        selected_company_id = company_options[selected_company_name]  # Fetch corresponding company ID

        selected_type_of_application_title = st.selectbox("Select Type of Application / ជ្រើសរើសប្រភេទនៃពាក្យសុំ", options=list(type_of_application_options.keys()))
        type_of_application_id = type_of_application_options[selected_type_of_application_title]  # Fetch corresponding type of application ID

        selected_official_user_name = st.selectbox("Select Official User / ជ្រើសរើសអ្នកប្រើប្រាស់ផ្លូវការ", options=list(official_user_options.keys()))
        selected_official_user_id = official_user_options[selected_official_user_name]  # Fetch corresponding official user ID

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            form_inputs = [
                application_date, local_rep_name, local_rep_position, local_rep_email, local_rep_phone, 
                local_rep_address, local_rep_company_name, selected_company_id, type_of_application_id, 
                selected_official_user_id
            ]
            submit_form(
                table_name='applicant',
                columns=[
                    'Applicationdate', 'LocalRepresentativeName', 'LocalRepresentativePosition', 'LocalRepresentativeEmail',
                    'LocalRepresentativePhone', 'LocalRepresentativeAddress', 'LocalRepresentativeCompanyName',
                    'ForOfficialUserOnlyID', 'TypeOfApplicationID', 'CompanyID'
                ],
                form_inputs=form_inputs
            )

def submit_personal_info_form():
  
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_data}

    with st.form(key='personal_info_form'):
        khmer_name = st.text_input("Khmer Name / ឈ្មោះជាភាសាខ្មែរ")
        latin_name = st.text_input("Latin Name / ឈ្មោះជាភាសាឡាតាំង")
        date_of_birth = st.date_input("Date of Birth / ថ្ងៃខែឆ្នាំកំណើត", min_value=datetime(1900,1,1))
        ethnicity = st.text_input("Ethnicity / ជនជាតិ")
        nationality = st.text_input("Nationality / សញ្ជាតិ")
        current_occupation = st.text_input("Current Occupation / មុខរបរបច្ចុប្បន្ន")
        gender = st.selectbox("Gender / ភេទ", options=["Male / ប្រុស", "Female / ស្រី", "Other / ផ្សេងៗ"])
        
        # Dropdown for selecting Applicant ID
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID', 'KhmerName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    personal_info_options = {row[0]: row[1] for row in personal_info_data}

    with st.form(key='id_card_passport_form'):
        id_card_or_passport_number = st.text_input("ID Card or Passport Number / លេខអត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន")
        issued_date = st.date_input("Issued Date / ថ្ងៃចេញ", min_value=datetime(1990,1,1))
        expiration_date = st.date_input("Expiration Date / ថ្ងៃផុតកំណត់", min_value=datetime(1990,1,1))
        
        # Dropdown for selecting Personal Information ID
        selected_personal_info_id = st.selectbox("Select Personal Information / ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួន", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID', 'KhmerName'])
    
    db_helper.close_connection()
    
    # Prepare dropdown options
    personal_info_options = {row[0]: row[1] for row in personal_info_data}

    with st.form(key='address_form'):
        house_number = st.text_input("House Number / លេខផ្ទះ")
        street = st.text_input("Street / ផ្លូវ")
        village = st.text_input("Village / ភូមិ")
        commune = st.text_input("Commune / ឃុំ")
        district = st.text_input("District / ស្រុក")
        province = st.text_input("Province / ខេត្ត")
        office_address = st.text_input("Office Address / អាសយដ្ឋានការិយាល័យ")
        currently_location = st.text_input("Currently Location / ទីតាំងបច្ចុប្បន្ន")
        
        # Dropdown for selecting Personal Information ID
        selected_personal_info_id = st.selectbox("Select Personal Information / ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួន", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
 
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    raw_water_sources = db_helper.fetch_data('raw_watersource', ['idRawWaterSource', 'RawWaterSource_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    raw_water_options = {row[0]: row[1] for row in raw_water_sources}

    with st.form(key='human_resources_form'):
        code = st.number_input("Code / លេខកូដ", min_value=0, step=1)
        human_resources_name = st.text_input("Human Resources Name / ឈ្មោះធនធានមនុស្ស")
        total_staff = st.number_input("Total Staff / បុគ្គលិកសរុប", min_value=0, step=1)
        staff_per_1000_subscribers = st.number_input("Staff per 1000 Subscribers / បុគ្គលិកក្នុងមួយពាន់អ្នកជាវ", format="%.2f")
        training_sessions = st.number_input("Training Sessions / វគ្គបណ្តុះបណ្តាល", min_value=0, step=1)
        organization_chart = st.file_uploader("Upload Organization Chart / ផ្ទុកតារាងអង្គភាព", type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"])

        # Dropdowns for selecting foreign key IDs
        selected_raw_water_source_id = st.selectbox("Select Raw Water Source / ជ្រើសរើសប្រភពទឹកឆៅ", options=list(raw_water_options.keys()), format_func=lambda x: raw_water_options[x])
    
        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
        if submit_button:
            # Handle the uploaded file (blob)
            organization_chart_blob = organization_chart.read() if organization_chart else None
            
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
 
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    raw_water_sources = db_helper.fetch_data('raw_watersource', ['idRawWaterSource', 'RawWaterSource_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    raw_water_options = {row[0]: row[1] for row in raw_water_sources}

    with st.form(key='treatment_plant_form'):
        code = st.number_input("Code / លេខកូដ", min_value=0, step=1)
        treatment_plant_name = st.text_input("Treatment Plant Name / ឈ្មោះរោងចក្រកែច្នៃទឹក")
        treatment_losses = st.number_input("Treatment Losses / ការបាត់បង់ក្នុងការកែច្នៃ", format="%.2f")
        pac_consumption = st.number_input("PAC Consumption / ការប្រើប្រាស់ PAC", format="%.2f")
        pac_per_m3_produced = st.number_input("PAC per m³ Produced / PAC ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        alum_consumption = st.number_input("Alum Consumption / ការប្រើប្រាស់ Alum", format="%.2f")
        alum_per_m3_produced = st.number_input("Alum per m³ Produced / Alum ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        chlorine_consumption = st.number_input("Chlorine Consumption / ការប្រើប្រាស់ក្លរ", format="%.2f")
        chlorine_per_m3_produced = st.number_input("Chlorine per m³ Produced / ក្លរ ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        electricity_consumption = st.number_input("Electricity Consumption / ការប្រើប្រាស់អគ្គិសនី", format="%.2f")
        electricity_per_m3_produced = st.number_input("Electricity per m³ Produced / អគ្គិសនី ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        lime_consumption = st.number_input("Lime Consumption / ការប្រើប្រាស់ស៊ីម៉ង់", format="%.2f")
        lime_per_m3_produced = st.number_input("Lime per m³ Produced / ស៊ីម៉ង់ ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        fuel_consumption = st.number_input("Fuel Consumption / ការប្រើប្រាស់ប្រេងឥន្ធនៈ", format="%.2f")
        fuel_per_m3_produced = st.number_input("Fuel per m³ Produced / ប្រេងឥន្ធនៈ ក្នុងមួយម៉ែត្រគូបផលិត", format="%.2f")
        production_capacity = st.number_input("Production Capacity / សមត្ថភាពផលិត", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_raw_water_source_id = st.selectbox("Select Raw Water Source / ជ្រើសរើសប្រភពទឹកឆៅ", options=list(raw_water_options.keys()), format_func=lambda x: raw_water_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
 
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    treatment_plants = db_helper.fetch_data('treatment_plant', ['idTreatmentPlant', 'TreatmentPlant_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    treatment_plant_options = {row[0]: row[1] for row in treatment_plants}

    with st.form(key='water_quality_form'):
        code = st.number_input("Code / លេខកូដ", min_value=0, step=1)
        water_quality_name = st.text_input("Water Quality Name / ឈ្មោះគុណភាពទឹក")
        color = st.number_input("Color / ពណ៌", format="%.2f")
        turbidity = st.number_input("Turbidity / ភាពអាប់អួរ", format="%.2f")
        ph_level = st.number_input("pH Level / កម្រិត pH", format="%.2f")
        arsenic_level = st.number_input("Arsenic Level / កម្រិតអាសេនិក", format="%.2f")
        total_dissolved_solids = st.number_input("Total Dissolved Solids / សារធាតុរលាយសរុប", format="%.2f")
        manganese_level = st.number_input("Manganese Level / កម្រិតម៉ង់ហ្គាណែ", format="%.2f")
        zinc_level = st.number_input("Zinc Level / កម្រិតស័ង្កសី", format="%.2f")
        sulfate_level = st.number_input("Sulfate Level / កម្រិតស៊ុលហ្វាត", format="%.2f")
        copper_level = st.number_input("Copper Level / កម្រិតស្ពាន់", format="%.2f")
        hydrogen_sulfide = st.number_input("Hydrogen Sulfide / កម្រិតអ៊ីដ្រូស៊ុលហ្វីត", format="%.2f")
        hardness = st.number_input("Hardness / ភាពរឹង", format="%.2f")
        aluminum_level = st.number_input("Aluminum Level / កម្រិតអាលុយមីញ៉ូម", format="%.2f")
        chloride_level = st.number_input("Chloride Level / កម្រិតក្លរួ", format="%.2f")
        iron_level = st.number_input("Iron Level / កម្រិតដែក", format="%.2f")
        ammonia_level = st.number_input("Ammonia Level / កម្រិតអាម៉ូនី", format="%.2f")
        barium_level = st.number_input("Barium Level / កម្រិតបារីញ៉ូម", format="%.2f")
        cadmium_level = st.number_input("Cadmium Level / កម្រិតកាដមីញ៉ូម", format="%.2f")
        chromium_level = st.number_input("Chromium Level / កម្រិតក្រូមីញ៉ូម", format="%.2f")
        fluoride_level = st.number_input("Fluoride Level / កម្រិតហ្វ្លូអរួ", format="%.2f")
        lead_level = st.number_input("Lead Level / កម្រិតសំណ", format="%.2f")
        mercury_level = st.number_input("Mercury Level / កម្រិតបារត", format="%.2f")
        nitrate_level = st.number_input("Nitrate Level / កម្រិតនីត្រាត", format="%.2f")
        nitrite_level = st.number_input("Nitrite Level / កម្រិតនីត្រាយ", format="%.2f")
        sodium_level = st.number_input("Sodium Level / កម្រិតសូដ្យូម", format="%.2f")
        residual_chlorine = st.number_input("Residual Chlorine / កម្រិតក្លរួសល់", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_treatment_plant_id = st.selectbox("Select Treatment Plant / ជ្រើសរើសរោងចក្រកែច្នៃទឹក", options=list(treatment_plant_options.keys()), format_func=lambda x: treatment_plant_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
    db_helper = DatabaseHelper()
    # Fetch necessary data for dropdowns
    treatment_plants = db_helper.fetch_data('treatment_plant', ['idTreatmentPlant', 'TreatmentPlant_name'])
    db_helper.close_connection()
    # Prepare dropdown options
    treatment_plant_options = {row[0]: row[1] for row in treatment_plants}
    with st.form(key='commercial_form'):
        code = st.number_input("កូដ | Code", min_value=0, step=1)
        commercial_name = st.text_input("ឈ្មោះពាណិជ្ជកម្ម | Commercial Name")
        population_served = st.number_input("ប្រជាជនដែលបានបម្រើ | Population Served", min_value=0)
        service_coverage_license_area = st.number_input("ផ្ទៃដីអាជ្ញាប័ណ្ណសេវាកម្ម (គម²) | Service Coverage License Area (sq km)", format="%.2f")
        service_coverage_network_area = st.number_input("ផ្ទៃដីបណ្តាញសេវាកម្ម (គម²) | Service Coverage Network Area (sq km)", format="%.2f")
        water_production = st.number_input("ផលិតទឹក (ម³) | Water Production (m³)", format="%.2f")
        water_sold = st.number_input("ទឹកលក់ (ម³) | Water Sold (m³)", format="%.2f")
        water_supplied_without_charge = st.number_input("ទឹកផ្គត់ផ្គង់ដោយមិនគិតថ្លៃ (ម³) | Water Supplied Without Charge (m³)", format="%.2f")
        total_water_consumption = st.number_input("ការប្រើប្រាស់ទឹកសរុប (ម³) | Total Water Consumption (m³)", format="%.2f")
        water_losses = st.number_input("ការបាត់បង់ទឹក (ម³) | Water Losses (m³)", format="%.2f")
        non_revenue_water = st.number_input("ទឹកដែលមិនបានចំណូល (ម³) | Non-Revenue Water (m³)", format="%.2f")
        average_daily_consumption = st.number_input("ការកំណត់ទឹកប្រចាំថ្ងៃមធ្យម (ម³) | Average Daily Consumption (m³)", format="%.2f")
        average_consumption_per_connection = st.number_input("ការកំណត់ទឹកមធ្យមចំពោះនីតិវិធីមួយ (ម³) | Average Consumption Per Connection (m³)", format="%.2f")
        average_consumption_per_capita = st.number_input("ការកំណត់ទឹកមធ្យមចំពោះប្រជាជនម្នាក់ (ម³) | Average Consumption Per Capita (m³)", format="%.2f")
        total_water_connections = st.number_input("ការតភ្ជាប់ទឹកសរុប | Total Water Connections", min_value=0)
        residential_connections = st.number_input("ការតភ្ជាប់លំនៅដ្ឋាន | Residential Connections", min_value=0)
        commercial_connections = st.number_input("ការតភ្ជាប់ពាណិជ្ជកម្ម | Commercial Connections", min_value=0)
        public_entity_connections = st.number_input("ការតភ្ជាប់អង្គភាពសាធារណៈ | Public Entity Connections", min_value=0)
        factory_connections = st.number_input("ការតភ្ជាប់រោងចក្រ | Factory Connections", min_value=0)
        sme_connections = st.number_input("ការតភ្ជាប់អាជីវកម្មតូច | SME Connections", min_value=0)
        poor_connections = st.number_input("ការតភ្ជាប់អ្នកក្រីក្រ | Poor Connections", min_value=0)
        poor_household_ratio = st.number_input("អត្រាផ្ទះក្រីក្រ (%) | Poor Household Ratio (%)", format="%.2f")
        customer_complaints = st.number_input("បណ្តឹងអតិថិជន | Customer Complaints", min_value=0)
        complaints_per_1000_connections = st.number_input("បណ្តឹងក្នុងមួយ 1000 ការតភ្ជាប់ | Complaints Per 1000 Connections", format="%.2f")
        license_area_profile = st.text_input("កំណត់ហេតុផ្ទៃដីអាជ្ញាប័ណ្ណ | License Area Profile")
        network_area_population = st.number_input("ប្រជាជនបណ្តាញផ្ទៃដី | Network Area Population", min_value=0)
        network_area_houses = st.number_input("ផ្ទះបណ្តាញផ្ទៃដី | Network Area Houses", min_value=0)
        licensed_area_population = st.number_input("ប្រជាជនផ្ទៃដីអាជ្ញាប័ណ្ណ | Licensed Area Population", min_value=0)
        licensed_area_houses = st.number_input("ផ្ទះផ្ទៃដីអាជ្ញាប័ណ្ណ | Licensed Area Houses", min_value=0)
        # Dropdown for selecting foreign key ID
        selected_treatment_plant_id = st.selectbox(
            "ជ្រើសរើសរុក្ខជាតិបច្ចេកទេស | Select Treatment Plant",
            options=list(treatment_plant_options.keys()),
            format_func=lambda x: treatment_plant_options[x]
        )
        submit_button = st.form_submit_button("បញ្ជូន | Submit")
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    commercial_list = db_helper.fetch_data('commercial', ['idCommercial', 'Commercial_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    commercial_options = {row[0]: row[1] for row in commercial_list}

    with st.form(key='financial_form'):
        code = st.number_input("កូដ | Code", min_value=0, step=1)
        financial_name = st.text_input("ឈ្មោះហិរញ្ញវត្ថុ | Financial Name")
        cash_from_water_sales = st.number_input("ប្រាក់ពីការលក់ទឹក | Cash From Water Sales", format="%.2f")
        other_cash = st.number_input("ប្រាក់ផ្សេងទៀត | Other Cash", format="%.2f")
        amount_billed_for_water_sales = st.number_input("ចំនួនវិក័យប័ត្រសម្រាប់លក់ទឹក | Amount Billed for Water Sales", format="%.2f")
        amount_billed_for_other_services = st.number_input("ចំនួនវិក័យប័ត្រសម្រាប់សេវាផ្សេងទៀត | Amount Billed for Other Services", format="%.2f")
        accounts_receivable = st.number_input("គណនីទទួលបាន | Accounts Receivable", format="%.2f")
        average_tariff = st.number_input("តំលៃមធ្យម | Average Tariff", format="%.2f")
        bill_collection_ratio = st.number_input("អត្រាប្រមូលវិក័យប័ត្រ (%) | Bill Collection Ratio (%)", format="%.2f")
        total_operating_expenses = st.number_input("ចំណាយប្រតិបត្តិការសរុប | Total Operating Expenses", format="%.2f")
        operating_ratio = st.number_input("អត្រាប្រតិបត្តិការ (%) | Operating Ratio (%)", format="%.2f")
        production_expenses = st.number_input("ចំណាយផលិត | Production Expenses", format="%.2f")
        unit_production_cost = st.number_input("ថ្លៃដើមផលិតនីតិវិធី | Unit Production Cost", format="%.2f")
        net_income = st.number_input("ចំណូលសុទ្ធ | Net Income", format="%.2f")
        net_profit_margin = st.number_input("អត្រាប្រាក់ចំណេញសុទ្ធ (%) | Net Profit Margin (%)", format="%.2f")
        investment_expenditures = st.number_input("ចំណាយវិនិយោគ | Investment Expenditures", format="%.2f")
        loans = st.number_input("ឥណទាន | Loans", format="%.2f")
        accounts_payable = st.number_input("គណនីត្រូវបង់ | Accounts Payable", format="%.2f")
        total_assets = st.number_input("ទ្រព្យសកម្មសរុប | Total Assets", format="%.2f")
        owner_equity = st.number_input("មូលដ្ឋានម្ចាស់ | Owner Equity", format="%.2f")
        debt_to_equity_ratio = st.number_input("អត្រាបំណុលទៅមូលដ្ឋាន | Debt to Equity Ratio", format="%.2f")
        return_on_assets = st.number_input("ប្រយោជន៍លើទ្រព្យសកម្ម (%) | Return on Assets (%)", format="%.2f")
        return_on_equity = st.number_input("ប្រយោជន៍លើមូលដ្ឋាន (%) | Return on Equity (%)", format="%.2f")
        interest_expense = st.number_input("ចំណាយការប្រាក់ | Interest Expense", format="%.2f")
        depreciation_expense = st.number_input("ចំណាយអាប់បង់ | Depreciation Expense", format="%.2f")
        other_expense = st.number_input("ចំណាយផ្សេងៗ | Other Expense", format="%.2f")
        residential_tariff = st.number_input("តំលៃលំនៅដ្ឋាន | Residential Tariff", format="%.2f")
        commercial_tariff = st.number_input("តំលៃពាណិជ្ជកម្ម | Commercial Tariff", format="%.2f")
        government_tariff = st.number_input("តំលៃរដ្ឋាភិបាល | Government Tariff", format="%.2f")

        # Dropdown for selecting foreign key ID
        selected_commercial_id = st.selectbox(
            "ជ្រើសរើសពាណិជ្ជកម្ម | Select Commercial",
            options=list(commercial_options.keys()),
            format_func=lambda x: commercial_options[x]
        )

        submit_button = st.form_submit_button("បញ្ជូន | Submit")
        
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    commercial_list = db_helper.fetch_data('commercial', ['idCommercial', 'Commercial_name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    commercial_options = {row[0]: row[1] for row in commercial_list}

    with st.form(key='distribution_network_form'):
        code = st.number_input("Code / លេខកូដ", min_value=0, step=1)
        distribution_network_name = st.text_input("Distribution Network Name / ឈ្មោះបណ្តាញចែកចាយ")
        supply_pressure_end_connection = st.number_input("Supply Pressure at End Connection / សម្ពាធផ្គត់ផ្គង់នៅចំណុចបញ្ចប់", format="%.2f")
        number_of_leaks_repaired = st.number_input("Number of Leaks Repaired / ចំនួនការជួសជុលការជ្រាប", format="%.2f")
        total_length = st.number_input("Total Length (m) / ប្រវែងសរុប (ម៉ែត្រ)", format="%.2f")
        transmission_length = st.number_input("Transmission Length (m) / ប្រវែងបញ្ជូន (ម៉ែត្រ)", format="%.2f")
        distribution_length = st.number_input("Distribution Length (m) / ប្រវែងចែកចាយ (ម៉ែត្រ)", format="%.2f")
        storage_capacity = st.number_input("Storage Capacity (m³) / សមត្ថភាពផ្ទុក (ម៉ែត្រគូប)", format="%.2f")
        supply_duration = st.number_input("Supply Duration (hours) / រយៈពេលផ្គត់ផ្គង់ (ម៉ោង)", min_value=0, step=1)

        # Dropdown for selecting foreign key ID
        selected_commercial_id = st.selectbox("Select Commercial / ជ្រើសរើសពាណិជ្ជកម្ម", options=list(commercial_options.keys()), format_func=lambda x: commercial_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_list = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_list}
    company_options = {row[0]: row[1] for row in company_list}

    with st.form(key='office_contact_form'):
        office_phone = st.text_input("Office Phone / លេខទូរស័ព្ទការិយាល័យ")
        fax_number = st.text_input("Fax Number / លេខទូរសារ")
        mobile_phone = st.text_input("Mobile Phone / លេខទូរស័ព្ទចល័ត")
        email = st.text_input("Email / អ៊ីមែល")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdown
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_list}

    with st.form(key='factory_form'):
        factory_name = st.text_input("Factory Name / ឈ្មោះរោងចក្រ")
        country = st.text_input("Country / ប្រទេស")
        address = st.text_input("Address / អាសយដ្ឋាន")

        # Dropdown for selecting foreign key (CompanyID)
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    applicant_list = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    factory_list = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    applicant_options = {row[0]: row[1] for row in applicant_list}
    factory_options = {row[0]: row[1] for row in factory_list}

    with st.form(key='product_form'):
        product_name = st.text_input("Product Name / ឈ្មោះផលិតផល")
        trade_name = st.text_input("Trade Name / ឈ្មោះពាណិជ្ជកម្ម")
        model_number = st.text_input("Model Number / លេខម៉ូដែល")
        referred_standard = st.file_uploader("Referred Standard / ស្តង់ដារដែលបានយោង", type=['pdf', 'docx', 'jpg', 'png'])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_factory_id = st.selectbox("Select Factory / ជ្រើសរើសរោងចក្រ", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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
    
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_list = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    product_list = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()
    
    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_list}
    product_options = {row[0]: row[1] for row in product_list}

    with st.form(key='license_form'):
        license_number = st.text_input("License Number / លេខអាជ្ញាប័ណ្ណ")
        license_issued_date = st.date_input("License Issued Date / កាលបរិច្ឆេទចេញអាជ្ញាប័ណ្ណ")
        license_expiry_date = st.date_input("License Expiry Date / កាលបរិច្ឆេទផុតកំណត់អាជ្ញាប័ណ្ណ")
        license_type = st.text_input("License Type / ប្រភេទអាជ្ញាប័ណ្ណ")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")
        
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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_list = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    product_list = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_list}
    product_options = {row[0]: row[1] for row in product_list}

    with st.form(key='factory_inspection_report_form'):
        certification_number = st.text_input("System Certification Number / លេខវិញ្ញាបនបត្រប្រព័ន្ធ")
        issued_date = st.date_input("Issued Date / កាលបរិច្ឆេទចេញ")
        certification_body_name = st.text_input("Certification Body Name / ឈ្មោះអង្គភាពវិញ្ញាបនបត្រ")

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("Select Factory / ជ្រើសរើសរោងចក្រ", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    factory_inspection_report_data = db_helper.fetch_data('factory_inspection_report', ['FactoryInspectionReportID', 'SystemCertificationNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    factory_inspection_report_options = {report[0]: report[1] for report in factory_inspection_report_data}

    with st.form(key='certificate_of_conformity_form'):
        certificate_number = st.text_input("Certificate Number / លេខវិញ្ញាបនបត្រ")
        issued_date = st.date_input("Issued Date / កាលបរិច្ឆេទចេញ")
        certification_body_name = st.text_input("Certification Body Name / ឈ្មោះអង្គភាពវិញ្ញាបនបត្រ")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_factory_inspection_report_id = st.selectbox("Select Factory Inspection Report / ជ្រើសរើសរបាយការណ៍ត្រួតពិនិត្យរោងចក្រ", options=list(factory_inspection_report_options.keys()), format_func=lambda x: factory_inspection_report_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    certificate_of_conformity_data = db_helper.fetch_data('certificate_of_conformity', ['CertificateOfConformityID', 'CertificateNumber'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    certificate_of_conformity_options = {cert[0]: cert[1] for cert in certificate_of_conformity_data}

    with st.form(key='test_report_form'):
        report_number = st.text_input("Report Number / លេខរបាយការណ៍")
        test_laboratory_name = st.text_input("Test Laboratory Name / ឈ្មោះមន្ទីរសាកល្បង")
        issued_date = st.date_input("Issued Date / កាលបរិច្ឆេទចេញ", min_value=datetime(1900, 1, 1))

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_certificate_of_conformity_id = st.selectbox("Select Certificate of Conformity / ជ្រើសរើសវិញ្ញាបនបត្រនៃការអនុលោម", options=list(certificate_of_conformity_options.keys()), format_func=lambda x: certificate_of_conformity_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {product[0]: product[1] for product in product_data}
    company_options = {company[0]: company[1] for company in company_data}

    with st.form(key='patent_card_form'):
        number = st.text_input("Patent Number / លេខប៉ាតង់")
        patent_issued_date = st.date_input("Patent Issued Date / កាលបរិច្ឆេទចេញប៉ាតង់", min_value=datetime(1900, 1, 1))
        tax_unit = st.text_input("Tax Unit / ឯកតាពន្ធ")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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
        description = st.text_input("Description / សេចក្ដីពិពណ៌នា")
        certificate_conformity_in_english = st.file_uploader("Upload Certificate Conformity in English / ផ្ទុកវិញ្ញាបនបត្រនៃការអនុលោមជាភាសាអង់គ្លេស", type=["pdf", "jpg", "png"])
        factory_inspection_report = st.file_uploader("Upload Factory Inspection Report / ផ្ទុករបាយការណ៍ត្រួតពិនិត្យរោងចក្រ", type=["pdf", "jpg", "png"])
        label = st.file_uploader("Upload Label / ផ្ទុកស្លាក", type=["pdf", "jpg", "png"])
        users_instruction_manual = st.file_uploader("Upload Users Instruction Manual / ផ្ទុកសៀវភៅណែនាំអ្នកប្រើប្រាស់", type=["pdf", "jpg", "png"])
        record_of_modification = st.file_uploader("Upload Record of Modification / ផ្ទុកកំណត់ត្រានៃការកែប្រែ", type=["pdf", "jpg", "png"])
        product_color_photographs = st.file_uploader("Upload Product Color Photographs / ផ្ទុករូបថតផលិតផលពណ៌", type=["pdf", "jpg", "png"])
        test_report_conformity_in_english = st.file_uploader("Upload Test Report Conformity in English / ផ្ទុករបាយការណ៍សាកល្បងជាភាសាអង់គ្លេស", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_certificate_of_conformity_id = st.selectbox("Select Certificate of Conformity / ជ្រើសរើសវិញ្ញាបនបត្រនៃការអនុលោម", options=list(certificate_of_conformity_options.keys()), format_func=lambda x: certificate_of_conformity_options[x])
        selected_factory_inspection_report_id = st.selectbox("Select Factory Inspection Report / ជ្រើសរើសរបាយការណ៍ត្រួតពិនិត្យរោងចក្រ", options=list(factory_inspection_report_options.keys()), format_func=lambda x: factory_inspection_report_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    documents_data = db_helper.fetch_data('doc_pro_or_spare_part_pro_registration', ['DocumentsID', 'Description'])
    
    db_helper.close_connection()

    # Prepare dropdown options
    documents_options = {row[0]: row[1] for row in documents_data}

    with st.form(key='doc_electri_and_electro_pro_registration_form'):
        full_electrical_wiring_circuit_diagrams = st.file_uploader("Upload Full Electrical Wiring Circuit Diagrams / ផ្ទុកគំនូសបញ្ជាក់បន្ទាត់ភ្លើងពេញលេញ", type=["pdf", "jpg", "png"])

        # Dropdown for selecting foreign keys
        selected_documents_id = st.selectbox("Select Document ID / ជ្រើសរើសលេខសម្គាល់ឯកសារ", options=list(documents_options.keys()), format_func=lambda x: documents_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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
        item_number = st.text_input("Item Number / លេខធាតុ")
        description_item = st.text_input("Description of Item / សេចក្ដីពិពណ៌នាធាតុ")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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
        industrial_announcement_letter = st.file_uploader("ផ្ទុកឡើងលិខិតប្រកាសឧស្សាហកម្ម | Upload Industrial Announcement Letter", type=["pdf", "jpg", "png"])
        certificate_of_operation_company_local = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្ររបស់ក្រុមហ៊ុនដំណើរការក្នុងស្រុក | Upload Certificate of Operation Company Local", type=["pdf", "jpg", "png"])
        company_establishment_statute = st.file_uploader("ផ្ទុកឡើងច្បាប់ស្ថាបនាក្រុមហ៊ុន | Upload Company Establishment Statute", type=["pdf", "jpg", "png"])
        commercial_registration_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រចុះបញ្ជីពាណិជ្ជកម្ម | Upload Commercial Registration Certificate", type=["pdf", "jpg", "png"])
        patent_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រកម្មសិទ្ធិបញ្ញា | Upload Patent Certificate", type=["pdf", "jpg", "png"])
        equivalent_legal_documents = st.file_uploader("ផ្ទុកឡើងឯកសារច្បាប់ស្មើ | Upload Equivalent Legal Documents", type=["pdf", "jpg", "png"])
        letter_of_recognition = st.file_uploader("ផ្ទុកឡើងលិខិតស្គាល់ | Upload Letter of Recognition", type=["pdf", "jpg", "png"])
        national_id_card_or_passport = st.file_uploader("ផ្ទុកឡើងកាតសម្គាល់ខ្លួនជាតិ ឬ លិខិតឆ្លងដែន | Upload National ID Card or Passport", type=["pdf", "jpg", "png"])
        analysis_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រវិភាគ | Upload Analysis Certificate", type=["pdf", "jpg", "png"])
        compliance_evaluation_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រវាយតម្លៃភាពស្របច្បាប់ | Upload Compliance Evaluation Certificate", type=["pdf", "jpg", "png"])
        license_using_vehicle_safety_mark = st.file_uploader("ផ្ទុកឡើងអាជ្ញាប័ណ្ណប្រើសញ្ញាសុវត្ថិភាពយានយន្ត | Upload License Using Vehicle Safety Mark", type=["pdf", "jpg", "png"])
        other_related_documents = st.file_uploader("ផ្ទុកឡើងឯកសារផ្សេងទៀតដែលពាក់ព័ន្ធ | Upload Other Related Documents", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ | Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន | Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល | Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_infor_detail_id = st.selectbox("ជ្រើសរើសព័ត៌មានលម្អិតនៃការកែប្រែ | Select Information Detail of Modification", options=list(infor_detail_options.keys()), format_func=lambda x: infor_detail_options[x])

        submit_button = st.form_submit_button("បញ្ជូន | Submit")

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
        test_report_in_english = st.file_uploader("Upload Test Report in English / ផ្ទុករបាយការណ៍សាកល្បងជាភាសាអង់គ្លេស", type=["pdf", "jpg", "png"])
        certificate_of_conformity_in_english = st.file_uploader("Upload Certificate of Conformity in English / ផ្ទុកវិញ្ញាបនបត្រនៃការអនុលោមជាភាសាអង់គ្លេស", type=["pdf", "jpg", "png"])
        product_safety_license = st.file_uploader("Upload Product Safety License / ផ្ទុកអាជ្ញាប័ណ្ណសុវត្ថិភាពផលិតផល", type=["pdf", "jpg", "png"])
        confirmed_letter = st.file_uploader("Upload Confirmed Letter / ផ្ទុកលិខិតបញ្ជាក់", type=["pdf", "jpg", "png"])
        document_related_regulated_products = st.file_uploader("Upload Document Related to Regulated Products / ផ្ទុកឯកសារពាក់ព័ន្ធនឹងផលិតផលដែលត្រូវបានគ្រប់គ្រង", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_infor_detail_id = st.selectbox("Select Information Detail of Modification / ជ្រើសរើសព័ត៌មានលម្អិតនៃការកែប្រែ", options=list(infor_detail_options.keys()), format_func=lambda x: infor_detail_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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
        chemical_name = st.text_input("Chemical Name / ឈ្មោះសារធាតុគីមី")
        commercial_name = st.text_input("Commercial Name / ឈ្មោះពាណិជ្ជកម្ម")
        recognition = st.text_input("Recognition / ការទទួលស្គាល់")
        quantity = st.text_input("Quantity / បរិមាណ")
        standard_of_usage = st.text_input("Standard of Usage / ស្តង់ដារនៃការប្រើប្រាស់")
        reference_chemical = st.text_input("Reference Chemical / សារធាតុគីមីយោង")
        support_purpose = st.text_input("Support Purpose / គោលបំណងគាំទ្រ")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("Select Applicant / ជ្រើសរើសអ្នកដាក់ពាក្យ", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_company_signature_id = st.selectbox("Select Company Signature / ជ្រើសរើសហត្ថលេខាក្រុមហ៊ុន", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])
        selected_product_id = st.selectbox("Select Product / ជ្រើសរើសផលិតផល", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='previous_chemical_usage_form'):
        chemical_name = st.text_input("Chemical Name / ឈ្មោះសារធាតុគីមី")
        previous_quantity = st.text_input("Previous Quantity / បរិមាណមុន")
        previous_import_license_number = st.text_input("Previous Import License Number / លេខអាជ្ញាប័ណ្ណនាំចូលមុន")
        previous_import_date = st.date_input("Previous Import Date / កាលបរិច្ឆេទនាំចូលមុន")

        # Dropdown for selecting foreign key
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance / ជ្រើសរើសសារធាតុគីមី", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='appli_details_chemical_form'):
        port_to_port = st.text_input("Port to Port / ព្រលានដល់ព្រលាន")
        port_to_applicant_storage_premise = st.text_input("Port to Applicant Storage Premise / ព្រលានដល់ទីតាំងផ្ទុករបស់អ្នកដាក់ពាក្យ")
        port_to_job_site_for_immediate_use = st.text_input("Port to Job Site for Immediate Use / ព្រលានដល់ទីតាំងការងារសម្រាប់ប្រើប្រាស់ភ្លាមៗ")
        port_to_customer_storage_premise = st.text_input("Port to Customer Storage Premise / ព្រលានដល់ទីតាំងផ្ទុករបស់អតិថិជន")
        other = st.text_input("Other Details / ព័ត៌មានលម្អិតផ្សេងទៀត")
        name_of_premise = st.text_input("Name of Premise / ឈ្មោះទីតាំង")
        kind_of_premise = st.text_input("Kind of Premise / ប្រភេទទីតាំង")
        size_capacity = st.text_input("Size Capacity / សមត្ថភាពទំហំ")
        emergency_action_plan = st.checkbox("Emergency Action Plan / ផែនការសកម្មភាពបន្ទាន់", value=False)
        date = st.date_input("Date / កាលបរិច្ឆេទ")

        # Dropdown for selecting foreign keys
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance / ជ្រើសរើសសារធាតុគីមី", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='chemical_pro_plan_annual_form'):
        production_quantity = st.text_input("Production Quantity / បរិមាណផលិត")
        recognition = st.text_input("Recognition / ការទទួលស្គាល់")
        start_date = st.date_input("Start Date / កាលបរិច្ឆេទចាប់ផ្តើម")
        end_date = st.date_input("End Date / កាលបរិច្ឆេទបញ្ចប់")

        # Dropdown for selecting foreign key (CompanyID)
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='declaration_buyer_importer_form'):
        usage_purpose = st.text_input("Usage Purpose / គោលបំណងប្រើប្រាស់")
        name = st.text_input("Name / ឈ្មោះ")
        position = st.text_input("Position / មុខតំណែង")
        stand_for_company = st.text_input("Stand For Company / តំណាងឱ្យក្រុមហ៊ុន")
        address = st.text_area("Address / អាសយដ្ឋាន")
        phone = st.text_input("Phone / លេខទូរស័ព្ទ")
        fax_number = st.text_input("Fax Number / លេខទូរសារ")
        email = st.text_input("Email / អ៊ីមែល")
        date = st.date_input("Date / កាលបរិច្ឆេទ")

        # Dropdowns for foreign keys
        selected_chemical_substance_id = st.selectbox("Select Chemical Substance / ជ្រើសរើសសារធាតុគីមី", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])
        selected_company_id = st.selectbox("Select Company / ជ្រើសរើសក្រុមហ៊ុន", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("Submit / ដាក់ស្នើ")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='doc_recog_standard_chemical_substance_form'):
        company_characteristics = st.file_uploader("ផ្ទុកឡើងលក្ខណៈពិសេសក្រុមហ៊ុន | Upload Company Characteristics", type=["pdf", "jpg", "png"])
        company_certification_letter = st.file_uploader("ផ្ទុកឡើងលិខិតវិញ្ញាបនបត្រក្រុមហ៊ុន | Upload Company Certification Letter", type=["pdf", "jpg", "png"])
        company_registration_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រចុះបញ្ជីក្រុមហ៊ុន | Upload Company Registration Certificate", type=["pdf", "jpg", "png"])
        value_added_tax_registration_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រចុះបញ្ជីអាករបន្ថែមតម្លៃ | Upload Value Added Tax Registration Certificate", type=["pdf", "jpg", "png"])
        valid_patents_copies = st.file_uploader("ផ្ទុកឡើងច្បាប់បង់ប្រាក់ដែលមានសុពលភាព | Upload Valid Patents Copies", type=["pdf", "jpg", "png"])
        factory_permit_and_certificate = st.file_uploader("ផ្ទុកឡើងអាជ្ញាប័ណ្ណនិងវិញ្ញាបនបត្ររោងចក្រ | Upload Factory Permit and Certificate", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("ផ្ទុកឡើងលិខិតផ្ទេរសិទ្ធិ | Upload Rights Transfer Letter", type=["pdf", "jpg", "png"])
        chemical_substances_list_and_values = st.file_uploader("ផ្ទុកឡើងបញ្ជីនិងតម្លៃសារធាតុគីមី | Upload Chemical Substances List and Values", type=["pdf", "jpg", "png"])
        applicant_id_or_passport_copy = st.file_uploader("ផ្ទុកឡើងច្បាប់សម្គាល់អ្នកដាក់ពាក្យ ឬ លិខិតឆ្លងដែន | Upload Applicant ID or Passport Copy", type=["pdf", "jpg", "png"])
        material_safety_data_sheet = st.file_uploader("ផ្ទុកឡើងទិន្នន័យសុវត្ថិភាពសម្ភារៈ | Upload Material Safety Data Sheet", type=["pdf", "jpg", "png"])
        analysis_certificate_or_sample = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រវិភាគ ឬ សំណាក | Upload Analysis Certificate or Sample", type=["pdf", "jpg", "png"])
        previous_importation_and_usage_report = st.file_uploader("ផ្ទុកឡើងរបាយការណ៍នាំចូលនិងប្រើប្រាស់មុន | Upload Previous Importation and Usage Report", type=["pdf", "jpg", "png"])
        other_documents_if_required = st.file_uploader("ផ្ទុកឡើងឯកសារផ្សេងៗ ប្រសិនបើត្រូវការ | Upload Other Documents if Required", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន | Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_chemical_substance_id = st.selectbox("ជ្រើសរើសសារធាតុគីមី | Select Chemical Substance", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("បញ្ជូន | Submit")

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
        license_type = st.text_input("ប្រភេទអាជ្ញាប័ណ្ណ (License Type)")
        old_license_number_if_renewal = st.text_input("លេខអាជ្ញាប័ណ្ណចាស់ (ប្រសិនបើធ្វើឱ្យថ្មី) (Old License Number (if Renewal))")
        product_name = st.text_input("ឈ្មោះផលិតផល (Product Name)")
        capacity_weight = st.text_input("សមត្ថភាព/ទំងន់ (Capacity/Weight)")
        trademark = st.text_input("ឈ្មោះពាណិជ្ជសញ្ញា (Trademark)")
        standard_reference = st.text_input("យោងស្តង់ដារ (Standard Reference)")
        related_terms_conditions = st.text_area("លក្ខខណ្ឌនិងលក្ខខណ្ឌដែលពាក់ព័ន្ធ (Related Terms and Conditions)")

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ (Select Applicant)", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល (Select Product)", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        machinery_name = st.text_input("ឈ្មោះម៉ាស៊ីន (Machinery Name)")
        inspection_date = st.date_input("កាលបរិច្ឆេទត្រួតពិនិត្យ (Inspection Date)")
        additional_information = st.text_area("ព័ត៌មានបន្ថែម (Additional Information)")

        # Dropdowns for selecting foreign keys
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណចុះបញ្ជីផលិតផល (Select Product Registration License)", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        declaration_of_factory = st.file_uploader("ផ្ទុកសេចក្តីប្រកាសរោងចក្រ (Upload Declaration of Factory)", type=["pdf", "jpg", "png"])
        product_label_compliance = st.file_uploader("ផ្ទុកការអនុលោមស្លាកផលិតផល (CS001:2000) (Upload Product Label Compliance (CS001:2000))", type=["pdf", "jpg", "png"])
        product_analysis_certificate = st.file_uploader("ផ្ទុកវិញ្ញាបនបត្រវិភាគផលិតផល (Upload Product Analysis Certificate)", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("ផ្ទុកលិខិតផ្ទេរសិទ្ធិ (Upload Rights Transfer Letter)", type=["pdf", "jpg", "png"])
        other_documents = st.file_uploader("ផ្ទុកឯកសារផ្សេងទៀត (Upload Other Documents)", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណចុះបញ្ជីផលិតផល (Select Product Registration License)", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])
        selected_company_signature_id = st.selectbox("ជ្រើសរើសហត្ថលេខាក្រុមហ៊ុន (Select Company Signature)", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        production_chain_diagram = st.file_uploader("ផ្ទុកគំនូសតាងខ្សែសង្វាក់ផលិតកម្ម (Upload Production Chain Diagram)", type=["pdf", "jpg", "png"])
        date_of_diagram = st.date_input("កាលបរិច្ឆេទនៃគំនូសតាង (Date of Diagram)")
        product_purpose = st.text_input("គោលបំណងផលិតកម្ម (Production Purpose)")
        issued_date = st.date_input("កាលបរិច្ឆេទចេញផ្សាយ (Issued Date)")

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ (Select Applicant)", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_product_registration_license_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណចុះបញ្ជីផលិតផល (Select Product Registration License)", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        material_name = st.text_input("ឈ្មោះសម្ភារៈ (Material Name)")
        trademark_used = st.text_input("ឈ្មោះពាណិជ្ជសញ្ញាដែលប្រើ (Trademark Used)")
        percentage_used_in_final_product = st.text_input("ភាគរយដែលប្រើក្នុងផលិតផលចុងក្រោយ (Percentage Used in Final Product)")
        additional_information = st.text_input("ព័ត៌មានបន្ថែម (Additional Information)")

        # Dropdowns for selecting foreign keys
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_registration_license_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណចុះបញ្ជីផលិតផល (Select Product Registration License)", options=list(product_registration_license_options.keys()), format_func=lambda x: product_registration_license_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    applicant_data = db_helper.fetch_data('applicant', ['ApplicantID', 'LocalRepresentativeName'])
    company_signature_data = db_helper.fetch_data('company_signatur_and_stamp', ['CompanySignatureID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    company_options = {row[0]: row[1] for row in company_data}
    applicant_options = {row[0]: row[1] for row in applicant_data}
    company_signature_options = {row[0]: row[1] for row in company_signature_data}

    with st.form(key='doc_restricted_chemicals_form'):
        company_statute = st.file_uploader("ផ្ទុកឡើងច្បាប់ក្រុមហ៊ុន | Upload Company Statute", type=["pdf", "jpg", "png"])
        company_verification_letter = st.file_uploader("ផ្ទុកឡើងលិខិតផ្ទៀងផ្ទាត់ក្រុមហ៊ុន | Upload Company Verification Letter", type=["pdf", "jpg", "png"])
        company_registration_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រចុះបញ្ជីក្រុមហ៊ុន | Upload Company Registration Certificate", type=["pdf", "jpg", "png"])
        vat_registration_certificate = st.file_uploader("ផ្ទុកឡើងវិញ្ញាបនបត្រចុះបញ្ជីអាករបន្ថែមតម្លៃ | Upload VAT Registration Certificate", type=["pdf", "jpg", "png"])
        patent_card = st.file_uploader("ផ្ទុកឡើងកាតប៉ាតង់ | Upload Patent Card", type=["pdf", "jpg", "png"])
        previous_compliance_status = st.file_uploader("ផ្ទុកឡើងស្ថានភាពការស្របច្បាប់មុន | Upload Previous Compliance Status", type=["pdf", "jpg", "png"])
        other_documents = st.file_uploader("ផ្ទុកឡើងឯកសារផ្សេងៗ | Upload Other Documents", type=["pdf", "jpg", "png"])
        rights_transfer_letter = st.file_uploader("ផ្ទុកឡើងលិខិតផ្ទេរសិទ្ធិ | Upload Rights Transfer Letter", type=["pdf", "jpg", "png"])
        factory_establishment_permission = st.file_uploader("ផ្ទុកឡើងការអនុញ្ញាតបង្កើតរោងចក្រ | Upload Factory Establishment Permission", type=["pdf", "jpg", "png"])
        craft_establishment_permission = st.file_uploader("ផ្ទុកឡើងការអនុញ្ញាតបង្កើតសិប្បកម្ម | Upload Craft Establishment Permission", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ | Select Applicant", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន | Select Company", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_company_signature_id = st.selectbox("ជ្រើសរើសហត្ថលេខាក្រុមហ៊ុន | Select Company Signature", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("បញ្ជូន | Submit")

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
        industrial_announcement_letter = st.file_uploader("ផ្ទុកលិខិតប្រកាសឧស្សាហកម្ម (Upload Industrial Announcement Letter)", type=["pdf", "jpg", "png"])
        certi_commercial_registration_or_equivalent_legal_doc = st.file_uploader("ផ្ទុកការចុះបញ្ជីពាណិជ្ជកម្ម ឬឯកសារច្បាប់ស្មើគ្នា (Upload Commercial Registration or Equivalent Legal Document)", type=["pdf", "jpg", "png"])
        national_id_card_or_passport = st.file_uploader("ផ្ទុកអត្តសញ្ញាណប័ណ្ណជាតិ ឬលិខិតឆ្លងដែន (Upload National ID Card or Passport)", type=["pdf", "jpg", "png"])
        other_related_documents = st.file_uploader("ផ្ទុកឯកសារដែលពាក់ព័ន្ធផ្សេងទៀត (Upload Other Related Documents)", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ (Select Applicant)", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល (Select Product)", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_company_signature_id = st.selectbox("ជ្រើសរើសហត្ថលេខាក្រុមហ៊ុន (Select Company Signature)", options=list(company_signature_options.keys()), format_func=lambda x: company_signature_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        photo_of_factory_owner = st.file_uploader("ផ្ទុករូបថត 4x6 របស់ម្ចាស់រោងចក្រ (Upload 4x6 Photo of Factory Owner)", type=["jpg", "png"])
        national_id_card_or_passport = st.file_uploader("ផ្ទុកអត្តសញ្ញាណប័ណ្ណជាតិ ឬលិខិតឆ្លងដែន (Upload National ID Card or Passport)", type=["pdf", "jpg", "png"])
        copy_of_corporate_statute = st.file_uploader("ផ្ទុកច្បាប់ចម្លងនៃច្បាប់សហគ្រាស (Upload Copy of Corporate Statute)", type=["pdf", "jpg", "png"])
        copy_letter_of_commercial_registration = st.file_uploader("ផ្ទុកច្បាប់ចម្លងនៃលិខិតចុះបញ្ជីពាណិជ្ជកម្ម (Upload Copy Letter of Commercial Registration)", type=["pdf", "jpg", "png"])
        construction_permit = st.file_uploader("ផ្ទុកការអនុញ្ញាតសាងសង់ពីអាជ្ញាធរ (Upload Construction Permit from Authority)", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ (Select Applicant)", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    chemical_substance_data = db_helper.fetch_data('list_chemical_substance', ['ChemicalSubstanceID', 'ChemicalName'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    chemical_substance_options = {row[0]: row[1] for row in chemical_substance_data}

    with st.form(key='infor_raw_material_form'):
        description_raw_material = st.text_input("ការពិពណ៌នាសម្ភារៈដើម (Description of Raw Material)")
        unit = st.text_input("ឯកតា (Unit)")
        domestic_quantity = st.text_input("បរិមាណក្នុងស្រុក (Domestic Quantity)")
        domestic_amount = st.text_input("ចំនួនទឹកប្រាក់ក្នុងស្រុក (Domestic Amount)")
        import_quantity = st.text_input("បរិមាណនាំចូល (Import Quantity)")
        import_amount = st.text_input("ចំនួនទឹកប្រាក់នាំចូល (Import Amount)")

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_chemical_substance_id = st.selectbox("ជ្រើសរើសសារធាតុគីមី (Select Chemical Substance)", options=list(chemical_substance_options.keys()), format_func=lambda x: chemical_substance_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_invest_pro_safety_and_sanitary_system_form'):
        total_surface_area = st.text_input("ផ្ទៃសរុប (Total Surface Area)")
        description_surrounding_environment = st.text_input("ការពិពណ៌នាពីបរិយាកាសជុំវិញ (Description of Surrounding Environment)")

        # Dropdown for selecting foreign key
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}

    with st.form(key='doc_for_inves_project_pro_safety_form'):
        application_form = st.file_uploader("ផ្ទុកបែបបទដាក់ពាក្យ (Upload Application Form)", type=["pdf", "jpg", "png"])
        factory_permit_authority = st.file_uploader("ផ្ទុកការអនុញ្ញាតរោងចក្រពីអាជ្ញាធរ (Upload Factory Permit from Authority)", type=["pdf", "jpg", "png"])
        lease_agreement = st.file_uploader("ផ្ទុកកិច្ចសន្យាធ្វើច្បាប់ (Upload Lease Agreement)", type=["pdf", "jpg", "png"])
        land_title = st.file_uploader("ផ្ទុកប្លង់ដី (Upload Land Title)", type=["pdf", "jpg", "png"])
        commercial_registration = st.file_uploader("ផ្ទុកការចុះបញ្ជីពាណិជ្ជកម្ម (Upload Commercial Registration)", type=["pdf", "jpg", "png"])
        statute = st.file_uploader("ផ្ទុកច្បាប់សហគ្រាស (Upload Statute)", type=["pdf", "jpg", "png"])
        feasibility_study = st.file_uploader("ផ្ទុកការសិក្សាអនុវត្ត (Upload Feasibility Study)", type=["pdf", "jpg", "png"])
        factory_signed_board = st.file_uploader("ផ្ទុកផ្ទាំងហត្ថលេខារបស់រោងចក្រ (Upload Factory Signed Board)", type=["pdf", "jpg", "png"])
        id_or_passport = st.file_uploader("ផ្ទុកអត្តសញ្ញាណប័ណ្ណ ឬលិខិតឆ្លងដែន (Upload ID or Passport)", type=["pdf", "jpg", "png"])
        owner_factory_photo = st.file_uploader("ផ្ទុករូបថតម្ចាស់រោងចក្រ (3x4) (Upload Owner Factory Photo (3x4))", type=["pdf", "jpg", "png"])
        lab_test = st.file_uploader("ផ្ទុកលទ្ធផលតេស្តមន្ទីរពិសោធន៍ (Upload Lab Test)", type=["pdf", "jpg", "png"])
        criminal_police_record = st.file_uploader("ផ្ទុកប្រវត្តិឧក្រិដ្ឋកម្មនៃប៉ូលិស (Upload Criminal Police Record)", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        id_or_passport = st.file_uploader("ផ្ទុកអត្តសញ្ញាណប័ណ្ណ ឬលិខិតឆ្លងដែន (Upload ID or Passport)", type=["pdf", "jpg", "png"])
        location_map_architecture = st.file_uploader("ផ្ទុកផែនទីទីតាំង/ប្លង់ស្ថាបត្យកម្ម/លំហូរដំណើរការ (Upload Location Map/Architecture Layouts/Process Flow)", type=["pdf", "jpg", "png"])
        letter_local_authority = st.file_uploader("ផ្ទុកលិខិតពីអាជ្ញាធរមូលដ្ឋាន (Upload Letter from Local Authority)", type=["pdf", "jpg", "png"])

        # Dropdowns for selecting foreign keys
        selected_applicant_id = st.selectbox("ជ្រើសរើសអ្នកដាក់ពាក្យ (Select Applicant)", options=list(applicant_options.keys()), format_func=lambda x: applicant_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
   
    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_factory_manager_form'):
        name = st.text_input("ឈ្មោះ (Name)")
        nationality = st.text_input("សញ្ជាតិ (Nationality)")
        gender = st.selectbox("ភេទ (Gender)", options=["ប្រុស (Male)", "ស្រី (Female)", "ផ្សេងទៀត (Other)"])
        age = st.text_input("អាយុ (Age)")
        phone = st.text_input("លេខទូរស័ព្ទ (Phone)")
        professional = st.text_input("វិជ្ជាជីវៈ (Professional)")
        expertise_working_experience = st.text_area("ជំនាញ/បទពិសោធន៍ការងារពាក់ព័ន្ធនឹងការងារដែលបានស្នើសុំ (Expertise/Working Experience Related to Proposed Works)")
        number_employee_production = st.text_input("ចំនួននិយោជិតក្នុងផ្នែកផលិតកម្ម (Number of Employees in Production Section)")
        number_employee_service = st.text_input("ចំនួននិយោជិតក្នុងផ្នែកសេវាកម្ម (Number of Employees in Service Section)")
        number_employee_other = st.text_input("ចំនួននិយោជិតក្នុងផ្នែកផ្សេងទៀត (Number of Employees in Other Section)")
        total_employees = st.text_input("ចំនួននិយោជិតសរុប (Total Employees)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_quality_controlprogram_form'):
        describe_processing_flow = st.text_area("ពិពណ៌នាអំពីលំហូរដំណើរការ (Describe Processing Flow)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_investment_asset_form'):
        total_values_machinery_facilities = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃគ្រឿងម៉ាស៊ីននិងសម្ភារៈ (Total Estimated Values of Machinery & Facilities)")
        total_values_vehicle_transportation = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃយានជំនិះនិងការដឹកជញ្ជូន (Total Estimated Values of Vehicle & Transportation)")
        total_values_building = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃអគារ (Total Estimated Values of Building)")
        total_values_other_fixed_assets = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃទ្រព្យសកម្មថេរផ្សេងទៀត (Total Estimated Values of Other Fixed Assets)")
        total_values_working_capital = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃដើមទុនប្រតិបត្តិការ (Total Estimated Values of Working Capital)")
        total_values_investment = st.text_input("តម្លៃសរុបប៉ាន់ស្មាននៃការវិនិយោគ (Total Estimated Values of Investment)")
        source_investment = st.text_input("ប្រភពនៃការវិនិយោគ (Source of Investment)")
        estimated_percentage = st.text_input("ភាគរយប៉ាន់ស្មាន (Estimated Percentage)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_machinery_facilities_form'):
        list_machinery_facilities = st.text_input("បញ្ជីគ្រឿងម៉ាស៊ីននិងសម្ភារៈ (List of Machinery Facilities)")
        unit = st.text_input("ឯកតា (Unit)")
        quantity = st.text_input("បរិមាណ (Quantity)")
        amount = st.text_input("ចំនួនទឹកប្រាក់ (Amount)")
        domestic = st.text_input("ក្នុងស្រុក (Domestic)")
        import_from = st.text_input("នាំចូលពី (Import From)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_planed_product_output_form'):
        description_products = st.text_input("ការពិពណ៌នាផលិតផល (Description of Products)")
        unit = st.text_input("ឯកតា (Unit)")
        quantity_first_year = st.text_input("បរិមាណសម្រាប់ឆ្នាំដំបូង (Quantity for First Year)")
        amount_first_year = st.text_input("ចំនួនទឹកប្រាក់សម្រាប់ឆ្នាំដំបូង (Amount for First Year)")
        domestic_percentage_market = st.text_input("ភាគរយទីផ្សារក្នុងស្រុក (Domestic Market Percentage)")
        export_percentage_market = st.text_input("ភាគរយទីផ្សារនាំចេញ (Export Market Percentage)")
        quantity_full_capacity = st.text_input("បរិមាណនៅសមត្ថភាពពេញលេញ (Quantity at Full Capacity)")
        amount_full_capacity = st.text_input("ចំនួនទឹកប្រាក់នៅសមត្ថភាពពេញលេញ (Amount at Full Capacity)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])

    db_helper.close_connection()

    # Prepare dropdown options
    factory_options = {row[0]: row[1] for row in factory_data}

    with st.form(key='infor_product_waste_form'):
        solid_waste = st.text_input("កាកសំណល់រឹង (Solid Waste)")
        liquid_waste = st.text_input("កាកសំណល់រាវ (Liquid Waste)")
        emission_waste = st.text_input("កាកសំណល់បញ្ចេញ (Emission Waste)")

        # Dropdown for selecting FactoryID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdown for selecting AddressID, FactoryID, CompanyID, PersonalInforForApplicantID, ProductID
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant's Personal Information)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល (Select Product)", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_metrology_calibration_form'):
        statute_technical = st.file_uploader("ផ្ទុកច្បាប់បច្ចេកទេស (Upload Technical Statute)", type=["pdf", "jpg", "jpeg", "png"])
        transfer_letter = st.file_uploader("ផ្ទុកលិខិតផ្ទេរ (Upload Transfer Letter)", type=["pdf", "jpg", "jpeg", "png"])
        id_passport_card = st.file_uploader("ផ្ទុកអត្តសញ្ញាណប័ណ្ណ ឬលិខិតឆ្លងដែន (Upload ID or Passport Card)", type=["pdf", "jpg", "jpeg", "png"])

        # Dropdown for selecting ApplicationMetrologyID
        selected_application_id = st.selectbox("ជ្រើសរើសលេខសម្គាល់កម្មវិធីវាស់វែងត្រឹមត្រូវ (Select Application Metrology ID)", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}
    product_options = {row[0]: row[1] for row in product_data}

    with st.form(key='applic_license_repair_metrology_form'):
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdown for selecting AddressID, FactoryID, CompanyID, PersonalInforForApplicantID, ProductID
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល (Select Product)", options=list(product_options.keys()), format_func=lambda x: product_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_metro_verify_form'):
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdowns for selecting addressID, FactoryID, CompanyID, PersonalInforForApplicantID
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address',['AddressID','OfficeAddress'])
    factory_data = db_helper.fetch_data('factory', ['FactoryID', 'Name'])
    company_data = db_helper.fetch_data('company', ['CompanyID', 'Name'])
    personal_info_data = db_helper.fetch_data('personal_infor_for_applicant', ['PersonalInforForApplicantID'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]:row[1] for row in address_data}
    factory_options = {row[0]: row[1] for row in factory_data}
    company_options = {row[0]: row[1] for row in company_data}
    personal_info_options = {row[0]: f"Applicant ID: {row[0]}" for row in personal_info_data}

    with st.form(key='applic_certific_recog_metro_expertise_form'):
        # File uploader for Photo Application
        photo_application = st.file_uploader("ផ្ទុករូបថតសម្រាប់ពាក្យ (Upload Photo Application)", type=["jpg", "png", "jpeg"])

        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")
        foreign_languages = st.text_input("ភាសាបរទេស (Foreign Languages)")
        general_education_level = st.text_input("កម្រិតការអប់រំទូទៅ (General Education Level)")
        work_history = st.text_area("ប្រវត្តិការងារ (Work History)")

        # Dropdowns for selecting FactoryID, CompanyID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        request_details = st.text_area("សេចក្តីលម្អិតនៃសំណើ (Request Details)")

        # Dropdowns for selecting FactoryID, CompanyID, AddressID, and PersonalInforForApplicantID
        selected_factory_id = st.selectbox("ជ្រើសរើសរោងចក្រ (Select Factory)", options=list(factory_options.keys()), format_func=lambda x: factory_options[x])
        selected_company_id = st.selectbox("ជ្រើសរើសក្រុមហ៊ុន (Select Company)", options=list(company_options.keys()), format_func=lambda x: company_options[x])
        selected_address_id = st.selectbox("ជ្រើសរើសអាសយដ្ឋាន (Select Address)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_personal_info_id = st.selectbox("ជ្រើសរើសព័ត៌មានផ្ទាល់ខ្លួនរបស់អ្នកដាក់ពាក្យ (Select Applicant)", options=list(personal_info_options.keys()), format_func=lambda x: personal_info_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}

    with st.form(key='doc_applic_licese_cam_metrotrand_form'):
        # File uploader for each document
        metrology_registration_certificate = st.file_uploader("វិញ្ញាបនបត្រចុះឈ្មោះវាស់វែង (Metrology Registration Certificate)", type=['pdf', 'jpg', 'png'])
        statute_company = st.file_uploader("ច្បាប់ក្រុមហ៊ុន (Statute Company)", type=['pdf', 'jpg', 'png'])
        expired_license = st.file_uploader("អាជ្ញាប័ណ្ណផុតកំណត់ប្រើប្រាស់វាស់វែងកម្ពុជា (Expired License Use Cambodia Metrology)", type=['pdf', 'jpg', 'png'])
        inspection_certificate = st.file_uploader("វិញ្ញាបនបត្រត្រួតពិនិត្យ (Inspection Verification Certificate)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting ApplicationMetrologyID
        selected_application_id = st.selectbox("ជ្រើសរើសលេខសម្គាល់កម្មវិធីវាស់វែង (Select Application Metrology)", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    product_data = db_helper.fetch_data('product', ['ProductID', 'ProductName'])
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])
    prototype_approval_data = db_helper.fetch_data('applic_prototype_approval_certificate', ['Applicatio_Prototype_Approval_CertificateID'])
    recognition_internal_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])
    doc_license_data = db_helper.fetch_data('doc_applic_licese_cam_metrotrand', ['DocAppliLiceUseCamMetroTrandID'])
    import_permision_equipment = db_helper.fetch_data('applic_checking_importpermmetro_equipment', ['ApplicationImportPermissionMetrologyEquipmentID'])

    db_helper.close_connection()

    # Prepare dropdown options
    product_options = {row[0]: row[1] for row in product_data}
    application_options = {row[0]: f"Application ID: {row[0]}" for row in application_data}
    repair_options = {row[0]: f"Application License Repair Metrology ID: {row[0]}" for row in license_repair_data}
    prototype_options = {row[0]: f"Application Prototype Approval Certificate ID: {row[0]}" for row in prototype_approval_data}
    recognition_options = {row[0]: f"Application Certificate Recognition Internal Industry ID: {row[0]}" for row in recognition_internal_data}
    license_in_cambodia_options = {row[0]: f"Document Application License Metrology Using in Cambodia ID: {row[0]}" for row in doc_license_data}
    application_permision_import_options = {row[0]: f"Application Checking Import Permission Metrology Equipment ID: {row[0]}" for row in import_permision_equipment}

    with st.form(key='metrology_instrument_form'):
        instrument_name = st.text_input("ឈ្មោះឧបករណ៍ | Instrument Name")
        serial_number = st.text_input("លេខសេរី | Serial Number")
        calibration_level = st.text_input("កម្រិតកាលីប្រេស្យិន | Calibration Level")
        calibration_number = st.text_input("លេខកាលីប្រេស្យិន | Calibration Number")
        other = st.text_area("ព័ត៌មានផ្សេងទៀត | Other Information")
        calibration_certificate_number = st.text_input("លេខវិញ្ញាបនបត្រកាលីប្រេស្យិន | Calibration Certificate Number")

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល | Select Product", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_application_id = st.selectbox("ជ្រើសរើសកម្មវិធីវាស់វែង | Select Application Metrology", options=list(application_options.keys()), format_func=lambda x: application_options[x])
        selected_Repair_License_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណជួសជុល | Select License Repair Metrology", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])
        selected_Prototype_Approval_id = st.selectbox("ជ្រើសរើសការអនុម័តគំរូ | Select Prototype Approval", options=list(prototype_options.keys()), format_func=lambda x: prototype_options[x])
        selected_recognition_id = st.selectbox("ជ្រើសរើសការស្គាល់ផ្ទៃក្នុង | Select Recognition Internal", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])
        selected_License_Metrology_Cambodia_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណប្រើប្រាស់ | Select License Metrology Using in Cambodia", options=list(license_in_cambodia_options.keys()), format_func=lambda x: license_in_cambodia_options[x])
        selected_permision_import_id = st.selectbox("ជ្រើសរើសអនុញ្ញាតនាំចូល | Select License", options=list(application_permision_import_options.keys()), format_func=lambda x: application_permision_import_options[x])

        submit_button = st.form_submit_button("បញ្ជូន | Submit")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    calibration_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])
    repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    calibration_options = {row[0]: f"Application Metrology ID: {row[0]}" for row in calibration_data}
    repair_options = {row[0]: f"Repair License ID: {row[0]}" for row in repair_data}

    with st.form(key='certificate_calibration_form'):
        result_calibration_no = st.number_input("លេខលទ្ធផលការវាស់វែងត្រឹមត្រូវ (Result Calibration Number)", min_value=0, step=1)

        # Dropdowns for selecting foreign keys
        selected_calibration_id = st.selectbox("ជ្រើសរើសលេខសម្គាល់កម្មវិធីវាស់វែង (Select Application Metrology)", options=list(calibration_options.keys()), format_func=lambda x: calibration_options[x])
        selected_repair_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណជួសជុល (Select Repair License)", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    metrology_instrument_data = db_helper.fetch_data('metrology_intrument', ['idMetrologyIntrument'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_options = {row[0]: f"Instrument ID: {row[0]}" for row in metrology_instrument_data}

    with st.form(key='instrument_infor_form'):
        product_capability = st.text_input("សមត្ថភាពផលិតផល (Product Capability)")
        produce_country = st.text_input("ប្រទេសផលិត (Country of Production)")
        location_using = st.text_input("ទីតាំងប្រើប្រាស់ (Location of Use)")

        # Dropdown for selecting Metrology Instrument ID
        selected_instrument_id = st.selectbox("ជ្រើសរើសឧបករណ៍វាស់វែង (Select Metrology Instrument)", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    metrology_instrument_data = db_helper.fetch_data('metrology_intrument', ['idMetrologyIntrument'])
    repair_license_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_options = {row[0]: f"Instrument ID: {row[0]}" for row in metrology_instrument_data}
    repair_options = {row[0]: f"Repair License ID: {row[0]}" for row in repair_license_data}

    with st.form(key='instrument_detail_repair_form'):
        name_metrology_list = st.text_input("ឈ្មោះបញ្ជីឧបករណ៍វាស់វែង (Name of Metrology List)")
        quantity = st.text_input("បរិមាណ (Quantity)")
        code_number = st.text_input("លេខកូដ (Code Number)")
        condition = st.text_input("លក្ខខណ្ឌ (Condition)")
        description_technical_specifications = st.text_area("ការពិពណ៌នាលក្ខណៈបច្ចេកទេស (Technical Specifications Description)")

        # Dropdowns for selecting foreign keys
        selected_repair_id = st.selectbox("ជ្រើសរើសអាជ្ញាប័ណ្ណជួសជុល (Select Repair License)", options=list(repair_options.keys()), format_func=lambda x: repair_options[x])
        selected_instrument_id = st.selectbox("ជ្រើសរើសឧបករណ៍វាស់វែង (Select Metrology Instrument)", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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
        model = st.text_input("ម៉ូដែល (Model)")
        method_calibration = st.text_input("វិធីសាស្រ្តវាស់វែងត្រឹមត្រូវ (Method of Calibration)")
        accept_date = st.date_input("កាលបរិច្ឆេទទទួលយក (Accept Date)")
        date_calibration = st.date_input("កាលបរិច្ឆេទវាស់វែងត្រឹមត្រូវ (Date of Calibration)", min_value=datetime(1990,1,1))
        date_recalibration = st.date_input("កាលបរិច្ឆេទវាស់វែងត្រឹមត្រូវម្តងទៀត (Date of Recalibration)", min_value=datetime(1990,1,1))

        # Dropdowns for selecting foreign keys
        selected_product_id = st.selectbox("ជ្រើសរើសផលិតផល (Select Product)", options=list(product_options.keys()), format_func=lambda x: product_options[x])
        selected_instrument_id = st.selectbox("ជ្រើសរើសឧបករណ៍វាស់វែង (Select Metrology Instrument)", options=list(instrument_options.keys()), format_func=lambda x: instrument_options[x])
        selected_detail_repair_id = st.selectbox("ជ្រើសរើសព័ត៌មានលម្អិតអំពីការជួសជុលឧបករណ៍ (Select Instrument Detail for Repair)", options=list(detail_repair_options.keys()), format_func=lambda x: detail_repair_options[x])

        submit_button = st.form_submit_button("បញ្ជូន (Submit)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    instrument_infor_data = db_helper.fetch_data('intrument_infor', ['idIntrumentInfor'])
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    instrument_infor_options = {row[0]: f"Instrument Information ID: {row[0]} (លេខសម្គាល់ព័ត៌មានឧបករណ៍: {row[0]})" for row in instrument_infor_data}
    license_repair_options = {row[0]: f"License Repair ID: {row[0]} (លេខសម្គាល់ការជួសជុលអាជ្ញាប័ណ្ណ: {row[0]})" for row in license_repair_data}

    with st.form(key='business_infor_form'):
        type_business = st.text_input("Type of Business (ប្រភេទអាជីវកម្ម)")
        business_characteristics = st.text_area("Business Characteristics (លក្ខណៈពិសេសអាជីវកម្ម)")
        initial_capital = st.text_input("Initial Capital (ដើមទុនដំបូង)")
        business_location_size = st.text_input("Business Location Size (ទំហំទីតាំងអាជីវកម្ម)")

        # Dropdowns for selecting foreign keys
        selected_instrument_infor_id = st.selectbox("Select Instrument Information (ជ្រើសព័ត៌មានឧបករណ៍)", options=list(instrument_infor_options.keys()), format_func=lambda x: instrument_infor_options[x])
        selected_license_repair_id = st.selectbox("Select License Repair (ជ្រើសការជួសជុលអាជ្ញាប័ណ្ណ)", options=list(license_repair_options.keys()), format_func=lambda x: license_repair_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    business_infor_data = db_helper.fetch_data('business_infor', ['idBusinessInfor'])

    db_helper.close_connection()

    # Prepare dropdown options
    business_infor_options = {row[0]: f"Business Information ID: {row[0]} (លេខសម្គាល់ព័ត៌មានអាជីវកម្ម: {row[0]})" for row in business_infor_data}

    with st.form(key='workforce_form'):
        technicians = st.text_input("Technicians (ជាងបច្ចេកទេស)")
        total_workforce = st.text_input("Total Workforce (កម្លាំងពលកម្មសរុប)")

        # Dropdown for selecting Business Information ID
        selected_business_infor_id = st.selectbox("Select Business Information (ជ្រើសព័ត៌មានអាជីវកម្ម)", options=list(business_infor_options.keys()), format_func=lambda x: business_infor_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

        if submit_button:
            form_inputs = [
                technicians,
                total_workforce,
                selected_business_infor_id
            ]

            submit_form(
                table_name='workforce',
                columns=[
                    'Technicians',
                    'Total_workforce',
                    'idBusinessInfor'
                ],
                form_inputs=form_inputs
            )

def submit_family_infor_form():

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    address_data = db_helper.fetch_data('address', ['addressID', 'OfficeAddress'])
    certificate_recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    address_options = {row[0]: f"Address ID: {row[0]} - {row[1]} (លេខសម្គាល់អាសយដ្ឋាន: {row[0]} - {row[1]})" for row in address_data}
    certificate_recognition_options = {row[0]: f"Certificate Recognition Internal ID: {row[0]} (លេខសម្គាល់ការទទួលស្គាល់វិញ្ញាបនបត្រក្នុងស្រុក: {row[0]})" for row in certificate_recognition_data}

    with st.form(key='family_infor_form'):
        name_of_spouse = st.text_input("Name of Husband or Wife (ឈ្មោះប្តីឬប្រពន្ធ)")
        date_of_birth = st.date_input("Date of Birth (ថ្ងៃខែឆ្នាំកំណើត)", min_value=datetime(1990,1,1))
        number_of_children = st.number_input("Number of Daughters and Sons (ចំនួនកូនស្រីនិងកូនប្រុស)", min_value=0, step=1)
        occupation = st.text_input("Occupation (មុខរបរ)")

        # Dropdown for selecting Address ID and Application Certificate Recognition Internal ID
        selected_address_id = st.selectbox("Select Address (ជ្រើសអាសយដ្ឋាន)", options=list(address_options.keys()), format_func=lambda x: address_options[x])
        selected_certificate_recognition_id = st.selectbox("Select Application Certificate Recognition Internal (ជ្រើសការទទួលស្គាល់វិញ្ញាបនបត្រក្នុងស្រុក)", options=list(certificate_recognition_options.keys()), format_func=lambda x: certificate_recognition_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    family_info_data = db_helper.fetch_data('family_infor', ['idfamilyInfor', 'name_of_husband_or_wife'])

    db_helper.close_connection()

    # Prepare dropdown options
    family_info_options = {row[0]: f"Family Info ID: {row[0]} - {row[1]} (លេខសម្គាល់ព័ត៌មានគ្រួសារ: {row[0]} - {row[1]})" for row in family_info_data}

    with st.form(key='background_application_form'):
        language = st.text_input("Language (ភាសា)")
        education_level = st.text_input("Education Level (កម្រិតការអប់រំ)")
        any_training = st.text_input("Any Training (ការបណ្តុះបណ្តាលណាមួយ)")
        work_experience = st.text_area("Work Experience (បទពិសោធន៍ការងារ)")
        background_application_col = st.text_area("Additional Background Information (ព័ត៌មានផ្ទៃខាងក្រោយបន្ថែម)")

        # Dropdown for selecting Family Information ID
        selected_family_info_id = st.selectbox("Select Family Information (ជ្រើសព័ត៌មានគ្រួសារ)", options=list(family_info_options.keys()), format_func=lambda x: family_info_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំ: {row[0]})" for row in application_data}

    with st.form(key='doc_applic_metrology_calibration_form'):
        # File uploaders for each document
        statute_technical = st.file_uploader("Statute Technical (ច្បាប់បច្ចេកទេស)", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter (លិខិតផ្ទេរ)", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card (អត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology ID
        selected_application_id = st.selectbox("Select Application Metrology (ជ្រើសពាក្យស្នើសុំមាត្រដ្ឋាន)", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    application_data = db_helper.fetch_data('applic_calibration_metrology', ['ApplicationMetrologyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    application_options = {row[0]: f"Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំ: {row[0]})" for row in application_data}

    with st.form(key='doc_applic_metro_calibra_second_form'):
        # File uploaders for each document
        expired_metrology_certificate = st.file_uploader("Expired Metrology Certificate (វិញ្ញាបនបត្រមាត្រដ្ឋានផុតកំណត់)", type=['pdf', 'jpg', 'png'])
        photograph_4x6cm = st.file_uploader("4x6 cm Photograph (រូបថត 4x6 សង់ទីម៉ែត្រ)", type=['jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card (អត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology ID
        selected_application_id = st.selectbox("Select Application Metrology (ជ្រើសពាក្យស្នើសុំមាត្រដ្ឋាន)", options=list(application_options.keys()), format_func=lambda x: application_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    license_repair_data = db_helper.fetch_data('applic_license_repair_metrology', ['licenserepair_metrologyId'])

    db_helper.close_connection()

    # Prepare dropdown options
    repair_license_options = {row[0]: f"License Repair ID: {row[0]} (លេខសម្គាល់ការជួសជុលអាជ្ញាប័ណ្ណ: {row[0]})" for row in license_repair_data}

    with st.form(key='doc_applic_license_repair_metrology_form'):
        # File uploaders for each document
        expired_license_repair = st.file_uploader("Expired License Repair Metrology Equipment (ឧបករណ៍ជួសជុលអាជ្ញាប័ណ្ណមាត្រដ្ឋានផុតកំណត់)", type=['pdf', 'jpg', 'png'])
        metrology_registration_certificate = st.file_uploader("Metrology Registration Certificate (វិញ្ញាបនបត្រចុះបញ្ជីមាត្រដ្ឋាន)", type=['pdf', 'jpg', 'png'])
        specialization_certificate = st.file_uploader("Certificate or Proof of Specialization of Applicant (វិញ្ញាបនបត្រឬភស្តុតាងនៃការបច្ចេកទេសរបស់អ្នកដាក់ពាក្យ)", type=['pdf', 'jpg', 'png'])
        technical_drawings = st.file_uploader("Technical Drawings of Requested Metrology Equipment (គំនូរបច្ចេកទេសនៃឧបករណ៍មាត្រដ្ឋានដែលបានស្នើសុំ)", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card (អត្តសញ្ញាណប័ណ្ណ)", type=['pdf', 'jpg', 'png'])
        transfer_rights_letter = st.file_uploader("Transfer Rights Letter (លិខិតផ្ទេរសិទ្ធិ)", type=['pdf', 'jpg', 'png'])
        statute_company = st.file_uploader("Statute Company (ច្បាប់ក្រុមហ៊ុន)", type=['pdf', 'jpg', 'png'])
        photograph_4x6 = st.file_uploader("4x6 Photograph (រូបថត 4x6)", type=['jpg', 'png'])

        # Dropdown for selecting License Repair ID
        selected_license_repair_id = st.selectbox("Select License Repair (ជ្រើសការជួសជុលអាជ្ញាប័ណ្ណ)", options=list(repair_license_options.keys()), format_func=lambda x: repair_license_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំត្រួតពិនិត្យ: {row[0]})" for row in verification_data}

    with st.form(key='doc_applic_metrology_verify_form'):
        # File uploaders for each document
        transfer_letter = st.file_uploader("Transfer Letter (លិខិតផ្ទេរ)", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card (អត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify (ជ្រើសពាក្យស្នើសុំត្រួតពិនិត្យមាត្រដ្ឋាន)", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំត្រួតពិនិត្យ: {row[0]})" for row in verification_data}

    with st.form(key='doc_applic_metro_verify_second_form'):
        # File uploader for initial verification document
        initial_verification = st.file_uploader("Initial Verification Previous Usage (ការត្រួតពិនិត្យដំបូងនៃការប្រើប្រាស់មុន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify (ជ្រើសពាក្យស្នើសុំត្រួតពិនិត្យមាត្រដ្ឋាន)", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំត្រួតពិនិត្យ: {row[0]})" for row in verification_data}

    with st.form(key='doc_applic_metro_verify_third_form'):
        # File uploaders for documents
        info_image_imported = st.file_uploader("Information Image of Imported Package (រូបភាពព័ត៌មាននៃកញ្ចប់នាំចូល)", type=['pdf', 'jpg', 'png'])
        technical_doc_imported = st.file_uploader("Technical Document of Imported Package (ឯកសារបច្ចេកទេសនៃកញ្ចប់នាំចូល)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify (ជ្រើសពាក្យស្នើសុំត្រួតពិនិត្យមាត្រដ្ឋាន)", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    verification_data = db_helper.fetch_data('applic_metro_verify', ['ApplicationMetrologyVerifyID'])

    db_helper.close_connection()

    # Prepare dropdown options
    verification_options = {row[0]: f"Verification Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំត្រួតពិនិត្យ: {row[0]})" for row in verification_data}

    with st.form(key='doc_appli_metro_verify_import_forth_form'):
        # File uploader for technical document
        technical_doc_imported = st.file_uploader("Technical Document of Imported Package (ឯកសារបច្ចេកទេសនៃកញ្ចប់នាំចូល)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Metrology Verify ID
        selected_verification_id = st.selectbox("Select Application Metrology Verify (ជ្រើសពាក្យស្នើសុំត្រួតពិនិត្យមាត្រដ្ឋាន)", options=list(verification_options.keys()), format_func=lambda x: verification_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    recognition_options = {row[0]: f"Recognition Application ID: {row[0]} (លេខសម្គាល់ពាក្យស្នើសុំទទួលស្គាល់: {row[0]})" for row in recognition_data}

    with st.form(key='doc_applc_certific_recogin_form'):
        # File uploaders for each document
        transfer_letter = st.file_uploader("Transfer Letter (លិខិតផ្ទេរ)", type=['pdf', 'jpg', 'png'])
        passport_card = st.file_uploader("ID Passport Card (អត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)", type=['pdf', 'jpg', 'png'])
        certificate_recognition = st.file_uploader("Certificate of Metrology Expertise Recognition (វិញ្ញាបនបត្រទទួលស្គាល់ជំនាញមាត្រដ្ឋាន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Application Certificate Recognition Internal ID
        selected_recognition_id = st.selectbox("Select Application Certificate Recognition Internal (ជ្រើសពាក្យស្នើសុំទទួលស្គាល់វិញ្ញាបនបត្រ)", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    recognition_data = db_helper.fetch_data('applic_certific_recognition_internal_indu', ['idApplicationCertificateRecognitionInternal'])

    db_helper.close_connection()

    # Prepare dropdown options
    recognition_options = {row[0]: f"Recognition ID: {row[0]} (លេខសម្គាល់ការទទួលស្គាល់: {row[0]})" for row in recognition_data}

    with st.form(key='doc_applic_certif_recog_expertise_form'):
        training_certificate = st.file_uploader("Training Certificate (វិញ្ញាបនបត្របណ្តុះបណ្តាល)", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card (អត្តសញ្ញាណប័ណ្ណ)", type=['pdf', 'jpg', 'png'])
        photo_4x6 = st.file_uploader("4x6 Photo (រូបថត 4x6)", type=['jpg', 'png'])

        # Dropdown for selecting Application Certificate Recognition Internal ID
        selected_recognition_id = st.selectbox("Select Recognition Application (ជ្រើសពាក្យស្នើសុំទទួលស្គាល់)", options=list(recognition_options.keys()), format_func=lambda x: recognition_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    prototype_data = db_helper.fetch_data('applic_prototype_approval_certificate', ['Applicatio_Prototype_Approval_CertificateID'])

    db_helper.close_connection()

    # Prepare dropdown options
    prototype_options = {row[0]: f"Prototype Approval ID: {row[0]} (លេខសម្គាល់ការអនុម័តគំរូ: {row[0]})" for row in prototype_data}

    with st.form(key='doc_applic_protoapprove_certificate_form'):
        statute_technical = st.file_uploader("Statute Technical (ច្បាប់បច្ចេកទេស)", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter (លិខិតផ្ទេរ)", type=['pdf', 'jpg', 'png'])
        id_passport_card = st.file_uploader("ID Passport Card (អត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Prototype Approval Certificate ID
        selected_prototype_id = st.selectbox("Select Prototype Approval (ជ្រើសការអនុម័តគំរូ)", options=list(prototype_options.keys()), format_func=lambda x: prototype_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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

    db_helper = DatabaseHelper()

    # Fetch necessary data for dropdowns
    import_permission_data = db_helper.fetch_data('applic_checking_importpermmetro_equipment', ['ApplicationImportPermissionMetrologyEquipmentID'])

    db_helper.close_connection()

    # Prepare dropdown options
    import_permission_options = {row[0]: f"Import Permission ID: {row[0]} (លេខសម្គាល់ការអនុញ្ញាតនាំចូល: {row[0]})" for row in import_permission_data}

    with st.form(key='doc_applic_importper_metroequi_form'):
        extract_of_information_picture = st.file_uploader("Extract of Information Picture (រូបភាពព័ត៌មាន)", type=['pdf', 'jpg', 'png'])
        identification_card = st.file_uploader("Identification Card (អត្តសញ្ញាណប័ណ្ណ)", type=['pdf', 'jpg', 'png'])
        transfer_letter = st.file_uploader("Transfer Letter (លិខិតផ្ទេរ)", type=['pdf', 'jpg', 'png'])

        # Dropdown for selecting Import Permission ID
        selected_import_permission_id = st.selectbox("Select Import Permission (ជ្រើសការអនុញ្ញាតនាំចូល)", options=list(import_permission_options.keys()), format_func=lambda x: import_permission_options[x])

        submit_button = st.form_submit_button("Submit (បញ្ជូន)")

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
