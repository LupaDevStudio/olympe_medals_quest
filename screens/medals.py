"""
Module to create the medals screen.
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
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
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


class MedalsScreen(OlympeScreen):
    """
    Class to manage the medals screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "medals",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    medals_title = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.medals
        self.medals_title = my_text["title"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fille scrollview")
