"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
    BooleanProperty
)

#############
### Class ###
#############

class MyScrollViewLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewLayout, self).__init__(**kwargs)
        self.size_hint_y = (None)
        self.bind(minimum_height=self.setter('height'))

    def refill(self):
        self.setter("height")

    def reset_scrollview(self):
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)


class CustomScrollview(ScrollView):
    
    header_mode = BooleanProperty(False)
