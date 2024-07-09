from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import cm
        
class NotificationDemoApp(App):
    def build(self):
        main_scroll = ScrollView(do_scroll_x=False)
        main_grid = GridLayout(cols=1, spacing=100, padding=[0, 50, 0, 50], size_hint_y=None)
        main_grid.bind(minimum_height=main_grid.setter('height'))
        main_scroll.add_widget(main_grid)
        scroll_count = 4
        for _ in range(scroll_count):
            scroll = ScrollView(size_hint=(0.5, None), height=300, do_scroll_x=False)
            grid = GridLayout(cols=1, spacing=1, size_hint=(0.5, None))
            grid.bind(minimum_height=grid.setter('height'))
            scroll.add_widget(grid)
            for r in range(0,50):
                bt = Button(text='Button '+str(r), size_hint_y=None, height=cm(2))
                bt.bind(on_press=self.print_btn)
                grid.add_widget(bt)
            main_grid.add_widget(scroll)
        return main_scroll

    def print_btn(self, instance):
        print ('Pressed', instance.text)


if __name__ == '__main__':
    NotificationDemoApp().run()