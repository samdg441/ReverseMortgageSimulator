import sys
sys.path.append('src')
from  ReverseMortgage import MonthlyPayment

def main_menu():
    client = None
    reverse_mortgage = None

    while True:
        print("\n--- Main Menu ---")
        print("1. Enter Client Information")
        print("2. Calculate Reverse Mortgage")
        print("3. Exit")
        
        try:
            option = int(input("Choose an option (1-3): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if option == 1:
            try:
                age = int(input("Enter your age: "))
                
                gender = input("Enter your gender (M/F): ").strip().upper()
                marital_status = input("Enter your marital status: ").strip()
                spouses_age = input("Enter your spouse's age (press Enter if not applicable): ").strip()
                spouses_age = int(spouses_age) if spouses_age else None
                spouses_gender = input("Enter your spouse's gender (press Enter if not applicable): ").strip().upper()
                spouses_gender = spouses_gender if spouses_gender else None

                client = MonthlyPayment.Client(age, gender, marital_status, spouses_age, spouses_gender)
                print("Client information successfully recorded.")
            
            except (MonthlyPayment.NegativeAge, MonthlyPayment.InvalidGender) as e:
                print(f"Error: {e}")
            except ValueError:
                print("Invalid input. Please enter the correct data.")
        
        elif option == 2:
            if client is None:
                print("You need to enter client information first.")
                continue
            
            try:
                property_value = int(input("Enter property value: "))
                interest = float(input("Enter interest rate (as a percentage): "))

                if property_value <= 0:
                    raise MonthlyPayment.NegativePropertyValue("Property value must be positive.")
                if interest < 0:
                    raise MonthlyPayment.NegativeInterest("Interest rate cannot be negative.")
                
                reverse_mortgage = MonthlyPayment.ReverseMortgage(property_value, interest, client)
                print(f"Estimated years of life: {client.estimated_years_of_life}")
                print(f"Monthly rate: {reverse_mortgage.monthly_rate:.4f}")
                print(f"Monthly fee: {reverse_mortgage.calculate_monthly_fee():.2f}")

            except (MonthlyPayment.NegativePropertyValue, MonthlyPayment.NegativeInterest) as e:
                print(f"Error: {e}")
            except ValueError:
                print("Invalid input. Please enter the correct data.")
        
        elif option == 3:
            print("Exiting the program...")
            break
        
        else:
            print("Invalid option, please choose a number from 1 to 3.")

if __name__ == "__main__":
    main_menu()

           

        


                