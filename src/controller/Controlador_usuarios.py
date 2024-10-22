# Importing to include the search path
import sys
sys.path.append("src")
sys.path.append(".")

import psycopg2
from controller import Secret_Config
from Model.User import User

# CONSTANTS
# Maximum age allowed
MAX_LIFE_EXPECTANCY_MALES = 84
MAX_LIFE_EXPECTANCY_FEMALES = 86

# Minimum age allowed
MIN_AGE = 62

# Minimum property value
MIN_PROPERTY_VALUE = 10000000

# Maximum and minimum interest rates allowed
MIN_INTEREST_RATE = 6
MAX_INTEREST_RATE = 43


# EXCEPTIONS
class ClientNotUpdatedException(Exception):
    """ 
    Custom exception for when the client cannot be updated
    """
    def __init__(self):
        super().__init__("The client could not be updated")

class ClientNotInsertedException(Exception):
    """ 
    Custom exception for when the client cannot be inserted into the table
    """
    def __init__(self):
        super().__init__("The client could not be inserted")

class ClientNotDeletedException(Exception):
    """ 
    Custom exception for when the client cannot be deleted from the table
    """
    def __init__(self):
        super().__init__("The client could not be deleted")

class AgeException(Exception):
    """ 
    Custom exception for age below minimum or above maximum
    """
    def __init__(self, age):
        super().__init__(f"The age: {age} is invalid; to apply for a reverse mortgage, one must be between {MIN_AGE} and {MAX_LIFE_EXPECTANCY_MALES}")

class NoneException(Exception):
    """ 
    Custom exception for None values
    """
    def __init__(self):
        super().__init__("There cannot be empty fields")

class PropertyValueException(Exception):
    """ 
    Custom exception for property values below the minimum
    """
    def __init__(self):
        super().__init__("Property value cannot be below the minimum")

class InterestRateException(Exception):
    """ 
    Custom exception for interest rates above the maximum, below the minimum, and zero
    """
    def __init__(self, interest_rate):
        super().__init__(f"The interest rate: {interest_rate} is invalid; it should not be less than {MIN_INTEREST_RATE} or greater than {MAX_INTEREST_RATE}")


