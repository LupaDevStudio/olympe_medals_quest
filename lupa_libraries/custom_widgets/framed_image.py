"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty,
    BooleanProperty
)

### Local imports ###

from tools.graphics import(
    COLORS,
    BUTTON_LINE_WIDTH
)

#############
### Class ###
#############

class FramedImage(ButtonBehavior, RelativeLayout):
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

    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
