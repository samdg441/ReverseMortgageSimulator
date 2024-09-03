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

    def check_minor_age(self):
        if self.marital_status != "Married" or self.age <= self.spouses_age:
            return self.age
        elif self.age < 0 or self.spouses_age < 0:
            raise NegativeAge('Age cannot be negative')
        else:
            return self.spouses_age
        
    def check_minor_gender(self):
        if self.marital_status != "Married" or self.minor_age == self.age:
            return self.gender
        else:
            return self.spouses_gender

    def calculate_years_of_life(self):
        male_life_expect = 75
        female_life_expect = 80

        if self.minor_gender == "M":
            if self.minor_age < 0:
                raise NegativeAge('Age cannot be negative')
            return male_life_expect - self.minor_age
        
        elif self.minor_gender == "F":
            if self.minor_age < 0:
                raise NegativeAge('Age cannot be negative')
            return female_life_expect - self.minor_age
        
        else:
            raise InvalidGender


class ReverseMortgage:
    def __init__(self, property_value: int, interest: float, client: Client):
        self.property_value = property_value
        self.interest = interest
        self.client = client
        self.quotas = self.calculate_quotas()
        self.monthly_rate = self.calculate_monthly_rate()
    

    def calculate_quotas(self):
        return self.client.estimated_years_of_life * 12
    
    def calculate_monthly_rate(self):
        if self.interest == 0:
            return 0
        
        annual_rate = self.interest / 100
        monthly_rate = (1 + annual_rate) ** (1 / 12) - 1
        return monthly_rate
        
    def calculate_monthly_fee(self):
        if self.interest == 0:
            return round(self.property_value / self.quotas, 2)
        
        numerator = self.property_value * self.monthly_rate * (1 + self.monthly_rate) ** self.quotas
        
        denominator = ((1 + self.monthly_rate) ** self.quotas) - 1
        
        monthly_fee = numerator / denominator
        
        return round(monthly_fee, 2)

