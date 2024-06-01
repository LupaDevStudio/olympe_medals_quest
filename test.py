from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import datetime

label = None

text = 'Hello World of Python!'
text_length = len(text)

index = 0
temp_text = text + ' ' + text

def update_label(dt):
    global index
    
    label.text = temp_text[0:index]
    index += 1
    
    if index >= text_length:
        index = 0
    
class MyApp(App):
    def build(self):
        global label
        
        label = Label(text="???")
        Clock.schedule_interval(update_label, 0.05)
        
        return label

if __name__ == '__main__':
    MyApp().run()