"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    BooleanProperty,
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty
)
from tools.graphics import(
    FONTS_SIZES,
    COLORS,
    HEADER_HEIGHT
)
from tools.path import (
    PATH_TITLE_FONT
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

class MyScrollViewVerticalLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewVerticalLayout, self).__init__(**kwargs)
        self.size_hint_x = (None)
        self.bind(minimum_width=self.setter('width'))

    def refill(self):
        self.setter("width")

    def reset_scrollview(self):
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)

class CustomScrollview(ScrollView):
    pass
