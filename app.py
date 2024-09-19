import streamlit as st
from PIL import Image
from scripts.render_form import (submit_type_of_application_form, submit_raw_water_source_form
                                 ,submit_for_of_oficial_user_only_form
                                 ,submit_company_form
                                 )


# Function to display the ministry's logo and align it with the name
def display_logo_with_name():
    # Load and display the image using Streamlit's st.image function
    image = Image.open("images/05_Ministry.png")
    
    # Display the logo and title in a horizontal layout
    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.image(image, width=100)  # Adjust width as needed
        
    with col2:
        st.markdown("<h3 style='text-align: left;'>Ministry of Industry, Science, Technology, and Innovation</h3>", unsafe_allow_html=True)

# Main function to handle navigation and different sections of the app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Submit Type of Application","Submit Company","Submit Official User Data", "Submit Raw Water Source"])

    # Home Section
    if selection == "Home":
        # Display the ministry's logo aligned with the title
        display_logo_with_name()
        st.subheader("Data Management System Platform")
        
        # Adding interactive description
        st.write(
            """
            This platform allows you to manage and submit critical data for various departments under the ministry. 
            Use the sidebar to navigate through different sections of the app.
            
            - **Submit Type of Application**: For submitting details of different applications.
            - **Submit Company**: For submitting some comapany information.
            - **Submit Official User Data**: For submitting Officer information
            - **Submit Raw Water Source**: For managing water source data.
            """
        )
        
    # Submit Type of Application Section
    elif selection == "Submit Type of Application":
        st.header("Submit Type of Application")
        submit_type_of_application_form()

    # Submit Raw Water Source Section
    elif selection == "Submit Raw Water Source":
        st.header("Submit Raw Water Source")
        submit_raw_water_source_form()
    
    # Submit Official User Data Section
    elif selection == "Submit Official User Data":
        st.header("Submit Official User Data")
        submit_for_of_oficial_user_only_form()
    # Submit Company Section
    elif selection == "Submit Company":
        st.header("Submit Company")
        submit_company_form()


# Entry point of the app
if __name__ == "__main__":
    main()
