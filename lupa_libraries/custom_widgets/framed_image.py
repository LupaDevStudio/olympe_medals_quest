"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty
)

### Local imports ###

from tools.graphics import(
    COLORS,
    BUTTON_LINE_WIDTH
)

#############
### Class ###
#############

class FramedImage(RelativeLayout):
    """
    An image with a frame around it.
    """

    ### Image settings ###

    image_source = StringProperty()
    fit_mode = StringProperty("contain")

    ### Colors ###

    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)
