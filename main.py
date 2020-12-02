#-*-coding:utf-8-*-
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp

from modules.dropdown import DropDownWidget
from modules.walking import WalkingWidget
from modules.past_record import PastRecordWidget
from modules.gps_tracking import GpsTrackingWidget
from modules.share_course import ShareCourseWidget
from modules.hot_place import HotPlaceWidget
from modules.gps_records import GpsRecordsWidget

import threading
import sqlite3


class MyApplicationApp(MDApp):
    def __init__(self):
        super().__init__()
        self.parent = FloatLayout()
        self.widget_list = dict()
        self.background_widget = Widget()  # color = (0.4,0.5,0.3))
        self.dropdown_widget = DropDownWidget()
        self.btn_callback_bind()

        # 1. walking
        self.walking_widget = WalkingWidget()
        self.widget_list['walking'] = self.walking_widget

        # 2. past_record
        self.past_record_widget = PastRecordWidget()
        self.widget_list['past_record'] = self.past_record_widget

        # 3. gps_tracking
        self.gps_tracking_widget = GpsTrackingWidget()
        self.widget_list['gps_tracking'] = self.gps_tracking_widget

        # 4. share_course
        self.share_course_widget = ShareCourseWidget()
        self.widget_list['share_course'] = self.share_course_widget

        # 5. hot_place
        self.hot_place_widget = HotPlaceWidget()
        self.widget_list['hot_place'] = self.hot_place_widget

        # 6. gps_records
        self.gps_records_widget = GpsRecordsWidget()
        self.widget_list['gps_records'] = self.gps_records_widget

        
    def btn_callback_bind(self):
        for (btn,func) in [('walking',self.walking_on_release),
                           ('past_record',self.past_record_on_release),
                           ('gps_tracking',self.gps_tracking_on_release),
                           ('share_course',self.share_course_on_release),
                           ('hot_place',self.hot_place_on_release),
                           ('gps_records',self.gps_records_on_release)]:
            self.dropdown_widget.dropdown_dict[btn].bind(on_release = func)
    
    def clear_screen(self,widget_name):
        self.widget_list[widget_name].set_screen(True)
        for name in ['walking','past_record','gps_tracking',
                     'share_course','hot_place','gps_records']:
            if widget_name != name:
                self.widget_list[name].set_screen(False)
    
    def walking_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('walking')
    def past_record_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('past_record')
    def gps_tracking_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('gps_tracking')
    def share_course_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('share_course')
    def hot_place_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('hot_place')
    def gps_records_on_release(self,btn):
        # 선택되면 select를 이용해 btn.text를 dropdown에 보냄
        self.dropdown_widget.dropdown.select(btn.text)
        self.clear_screen('gps_records')
        # 위젯들의 사이즈를 0으로 만들어 화면에서 사라지는 모습을 구현
    
    def build(self):
        self.parent.add_widget(self.walking_widget.widget_layout_main)
        self.parent.add_widget(self.past_record_widget.widget_layout)
        self.parent.add_widget(self.gps_tracking_widget.widget_layout)
        #self.parent.add_widget(self.share_course_widget.widget_layout)
        self.parent.add_widget(self.hot_place_widget.widget_layout)
        self.parent.add_widget(self.gps_records_widget.widget_layout)


        self.clear_screen('walking')

        self.parent.add_widget(self.background_widget)
        self.parent.add_widget(self.dropdown_widget.mainbutton)
        
        return self.parent

if __name__ == '__main__':
    
    MyApplicationApp().run()
