# scripts/help_functions.py
import mysql.connector
from config import get_connection
from mysql.connector import Error

class DatabaseHelper:
    def __init__(self):
        self.connection = get_connection()

    def fetch_data(self, table_name, columns):
        """Fetches specified columns from a given table."""
        try:
            cursor = self.connection.cursor()
            query = f"SELECT {', '.join(columns)} FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return [], f"Error: {err}"
        finally:
            cursor.close()
    
    def insert_type_of_application(self, title, description=None):
        """Inserts a new type of application and returns the generated TypeOfApplicationID."""
        try:
            cursor = self.connection.cursor()

            # Ensure the title is not empty
            if not title:
                return False, "Title cannot be empty", None
            
            # Insert the data into the type_of_application table
            query = """
            INSERT INTO type_of_application (Title, Description)
            VALUES (%s, %s)
            """
            cursor.execute(query, (title, description))
            self.connection.commit()

            # Get the last inserted TypeOfApplicationID
            type_of_application_id = cursor.lastrowid

            return True, f"Type of application added successfully! ID: {type_of_application_id}", type_of_application_id
        
        except mysql.connector.Error as err:
            return False, f"Error: {err}", None
        
        finally:
            cursor.close()

            


    def submit_raw_water_source_form(self, code, RawWaterSource_name,
                                     availability_year_round, total_abstraction,
                                     Drawing_RawWater_PumpingStation, Drawing_Water_Transmission_Network,
                                     Drawing_Water_Treatment_Plant):
        """
        Inserts form data into the raw_watersource table in the database.
        """
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO raw_watersource (code, RawWaterSource_name, 
                                         availability_year_round, total_abstraction, 
                                         Drawing_RawWater_PumpingStation, 
                                         Drawing_Water_Transmission_Network, 
                                         Drawing_Water_Treatment_Plant)
            VALUES ( %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare data for insertion
            data = (
                 code, RawWaterSource_name,
                int(availability_year_round), total_abstraction,
                Drawing_RawWater_PumpingStation.read() if Drawing_RawWater_PumpingStation else None,
                Drawing_Water_Transmission_Network.read() if Drawing_Water_Transmission_Network else None,
                Drawing_Water_Treatment_Plant.read() if Drawing_Water_Treatment_Plant else None
            )
            
            cursor.execute(query, data)
            self.connection.commit()

            return True, "Data submitted successfully!"

        except Error as err:
            return False, f"Error: {err}"
        finally:
            cursor.close()
    
    def insert_for_of_oficial_user_only(self, safety_mark_number, officer_number, applicant_id):
        try:
            cursor = self.connection.cursor()
            
            # Check if the ApplicantID exists in the Applicant table
            check_query = "SELECT COUNT(*) FROM Applicant WHERE ApplicantID = %s"
            cursor.execute(check_query, (applicant_id,))
            exists = cursor.fetchone()[0]
            
            if not exists:
                return False, "Error: ApplicantID does not exist."

            # Insert the data into the for_of_oficial_user_only table
            insert_query = """
            INSERT INTO for_of_oficial_user_only (SafetyMarkNumber, OfficerNumber, ApplicantID)
            VALUES (%s, %s, %s)
            """
            data = (safety_mark_number, officer_number, applicant_id)
            cursor.execute(insert_query, data)
            self.connection.commit()
            return True, "Data submitted successfully!"
        
        except mysql.connector.Error as err:
            return False, f"Error: {err}"
        
        finally:
            cursor.close()
    
    def insert_company(self, name, email, address, phone, location_plan, type_of_application_id):
        try:
            cursor = self.connection.cursor()
            
            # Insert the data into the company table
            insert_query = """
            INSERT INTO company (Name, Email, Address, Phone, LocationPlan, TypeOfApplicationID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (
                name, email, address, phone,
                location_plan.read() if location_plan else None,
                type_of_application_id
            )
            cursor.execute(insert_query, data)
            self.connection.commit()

            # Get the last inserted TypeOfApplicationID
            company_id = cursor.lastrowid

            return True, f"Company added successfully! ID: {company_id}", company_id
 
        except mysql.connector.Error as err:
            return False, f"Error: {err}"
        
        finally:
            cursor.close()

    def insert_company_signature(self, name, date, position, signature, stamp, company_id):
        """Inserts a new company signature and stamp into the table and returns the generated CompanySignatureID."""
        try:
            cursor = self.connection.cursor()

            # Ensure the name and company_id are not empty
            if not name or not company_id:
                return False, "Name and Company must be provided", None
            
            # Insert the data into the company_signature_and_stamp table
            query = """
            INSERT INTO company_signatur_and_stamp 
            (Name, Date, Position, SignatureOrFingerprint, Stamp, CompanyID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (name, date, position, signature, stamp, company_id)
            cursor.execute(query, data)
            self.connection.commit()

            # Get the last inserted CompanySignatureID
            company_signature_id = cursor.lastrowid

            return True, f"Company signature and stamp added successfully! ID: {company_signature_id}", company_signature_id
        
        except mysql.connector.Error as err:
            return False, f"Error: {err}", None
        
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
