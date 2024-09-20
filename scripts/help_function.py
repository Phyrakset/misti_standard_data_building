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
    
    def insert_record(self, table_name, columns, values, return_id=True):
        """
        Inserts data into a specified table and returns the result.
        
        :param table_name: The name of the table to insert data into.
        :param columns: List of column names as a string to insert data into.
        :param values: List of values to insert into the corresponding columns.
        :return: Tuple (success, message, inserted_id) where inserted_id is the last inserted row ID if applicable.
        """
        try:
            cursor = self.connection.cursor()

            # Create a dynamic SQL query
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))

            query = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
            
            # Execute the query
            cursor.execute(query, values)
            self.connection.commit()

            if return_id:
        
                # Get the last inserted row ID (useful for auto-increment fields)
                inserted_id = cursor.lastrowid
                return True, f"Data added successfully to {table_name} Table in Database and  it's ID!: {inserted_id}", inserted_id
            else:

                return True, f"Data added successfully to {table_name} Table In Database!", None

        except mysql.connector.Error as err:
            return False, f"Error: {err}", None

        finally:
            cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
