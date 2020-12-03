from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty,StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp

import sqlite3
import pickle

class ImageButton(ButtonBehavior, AsyncImage):
    def __init__(self, *args, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.filename, self.lat, self.lon, self.title, self.markers,self.recommend, self.count, self.obj = args
        self.popup = ""

    def on_press(self):  # title수정/삭제/뒤로가기/공유하기 버튼 만들기 => db에 공유 여부를 체크해야 하지만.. 일단 넘어가는 걸로 하자
        recommend,filename = self.recommend,self.filename
        popup = Popup(title='popup')
        def recommend_button_pressed(btn):
            back_popup = Popup(title='popup')
            def back_button_pressed2(_btn):
                back_popup.dismiss()
            sql_connection = sqlite3.connect('Records/records.db')
            cursor = sql_connection.cursor()
            cursor.execute('update shared_records set recommend = ? where datetime = ?',
                           [recommend+1,filename])
            sql_connection.commit()
            sql_connection.close()
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(text='추천이 적용됐습니다',font_name='Fonts/NanumBarunGothic.ttf'))
            box.add_widget(Button(text='뒤로가기',font_name='Fonts/NanumBarunGothic.ttf',on_release=back_button_pressed2))
            back_popup.content=box
            back_popup.open()
        def back_button_pressed(btn):
            popup.dismiss()
        recommend_button = Button(text='추천',font_name='Fonts/NanumBarunGothic.ttf',on_release=recommend_button_pressed)
        back_button = Button(text='뒤로가기',font_name='Fonts/NanumBarunGothic.ttf',on_release=back_button_pressed)
        box_vertical = BoxLayout(orientation='vertical')
        box_horizontal = BoxLayout(orientation='horizontal',size_hint_y=.2)
        box_horizontal.add_widget(recommend_button)
        box_horizontal.add_widget(back_button)
        box_vertical.add_widget(self.create_map(self.filename, self.lat, self.lon, self.markers))
        box_vertical.add_widget(box_horizontal)
        popup.content = box_vertical
        popup.open()

    def create_map(self, *args):
        _, latitude, longitude, markers = args
        markers = pickle.loads(markers)
        map = MapView(zoom=12, lat=latitude, lon=longitude, size_hint=(1, .8))
        marker_layer = MarkerMapLayer()
        map.add_layer(marker_layer)
        for (lat, lon) in markers:
            # print(type(lat),type(lon))
            map.add_marker(MapMarker(lat=lat, lon=lon, source='images/mmy_marker.png'), layer=marker_layer)
        return map

class ShareCourseWidget(Widget):
    is_screen = BooleanProperty(True)
    order_state = StringProperty('recommend')
    def __init__(self):
        super().__init__()
        self.widget_layout_main = FloatLayout()
        self.widget_layout = GridLayout(cols=2, spacing=20, size_hint_y=None, size=(Window.width, Window.height * 3),pos_hint={'y':.8})
        self.button_box = BoxLayout(orientation='horizontal',pos_hint={'y':.9},size_hint=(.2,.1))
        self.recommend_order_button = Button(text='추천순',font_name='Fonts/NanumBarunGothic.ttf',on_release=self.recommend_order_pressed)
        self.date_order_button = Button(text='날짜순',font_name='Fonts/NanumBarunGothic.ttf',on_release=self.date_order_pressed)
        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), effect_cls=ScrollEffect)

        self.button_box.add_widget(self.recommend_order_button)
        self.button_box.add_widget(self.date_order_button)


        self.items_bind()

    def recommend_order_pressed(self,btn):
        self.order_state = 'recommend'
    def date_order_pressed(self,btn):
        self.order_state = 'date'

    def create_img(self, *args):
        (filename, lat, lon, title, markers,recommend), count, obj = args
        return ImageButton(filename, lat, lon, title, markers,recommend, count, obj,
                           source='Records/' + filename + '.png',
                           size_hint_y=None,
                           size=(Window.size[0] * 3 // 5, Window.size[1] * 3 // 5))

    def items_bind(self):
        self.widget_layout.clear_widgets()
        self.scrollview.clear_widgets()
        self.widget_layout_main.clear_widgets()

        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()
        cursor.execute('select datetime,lat,lon,title,markers,recommend from shared_records')
        fetched = cursor.fetchall()
        (q, r), count = divmod(len(fetched), 4), 0
        self.widget_layout = GridLayout(cols=2, spacing=10, size_hint_y=None,
                                        size=(Window.width, (Window.height * 3 // 5) * len(fetched) // 2 + 1))

        if self.order_state == 'recommend':
            fetched.sort(key=lambda x: x[5])
        elif self.order_state == 'date':
            fetched.sort(key=lambda x: x[0])

        for i in range(len(fetched)):
            self.widget_layout.add_widget(self.create_img(fetched[i], count, self))
        self.scrollview.add_widget(self.widget_layout)
        self.widget_layout_main.add_widget(self.scrollview)
        self.widget_layout_main.add_widget(self.button_box)

        self.bind(is_screen=self.on_is_screen)
        self.bind(order_state=self.order_state_changed)
        sql_connection.close()

    def on_is_screen(self, instance, value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            self.scrollview.clear_widgets()
            self.widget_layout_main.clear_widgets()

    def set_screen(self, value):
        self.is_screen = value
    def order_state_changed(self,instance,value):
        self.widget_layout.clear_widgets()
        self.scrollview.clear_widgets()
        self.widget_layout_main.clear_widgets()
        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()
        cursor.execute('select datetime,lat,lon,title,markers,recommend from shared_records')
        fetched = cursor.fetchall()
        (q, r), count = divmod(len(fetched), 4), 0
        self.widget_layout = GridLayout(cols=2, spacing=10, size_hint_y=None,
                                        size=(Window.width, (Window.height * 3 // 5) * len(fetched) // 2 + 1))

        if value == 'recommend':
            fetched.sort(key=lambda x : x[5])
        elif value == 'date':
            fetched.sort(key=lambda x : x[0])

        for i in range(len(fetched)):
            self.widget_layout.add_widget(self.create_img(fetched[i], count, self))
        self.scrollview.add_widget(self.widget_layout)
        self.widget_layout_main.add_widget(self.scrollview)
        self.widget_layout_main.add_widget(self.button_box)
        sql_connection.close()