import unittest
from src.model import mortgage_calc_logic


class MortgageCalcTest(unittest.TestCase):
    def testMortgageN1(self):
        property_value = 150000000
        client_age = 65
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 63
        spouses_gender = "M"
        interest = 5.5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 1122501.78
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageN2(self):
        property_value = 300000000
        client_age = 75
        client_gender = "M"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = 3.5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 5450147.92
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageN3(self):
        property_value = 200000000
        client_age = 60
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 70
        spouses_gender = "H"
        interest = 6
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 1670588.20
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageN4(self):
        property_value = 500000000
        client_age = 74
        client_gender = "M"
        marital_status = "Married"
        spouses_age = 68
        spouses_gender = "H"
        interest = 5.2
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 7085773.15
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageN5(self):
        property_value = 250000000
        client_age = 60
        client_gender = "M"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = 7
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 1906111.88
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageN6(self):
        property_value = 100000000
        client_age = 70
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 60
        spouses_gender = "M"
        interest = 7.5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 790612.47
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    # Casos de prueba extraordinarios
    def testMortgageS1(self):
        property_value = 760000000
        client_age = 62
        client_gender = "M"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = 0
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3518518.52
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageS2(self):
        property_value = 310000000
        client_age = 71
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 69
        spouses_gender = "M"
        interest = 8
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageS3(self):
        property_value = 310000000
        client_age = 71
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 69
        spouses_gender = "M"
        interest = 8
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    # Casos de prueba de error
    def testMortgageE1(self):
        property_value = 310000000
        client_age = 71
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 69
        spouses_gender = "M"
        interest = 8
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    if __name__ == "__main__":
        unittest.main()
