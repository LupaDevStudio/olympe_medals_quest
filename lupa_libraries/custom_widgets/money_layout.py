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
    spent_coins_count = NumericProperty(0)

    minus_mode = BooleanProperty(False)
    plus_mode = BooleanProperty(False)
    salary_mode = BooleanProperty(False)
    recruit_mode = BooleanProperty(False)
    spend_mode = BooleanProperty(False)
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
        self.bind(spend_mode=self.update_coins_count)
        self.bind(spent_coins_count=self.update_coins_count)

    def update_coins_count(self, *args):
        self.coins_count_text = ""

        # Text before the amount of money
        if self.minus_mode:
            self.coins_count_text += "- "
        elif self.plus_mode:
            self.coins_count_text += "+ "
        elif self.salary_mode:
            self.coins_count_text += TEXT.general["salary"]
        elif self.recruit_mode:
            self.coins_count_text += TEXT.general["recruit"]

        if self.spend_mode:
            previous_count = self.coins_count
            if previous_count >= 1000:
                round_thousands = math.floor(self.coins_count / 1000)
                previous_text = str(round_thousands) + " k"
            else:
                round_number = math.floor(previous_count)
                previous_text = str(round_number)

            next_count = self.coins_count - self.spent_coins_count
            if next_count >= 1000:
                round_thousands = math.floor(next_count / 1000)
                next_text = str(round_thousands) + " k"
            else:
                round_number = math.floor(next_count)
                next_text = str(round_number)

            self.coins_count_text += previous_text + " -> " + next_text
        else:
            if self.coins_count >= 1000000:
                round_thousands = math.floor(self.coins_count / 1000)
                self.coins_count_text += str(round_thousands) + " k"
            elif self.coins_count >= 1000:
                round_thousands = str(round(self.coins_count / 1000, ndigits=1))
                if round_thousands[-1] == "0" and len(round_thousands) > 3:
                    round_thousands = round_thousands[:-2]
                self.coins_count_text += str(round_thousands) + " k"
            else:
                round_number = math.floor(self.coins_count)
                self.coins_count_text += str(round_number)
