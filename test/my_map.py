from kivy.garden.mapview import MapView,MapMarker
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
import os

class MapViewApp(App):
    def build(self):
        layout = FloatLayout()
        map_view = MapView(zoom=14, lat=37.5606, lon=126.9790) # gps에서 현재위치 받아서 띄우기
        marker = MapMarker(lat=37.5606,lon=126.9790,source='mmy_marker.png')
        #layout.add_widget(map_view)
        #layout.add_widget(marker)
        map_view.add_widget(marker)
        return map_view

MapViewApp().run()