#-*-coding:utf-8-*-
from kivy.garden.mapview import MapView,MapMarker,MarkerMapLayer
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty,NumericProperty
from kivy.graphics import Line
import threading
import time

class GpsTrackingWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        self.widget_layout = FloatLayout()
        self.origin_size = (1,1)
        self.map_view = MapView(zoom=12, lat=37.5606, lon=126.9790) # gps에서 현재위치 받아서 띄우기
        self.cur_lat,self.cur_lon = 37.5606,126.9790
        self.marker_layer = MarkerMapLayer()
        self.map_view.add_layer(self.marker_layer)
        self.map_view.add_marker(MapMarker(lat=self.cur_lat,lon=self.cur_lon,
                                           source='images/mmy_marker.png'),layer=self.marker_layer)
        self.positions = [(self.cur_lat,self.cur_lon)]
        
        self.save_button = Button(text='save',pos_hint={'x':0.0,'y':0.0},size_hint=(.1,.1))
        self.clear_button = Button(text='clear',pos_hint={'x':0.1,'y':0.0},size_hint=(.1,.1))
        
        self.items_bind()
    
    def pos_changed(self,instance,coord,gps):
        self.cur_lat,self.cur_lon = gps.lat,gps.lon
        self.positions.append((gps.lon,gps.lat))
        self.map_view.add_marker(MapMarker(lat=gps.lon,lon=gps.lat,
                                           source='images/mmy_marker.png'),layer=self.marker_layer)#오류로 gps.lat과 gps.lon의 값이 바뀌어있음
        
    def clear_button_release(self,btn):
        self.marker_layer.unload()
        
    def save_button_release(self,btn):
        pass
    
    def items_bind(self):
        self.widget_layout.add_widget(self.map_view)
        self.widget_layout.add_widget(self.save_button)
        self.widget_layout.add_widget(self.clear_button)                             
        self.bind(is_screen=self.on_is_screen)
        self.map_view.bind(on_map_relocated = self.pos_changed)
        self.save_button.bind(on_release=self.save_button_release)
        self.clear_button.bind(on_release=self.clear_button_release)
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value