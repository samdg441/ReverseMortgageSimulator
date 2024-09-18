from kivy.app import App


from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

import sys
sys.path.append("src")

# Logica de la tarjeta de credito
from ReverseMortgage import MonthlyPayment

class ReverseMortgageApp(App):
    def build(self):
        client_info_layout = GridLayout(cols=2, spacing=10)

        name_label = Label(text="Name", size_hint=(0.5, 0.1))
        client_info_layout.add_widget(name_label)
        name_input = TextInput(multiline=False, size_hint=(0.5, 0.1))
        client_info_layout.add_widget(name_input)
        age_label = Label(text="Age", size_hint=(0.5, 0.1))
        client_info_layout.add_widget(age_label)
        age_input = TextInput(multiline=False, size_hint=(0.5, 0.1))
        client_info_layout.add_widget(age_input)

        gender_box = BoxLayout(orientation='horizontal')
        choises_box = BoxLayout(orientation='vertical')
        gender_box.add_widget(Label(text="Gender"))
        choises_box.add_widget(CheckBox(group = 'Gender'))
        choises_box.add_widget(CheckBox(group = 'Gender'))
        gender_box.add_widget(choises_box)
        client_info_layout.add_widget(gender_box)

        property_info_layout = GridLayout(cols=2)

        home_value_label = Label(text="Home Value", size_hint=(0.5, 0.1))
        property_info_layout.add_widget(home_value_label)
        home_value_input = TextInput(multiline=False, size_hint=(0.5, 0.1))
        property_info_layout.add_widget(home_value_input)

        inputs_layout = GridLayout(cols=2)

        inputs_layout.add_widget(client_info_layout)
        inputs_layout.add_widget(property_info_layout)

        global_layout = GridLayout(rows=3, padding=15, spacing=10)

        global_layout.add_widget(Label(text="Reverse Mortgage Calculator", size_hint=(1, 0.1), halign="center", font_family="Arial", font_size=30))
        global_layout.add_widget(inputs_layout)
        calc_button = Button(text="Calculate", size_hint=(0.5, 0.1))
        global_layout.add_widget(calc_button)
        
        return global_layout
        

if __name__ == "__main__":
    ReverseMortgageApp().run()