from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder


Builder.load_string('''
#:import ScrollEffect  kivy.effects.scroll.ScrollEffect
#:import Button kivy.uix.button.Button
<RootWidget>
    effect_cls: ScrollEffect
    GridLayout:
        size_hint_y: None
        height: self.minimum_height
        cols: 1
        on_parent:
            for i in range(10): self.add_widget(Button(text=str(i), size_hint_y=None))
''')

class RootWidget(ScrollView):
    pass

class MainApp(App):
    def build(self):
        root = RootWidget()
        return root

if __name__ == '__main__':
    MainApp().run()