import streamlit as st
from PIL import Image
from scripts.render_form import (
    submit_type_of_application_form,
    submit_raw_water_source_form,
    submit_for_of_oficial_user_only_form,
    submit_company_form,
    submit_company_signature_form,
    submit_applicant_form,
    submit_personal_info_form,
    submit_id_card_or_passport_form,
    submit_address_form,
    submit_human_resources_form,
    submit_treatment_plant_form,
    submit_water_quality_form,
    submit_commercial_form,
    submit_financial_form,
    submit_distribution_network_form,
    submit_office_contact_form,
    submit_factory_form,
    submit_product_form,
    submit_license_form,
    submit_factory_inspection_report_form,
    submit_certificate_of_conformity_form,
    submit_test_report_form,
    submit_patent_card_form,
    submit_doc_pro_or_spare_part_pro_registration_form,
    submit_doc_electri_and_electro_pro_registration_form,
    submit_infor_detail_of_modification_form,
    submit_doc_of_modification_part_pro_form,
    submit_doc_of_modification_electri_electro_part_pro_form,
    submit_list_chemical_substance_form,
    submit_previous_chemical_usage_form,
    submit_appli_details_chemical_form,
    submit_chemical_pro_plan_annual_form,
    submit_declaration_buyer_importer_form,
    submit_doc_recog_standard_chemical_substance_form,
    submit_pro_registration_license_form,
    submit_machinery_equipment_in_factory_form,
    submit_doc_pro_regis_license_form,
    submit_production_chain_form,
    submit_raw_materials_form,
    submit_doc_restricted_chemicals_form,
    submit_doc_represent_company_form,
    submit_doc_establishment_factory_form,
    submit_infor_raw_material_form,
    submit_infor_invest_pro_safety_and_sanitary_system_form,
    submit_doc_for_inves_project_pro_safety_form,
    submit_doc_permit_small_medium_enterprises_handicraft_form,
    submit_infor_factory_manager_form,

)

# Function to display the ministry's logo and align it with the name
def display_logo_with_name():
    image = Image.open("images/05_Ministry.png")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(image, width=100)
    with col2:
        st.markdown("<h3 style='text-align: left;'>Ministry of Industry, Science, Technology, and Innovation</h3>", unsafe_allow_html=True)

# Dictionary to map form types to their corresponding functions
form_mapping = {
    "Submit Type of Application": submit_type_of_application_form,
    "Submit Company": submit_company_form,
    "Submit Company Signature": submit_company_signature_form,
    "Submit Official User Data": submit_for_of_oficial_user_only_form,
    "Submit Applicant Information": submit_applicant_form,
    "Submit Personal Information": submit_personal_info_form,
    "Submit National Card Or Passport": submit_id_card_or_passport_form,
    "Submit Address Information ": submit_address_form,
    "Submit office Contact Information": submit_office_contact_form,
    "Submit Factory Information": submit_factory_form,
    "Submit Product Information": submit_product_form,
    "Submit License Information": submit_license_form,
    "Submit Factory Inspection Report": submit_factory_inspection_report_form,
    "Submit Certificate of Conformity Information": submit_certificate_of_conformity_form,
    "Submit Test Report Information": submit_test_report_form,
    "Submit Patent Card Information": submit_patent_card_form,
    "Submit Document for Product or Spare Part Registration Form":submit_doc_pro_or_spare_part_pro_registration_form,
    "Submit Document for Electrical and Electronic Product Registration Form": submit_doc_electri_and_electro_pro_registration_form,
    "Submit Information Detail of Modification for Part or Electrical and Electronic Product": submit_infor_detail_of_modification_form,
    "Submit Document of Modification for Part Product":submit_doc_of_modification_part_pro_form,
    "Submit Document of Modification for Electrical and Electro Part Product": submit_doc_of_modification_electri_electro_part_pro_form,
    "Submit Product Registration License Form": submit_pro_registration_license_form,
    "Submit Machinery Equipment in Factory Form": submit_machinery_equipment_in_factory_form,
    "Submit Document for Product Registration License Form": submit_doc_pro_regis_license_form,
    "Submit Production Chain Form": submit_production_chain_form,
    "Submit Raw Materials Form": submit_raw_materials_form,
    "Submit Document for Representative Companies (Electri, Electro, or Spare Part)": submit_doc_represent_company_form,
    "Submit Document for Establishment of Factory": submit_doc_establishment_factory_form,
    "Submit Information for Investment Production Safety and Sanitary System": submit_infor_invest_pro_safety_and_sanitary_system_form,
    "Submit Document for Investment Project Production Safety": submit_doc_for_inves_project_pro_safety_form,
    "Submit Document for Small Medium Enterprises Handicraft Permit" : submit_doc_permit_small_medium_enterprises_handicraft_form,
    "Submit Information for Factory Manager": submit_infor_factory_manager_form,
    ## Chemical Submit
    "Submit Chemical Substance Information": submit_list_chemical_substance_form,
    "Submit Previous Chemical Usage Information": submit_previous_chemical_usage_form,
    "Submit Application Details for Chemical Substance": submit_appli_details_chemical_form,
    "Submit Chemical Production Plan Annual": submit_chemical_pro_plan_annual_form,
    "Submit Declaration for Buyer/Importer": submit_declaration_buyer_importer_form,
    "Submit Document for Recognition of Standard Chemical Substance": submit_doc_recog_standard_chemical_substance_form,
    "Submit Document for Restricted Chemicals" : submit_doc_restricted_chemicals_form,
    "Submit Information for Raw Material": submit_infor_raw_material_form,

    ## Section WSMS Indicator
    "Submit Raw Water Source": submit_raw_water_source_form,
    "Submit Human Resources Information": submit_human_resources_form,
    "Submit Treatment Plan": submit_treatment_plant_form,
    "Submit Water Quality Information": submit_water_quality_form,
    "Submit Comercial Information": submit_commercial_form,
    "Submit Financial Information": submit_financial_form,
    "Submit Distribution Network Information": submit_distribution_network_form,

    
  
    
}

# Main function to handle navigation and different sections of the app
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home"]+list(form_mapping.keys()))

    if selection == "Home":
        display_logo_with_name()
        st.subheader("Data Management System Platform")
        st.write(
            """
            This platform allows you to manage and submit critical data for various departments under the ministry. 
            Use the sidebar to navigate through different sections of the app.
            """
        )

    else:
        st.header(selection)
        # Call the corresponding form function based on the selection
        form_function = form_mapping[selection]
        form_function()

# Entry point of the app
if __name__ == "__main__":
    main()
