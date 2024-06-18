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
    NumericProperty
)
from tools.graphics import(
    FONTS_SIZES,
    COLORS,
    SCROLL_VIEW_HEADER_HEIGHT
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


class CustomScrollview(ScrollView):
    pass


class OlympeScrollView(RelativeLayout):

    header_mode = BooleanProperty(False)
    header_height = NumericProperty(SCROLL_VIEW_HEADER_HEIGHT)
    header_text = StringProperty()
    font_ratio = NumericProperty(1)
    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = StringProperty(COLORS.white)
