"""
Module to create the team screen.
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
    OlympeScreen
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN,
    COLORS
)
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class SportsMenuScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON: "sports_menu",
        SCREEN_BACK_ARROW: "game",
        SCREEN_MONEY_RIGHT: True
    }
    sports_menu_title = StringProperty()

    strength_label = StringProperty()
    speed_label = StringProperty()
    technique_label = StringProperty()
    precision_label = StringProperty()
    charm_label = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.sports_menu
        self.sports_menu_title = my_text["title"]
        self.strength_label = TEXT.stats["strength"].upper()
        self.speed_label = TEXT.stats["speed"].upper()
        self.technique_label = TEXT.stats["technique"].upper()
        self.precision_label = TEXT.stats["precision"].upper()
        self.charm_label = TEXT.stats["charm"].upper()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.ids.sport_tree.build_tree(self.GAME.sports_unlocking_progress)

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")
