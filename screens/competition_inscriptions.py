"""
Module to create the competition inscription screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
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


class CompetitionInscriptionsScreen(OlympeScreen):
    """
    Class to manage the competition inscriptions screen of the game.
    """

    dict_type_screen = {
        SCREEN_CUSTOM_TITLE: "edition",
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.team

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")
