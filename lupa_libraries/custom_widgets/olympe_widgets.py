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

class OlympeCard(RelativeLayout):

    header_mode = BooleanProperty(False)
    icon_mode = BooleanProperty(False)

    header_height = NumericProperty(HEADER_HEIGHT)
    header_text = StringProperty()

    icon_source = StringProperty()
    icon_function = ObjectProperty(lambda: 1 + 1)

    font_ratio = NumericProperty(1)

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)
