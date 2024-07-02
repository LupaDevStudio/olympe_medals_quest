"""
Module to create the money layout, with the amount and the unit icon.
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

from tools.constants import (
    TEXT
)
from tools.path import (
    PATH_TEXT_FONT,
    PATH_ICONS
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    RADIUS,
    BUTTON_LINE_WIDTH
)

#############
### Class ###
#############


class MoneyLayout(RelativeLayout):
    """
    A layout to display the money with the amount and the unit icon.
    """

    coins_count = NumericProperty(0)

    minus_mode = BooleanProperty(False)
    plus_mode = BooleanProperty(False)
    salary_mode = BooleanProperty(False)
    recruit_mode = BooleanProperty(False)
    line_mode = BooleanProperty(True)

    coins_count_text = StringProperty()
    coins_image_source = StringProperty(PATH_ICONS + "money.png")

    font_size = NumericProperty(FONTS_SIZES.coins_count)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_ratio = NumericProperty(1)

    color = ColorProperty(COLORS.white)
    radius = NumericProperty(RADIUS)
    line_width = NumericProperty(BUTTON_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.update_coins_count()
        self.bind(coins_count=self.update_coins_count)
        self.bind(minus_mode=self.update_coins_count)
        self.bind(plus_mode=self.update_coins_count)
        self.bind(salary_mode=self.update_coins_count)
        self.bind(recruit_mode=self.update_coins_count)

    def update_coins_count(self, *args):
        self.coins_count_text = ""
        if self.minus_mode:
            self.coins_count_text += "- "
        elif self.plus_mode:
            self.coins_count_text += "+ "
        elif self.salary_mode:
            self.coins_count_text += TEXT.general["salary"]
        elif self.recruit_mode:
            self.coins_count_text += TEXT.general["recruit"]
        if self.coins_count >= 1000:
            round_thousands = math.floor(self.coins_count / 1000)
            self.coins_count_text += str(round_thousands) + " k"
        else:
            self.coins_count_text += str(self.coins_count)
