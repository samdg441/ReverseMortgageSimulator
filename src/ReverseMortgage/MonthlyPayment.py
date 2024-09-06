class ClientException(Exception):
    """
    Base class for all client-related exceptions.
    This exception is used for errors related to invalid client information.
    """
    pass


class ReverseMortgageException(Exception):
    """
    Base class for all reverse mortgage-related exceptions.
    This exception is used for errors related to reverse mortgage calculations or constraints.
    """
    pass


class NegativeInterest(ReverseMortgageException):
    """
    Raised when a negative interest rate is encountered.
    Reverse mortgages should not have negative interest rates.
    """
    pass


class AboveMaxInterest(ReverseMortgageException):
    """
    Raised when an interest rate exceeds the maximum allowable rate.
    Reverse mortgages have a maximum interest rate limit.
    """
    pass


class NegativePropertyValue(ReverseMortgageException):
    """
    Raised when a negative property value is provided.
    Property values must be positive for reverse mortgage calculations.
    """
    pass


class PropertyZeroValue(ReverseMortgageException):
    """
    Raised when a zero property value is provided.
    A property value of zero is invalid for reverse mortgage calculations.
    """
    pass


class NegativeAge(ClientException):
    """
    Raised when a negative age is provided for a client.
    Client age must be a positive integer.
    """
    pass


class AboveMaxAge(ClientException):
    """
    Raised when a client's age exceeds the maximum allowable age.
    There is typically an upper limit for age in client-related calculations or constraints.
    """
    pass


class InvalidAge(ClientException):
    """
    Raised when an invalid age value is provided.
    Age must be a valid positive integer within acceptable ranges.
    """
    pass


class InvalidGender(ClientException):
    """
    Raised when an invalid gender value is provided.
    Gender must be specified in an acceptable format.
    """
    pass


class InvalidMaritalStatus(ClientException):
    """
    Raised when an invalid marital status value is provided.
    Marital status must be specified in an acceptable format.
    """
    pass


class Client:
    def __init__(self, age: int, gender: str, marital_status: str, spouses_age: int | None, spouses_gender: str | None):
        self.age = age
        self.gender = gender
        self.marital_status = marital_status
        self.spouses_age = spouses_age
        self.spouses_gender = spouses_gender
        self.minor_age = self.check_minor_age()
        self.minor_gender = self.check_minor_gender()
        self.estimated_years_of_life = self.calculate_years_of_life()

    def check_valid_age(self):
        max_male_age_allowed = 74
        max_female_age_allowed = 79

        if type(self.age) != int:
            raise InvalidAge(f'Age ({self.age}) is not a valid number')

        if self.age < 0:
            raise NegativeAge(f'Age ({self.age}) can not be negative')
        elif self.gender.lower() == 'm' and self.age > max_male_age_allowed:
            raise AboveMaxAge(f'Age ({self.age}) is greater than the maximum age allowed for males ({max_male_age_allowed})')
        elif self.gender.lower() == 'f' and self.age > max_female_age_allowed:
            raise AboveMaxAge(f'Age ({self.age}) is greater than the maximum age allowed for females ({max_female_age_allowed})')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_age < 0:
                raise NegativeAge(f'Age ({self.spouses_age}) can not be negative')
            elif self.spouses_gender.lower() == 'm' and self.spouses_age > max_male_age_allowed:
                raise AboveMaxAge(f'Age ({self.spouses_age}) is greater than the maximum age allowed for males ({max_male_age_allowed})')
            elif self.spouses_gender.lower() == 'f' and self.spouses_age > max_female_age_allowed:
                raise AboveMaxAge(f'Age ({self.spouses_age}) is greater than the maximum age allowed for females ({max_female_age_allowed})')
        
    def check_valid_gender(self):
        available_genders = ['m', 'f']
        if self.gender.lower() not in available_genders:
            raise InvalidGender(f'Gender ({self.gender}) is not valid, only "M" or "F" allowed')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_gender.lower() not in available_genders:
                raise InvalidGender(f'Spouses gender ({self.spouses_gender}) is not valid')
        
    def check_valid_marital_status(self):
        available_marital_status = ['married', 'single', 'widowed', 'divorced']
        if self.marital_status.lower() not in available_marital_status:
            raise InvalidMaritalStatus(f'Marital status ({self.marital_status}) is not valid, only married, single, widowed or divorced allowed')

    def check_minor_age(self):
        self.check_valid_age()
        self.check_valid_marital_status()
        if self.marital_status.lower() != "married" or self.age <= self.spouses_age:
            return self.age
        else:
            return self.spouses_age

    def check_minor_gender(self):
        self.check_valid_gender()
        self.check_valid_gender()
        self.check_valid_marital_status()
        if self.marital_status.lower() != "married" or self.minor_age == self.age:
            return self.gender
        else:
            return self.spouses_gender

    def calculate_years_of_life(self):
        male_life_expect = 75
        female_life_expect = 80

        self.check_valid_age()
        self.check_valid_gender()

        if self.minor_gender.lower() == "m":
            return male_life_expect - self.minor_age
        
        elif self.minor_gender.lower() == "f":
            return female_life_expect - self.minor_age

    def __repr__(self) -> str:
        if self.marital_status.lower() == "married":
            return f'Age: {self.age} \nGender: {self.gender.upper()} \nMarital Status: {self.marital_status.title()} \n\nSpouse\'s Age: {self.spouses_age} \nSpouse\'s Gender: {self.spouses_gender.upper()}'
        else:
            return f'Age: {self.age} \nGender: {self.gender.upper()} \nMarital Status: {self.marital_status.title()}'


class ReverseMortgage:
    def __init__(self, property_value: int, interest: float, client: Client):
        self.property_value = property_value
        self.interest = interest
        self.client = client
        self.quotas = self.calculate_quotas()
        self.monthly_rate = self.calculate_monthly_rate()
    
    def check_valid_property_value(self):
        if self.property_value < 0:
            raise NegativePropertyValue(f'Property value {self.property_value} can not be negative')
        elif self.property_value == 0:
            raise PropertyZeroValue(f'Property value {self.property_value} can not be zero')
        
    def check_valid_interest(self):
        max_interest = 8
        if self.interest < 0:
            raise NegativeInterest(f'Interest {self.interest} can not be negative')
        elif self.interest > max_interest:
            raise AboveMaxInterest(f'interest {self.interest} can not be above {max_interest}')

    def calculate_quotas(self):
        return self.client.estimated_years_of_life * 12
    
    def calculate_monthly_rate(self):
        self.check_valid_interest()

        if self.interest == 0:
            return 0
        
        annual_rate = self.interest / 100
        monthly_rate = (1 + annual_rate) ** (1 / 12) - 1
        return monthly_rate
        
    def calculate_monthly_fee(self):
        self.check_valid_interest()
        self.check_valid_property_value()

        if self.interest == 0:
            return round(self.property_value / self.quotas, 2)
        
        numerator = self.property_value * self.monthly_rate * (1 + self.monthly_rate) ** self.quotas
        
        denominator = ((1 + self.monthly_rate) ** self.quotas) - 1
        
        monthly_fee = numerator / denominator
        
        return round(monthly_fee, 2)

    def __repr__(self) -> str:
        return f'Property Value: ${self.property_value:,} \nInterest: {self.interest}% \nQuotas: {self.quotas} \nMonthly Rate: {round(self.monthly_rate, 6)} \n\nMonthly Fee: ${self.calculate_monthly_fee():,}'
    
