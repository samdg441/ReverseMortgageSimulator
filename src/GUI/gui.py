from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner

import sys
sys.path.append("src")

# Logica de la tarjeta de credito
from ReverseMortgage import MonthlyPayment

class ReverseMortgageApp(App):
    def build(self):
        def create_client_information_layout():
            layout = GridLayout(cols=2, spacing=10)

            layout.add_widget(Label(text="Name", size_hint=(0.5, 0.15)))

            self.name_input = TextInput(multiline=False, size_hint=(0.5, 0.15))
            layout.add_widget(self.name_input)

            layout.add_widget(Label(text="Age", size_hint=(0.5, 0.15)))

            self.age_input = TextInput(multiline=False, size_hint=(0.5, 0.15), input_filter="int")
            layout.add_widget(self.age_input)

            layout.add_widget(Label(text="Gender", size_hint=(0.5, 0.15)))

            self.gender_spinner = Spinner(text="Select", values=('Male', 'Female'), size_hint=(0.5, 0.15))
            layout.add_widget(self.gender_spinner)

            layout.add_widget(Label(text="Marital Status", size_hint=(0.5, 0.1)))

            self.marital_status_spinner = Spinner(text="Select", values=('Married', 'Single', 'Widowed', 'Divorced'), size_hint=(0.5, 0.15))
            layout.add_widget(self.marital_status_spinner)

            self.marital_status_spinner.bind(text=self.update_spouse_fields)

            self.is_married = False
            
            return layout
        

        def create_property_information_layout():
            layout = GridLayout(cols=2)

            self.home_value_label = Label(text="Home Value", size_hint=(0.5, 0.1))
            layout.add_widget(self.home_value_label)

            self.home_value_input = TextInput(multiline=False, size_hint=(0.5, 0.1))
            layout.add_widget(self.home_value_input)

            return layout
        
        def create_inputs_layout(client_layout, property_layout):
            layout = GridLayout(cols=2)

            layout.add_widget(client_layout)

            layout.add_widget(property_layout)

            return layout

        def create_global_layout(inputs_layout):
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

if __name__ == "__main__":
    ReverseMortgageApp().run()