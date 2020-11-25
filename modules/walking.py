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
        self.widget_layout = GridLayout(cols = 2, size_hint = (0.8,0.8), pos_hint = {'y':0.05})
        self.background_widget = Image(source='images/background2.png',size = Window.size,allow_stretch=True, keep_ratio=False)
        self.data_tables = MDDataTable(
            size_hint=(0.7, 0.9),
            column_data=[
                ("", dp(40)),
                ("", dp(70)),
                # ("Team Lead", dp(30))
            ]
            ,
            row_data=[
                ('steps', self.steps_value),
                ('dist', self.steps_value),
                ('calories', self.steps_value),
                ('a',self.steps_value),
                ('b',self.steps_value),
                ('c',self.steps_value)
            ]
        )

        '''
        self.steps_label, self.steps_value_label = Label(text = 'steps',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.distance_label, self.distance_value_label = Label(text = 'dist',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.kcal_label, self.kcal_value_label = Label(text = 'kcal',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.a_label, self.a_value_label = Label(text = 'abcd',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.b_label, self.b_value_label = Label(text = 'asdas',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.c_label, self.c_value_label = Label(text = 'asd',color = self.color), Label(text = f'{self.steps_value}',color = self.color)
        self.labels = [self.steps_label,self.steps_value_label,
                       self.distance_label,self.distance_value_label,self.kcal_label,
                       self.kcal_value_label,self.a_label,self.a_value_label,
                       self.b_label,self.b_value_label,self.c_label,self.c_value_label]
        '''
        self.items_bind()
        
    def items_bind(self):
        for _label in self.labels:
            self.widget_layout.add_widget(_label)
        self.widget_layout_main.add_widget(self.background_widget)
        self.widget_layout_main.add_widget(self.widget_layout)
        self.bind(is_screen=self.on_is_screen)
        self.bind(steps_value=self.steps_value_changed)
        
    def steps_value_changed(self,instance,value):
        for label in [self.steps_value_label,self.distance_value_label,self.kcal_value_label,
                      self.a_value_label,self.b_value_label,self.c_value_label]:
            label.text = str(time.time())
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout_main.clear_widgets()
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value
        self.steps_value = time.time()