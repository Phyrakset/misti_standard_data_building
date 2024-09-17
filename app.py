# app.py
import streamlit as st
import mysql.connector
from config import get_connection

def fetch_table_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

def main():
    st.title("Survey Form")
    
    # Fetch table names from the database
    tables = fetch_table_names()

    # Create a form
    with st.form(key='survey_form'):
        st.write("Please fill out the survey below:")

        # Dynamically create form fields based on the database schema
        for table in tables:
            st.subheader(f"Table: {table}")
            table_name = st.text_input(f"Enter your {table} name:")
            st.text_area(f"Enter details for {table}:")

        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            st.write("Thank you for your submission!")
            # Handle form submission and save data to the database or process it

if __name__ == "__main__":
    main()
