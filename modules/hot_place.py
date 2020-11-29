from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer
import sqlite3

class HotPlaceWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        super().__init__()
        self.origin_size = (1,1)
        self.widget_layout = FloatLayout()

        #줌을 12에서 붐비는정도라는 의도에 걸맞게 zoom을 높여주기 -> ux 개선사항
        self.map_view = MapView(zoom=15, lat=37.5606, lon=126.9790)  # gps에서 현재위치 받아서 띄우기

        self.cur_lat, self.cur_lon = 37.5606, 126.9790
        self.marker_layer = MarkerMapLayer()
        self.map_view.add_layer(self.marker_layer)

        self.items_bind()
        
    def items_bind(self):
        self.widget_layout.clear_widgets()
        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()
        cursor.execute('select lat,lon,count from popularity')
        for (lat,lon,count) in cursor.fetchall():
            if count < 3:
                self.map_view.add_marker(MapMarker(lat=lat,lon=lon,
                                                   source='images/heart_yellow.png'), layer=self.marker_layer)
            elif 3 <= count < 7:
                self.map_view.add_marker(MapMarker(lat=lat,lon=lon,
                                                   source='images/heart_green.png'), layer=self.marker_layer)
            else:
                self.map_view.add_marker(MapMarker(lat=lat,lon=lon,
                                                   source='images/heart_red.png'), layer=self.marker_layer)
        sql_connection.close()

        self.widget_layout.add_widget(self.map_view)
        self.bind(is_screen=self.on_is_screen)
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value
