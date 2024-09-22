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
    submit_infor_quality_controlprogram_form,
    submit_infor_investment_asset_form,
    submit_infor_machinery_facilities_form,
    submit_infor_planed_product_output_form,
    submit_infor_product_waste_form,
    submit_applic_calibration_metrology_form,
    submit_doc_applic_metrology_calibration_form,
    submit_applic_license_repair_metrology_form,
    submit_applic_metro_verify_form,
    submit_applic_certific_recog_metro_expertise_form,
    submit_applic_checking_importpermmetro_equipment_form,
    submit_applic_prototype_approval_certificate_form,
    submit_applic_certific_recognition_internal_indu_form,
    submit_doc_applic_licese_cam_metrotrand_form,
    submit_metrology_instrument_form,
    submit_certificate_calibration_form,
    submit_instrument_infor_form,
    submit_instrument_detail_repair_form,
    submit_result_of_calibration_form,
    submit_business_infor_form,
    submit_workforce_form,
    submit_family_infor_form,
    submit_background_application_form,
    submit_doc_applic_metrology_calibration_form,
    submit_doc_applic_metro_calibra_second_form,
    submit_doc_applic_license_repair_metrology_form,
    submit_doc_applic_metrology_verify_form,
    submit_doc_applic_metro_verify_second_form,
    submit_doc_applic_metro_verify_third_form,
    submit_doc_appli_metro_verify_import_forth_form,
    submit_doc_applc_certific_recogin_form,
    submit_doc_applic_certif_recog_expertise_form,
    submit_doc_applic_protoapprove_certificate_form,
    submit_doc_applic_importper_metroequi_form,
)

# Function to display the ministry's logo and align it with the name in both Khmer and English
def display_logo_with_name():
    image = Image.open("images/05_Ministry.png")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(image, width=100)
    with col2:
     st.markdown(
        """
        <h2 style='text-align: left;'>ក្រសួងឧស្សាហកម្ម វិទ្យាសាស្រ្ត បច្ចេកវិទ្យា និងវិចិត្រសិល្ប </h2>
        <h3 style='text-align: left;'>Ministry of Industry, Science, Technology, and Innovation</h3>
        """, unsafe_allow_html=True
    )
