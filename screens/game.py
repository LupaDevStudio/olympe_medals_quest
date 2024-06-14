"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR
)

#############
### Class ###
#############


class GameScreen(OlympeScreen):
    """
    Class to manage the game screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR : True,
        SCREEN_BACK_ARROW : True,
        SCREEN_MONEY_RIGHT : True
    }

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.reload_language()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.game
