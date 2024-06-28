"""
Module to create the athlete screen.
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
    CharacterWithNameLayout
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
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


class AthleteScreen(OlympeScreen):
    """
    Class to manage the athlete screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "team",
        SCREEN_BACK_ARROW : "backwards",
        SCREEN_MONEY_RIGHT : True
    }
    athlete_title = StringProperty()
    team_label = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.athlete: Athlete = dict_kwargs["athlete"]
        self.athlete_title = self.athlete.first_name + " " + self.athlete.name

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.athlete

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