# Dictionary to map form types to their corresponding functions
form_mapping = {
    "Submit Type of Application (ដាក់ស្នើប្រភេទនៃពាក្យសុំ)": submit_type_of_application_form,
    "Submit Company (ដាក់ស្នើព័ត៌មានក្រុមហ៊ុន)": submit_company_form,
    "Submit Company Signature (ដាក់ស្នើហត្ថលេខាក្រុមហ៊ុន)": submit_company_signature_form,
    "Submit Official User Data (ដាក់ស្នើព័ត៌មានសម្រាប់អ្នកប្រើប្រាស់ផ្លូវការ)": submit_for_of_oficial_user_only_form,
    "Submit Applicant Information (ដាក់ស្នើព័ត៌មានអ្នកដាក់ពាក្យ)": submit_applicant_form,
    "Submit Personal Information (ដាក់ស្នើព័ត៌មានផ្ទាល់ខ្លួន)": submit_personal_info_form,
    "Submit National Card Or Passport (ដាក់ស្នើអត្តសញ្ញាណប័ណ្ណ ឬ លិខិតឆ្លងដែន)": submit_id_card_or_passport_form,
    "Submit Address Information (ដាក់ស្នើព័ត៌មានអាសយដ្ឋាន)": submit_address_form,
    "Submit Office Contact Information (ដាក់ស្នើព័ត៌មានទំនាក់ទំនងរបស់ការិយាល័យ)": submit_office_contact_form,
    "Submit Factory Information (ដាក់ស្នើព័ត៌មានរោងចក្រ)": submit_factory_form,
    "Submit Product Information (ដាក់ស្នើព័ត៌មានផលិតផល)": submit_product_form,
    "Submit License Information (ដាក់ស្នើព័ត៌មានអាជ្ញាប័ណ្ណ)": submit_license_form,
    "Submit Factory Inspection Report (ដាក់ស្នើរបាយការណ៍ត្រួតពិនិត្យរោងចក្រ)": submit_factory_inspection_report_form,
    "Submit Certificate of Conformity Information (ដាក់ស្នើវិញ្ញាបនប័ត្រស្តង់ដា)": submit_certificate_of_conformity_form,
    "Submit Test Report Information (ដាក់ស្នើរបាយការណ៍សាកល្បង)": submit_test_report_form,
    "Submit Patent Card Information (ដាក់ស្នើប័ណ្ណប៉ាតង់)": submit_patent_card_form,
    "Submit Document for Product or Spare Part Registration (ដាក់ស្នើឯកសារសម្រាប់ការចុះបញ្ជីផលិតផល ឬ ផ្នែកជំនួយ)": submit_doc_pro_or_spare_part_pro_registration_form,
    "Submit Document for Electrical and Electronic Product Registration (ដាក់ស្នើឯកសារសម្រាប់ការចុះបញ្ជីផលិតផលអគ្គិសនី និងអេឡិចត្រូនិក)": submit_doc_electri_and_electro_pro_registration_form,
    "Submit Information Detail of Modification for Part or Electrical Product (ដាក់ស្នើព័ត៌មានលម្អិតនៃការកែប្រែសម្រាប់ផលិតផល)": submit_infor_detail_of_modification_form,
    "Submit Document of Modification for Part Product (ដាក់ស្នើឯកសារនៃការកែប្រែសម្រាប់ផលិតផល)": submit_doc_of_modification_part_pro_form,
    "Submit Document of Modification for Electrical Part Product (ដាក់ស្នើឯកសារនៃការកែប្រែសម្រាប់ផ្នែកអគ្គិសនី)": submit_doc_of_modification_electri_electro_part_pro_form,
    "Submit Product Registration License (ដាក់ស្នើអាជ្ញាប័ណ្ណចុះបញ្ជីផលិតផល)": submit_pro_registration_license_form,
    "Submit Machinery Equipment in Factory (ដាក់ស្នើឯកសារអំពីឧបករណ៍ម៉ាស៊ីនក្នុងរោងចក្រ)": submit_machinery_equipment_in_factory_form,
    "Submit Document for Product Registration License (ដាក់ស្នើឯកសារចុះបញ្ជីអាជ្ញាប័ណ្ណ)": submit_doc_pro_regis_license_form,
    "Submit Production Chain (ដាក់ស្នើបណ្តាញផលិតកម្ម)": submit_production_chain_form,
    "Submit Raw Materials (ដាក់ស្នើព័ត៌មានសម្ភារដើម)": submit_raw_materials_form,
    "Submit Document for Representative Company (Electri/Electro/Spare Part) (ដាក់ស្នើឯកសារសម្រាប់ក្រុមហ៊ុនតំណាង)": submit_doc_represent_company_form,
    "Submit Document for Establishment of Factory (ដាក់ស្នើឯកសារសម្រាប់ការបង្កើតរោងចក្រ)": submit_doc_establishment_factory_form,
    "Submit Information for Investment Production Safety and Sanitary System (ដាក់ស្នើព័ត៌មានសម្រាប់ប្រព័ន្ធអនាម័យផលិតកម្ម)": submit_infor_invest_pro_safety_and_sanitary_system_form,
    "Submit Document for Investment Project Production Safety (ដាក់ស្នើឯកសារសម្រាប់គម្រោងផលិតភាពសុវត្ថិភាព)": submit_doc_for_inves_project_pro_safety_form,
    "Submit Document for Small Medium Enterprises Handicraft Permit (ដាក់ស្នើឯកសារសម្រាប់អាជ្ញាប័ណ្ណសិប្បកម្មអាជីវកម្មតូចនិងមធ្យម)": submit_doc_permit_small_medium_enterprises_handicraft_form,
    "Submit Information for Factory Manager (ដាក់ស្នើព័ត៌មានអ្នកគ្រប់គ្រងរោងចក្រ)": submit_infor_factory_manager_form,
    "Submit Information for Quality Control Program (ដាក់ស្នើព័ត៌មានកម្មវិធីត្រួតពិនិត្យគុណភាព)": submit_infor_quality_controlprogram_form,
    "Submit Information for Investment Asset (ដាក់ស្នើព័ត៌មានទ្រព្យសម្បត្តិវិនិយោគ)": submit_infor_investment_asset_form,
    "Submit Information for Machinery Facilities (ដាក់ស្នើព័ត៌មានសំភារៈម៉ាស៊ីន)": submit_infor_machinery_facilities_form,
    "Submit Planned Product Output Information (ដាក់ស្នើព័ត៌មានផលិតផលដែលបានគ្រោងទុក)": submit_infor_planed_product_output_form,
    "Submit Product Waste Information (ដាក់ស្នើព័ត៌មានសំរាមផលិតផល)": submit_infor_product_waste_form,
    "Submit Calibration Metrology Application (ដាក់ស្នើពាក្យសុំកាលីបមាត្រដ្ឋាន)": submit_applic_calibration_metrology_form,
    "Submit Metrology Calibration Application Documents (ដាក់ស្នើឯកសារពាក្យសុំព័ត៌មានមាត្រដ្ឋានកាលីប)": submit_doc_applic_metrology_calibration_form,
    "Submit License Repair Metrology Application (ដាក់ស្នើពាក្យសុំព័ត៌មានសម្រាប់ជួសជុលឧបករណ៍មាត្រដ្ឋាន)": submit_applic_license_repair_metrology_form,
    "Submit Metrology Verification Application (ដាក់ស្នើពាក្យសុំបញ្ជាក់មាត្រដ្ឋាន)": submit_applic_metro_verify_form,
    "Submit Application for Certificate Recognition in Metrology Expertise (ដាក់ស្នើពាក្យសុំវិញ្ញាបនប័ត្រទទួលស្គាល់ជំនាញមាត្រដ្ឋាន)": submit_applic_certific_recog_metro_expertise_form,
    "Submit Application for Checking Import Permission of Metrology Equipment (ដាក់ស្នើពាក្យសុំត្រួតពិនិត្យការនាំចូលឧបករណ៍មាត្រដ្ឋាន)": submit_applic_checking_importpermmetro_equipment_form,
    "Submit Application for Prototype Approval Certificate (ដាក់ស្នើពាក្យសុំវិញ្ញាបនប័ត្រអនុម័តគំរូ)": submit_applic_prototype_approval_certificate_form,
    "Submit Application for Internal Industry Certification Recognition (ដាក់ស្នើពាក្យសុំទទួលស្គាល់វិញ្ញាបនប័ត្រឧស្សាហកម្មក្នុងស្រុក)": submit_applic_certific_recognition_internal_indu_form,
    "Submit Application License for Cambodia Metrology and Standards (ដាក់ស្នើពាក្យសុំអាជ្ញាប័ណ្ណមាត្រដ្ឋានកម្ពុជា)": submit_doc_applic_licese_cam_metrotrand_form,
    "Submit Metrology Instrument Information (ដាក់ស្នើព័ត៌មានឧបករណ៍មាត្រដ្ឋាន)": submit_metrology_instrument_form,
    "Submit Calibration Certificate Information (ដាក់ស្នើព័ត៌មានវិញ្ញាបនប័ត្រកាលីប)": submit_certificate_calibration_form,
    "Submit Instrument Information (ដាក់ស្នើព័ត៌មានឧបករណ៍)": submit_instrument_infor_form,
    "Submit Instrument Detail for Repair (ដាក់ស្នើព័ត៌មានលម្អិតសម្រាប់ជួសជុលឧបករណ៍)": submit_instrument_detail_repair_form,
    "Submit Result of Calibration (ដាក់ស្នើលទ្ធផលកាលីប)": submit_result_of_calibration_form,
    "Submit Business Information (ដាក់ស្នើព័ត៌មានអាជីវកម្ម)": submit_business_infor_form,
    "Submit Workforce Information (ដាក់ស្នើព័ត៌មានកម្លាំងការងារ)": submit_workforce_form,
    "Submit Family Information (ដាក់ស្នើព័ត៌មានគ្រួសារ)": submit_family_infor_form,
    "Submit Background Application Information (ដាក់ស្នើព័ត៌មានទូទៅនៃពាក្យសុំ)": submit_background_application_form,
    "Submit Metrology Calibration Document Application (ដាក់ស្នើឯកសារពាក្យសុំកាលីបមាត្រដ្ឋាន)": submit_doc_applic_metrology_calibration_form,
    "Submit Second Metrology Calibration Document Application (ដាក់ស្នើឯកសារពាក្យសុំកាលីបមាត្រដ្ឋានទីពីរ)": submit_doc_applic_metro_calibra_second_form,
    "Submit License Repair Metrology Document Application (ដាក់ស្នើឯកសារពាក្យសុំជួសជុលមាត្រដ្ឋាន)": submit_doc_applic_license_repair_metrology_form,
    "Submit Metrology Verification Document Application (ដាក់ស្នើឯកសារពាក្យសុំបញ្ជាក់មាត្រដ្ឋាន)": submit_doc_applic_metrology_verify_form,
    "Submit Second Metrology Verification Document Application (ដាក់ស្នើឯកសារពាក្យសុំបញ្ជាក់មាត្រដ្ឋានទីពីរ)": submit_doc_applic_metro_verify_second_form,
     "Submit Third Metrology Verification Document Application (ដាក់ស្នើឯកសារពាក្យសុំបញ្ជាក់មាត្រដ្ឋានទីបី)": submit_doc_applic_metro_verify_third_form,
    "Submit Fourth Metrology Verification Document Application (ដាក់ស្នើឯកសារពាក្យសុំបញ្ជាក់មាត្រដ្ឋានទីបួន)": submit_doc_appli_metro_verify_import_forth_form,
    "Submit Certificate Recognition Document Application (ដាក់ស្នើឯកសារពាក្យសុំទទួលស្គាល់វិញ្ញាបនប័ត្រ)": submit_doc_applc_certific_recogin_form,
    "Submit Document for Certification Recognition Expertise (ដាក់ស្នើឯកសារសម្រាប់ទទួលស្គាល់ជំនាញវិញ្ញាបនប័ត្រ)": submit_doc_applic_certif_recog_expertise_form,
    "Submit Document for Prototype Approval Certificate (ដាក់ស្នើឯកសារសម្រាប់វិញ្ញាបនប័ត្រអនុម័តគំរូ)": submit_doc_applic_protoapprove_certificate_form,
    "Submit Document for Import Permission of Metrology Equipment (ដាក់ស្នើឯកសារសម្រាប់ការនាំចូលឧបករណ៍មាត្រដ្ឋាន)": submit_doc_applic_importper_metroequi_form,

    ## Chemical Submit
    "Submit Chemical Substance Information (ដាក់ស្នើព័ត៌មានស្តុកគីមី)": submit_list_chemical_substance_form,
    "Submit Previous Chemical Usage Information (ដាក់ស្នើព័ត៌មានការប្រើប្រាស់គីមីកន្លងមក)": submit_previous_chemical_usage_form,
    "Submit Application Details for Chemical Substance (ដាក់ស្នើព័ត៌មានលម្អិតសម្រាប់ស្តុកគីមី)": submit_appli_details_chemical_form,
    "Submit Chemical Production Plan Annual (ដាក់ស្នើផែនការផលិតគីមីប្រចាំឆ្នាំ)": submit_chemical_pro_plan_annual_form,
    "Submit Declaration for Buyer/Importer (ដាក់ស្នើការប្រាប់សម្រាប់អ្នកទិញ/នាំចូល)": submit_declaration_buyer_importer_form,
    "Submit Document for Recognition of Standard Chemical Substance (ដាក់ស្នើឯកសារសម្រាប់ទទួលស្គាល់ស្តុកគីមី)": submit_doc_recog_standard_chemical_substance_form,
    "Submit Document for Restricted Chemicals (ដាក់ស្នើឯកសារសម្រាប់គីមីដែលបានកំណត់)": submit_doc_restricted_chemicals_form,
    "Submit Information for Raw Material (ដាក់ស្នើព័ត៌មានសម្ភារដើម)": submit_infor_raw_material_form,

    ## Section WSMS Indicator
    "Submit Raw Water Source (ដាក់ស្នើប្រភពទឹកធម្មតា)": submit_raw_water_source_form,
    "Submit Human Resources Information (ដាក់ស្នើព័ត៌មានធនធានមនុស្ស)": submit_human_resources_form,
    "Submit Treatment Plan (ដាក់ស្នើផែនការព្យាបាល)": submit_treatment_plant_form,
    "Submit Water Quality Information (ដាក់ស្នើព័ត៌មានគុណភាពទឹក)": submit_water_quality_form,
    "Submit Commercial Information (ដាក់ស្នើព័ត៌មានពាណិជ្ជកម្ម)": submit_commercial_form,
    "Submit Financial Information (ដាក់ស្នើព័ត៌មានហិរញ្ញវត្ថុ)": submit_financial_form,
    "Submit Distribution Network Information (ដាក់ស្នើព័ត៌មានបណ្តាញចែកចាយ)": submit_distribution_network_form
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
