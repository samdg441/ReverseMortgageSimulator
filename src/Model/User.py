class User:
    """
    Belongs to the Business Rules Layer (Model)

    Represents a Reverse Mortgage user in the application
    """
    def __init__(self, id, age, marital_status, spouse_age, spouse_gender, property_value, interest_rate):
        self.id = id
        self.age = age
        self.marital_status = marital_status
        self.spouse_age = spouse_age
        self.spouse_gender = spouse_gender
        self.property_value = property_value
        self.interest_rate = interest_rate

    def __repr__(self):
        """
        Method to return the user's data
        """
        # Conditional to check if the user has a spouse
        if (self.marital_status.title() == "Married"):
            # If the previous condition is met, return all the user's data
            return str(f"ID NUMBER: {self.id} \n AGE: {self.age} \n MARITAL STATUS: {self.marital_status} \n SPOUSE AGE: {self.spouse_age} \n SPOUSE GENDER: {self.spouse_gender} ")

        else:
            # If the previous condition is not met, return the user's data without spouse-related details
            return str(f"ID NUMBER: {self.id} \n AGE: {self.age} \n MARITAL STATUS: {self.marital_status} ")

    def is_equal(self, compare_with):
        """
        Compares the current object with another instance of the User class
        """
        assert(self.id == compare_with.id)
        assert(self.age == compare_with.age)
        assert(self.marital_status == compare_with.marital_status)
        assert(self.spouse_age == compare_with.spouse_age)
        assert(self.spouse_gender == compare_with.spouse_gender)
        assert(self.property_value == compare_with.property_value)
        assert(self.interest_rate == compare_with.interest_rate)