class ClientController:

    @staticmethod
    def get_connection():
        """
        Creates a connection to the database and returns it
        """
        DATABASE = Secret_Config.PGDATABASE
        USER = Secret_Config.PGUSER
        PASSWORD = Secret_Config.PGPASSWORD
        HOST = Secret_Config.PGHOST
        PORT = Secret_Config.PGPORT
        
        # Connecting to the database
        return psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

    @staticmethod
    def create_table():
        """ 
        Creates the clients table in the database 
        """
        try:
            connection = ClientController.get_connection()
            cursor = connection.cursor()

            # Execute the query to create the table in the database
            cursor.execute("""CREATE TABLE Users (
                                id VARCHAR(20) NOT NULL PRIMARY KEY,
                                age VARCHAR(2) NOT NULL,
                                marital_status TEXT NOT NULL,
                                spouse_age VARCHAR(2),
                                spouse_gender TEXT,
                                property_value VARCHAR(20) NOT NULL,
                                interest_rate VARCHAR(4) NOT NULL)
                            """)
            
            # Confirm changes made to the database
            cursor.connection.commit()
            print("TABLE CREATED SUCCESSFULLY")
            print("\n")
        except psycopg2.errors.DuplicateTable:
            print("THE TABLE ALREADY EXISTS")
            print("\n")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def clear_table():
        """ 
        Deletes all records from the clients table in the database 
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        # Execute the query to delete all records from the table
        cursor.execute("DELETE FROM Clients")
        cursor.connection.commit()
        print("RECORDS DELETED SUCCESSFULLY")
        print("\n")
        cursor.close()
        connection.close()
        
    @staticmethod
    def insert_client(client: User):
        """ 
        Receives an instance of the User class and inserts it into the respective table
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        ClientController.verify_empty_fields(client.id, client.marital_status, client.age, client.property_value, client.interest_rate)
        ClientController.verify_age(int(client.age))
        ClientController.verify_property(float(client.property_value))
        ClientController.verify_interest(float(client.interest_rate))

        try:
            # Conditional to check if the client has a spouse
            if client.marital_status.title() in ["Married", "Wedded"]: 
                # Insert the client's and spouse's data
                cursor.execute("""
                    CLIENT (id, age, marital_status, spouse_age, spouse_gender, property_value, interest_rate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                    (client.id, client.age, client.marital_status, client.spouse_age, client.spouse_gender, client.property_value, client.interest_rate))
            else:
                # Insert only the client's data
                cursor.execute("""
                    INSERT INTO users (id, age, marital_status, property_value, interest_rate)
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (client.id, client.age, client.marital_status, client.property_value, client.interest_rate))

            # Confirm changes made to the database
            cursor.connection.commit()
            print("CLIENT INSERTED SUCCESSFULLY")
            print("\n")
                     
        except Exception as e:
            connection.rollback()
            print(f"Error inserting client: {e}")
            raise ClientNotInsertedException()
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def find_client(id):
        """ 
        Fetches a client from the clients table by ID number 
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, age, marital_status, spouse_age, spouse_gender, property_value, interest_rate
            FROM Clients WHERE id = %s""", (id,))

        row = cursor.fetchone()
        if row:
            result = User(id=row[0], age=row[1], marital_status=row[2], spouse_age=row[3],
                          spouse_gender=row[4], property_value=row[5], interest_rate=row[6])
            print(result)
            return result
        else:
            print("Client not found")
            return None

    
    @staticmethod
    def delete_client(id):
        """ 
        Deletes a client from the Clients table
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM Clients WHERE id = %s", (id,))
            cursor.connection.commit()
            print("CLIENT DELETED SUCCESSFULLY")
        except Exception as e:
            print(f"Error deleting client: {e}")
            raise ClientNotDeletedException()
        finally:
            cursor.close()
            connection.close()
             
    @staticmethod
    def update_client(id, updated_data: User):
        """ 
        Updates the values of a client in the clients table by ID number
        """
        connection = ClientController.get_connection()
        cursor = connection.cursor()

        try:
            # Update client's ID number if it's provided
            if updated_data.id:
                cursor.execute("UPDATE Clients SET id = %s WHERE id = %s", (updated_data.id, id))
                connection.commit()
                print("ID NUMBER UPDATED SUCCESSFULLY")

            # Update marital status
            if updated_data.marital_status:
                if updated_data.marital_status.title() == "Married":  
                    cursor.execute("UPDATE Clients SET marital_status = %s WHERE id = %s", (updated_data.marital_status, id))
                    if updated_data.spouse_age and updated_data.spouse_gender:
                        cursor.execute("UPDATE Clients SET spouse_age = %s, spouse_gender = %s WHERE id = %s", 
                                       (updated_data.spouse_age, updated_data.spouse_gender, id))
                    connection.commit()
                    print("MARITAL STATUS UPDATED SUCCESSFULLY") 
                else:
                    cursor.execute("UPDATE Clients SET marital_status = 'Single', spouse_age = NULL, spouse_gender = NULL WHERE id = %s", (id,))
                    connection.commit()
                    print("MARITAL STATUS UPDATED SUCCESSFULLY") 
            
            # Update property value
            if updated_data.property_value:
                cursor.execute("UPDATE Clients SET property_value = %s WHERE id = %s", (updated_data.property_value, id))
                connection.commit()
                print("PROPERTY VALUE UPDATED SUCCESSFULLY") 

            # Update interest rate
            if updated_data.interest_rate:
                cursor.execute("UPDATE Clients SET interest_rate = %s WHERE id = %s", (updated_data.interest_rate, id))
                connection.commit()
                print("INTEREST RATE UPDATED SUCCESSFULLY") 

        except Exception as e:
            print(f"Error updating client: {e}")
            raise ClientNotUpdatedException()
        finally:
            cursor.close()
            connection.close()
        
    @staticmethod
    def verify_empty_fields(id, marital_status, age, property_value, interest_rate):
        if id is None or marital_status is None or age is None or property_value is None or interest_rate is None:
            raise NoneException()

    @staticmethod
    def verify_age(age):
        if age < MIN_AGE or age > MAX_LIFE_EXPECTANCY_MALES:
            raise AgeException(age)
        
    @staticmethod
    def verify_property(property_value):
        if property_value < MIN_PROPERTY_VALUE:
            raise PropertyValueException()
    
    @staticmethod
    def verify_interest(interest_rate):
        if interest_rate < MIN_INTEREST_RATE or interest_rate > MAX_INTEREST_RATE:
            raise InterestRateException(interest_rate)


