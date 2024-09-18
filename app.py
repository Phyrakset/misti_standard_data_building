import streamlit as st
from scripts.render_form import submit_type_of_application_form,submit_raw_water_source_form

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Submit Type of Application", "Submit Raw Water Source"])

    if selection == "Home":
        st.title("Welcome to the Home Page")
        st.write("Use the sidebar to navigate through the app.")
    
    elif selection == "Submit Type of Application":
        submit_type_of_application_form()
    
    elif selection == "Submit Raw Water Source":
        submit_raw_water_source_form()

if __name__ == "__main__":
    main()