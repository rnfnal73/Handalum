#-*-coding:utf-8-*-
from kivy.garden.mapview import MapView,MapMarker,MarkerMapLayer
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty,NumericProperty
from kivy.core.window import WindowBase
import threading
import time
import pickle
import datetime
import sqlite3

class GpsTrackingWidget(Widget):
    is_screen = BooleanProperty(True)
    
    def __init__(self):
        super().__init__()
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
        cur_time = datetime.datetime.now()
        self.map_view.export_to_png(filename='Records/'+str(cur_time.year) + str(cur_time.month) + str(cur_time.day) + str(cur_time.hour) + str(
            cur_time.minute) + str(cur_time.second)+'.png')
        t = threading.Thread(target=self.save_data,args=[self.positions,cur_time])
        t.start()
        t.join()

    def save_data(self,*args):
        _list, cur_time = args
        sql_connection = sqlite3.connect('Records/records.db')
        cur = str(cur_time.year) + str(cur_time.month) + str(cur_time.day) + str(cur_time.hour) + str(
            cur_time.minute) + str(cur_time.second)
        cursor = sql_connection.cursor()
        #print("insert into my_records (datetime,lat,lon,year,month,day,hr,min,sec) values ("+f"{cur},{_list[0]},{_list[1]},{cur_time.year},{cur_time.month},{cur_time.day},{cur_time.hour},{cur_time.minute},{cur_time.second}"+")")
        cursor.execute("insert into my_records (datetime,lat,lon,markers) values (?,?,?,?)",[cur,_list[0][0],_list[0][1],pickle.dumps(_list)])
        #with open('Records/'+ cur, 'wb') as fd:
        #    pickle.dump(_list, fd)
        sql_connection.commit()
        sql_connection.close()
        #WindowBase.screenshot(WindowBase,name='img.png')
        #self.screenshot(name='Records/img.png')


    def items_bind(self):
        self.map_view.bind(on_map_relocated=self.pos_changed)
        self.save_button.bind(on_release=self.save_button_release)
        self.clear_button.bind(on_release=self.clear_button_release)
        self.widget_layout.add_widget(self.map_view)
        self.widget_layout.add_widget(self.save_button)
        self.widget_layout.add_widget(self.clear_button)                             
        self.bind(is_screen=self.on_is_screen)
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value