from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner

import sys
sys.path.append("src")

# Reverse Mortgage logic
from ReverseMortgage import MonthlyPayment

class ReverseMortgageApp(App):
    def build(self):
        """
        Method responsible for creating the GUI.
        """
        def create_client_information_layout():
            """
            Method responsible for creating the client information layout.
            """
            layout = GridLayout(cols=2, spacing=10)

            self.age_label = Label(text="Age (Required)", size_hint=(0.5, 0.15))
            layout.add_widget(self.age_label)
            self.age_input = TextInput(multiline=False, size_hint=(0.5, 0.15), input_filter="int")
            layout.add_widget(self.age_input)
            self.age_input.bind(text=self.check_valid_age)

            self.gender_label = Label(text="Gender (Required)", size_hint=(0.5, 0.15))
            layout.add_widget(self.gender_label)
            self.gender_spinner = Spinner(text="Select", values=('Male', 'Female'), size_hint=(0.5, 0.15))
            layout.add_widget(self.gender_spinner)
            self.gender_spinner.bind(text=self.check_valid_spinner)

            self.marital_status_label = Label(text="Marital Status (Required)", size_hint=(0.5, 0.15))
            layout.add_widget(self.marital_status_label)
            self.marital_status_spinner = Spinner(text="Select", values=('Married', 'Single', 'Widowed', 'Divorced'), size_hint=(0.5, 0.15))
            layout.add_widget(self.marital_status_spinner)
            self.marital_status_spinner.bind(text=self.update_spouse_fields)
            self.marital_status_spinner.bind(text=self.check_valid_spinner)

            self.is_married = False

            return layout
        

        def create_property_information_layout():
            """
            Method responsible for creating the property information layout.
            """
            layout = GridLayout(cols=2)

            self.home_value_label = Label(text="Home Value (Required)", size_hint=(0.5, 0.1))
            layout.add_widget(self.home_value_label)
            self.home_value_input = TextInput(multiline=False, size_hint=(0.5, 0.1), input_filter="float")
            layout.add_widget(self.home_value_input)

            self.interest_rate_label = Label(text="Interest Rate (Required)", size_hint=(0.5, 0.1))
            layout.add_widget(self.interest_rate_label)
            self.interest_rate_input = TextInput(multiline=False, size_hint=(0.5, 0.1), input_filter="float")
            layout.add_widget(self.interest_rate_input)

            return layout
        
        def create_inputs_layout(client_layout, property_layout):
            """
            Method responsible for creating the inputs layout.
            """
            layout = BoxLayout(orientation="horizontal", padding=15, spacing=10)

            layout.add_widget(client_layout)
            layout.add_widget(property_layout)

            return layout

        def create_global_layout(inputs_layout):
            """
            Method responsible for creating the global layout.
            """
            layout = GridLayout(rows=3, padding=15, spacing=10)

            layout.add_widget(Label(text="Reverse Mortgage Calculator", size_hint=(1, 0.1), halign="center", font_family="Arial", font_size=30))

            layout.add_widget(inputs_layout)

            self.calc_button = Button(text="Calculate", size_hint=(0.5, 0.1))
            layout.add_widget(self.calc_button)

            return layout
        
        self.client_layout = create_client_information_layout()
        self.property_layout = create_property_information_layout()
        self.inputs_layout = create_inputs_layout(self.client_layout, self.property_layout)
        self.global_layout = create_global_layout(self.inputs_layout)

        return self.global_layout
    
    def update_spouse_fields(self, sender, text):
        if text == 'Married' and not self.is_married:
            self.spouse_age_label = Label(text="Spouse's Age", size_hint=(0.5, 0.15))
            self.client_layout.add_widget(self.spouse_age_label)

            self.spouse_age_input = TextInput(multiline=False, size_hint=(0.5, 0.15), input_filter="int")
            self.client_layout.add_widget(self.spouse_age_input)

            self.spouse_gender_label = Label(text="Spouse's Gender", size_hint=(0.5, 0.15))
            self.client_layout.add_widget(self.spouse_gender_label)

            self.spouse_gender_spinner = Spinner(text="Select", values=('Male', 'Female'), size_hint=(0.5, 0.15))
            self.client_layout.add_widget(self.spouse_gender_spinner)

            self.is_married = True
    
        elif text != 'Married' and self.is_married:
            self.client_layout.remove_widget(self.spouse_age_input)
            self.client_layout.remove_widget(self.spouse_age_label)
            self.client_layout.remove_widget(self.spouse_gender_label)
            self.client_layout.remove_widget(self.spouse_gender_spinner)

            self.is_married = False

    def check_valid_age(self, sender, text):
        if (text != '' and text != '-') and (int(text) < 0 or int(text) > 100):
            self.age_label.text = "Age (Invalid)"
        elif text == '' or text == '-':
            self.age_label.text = "Age (Required)"
        else:
            self.age_label.text = "Age"
        
    def check_valid_spinner(self, sender, text):
        if text != 'Select' and sender is self.gender_spinner:
            self.gender_label.text = 'Gender'
        elif text != 'Select' and sender is self.marital_status_spinner:
            self.marital_status_label.text = 'Marital Status'


if __name__ == "__main__":
    ReverseMortgageApp().run()