# config.py
import streamlit as st
import os
import mysql.connector

def get_connection():
    if os.getenv("STREAMLIT_ENV") == "cloud":
        # Cloud environment: Use Streamlit secrets
        secrets = st.secrets["mysql"]
        return mysql.connector.connect(
            host=secrets["host"],
            user=secrets["user"],
            password=secrets["password"],
            database=secrets["database"]
        )
    else:
        # Local environment: Use local MySQL configuration
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_local_password",  # Update with your local password
            database="misti"
        )
