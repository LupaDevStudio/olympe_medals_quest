"""
Module to create the recruit screen.
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
    CharacterLayout
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    GAME
)
from tools.graphics import (
    SCROLLVIEW_WIDTH
)
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class RecruitScreen(OlympeScreen):
    """
    Class to manage the recruit screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR : True,
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    recruit_title = StringProperty()
    team_label = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.recruit

        self.team_label = my_text["team"]

        number_athletes_current = GAME.number_athletes
        if number_athletes_current <= 1:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athlete"]
        else:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athletes"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
