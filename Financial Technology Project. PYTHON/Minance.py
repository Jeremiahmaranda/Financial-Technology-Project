import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

# Database setup
def create_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            description TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

create_db()

class MinanceApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.transaction_input = TextInput(hint_text='Enter transaction description')
        self.add_widget(self.transaction_input)

        self.amount_input = TextInput(hint_text='Enter amount', input_filter='float')
        self.add_widget(self.amount_input)

        self.category_dropdown = DropDown()
        self.categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Savings']
        
        for category in self.categories:
            btn = Button(text=category, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.category_dropdown.select(btn.text))
            self.category_dropdown.add_widget(btn)

        self.category_button = Button(text='Select Category', size_hint_y=None, height=40)
        self.category_button.bind(on_release=self.category_dropdown.open)
        self.category_dropdown.bind(on_select=lambda instance, x: setattr(self.category_button, 'text', x))
        
        self.add_widget(self.category_button)

        add_button = Button(text='Add Transaction', size_hint_y=None, height=40)
        add_button.bind(on_press=self.add_transaction)
        self.add_widget(add_button)

        self.transaction_list = Label(text='Transactions:', size_hint_y=None, height=200)
        self.add_widget(self.transaction_list)

        self.budget_button = Button(text='Set Budget', size_hint_y=None, height=40)
        self.budget_button.bind(on_press=self.set_budget)
        self.add_widget(self.budget_button)

        self.goal_input = TextInput(hint_text='Enter financial goal', size_hint_y=None, height=40)
        self.add_widget(self.goal_input)

        goal_button = Button(text='Set Financial Goal', size_hint_y=None, height=40)
        goal_button.bind(on_press=self.set_goal)
        self.add_widget(goal_button)

    def add_transaction(self, instance):
        description = self.transaction_input.text
        category = self.category_button.text
        amount = self.amount_input.text
        
        if description and category != 'Select Category' and amount:
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            c.execute("INSERT INTO transactions (description, category, amount) VALUES (?, ?, ?)", 
                      (description, category, float(amount)))
            conn.commit()
            conn.close()
            
            self.transaction_list.text += f'\n{description} - {category}: ${amount}'
            self.transaction_input.text = ''
            self.amount_input.text = ''
            self.category_button.text = 'Select Category'

    def set_budget(self, instance):
        # Placeholder for budget implementation
        Popup(title='Budgeting', content=Label(text='Implement budgeting here!'), size_hint=(0.8, 0.4)).open()

    def set_goal(self, instance):
        goal = self.goal_input.text
        if goal:
            Popup(title='Financial Goal', content=Label(text=f'Goal set: {goal}'), size_hint=(0.8, 0.4)).open()
            self.goal_input.text = ''

class MyApp(App):
    def build(self):
        return MinanceApp()

if __name__ == '__main__':
    MyApp().run()
