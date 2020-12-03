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

import os

#fontname = '/'.join([os.getenv('SystemRoot'),'/Fonts/NanumGothic.ttf'])


"""
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
        self.parent.add_widget(self.share_course_widget.widget_layout_main)
        self.parent.add_widget(self.hot_place_widget.widget_layout)
        #self.parent.add_widget(self.gps_records_widget.widget_layout)
        self.parent.add_widget(self.gps_records_widget.widget_layout_main)

        self.clear_screen('walking')

        self.parent.add_widget(self.background_widget)
        self.parent.add_widget(self.dropdown_widget.mainbutton)
        
        return self.parent

if __name__ == '__main__':
    
    MyApplicationApp().run()
"""
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform

kv = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        text: app.gps_location
    Label:
        text: app.gps_status
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'
        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.start(1000, 0) if self.state == 'down' else \
                app.stop()
'''


class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return Builder.load_string(kv)

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        print(self.gps_location)

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
        print(self.gps_status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass


if __name__ == '__main__':
    GpsTest().run()