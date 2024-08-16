import unittest
from src.model import mortgage_calc_logic


class MortgageCalcTest(unittest.TestCase):
    # Normal cases
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
        marital_status = "Widowed"
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

    # Special cases
    def testMortgageS1(self):
        property_value = 760000000
        client_age = 62
        client_gender = "M"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = 0  # Zero interest rate
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
        interest = 8  # Max interest rate (8)
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageS3(self):
        property_value = 800000000
        client_age = 74
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 71  # Minimum M age (71)
        spouses_gender = "M"
        interest = 5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 8441882.70

        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageS4(self):
        property_value = 424000000
        client_age = 79
        client_gender = "M"
        marital_status = "Married"
        spouses_age = 66  # Minimum H age (66)
        spouses_gender = "H"
        interest = 6.2
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 5096834.26

        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageS5(self):
        property_value = 280000000
        client_age = 79  # Maximum M age (79)
        client_gender = "M"
        marital_status = "Married"
        spouses_age = 79  # Maximum M age (79)
        spouses_gender = "M"
        interest = 3.3
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 23746276.32

        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

        # Edad máxima hombre

    def testMortgageS6(self):
        property_value = 900000000
        client_age = 76
        client_gender = "M"
        marital_status = "Married"
        spouses_age = 74  # Maximum H age (74)
        spouses_gender = "H"
        interest = 4.3
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 9205388.81

        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    # Error cases
    def testMortgageE1(self):
        property_value = 450000000
        client_age = 70
        client_gender = "M"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = -5  # Error: NegativeInterest
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE2(self):
        property_value = 310000000
        client_age = 72
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 68
        spouses_gender = "M"
        interest = 9  # Error: AboveMaxInterest (max 8)
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE3(self):
        property_value = -250000000  # (Error: NegativePropertyValue)
        client_age = 73
        client_gender = "H"
        marital_status = "Widowed"
        spouses_age = None
        spouses_gender = None
        interest = 7.5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE4(self):
        property_value = 0  # (Error: PropertyZeroValue)
        client_age = 74
        client_gender = "M"
        marital_status = "Divorced"
        spouses_age = None
        spouses_gender = None
        interest = 6.8
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE5(self):
        property_value = 290000000
        client_age = -71  # Error: NegativeAge
        client_gender = "H"
        marital_status = "Married"
        spouses_age = 65
        spouses_gender = "M"
        interest = 8
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE6(self):
        property_value = 320000000
        client_age = 75  # Error: AboveMaxAge (max 74 for gender H)
        client_gender = "H"
        marital_status = "Single"
        spouses_age = None
        spouses_gender = None
        interest = 7.2
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE7(self):
        property_value = 330000000
        client_age = 80  # Error: AboveMaxAge (max 79 for gender M)
        client_gender = "M"
        marital_status = "Married"
        spouses_age = 75
        spouses_gender = "H"
        interest = 7.9
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE8(self):
        property_value = 350000000
        client_age = 68
        client_gender = "X"  # Error: InvalidGender (only M or H)
        marital_status = "Widowed"
        spouses_age = None
        spouses_gender = None
        interest = 7
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    def testMortgageE9(self):
        property_value = 400000000
        client_age = 74
        client_gender = "H"
        marital_status = "Complicated"  # Error: InvalidMaritalStatus (only Married, Single, Widowed, Divorced)
        spouses_age = None
        spouses_gender = None
        interest = 7.5
        client = mortgage_calc_logic.Client(client_age, client_gender, marital_status, spouses_age, spouses_gender)
        mortgage = mortgage_calc_logic.Mortgage(property_value, interest, client)
        monthly_fee = 3492364.69
        self.assertEqual(monthly_fee, mortgage.calculate_monthly_fee())

    if __name__ == "__main__":
        unittest.main()
