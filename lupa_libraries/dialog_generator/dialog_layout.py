"""
Module to manage the dialogs.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ColorProperty
)
from kivy.uix.relativelayout import RelativeLayout

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_TITLE_FONT
)
from tools.graphics import (
    COLORS,
    FONTS_SIZES,
    BUTTON_LINE_WIDTH
)

#############
### Class ###
#############

class DialogLayout(RelativeLayout):

    mode = StringProperty("left") # can be "left" or "right"

    ### Content ###

    character_name = StringProperty()
    character_title = StringProperty()
    character_image = StringProperty()
    text = StringProperty()

    ### Fonts ###

    font_size_title = NumericProperty(FONTS_SIZES.subtitle)
    font_size_text = NumericProperty(FONTS_SIZES.label)
    font_ratio = NumericProperty(1)
    font_name_title = StringProperty(PATH_TITLE_FONT)
    font_name_text = StringProperty(PATH_TEXT_FONT)
    
    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.dark_transparent_black)
    frame_color = ColorProperty(COLORS.white)
    
    frame_width = NumericProperty(BUTTON_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
