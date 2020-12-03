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
from kivy.uix.popup import Popup
import re
import sqlite3

class PastRecordWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        super().__init__()
        
        self.widget_layout = BoxLayout(orientation='vertical')
        self.calendar = MDDatePicker(callback=self.get_date,size=(Window.width,Window.height))


        self.items_bind()
        
    def items_bind(self):
        self.widget_layout.add_widget(self.calendar)

        self.bind(is_screen=self.on_is_screen)

    def get_date(self,date):
        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()

        cursor.execute('select * from past_records where date=?',[''.join(re.findall('[0-9]',str(date)))])
        def result_back_button_pressed(btn):
            result_popup.dismiss()
        def bad_back_button_pressed(btn):
            bad_popup.dismiss()
        result = cursor.fetchone()
        sql_connection.close()
        if result:
            result_popup = Popup(title='popup', size_hint=(0.5, 0.7))
            result_box = BoxLayout(orientation='vertical')
            data_tables = MDDataTable(
                size_hint=(1, 0.5),
                # pos_hint = {'y':0},
                column_data=[
                    ("", dp(25)),
                    ("", dp(30)),
                    # ("Team Lead", dp(30))
                ]
                ,
                row_data=[
                    ('steps', str(result[1])),
                    ('dist', str(result[2])),
                    ('calories', str(result[3])),
                ]
            )
            result_box.add_widget(data_tables)
            result_box.add_widget(Button(pos_hint={'x':0.4},size_hint=(0.2,0.1),text='뒤로가기',on_release=result_back_button_pressed,font_name='Fonts/NanumBarunGothic.ttf'))
            result_popup.add_widget(result_box)
            result_popup.open()
        else:
            bad_popup = Popup(title='popup',size_hint=(0.3,0.3))
            bad_box = BoxLayout(orientation='vertical')
            bad_box.add_widget(Label(text='결과가 없습니다',font_name='Fonts/NanumBarunGothic.ttf'))
            bad_box.add_widget(Button(text='뒤로가기', on_release=bad_back_button_pressed, font_name='Fonts/NanumBarunGothic.ttf'))
            bad_popup.add_widget(bad_box)
            bad_popup.open()

    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
    def set_screen(self,value):
        self.is_screen = value