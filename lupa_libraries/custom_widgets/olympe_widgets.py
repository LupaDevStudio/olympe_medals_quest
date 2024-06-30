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
    PATH_TITLE_FONT,
    PATH_ICONS
)

#############
### Class ###
#############

class OlympeCard(RelativeLayout):

    header_mode = BooleanProperty(False)
    icon_mode = BooleanProperty(False)
    foldable_mode = BooleanProperty(False)
    is_folded = BooleanProperty(False)

    header_height = NumericProperty(HEADER_HEIGHT)
    header_text = StringProperty()

    icon_source = StringProperty()
    icon_function = ObjectProperty(lambda: 1 + 1)

    font_ratio = NumericProperty(1)
    background_size = ObjectProperty()

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.bind(foldable_mode=self.apply_foldable_mode)
        self.bind(is_folded=self.apply_foldable_mode)

    def apply_foldable_mode(self, *args):
        if self.foldable_mode:
            self.icon_mode = True
            if self.is_folded:
                self.icon_source = PATH_ICONS + "plus.png"
            else:
                self.icon_source = PATH_ICONS + "minus.png"
            self.icon_function = self.ask_redraw
    
    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)