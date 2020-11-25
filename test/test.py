from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

class MyApplicationApp(MDApp):
    def build(self):
        screen=Screen()
        table = MDDataTable(column_data=[
            ('food',dp(30)),
            #('kcal',dp(30))
        ],
        row_data=[
            ('burger','300'),
            #('oats','150')
            ]
        )
        screen.add_widget(table)
        return screen

if __name__ == '__main__':
    x=MyApplicationApp()
    x.run()