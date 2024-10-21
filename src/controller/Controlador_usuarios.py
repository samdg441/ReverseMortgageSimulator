# Importing to include the search path
import sys
sys.path.append("src")
sys.path.append(".")


import psycopg2

from controller import Secret_Config
from model.Client import Client

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
        super().__init__(f"The client could not be updated")

class ClientNotInsertedException(Exception):
    """ 
    Custom exception for when the client cannot be inserted into the table
    """
    def __init__(self):
        super().__init__(f"The client could not be inserted")

class ClientNotDeletedException(Exception):
    """ 
    Custom exception for when the client cannot be deleted from the table
    """
    def __init__(self):
        super().__init__(f"The client could not be deleted")

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
        super().__init__(f"There cannot be empty fields")

class PropertyValueException(Exception):
    """ 
    Custom exception for property values below the minimum
    """
    def __init__(self):
        super().__init__(f"Property value cannot be below the minimum")

class InterestRateException(Exception):
    """ 
    Custom exception for interest rates above the maximum, below the minimum, and zero
    """
    def __init__(self, interest_rate):
        super().__init__(f"The interest rate: {interest_rate} is invalid; it should not be less than {MIN_INTEREST_RATE} or greater than {MAX_INTEREST_RATE}")


class ClientController:

    @staticmethod
    def get_cursor():
        """
        Creates a connection to the database and returns a cursor for executing instructions
        """
        DATABASE = Secret_Config.PGDATABASE
        USER = Secret_Config.PGUSER
        PASSWORD = Secret_Config.PGPASSWORD
        HOST = Secret_Config.PGHOST
        PORT = Secret_Config.PGPORT
        # Connecting to the database
        connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

        # All instructions are executed through a cursor
        cursor = connection.cursor()
        return cursor
    
    @staticmethod
    def create_table():
        """ 
        Creates the clients table in the database 
        """
        try:
            # Get the cursor for the database connection
            cursor = ClientController.get_cursor()

            # Execute the query to create the table in the database
            cursor.execute("""CREATE TABLE Clients (id_number VARCHAR(20) NOT NULL PRIMARY KEY,
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
        except:
            # If we get here, it means the table already exists and could not be created
            cursor.connection.rollback()
            print("THE TABLE ALREADY EXISTS")
            print("\n")
            return "Table Exists"
        
    @staticmethod
    def clear_table():
        """ 
        Deletes all records from the clients table in the database 
        """
        # Get the cursor for the database connection
        cursor = ClientController.get_cursor()

        # Execute the query to delete all records from the table
        cursor.execute("""DELETE FROM Clients""" )

        # Confirm changes made to the database
        cursor.connection.commit()
        print("RECORDS DELETED SUCCESSFULLY")
        print("\n")
        
    @staticmethod
    def insert_client(client: Client):
        """ 
        Receives an instance of the Client class and inserts it into the respective table
        """
        # Get the cursor for the database connection
        cursor = ClientController.get_cursor()

        ClientController.verify_empty_fields(client.id_number, client.marital_status, client.age, client.property_value, client.interest_rate)
        ClientController.verify_age(int(client.age))
        ClientController.verify_property(float(client.property_value))
        ClientController.verify_interest(float(client.interest_rate))

        try:
            # Conditional to check if the client has a spouse
            if client.marital_status.title() in ["Married", "Wedded"]: 
                # If the condition is met, insert the client's and spouse's data
                cursor.execute(f"""INSERT INTO Clients (id_number, age, marital_status, spouse_age, spouse_gender, property_value, interest_rate)
                                   VALUES ('{client.id_number}', '{client.age}', '{client.marital_status}', '{client.spouse_age}', '{client.spouse_gender}', '{client.property_value}', '{client.interest_rate}')""")

                # Confirm changes made to the database
                cursor.connection.commit()
                print("CLIENT INSERTED SUCCESSFULLY")
                print("\n")

            else:
                # If the condition is not met, insert only the client's data
                cursor.execute(f"""INSERT INTO Clients (id_number, age, marital_status, property_value, interest_rate)
                                   VALUES ('{client.id_number}', '{client.age}', '{client.marital_status}', '{client.property_value}', '{client.interest_rate}')""")

                # Confirm changes made to the database
                cursor.connection.commit()
                print("CLIENT INSERTED SUCCESSFULLY")
                print("\n")
                     
        except:
            cursor.connection.rollback()
            raise ClientNotInsertedException()
    
    @staticmethod
    def find_client(id_number):
        """ 
        Fetches a client from the clients table by ID number 
        """
        # Get the cursor for the database connection
        cursor = ClientController.get_cursor()

        # Execute the query to find the client by ID number
        cursor.execute(f"""SELECT id_number, age, marital_status, spouse_age, spouse_gender, property_value, interest_rate
                           FROM Clients WHERE id_number = '{id_number}'""" )
        
        # Get each field of the client
        row = cursor.fetchone()
        result = Client(id_number=row[0], age=row[1], marital_status=row[2], spouse_age=row[3],
                        spouse_gender=row[4], property_value=row[5], interest_rate=row[6])
        # Show the obtained data
        print(result)
        return result
    
    @staticmethod
    def delete_client(id_number):
        """ 
        Deletes a client from the Clients table
        """
        # Get the cursor for the database connection
        cursor = ClientController.get_cursor()
        try:
            cursor.execute(f"""DELETE FROM Clients WHERE id_number='{id_number}'""")
            cursor.connection.commit()
            print("CLIENT DELETED SUCCESSFULLY")

        except:
            raise ClientNotDeletedException()
             
    @staticmethod
    def update_client(id_number, updated_data: Client):
        """ 
        Fetches a client from the clients table by ID number and updates its values
        """
        # Get the cursor for the database connection
        cursor = ClientController.get_cursor()
        try:
            # Conditional to check if the ID number of the client is to be updated
            if updated_data.id_number is not None:
                cursor.execute(f"""UPDATE Clients SET id_number='{updated_data.id_number}' WHERE id_number='{id_number}'""")
                cursor.connection.commit()
                print("ID NUMBER UPDATED SUCCESSFULLY")

            # Conditional to check if the marital status of the client is to be updated
            elif updated_data.marital_status is not None:
                # Conditional to check if the client has a spouse
                if updated_data.marital_status.title() == "Married":  
                    cursor.execute(f"""UPDATE Clients SET marital_status='{updated_data.marital_status}' WHERE id_number='{id_number}'""")

                    # Conditional to verify that the spouse's data is correct
                    if updated_data.spouse_age is not None and updated_data.spouse_gender is not None:
                        cursor.execute(f"""UPDATE Clients SET spouse_age='{updated_data.spouse_age}', spouse_gender='{updated_data.spouse_gender}' WHERE id_number='{id_number}'""")
                        cursor.connection.commit()
                        print("MARITAL STATUS UPDATED SUCCESSFULLY") 

                else:
                    cursor.execute(f"""UPDATE Clients SET marital_status='single', spouse_age='', spouse_gender='' WHERE id_number='{id_number}'""")
                    cursor.connection.commit()
                    print("MARITAL STATUS UPDATED SUCCESSFULLY") 
            
            # Conditional to check if the property value of the client is to be updated
            elif updated_data.property_value is not None:
                cursor.execute(f"""UPDATE Clients SET property_value='{updated_data.property_value}' WHERE id_number='{id_number}'""")
                cursor.connection.commit()
                print("PROPERTY VALUE UPDATED SUCCESSFULLY") 

            # Conditional to check if the interest rate is to be updated
            elif updated_data.interest_rate is not None:
                cursor.execute(f"""UPDATE Clients SET interest_rate='{updated_data.interest_rate}' WHERE id_number='{id_number}'""")
                cursor.connection.commit()
                print("INTEREST RATE UPDATED SUCCESSFULLY") 

        except:
            raise ClientNotUpdatedException()
        
    # Verifies that no field is left empty
    @staticmethod
    def verify_empty_fields(id_number, marital_status, age, property_value, interest_rate):
        if id_number is None or marital_status is None or age is None or property_value is None or interest_rate is None:
            raise NoneException()

    # Verifies that the age of the client is not below the limit
    @staticmethod
    def verify_age(age):
        if age < MIN_AGE or age > MAX_LIFE_EXPECTANCY_MALES:
            raise AgeException(age)
        
    # Verifies that the property value of the client is not below the limit
    @staticmethod
    def verify_property(property_value):
        if property_value < MIN_PROPERTY_VALUE:
            raise PropertyValueException()
    
    @staticmethod
    def verify_interest(interest_rate):
        if interest_rate < MIN_INTEREST_RATE or interest_rate > MAX_INTEREST_RATE:
            raise InterestRateException(interest_rate)
