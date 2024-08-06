"""
Module to create popups for the game.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import (
    BooleanProperty,
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty,
    ListProperty
)

### Local imports ###

from tools.constants import (
    TEXT
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    SCROLLVIEW_WIDTH,
    HEADER_HEIGHT,
    LARGE_LINE_WIDTH,
    BUTTON_LINE_WIDTH,
    SUBTITLE_HEIGHT,
    LABEL_HEIGHT,
    MEDAL_HEIGHT,
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN,
    BUTTON_HEIGHT
)
from tools.path import (
    PATH_TITLE_FONT,
    PATH_TEXT_FONT,
    PATH_BACKGROUNDS
)
from lupa_libraries.custom_widgets import (
    OlympeCard,
    SeparationLine
)

###############
### Classes ###
###############


class OlympePopup(Popup):
    # Colors
    true_background_color = ColorProperty(COLORS.transparent_black)
    border_color = ColorProperty(COLORS.white)
    path_background = StringProperty()

    popup_size_hint = ObjectProperty((SCROLLVIEW_WIDTH, 0.8))

    # Font
    font_color = ColorProperty(COLORS.white)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    title_font_name = StringProperty(PATH_TITLE_FONT)
    font_size = NumericProperty(FONTS_SIZES.subtitle)

    # Font ratio
    font_ratio = NumericProperty(1)

    # Width for the border
    border_width = NumericProperty(LARGE_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        black_background = OlympeCard(
            font_ratio=self.font_ratio,
            header_mode=True,
            size_hint=(None, None),
            size=(self.popup_size_hint[0]*Window.size[0], self.popup_size_hint[1]*Window.size[1]),
            x=(1-self.popup_size_hint[0])/2*Window.size[0],
            y=(1-self.popup_size_hint[1])/2*Window.size[1],
            header_text=self.title
        )
        self.ids.popup_layout.add_widget(black_background, 100)

        background_image = Image(
            source=self.path_background,
            size_hint=(None, None),
            size=Window.size,
            pos=(0, 0),
            fit_mode="cover"
        )
        self.ids.popup_layout.add_widget(background_image, 100)

        buttons_separation_line = SeparationLine(
            font_ratio=self.font_ratio,
            size_hint=(None, None),
            width=self.popup_size_hint[0]*Window.size[0]-16*self.font_ratio,
            x=((1-self.popup_size_hint[0])/2)*Window.size[0]+8*self.font_ratio,
            y=(1-self.popup_size_hint[1])/2*Window.size[1]+(BUTTON_HEIGHT+2*MARGIN)*self.font_ratio,
            line_width=LARGE_LINE_WIDTH
        )
        self.ids.popup_layout.add_widget(buttons_separation_line)

class OlympeMessagePopup(OlympePopup):
    """
    Class to create a popup with a message and a confirm button.
    """

    text = StringProperty()
    font_size_text = StringProperty(FONTS_SIZES.label)
    text_filling_ratio = NumericProperty(0.9)

    def __init__(self, confirm_function=lambda: 1 + 1, **kwargs):
        super().__init__(**kwargs)
        self.confirm_function = confirm_function

    def confirm(self):
        self.dismiss()
        self.confirm_function()
