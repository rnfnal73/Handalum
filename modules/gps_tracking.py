#-*-coding:utf-8-*-
from kivy.garden.mapview import MapView,MapMarker,MarkerMapLayer
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty,NumericProperty,ListProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import WindowBase
import threading
import time
import pickle
import datetime
import sqlite3

class GpsTrackingWidget(Widget):
    is_screen = BooleanProperty(True)
    cur_loc = ListProperty([0,0])

    def __init__(self,walking_widget):
        super().__init__()
        self.walking_widget = walking_widget
        self.widget_layout = FloatLayout()
        self.origin_size = (1,1)
        self.map_view = MapView(zoom=12, lat=37.5606, lon=126.9790) # gps에서 현재위치 받아서 띄우기
        self.cur_lat,self.cur_lon = 37.5606,126.9790
        self.marker_layer = MarkerMapLayer()
        self.map_view.add_layer(self.marker_layer)
        self.positions = [(self.cur_lat,self.cur_lon)]
        self.save_button = Button(text='save',pos_hint={'x':0.0,'y':0.0},size_hint=(.1,.1))
        self.clear_button = Button(text='clear',pos_hint={'x':0.1,'y':0.0},size_hint=(.1,.1))
        
        self.items_bind()
    
    def pos_changed(self,instance,coord,gps):
        self.walking_widget.on_walk()
        self.positions.append((gps.lon,gps.lat))
        self.map_view.add_marker(MapMarker(lat=gps.lon,lon=gps.lat,
                                           source='images/mmy_marker.png'),layer=self.marker_layer)#오류로 gps.lat과 gps.lon의 값이 바뀌어있음

    def clear_button_release(self,btn):
        self.marker_layer.unload()
        
    def save_button_release(self,btn):
        cur_time = datetime.datetime.now()
        t = threading.Thread(target=self.save_data,args=[self.positions,cur_time])
        t.start()
        t.join()

    def save_data(self,*args):
        obj = self.map_view
        def insert_pressed(btn):
            def wrong_back_pressed(_btn):
                popupp.dismiss()
            def good_back_pressed(_btn):
                popuppp.dismiss()
            box3 = BoxLayout(orientation='vertical')
            box3.add_widget(Label(text='wrong'))
            box3.add_widget(Button(text='back',on_release=wrong_back_pressed))
            popupp = Popup(title='wrong',content=box3)

            box4 = BoxLayout(orientation='vertical')
            box4.add_widget(Label(text='good'))
            box4.add_widget(Button(text='back', on_release=good_back_pressed))
            popuppp = Popup(title='good', content=box4)

            if not text_input.text:
                popupp.open()
            else:
                _list, cur_time = args
                sql_connection = sqlite3.connect('Records/records.db')
                cur = str(cur_time.year) + str(cur_time.month) + str(cur_time.day) + str(cur_time.hour) + str(
                    cur_time.minute) + str(cur_time.second)
                cursor = sql_connection.cursor()
                cursor.execute("insert into my_records (datetime,lat,lon,title,markers) values (?,?,?,?,?)",
                               [cur, _list[0][0], _list[0][1],text_input.text, pickle.dumps(_list)])

                sql_connection.commit()
                sql_connection.close()
                obj.export_to_png(filename='Records/' + str(cur_time.year) + str(cur_time.month) + str(cur_time.day) +
                                            str(cur_time.hour) + str(cur_time.minute) + str(cur_time.second) + '.png')
                text_input.text=''
                popuppp.open()
        def back_pressed(btn):
            popup.dismiss()
        box = BoxLayout(orientation='vertical')
        box2 = BoxLayout(orientation='horizontal')

        insert_button = Button(text='insert',on_release=insert_pressed)
        back_button = Button(text='back',on_release=back_pressed)
        box2.add_widget(insert_button)
        box2.add_widget(back_button)

        text_input = TextInput(text='insert title for map')

        box.add_widget(text_input)
        box.add_widget(box2)
        popup = Popup(title='title the map',content=box)
        popup.open()



    def items_bind(self):
        self.map_view.bind(on_map_relocated=self.pos_changed)
        self.save_button.bind(on_release=self.save_button_release)
        self.clear_button.bind(on_release=self.clear_button_release)
        self.widget_layout.add_widget(self.map_view)
        self.widget_layout.add_widget(self.save_button)
        self.widget_layout.add_widget(self.clear_button)                             
        self.bind(is_screen=self.on_is_screen)
        #self.bind(cur_loc=self.pos_changed)
        
    def on_is_screen(self,instance,value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            
    def set_screen(self,value):
        self.is_screen = value

    """    def on_walk(self,lat,lon):
        print('333333333333333333333333333333')
        self.cur_loc = [lat,lon]
        '''
        self.cur_lat, self.cur_lon = lat, lon
        self.positions.append((lat, lon))
        self.map_view.add_marker(MapMarker(lat=lat, lon=lon,source='images/mmy_marker.png'),
                                 layer=self.marker_layer)  # 오류로 gps.lat과 gps.lon의 값이 바뀌어있음
        '''
    """