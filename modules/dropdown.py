#-*-coding:utf-8-*-
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.garden.mapview import MapView

'''
# create a dropdown with 10 buttons
dropdown = DropDown()

for index in range(10):#사전에 dropdown size를 pre-define 해야함
    # When adding widgets, we need to specify the height manually
    # (disabling the size_hint_y) so the dropdown can calculate
    # the area it needs.

    btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

    # for each button, attach a callback that will call the select() method
    # on the dropdown. We'll pass the text of the button as the data of the
    # selection.
    btn.bind(on_release=lambda btn: dropdown.select(btn.text)) 

    # then add the button inside the dropdown
    dropdown.add_widget(btn)
'''

class DropDownWidget(Widget):
    def __init__(self):
        super().__init__()
        self.dropdown = DropDown() # dropdown menu
        
        self.walking_btn = Button(text = '만보기',size_hint_y = None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        self.past_record_btn = Button(text = '만보기 기록',size_hint_y=None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        self.gps_tracking_btn = Button(text = 'GPS',size_hint_y=None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        self.share_course_btn = Button(text = '기록 공유',size_hint_y=None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        self.hot_place_btn = Button(text = '핫플',size_hint_y=None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        self.gps_records_btn = Button(text = 'GPS 기록',size_hint_y=None, height = 60,font_name='Fonts/NanumBarunGothic.ttf')
        
        self.dropdown_dict = {'walking':self.walking_btn,'past_record':self.past_record_btn,
                              'gps_tracking':self.gps_tracking_btn,'share_course':self.share_course_btn,
                              'hot_place':self.hot_place_btn,'gps_records':self.gps_records_btn}
        
        # create a big main button
        self.mainbutton = Button(text='메뉴', pos_hint = {'x':.75,'y':.925}, size_hint=(.25,.075),font_name='Fonts/NanumBarunGothic.ttf')
        
        self.btn_callback_bind()
        
    def btn_callback_bind(self):
        for btn in ['walking','gps_tracking','past_record',
                    'gps_records','share_course','hot_place']:
            self.dropdown.add_widget(self.dropdown_dict[btn])
            
        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.

         # x가 select로 전달된 파라미터,'text' 속성을 x로 바꾸라는 setattr 함수, callback 대신 람다 함수로 대체한 모습
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
            
    
        
