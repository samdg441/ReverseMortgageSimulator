class Client:
    def __init__(self, age: int, gender: str, marital_status: str, spouses_age: int | None, spouses_gender: str | None):
        pass


class Mortgage:
    def __init__(self, property_value: int, interest: float, client: Client):
        pass

    def calculate_quotas(self):
        pass

    def calculate_monthly_fee(self):
        pass
