from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

class GpsRecordsWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        super().__init__()
        self.origin_size = (1,1)
        self.widget_layout = FloatLayout()
        self.img = Image(source = 'images/3.jpg')#,pos_hint = {'x':0.4,'y':0.3},size_hint = (0.3,0.3))
        self.items_bind()
        
    def items_bind(self):
        self.widget_layout.add_widget(self.img)
        self.bind(is_screen=self.on_is_screen)
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value