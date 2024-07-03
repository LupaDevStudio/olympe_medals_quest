"""
Module to create the planification screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterWithNameLayout,
    CharacterInfoWithMainSportsLayout
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_CUSTOM_TITLE,
    GAME
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN_HEIGHT
)
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class PlanificationScreen(OlympeScreen):
    """
    Class to manage the planification screen of the game.
    """

    dict_type_screen = {
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    validate_label = StringProperty()
    spent_coins = NumericProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.planification
        self.validate_label = TEXT.general["validate"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")

    def ask_validate_planning(self):
        print("TODO ask validation planing")

    def validate_planning(self):
        print("TODO validate planning")
