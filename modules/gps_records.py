from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.garden.mapview import MapView, MapMarker, MarkerMapLayer
from kivy.uix.popup import Popup
from kivy.metrics import dp

import sqlite3
import pickle


class ImageButton(ButtonBehavior, AsyncImage):
    def __init__(self, *args, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.filename, self.lat, self.lon, self.markers, self.count, self.obj = args

    def on_press(self):  # title수정/삭제/뒤로가기/공유하기 버튼 만들기 => db에 공유 여부를 체크해야 하지만.. 일단 넘어가는 걸로 하자
        def back_pressed(btn):
            self.obj.items_bind()
            popup.dismiss()

        box1 = BoxLayout(orientation='vertical')
        box1.add_widget(self.create_map(self.filename, self.lat, self.lon, self.markers))
        box2 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        retitle_button = Button(text='retitle')
        delete_button = Button(text='delete')
        share_button = Button(text='share', on_release=self.share_pressed)
        back_button = Button(text='back', on_release=back_pressed)

        box2.add_widget(retitle_button)
        box2.add_widget(delete_button)
        box2.add_widget(share_button)
        box2.add_widget(back_button)
        box1.add_widget(box2)

        popup = Popup(size_hint=(.8, .8), title='location title', content=box1)
        popup.open()
        print(self.lat, self.lon, self.count)

    def retitle_pressed(self, btn):
        pass

    def delete_pressed(self, btn):
        pass

    def share_pressed(self, btn):
        def no_pressed(_btn):
            popup.dismiss()

        def yes_pressed(_btn):

            def back_pressed(__btn):
                popupp.dismiss()

            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(size_hint=(1, .8), text='already registered'))
            box.add_widget(Button(size_hint=(1, .2), text='back', on_release=back_pressed))
            popupp = Popup(size_hint=(.3, .3), title='already registered', content=box)

            try:
                sql_connection = sqlite3.connect('Records/records.db')
                cursor = sql_connection.cursor()
                cursor.execute('insert into shared_records (datetime,lat,lon,markers,recommend) values (?,?,?,?,?)',
                               [filename, lat, lon, markers, 0])
                sql_connection.commit()
                sql_connection.close()
            except:
                popupp.open()

        filename, lat, lon, markers = self.filename, self.lat, self.lon, self.markers
        box = BoxLayout(orientation='vertical')
        yes_button, no_button = Button(text='yes', on_release=yes_pressed), Button(text='no', on_release=no_pressed)
        box.add_widget(yes_button)
        box.add_widget(no_button)
        popup = Popup(size_hint=(.3, .3), title='real?', content=box)
        popup.open()


    def create_map(self, *args):
        _, latitude, longitude, markers = args
        markers = pickle.loads(markers)
        map = MapView(zoom=12, lat=latitude, lon=longitude, size_hint=(1, .7))
        marker_layer = MarkerMapLayer()
        map.add_layer(marker_layer)
        for (lat, lon) in markers:
            # print(type(lat),type(lon))
            map.add_marker(MapMarker(lat=lat, lon=lon, source='images/mmy_marker.png'), layer=marker_layer)
        return map


class GpsRecordsWidget(Widget):
    is_screen = BooleanProperty(True)

    def __init__(self):
        super().__init__()
        self.origin_size = (1, 1)
        self.widget_layout = PageLayout()
        self.widget_layout.border = dp(0)
        self.pages = []
        self.cur_page = 0

        self.items_bind()

    def create_img(self, *args):
        print(args)
        (filename, lat, lon, markers), count, obj = args
        return ImageButton(filename, lat, lon, markers, count, obj
                           , source='Records/' + filename + '.png',
                           size=(Window.size[0] * 3 // 5, Window.size[1] * 3 // 5),
                           allow_stretch=True, keep_ratio=False)

    def items_bind(self):
        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()
        cursor.execute('select datetime,lat,lon,markers from my_records')
        fetched = cursor.fetchall()
        (q, r), count = divmod(len(fetched), 4), 0

        for i in range(q):
            grid_layout = GridLayout(cols=2)
            for j in range(4):
                grid_layout.add_widget(self.create_img(fetched[count], count, self))
                count += 1
            self.widget_layout.add_widget(grid_layout)
        grid_layout = GridLayout(cols=2)
        for _ in range(4):
            try:
                grid_layout.add_widget(self.create_img(fetched[count], count, self))
                count += 1
            except:
                grid_layout.add_widget(Widget())
        self.widget_layout.add_widget(grid_layout)

        # self.widget_layout.add_widget(self.img3)
        # self.widget_layout.add_widget(self.img2)
        # self.widget_layout.add_widget(self.img)
        self.bind(is_screen=self.on_is_screen)

    def on_is_screen(self, instance, value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()

    def set_screen(self, value):
        self.is_screen = value
