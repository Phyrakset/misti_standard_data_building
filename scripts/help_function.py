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


    def submit_raw_water_source_form(self, idRawWaterSource, code, RawWaterSource_name,
                                     availability_year_round, total_abstraction,
                                     Drawing_RawWater_PumpingStation, Drawing_Water_Transmission_Network,
                                     Drawing_Water_Treatment_Plant):
        """
        Inserts form data into the raw_watersource table in the database.
        """
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO raw_watersource (idRawWaterSource, code, RawWaterSource_name, 
                                         availability_year_round, total_abstraction, 
                                         Drawing_RawWater_PumpingStation, 
                                         Drawing_Water_Transmission_Network, 
                                         Drawing_Water_Treatment_Plant)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare data for insertion
            data = (
                idRawWaterSource, code, RawWaterSource_name,
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

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
