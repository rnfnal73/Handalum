from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
import sqlite3

class PastRecordWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        super().__init__()
        
        self.widget_layout = BoxLayout()
        self.calendar = MDDatePicker(callback=self.get_date)

        self.data_tables = MDDataTable(
            size_hint=(0.5, 0.8),
            column_data=[
                ("", dp(40)),
                ("", dp(70)),
                # ("Team Lead", dp(30))
            ]
            ,
            row_data=[
                ('steps', 1),
                ('dist', 1),
                ('calories', 1),
                ('a', 1),
                ('b', 1),
                ('c', 1)
            ]
        )
        self.items_bind()
        
    def items_bind(self):
        self.widget_layout.add_widget(self.calendar)
        self.widget_layout.add_widget(self.data_tables)

        self.bind(is_screen=self.on_is_screen)

    def get_date(self,date):
        print(date)
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
    def set_screen(self,value):
        self.is_screen = value