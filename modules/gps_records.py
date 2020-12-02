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
        self.filename, self.lat, self.lon, self.title, self.markers, self.count, self.obj = args
        self.popup = ""

    def on_press(self):  # title수정/삭제/뒤로가기/공유하기 버튼 만들기 => db에 공유 여부를 체크해야 하지만.. 일단 넘어가는 걸로 하자
        master_obj = self.obj
        my_popup = self.popup = Popup(size_hint=(.8, .8), title=self.title)
        def back_pressed(btn):
            master_obj.items_bind()
            my_popup.dismiss()

        box1 = BoxLayout(orientation='vertical')
        box1.add_widget(self.create_map(self.filename, self.lat, self.lon, self.markers))
        box2 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        retitle_button = Button(text='retitle',on_release=self.retitle_pressed)
        delete_button = Button(text='delete',on_release=self.delete_pressed)
        share_button = Button(text='share', on_release=self.share_pressed)
        back_button = Button(text='back', on_release=back_pressed)

        box2.add_widget(retitle_button)
        box2.add_widget(delete_button)
        box2.add_widget(share_button)
        box2.add_widget(back_button)
        box1.add_widget(box2)

        self.popup.content = box1
        self.popup.open()


    def retitle_pressed(self, btn):
        obj = self.obj
        filename = self.filename
        master_popup = self.popup
        def confirm_pressed(_btn):
            def wrong_btn_pressed(__btn):
                popupp.dismiss()
            def good_btn_pressed(__btn):
                popuppp.dismiss()
            def dup_btn_pressed(__btn):
                popupppp.dismiss()
            box_wrong = BoxLayout(orientation='vertical')
            box_good = BoxLayout(orientation='vertical')
            box_dup = BoxLayout(orientation='vertical')
            box_wrong.add_widget(Label(text='empty title'))
            box_wrong.add_widget(Button(text='back',on_release=wrong_btn_pressed))
            box_good.add_widget(Label(text='good'))
            box_good.add_widget(Button(text='back',on_release=good_btn_pressed))
            box_dup.add_widget(Label(text='duplicated'))
            box_dup.add_widget(Button(text='dup',on_release=dup_btn_pressed))
            popupp = Popup(title='wrong',content=box_wrong)
            popuppp = Popup(title='good',content=box_good)
            popupppp = Popup(title='dup',content=box_dup)
            if not text_input.text:
                popupp.open()
            elif text_input.text==self.title:
                popupppp.open()
            else:
                sql_connection = sqlite3.connect('Records/records.db')
                cursor = sql_connection.cursor()
                cursor.execute('update my_records set title = ? where datetime = ?', [text_input.text, filename])
                sql_connection.commit()
                sql_connection.close()
                popuppp.open()
                #master_popup.title = text_input.text
                text_input.text=''
                obj.items_bind()

        def back_pressed(_btn):
            popup.dismiss()
        text_input = TextInput(text='')
        confirm_button = Button(text='confirm',on_release=confirm_pressed)
        back_button = Button(text='back',on_release=back_pressed)
        box  = BoxLayout(orientation='vertical')
        box2 = BoxLayout(orientation='horizontal')
        box2.add_widget(confirm_button)
        box2.add_widget(back_button)
        box.add_widget(text_input)
        box.add_widget(box2)
        popup = Popup(title='retitle',content=box)
        popup.open()

    def delete_pressed(self, btn):
        filename = self.filename
        obj = self.obj
        def yes_pressed(_btn):
            def back_pressed(__btn):
                popup_good.dismiss()
            try:
                box3 = BoxLayout(orientation='vertical')
                box3.add_widget(Label(text='good'))
                box3.add_widget(Button(text='back',on_release=back_pressed))
                popup_good = Popup(title='good', content=box3)
                sql_connection = sqlite3.connect('Records/records.db')
                cursor = sql_connection.cursor()
                cursor.execute('delete from my_records where datetime = ?',[filename])
                sql_connection.commit()
                sql_connection.close()
                obj.items_bind()
                popup_good.open()
            except:
                print('stop pressing')
            #popup_wrong = Popup(title='wrong', content)
        def no_pressed(_btn):
            popup.dismiss()

        box = BoxLayout(orientation='vertical')
        box2 = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='you want delete this map info?'))
        box2.add_widget(Button(text='yes',on_release=yes_pressed))
        box2.add_widget(Button(text='no',on_release=no_pressed))
        box.add_widget(box2)
        popup = Popup(title='delete popup',content=box)
        popup.open()
        self.obj.items_bind()

    def share_pressed(self, btn):
        def no_pressed(_btn):
            popup.dismiss()

        def yes_pressed(_btn):
            def back_pressed(__btn):
                popupp.dismiss()
            def back_pressed2(__btn):
                popuppp.dismiss()
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(size_hint=(1, .8), text='already registered'))
            box.add_widget(Button(size_hint=(1, .2), text='back', on_release=back_pressed))
            popupp = Popup(size_hint=(.3, .3), title='already registered', content=box)

            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(size_hint=(1, .8), text='good'))
            box.add_widget(Button(size_hint=(1, .2), text='back', on_release=back_pressed2))
            popuppp = Popup(size_hint=(.3, .3), title='good', content=box)

            sql_connection = sqlite3.connect('Records/records.db')
            cursor = sql_connection.cursor()
            try:
                cursor.execute('insert into shared_records (datetime,lat,lon,title,markers,recommend) values (?,?,?,?,?,?)',
                               [filename, lat, lon, title,markers, 0])
                popuppp.open()
            except sqlite3.IntegrityError as err:
                popupp.open()

            for (latitude, longitude) in pickle.loads(markers):
                try:
                    cursor.execute('insert into popularity (location,lat,lon,count) values (?,?,?,?)',
                                   [str(latitude) + str(longitude), latitude, longitude, 1])
                except sqlite3.IntegrityError as err:
                    cursor.execute('select count from popularity')
                    cnt = cursor.fetchone()[0]
                    cursor.execute('update popularity set count = ? where location = ?',[cnt+1,str(latitude)+str(longitude)])
                    continue


            sql_connection.commit()
            sql_connection.close()
        filename, lat, lon, title,markers = self.filename, self.lat, self.lon, self.title,self.markers
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
        self.widget_layout_main = FloatLayout()
        self.widget_layout = GridLayout(cols=2,spacing=10,size_hint_y=None,size=(Window.width,Window.height*3))
        self.pages = []

        self.scrollview = ScrollView(size_hint=(1,None),size=(Window.width,Window.height),effect_cls=ScrollEffect)
        for x in dir(self.scrollview):
            print(x)
        self.items_bind()

    def create_img(self, *args):
        print(args)
        (filename, lat, lon, title,markers), count, obj = args
        return ImageButton(filename, lat, lon, title, markers, count, obj,
                           source='Records/' + filename + '.png',
                           size_hint_y=None,
                           size=(Window.size[0] * 3 // 5, Window.size[1] * 3 // 5))
                           #height=Window.height//4)
                           #allow_stretch=True, keep_ratio=False)

    def items_bind(self):
        self.widget_layout.clear_widgets()
        self.scrollview.clear_widgets()
        self.widget_layout_main.clear_widgets()

        sql_connection = sqlite3.connect('Records/records.db')
        cursor = sql_connection.cursor()
        cursor.execute('select datetime,lat,lon,title,markers from my_records')
        fetched = cursor.fetchall()
        (q, r), count = divmod(len(fetched), 4), 0
        self.widget_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, size=(Window.width, (Window.height * 3 // 5) * len(fetched)//2+1))

        for i in range(len(fetched)):
            self.widget_layout.add_widget(self.create_img(fetched[i], count, self))
        self.scrollview.add_widget(self.widget_layout)
        self.widget_layout_main.add_widget(self.scrollview)

        self.bind(is_screen=self.on_is_screen)

    def on_is_screen(self, instance, value):
        if value:
            self.items_bind()
        else:
            self.widget_layout.clear_widgets()
            self.scrollview.clear_widgets()
            self.widget_layout_main.clear_widgets()

    def set_screen(self, value):
        self.is_screen = value
