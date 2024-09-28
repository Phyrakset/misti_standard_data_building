# config.py
import streamlit as st
import os
import mysql.connector

def is_cloud_env():
    # Check for the existence of an environment variable or another method to detect cloud
    return os.getenv("STREAMLIT_ENV") == "cloud"

def get_connection():
    if not is_cloud_env():
        # Only try to connect to the database when running locally
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="phyrak23",  # Your local DB password
            database="misti"
        )
    else:
        # On cloud, you should not attempt to connect to the database
        raise RuntimeError("Database connections are not allowed in cloud environments")