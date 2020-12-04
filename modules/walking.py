#-*-coding:utf-8-*-
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
import time

class WalkingWidget(Widget):
    is_screen = BooleanProperty(True)
    steps_value = NumericProperty(0)
    def __init__(self):
        super().__init__()
        self.color = (0.0, 1.0, 0.0, 1.0)
        self.widget_layout_main = FloatLayout()
        #self.widget_layout = GridLayout(cols = 2, size_hint = (0.8,0.8), pos_hint = {'x':0.1,'y':0.05})
        self.background_widget = Image(source='images/background2.png',size = Window.size,allow_stretch=True, keep_ratio=False)
        self.data_tables = MDDataTable(
            pos_hint={'x':.1,'y':.1},
            size_hint=(0.8, 0.8),
            column_data=[
                ("", dp(20)),
                ("", dp(30)),
                # ("Team Lead", dp(30))
            ]
            ,
            row_data=[
                ('steps', self.steps_value),
                ('dist', self.steps_value),
                ('calories', self.steps_value),
            ]
        )
        self.items_bind()
        
    def items_bind(self):
        self.widget_layout_main.clear_widgets()

        self.data_tables = MDDataTable(
            pos_hint={'x': .1, 'y': .1},
            size_hint=(0.8, 0.8),
            column_data=[
                ("", dp(20)),
                ("", dp(30)),
                # ("Team Lead", dp(30))
            ]
            ,
            row_data=[
                ('steps', self.steps_value),
                ('dist', self.steps_value),
                ('calories', self.steps_value),
            ]
        )

        self.widget_layout_main.add_widget(self.background_widget)
        self.widget_layout_main.add_widget(self.data_tables)
        self.bind(is_screen=self.on_is_screen)
        self.bind(steps_value=self.steps_value_changed)
        
    def steps_value_changed(self,instance,value):
        print('here executed')

        '''
        self.data_tables.row_data[0] = ('steps',self.steps_value)
        self.data_tables.row_data[1] = ('dist', self.steps_value)
        self.data_tables.row_data[2] = ('calories', self.steps_value)

        print(self.data_tables.row_data)

        self.widget_layout_main.clear_widgets()

        self.widget_layout_main.add_widget(self.background_widget)
        self.widget_layout_main.add_widget(self.data_tables)
        '''

    def on_walk(self):
        print('44444444444444444444444')
        self.steps_value = self.steps_value + 1

    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout_main.clear_widgets()
            #self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value
        #self.steps_value = time.time()