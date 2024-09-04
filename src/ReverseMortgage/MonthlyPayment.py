class NegativeInterest(Exception):
    pass


class AboveMaxInterest(Exception):
    pass


class NegativePropertyValue(Exception):
    pass


class PropertyZeroValue(Exception):
    pass


class NegativeAge(Exception):
    pass


class AboveMaxAge(Exception):
    pass


class InvalidGender(Exception):
    pass


class InvalidMaritalStatus(Exception):
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

    def check_valid_age(self) -> None:
        max_male_age_allowed = 74
        max_female_age_allowed = 79

        if self.age < 0:
            raise NegativeAge(f'Age {self.age} can not be negative')
        elif self.gender.lower() == 'm' and self.age > max_male_age_allowed:
            raise AboveMaxAge(f'Age {self.age} is greater than the maximum age allowed for men {max_male_age_allowed}')
        elif self.gender.lower() == 'f' and self.age > max_female_age_allowed:
            raise AboveMaxAge(f'Age {self.age} is greater than the maximum age allowed for women {max_female_age_allowed}')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_age < 0:
                raise NegativeAge(f'Age {self.spouses_age} can not be negative')
            elif self.spouses_gender.lower() == 'm' and self.spouses_age > max_male_age_allowed:
                raise AboveMaxAge(f'Age {self.spouses_age} is greater than the maximum age allowed for men {max_male_age_allowed}')
            elif self.spouses_gender.lower() == 'f' and self.spouses_age > max_female_age_allowed:
                raise AboveMaxAge(f'Age {self.spouses_age} is greater than the maximum age allowed for women {max_female_age_allowed}')
        
    def check_valid_gender(self) -> None:
        available_genders = ['m', 'f']
        if self.gender.lower() not in available_genders:
            raise InvalidGender(f'Gender {self.gender} is not valid, only "M" or "F" allowed')
        
        if self.marital_status.lower() == 'married':
            if self.spouses_gender.lower() not in available_genders:
                raise InvalidGender(f'Spouses gender {self.spouses_gender} is not valid')
        
    def check_valid_marital_status(self) -> None:
        available_marital_status = ['married', 'single', 'widowed', 'divorced']
        if self.marital_status.lower() not in available_marital_status:
            raise InvalidMaritalStatus(f'Marital status {self.marital_status} is not valid, only married, single, widowed or divorced allowed')

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
        
    def calculate_monthly_fee(self) -> float:
        self.check_valid_interest()
        self.check_valid_property_value()

        if self.interest == 0:
            return round(self.property_value / self.quotas, 2)
        
        numerator = self.property_value * self.monthly_rate * (1 + self.monthly_rate) ** self.quotas
        
        denominator = ((1 + self.monthly_rate) ** self.quotas) - 1
        
        monthly_fee = numerator / denominator
        
        return round(monthly_fee, 2)
