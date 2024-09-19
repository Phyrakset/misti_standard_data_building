# scripts/help_functions.py
import mysql.connector
from config import get_connection
from mysql.connector import Error

class DatabaseHelper:
    def __init__(self):
        self.connection = get_connection()
    
    def insert_type_of_application(self, title, description):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO type_of_application (Title, Description)
            VALUES (%s, %s)
            """
            data = (title, description)
            cursor.execute(query, data)
            self.connection.commit()
            return True, "Data submitted successfully!"
        except mysql.connector.Error as err:
            return False, f"Error: {err}"


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
            
            # Check if the TypeOfApplicationID exists in the type_of_application table
            check_query = "SELECT COUNT(*) FROM type_of_application WHERE TypeOfApplicationID = %s"
            cursor.execute(check_query, (type_of_application_id,))
            exists = cursor.fetchone()[0]
            
            if not exists:
                return False, "Error: TypeOfApplicationID does not exist."

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
            return True, "Data submitted successfully!"
        
        except mysql.connector.Error as err:
            return False, f"Error: {err}"
        
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
