"""
Module to create a surrounded label.
"""

###############
### Imports ###
###############

### Python imports ###

import math

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    RADIUS
)

#############
### Class ###
#############


class SurroundedLabel(RelativeLayout):
    """
    A layout to display a label with a rounded rectangle line around.
    """

    text = StringProperty()

    font_size = NumericProperty(FONTS_SIZES.coins_count)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)

    color = ColorProperty(COLORS.white)
    radius = NumericProperty(RADIUS)
