"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

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
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class TeamScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR : True,
        SCREEN_BACK_ARROW : True,
        SCREEN_MONEY_RIGHT : True
    }
    team_title = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.team

        self.team_title = my_text["team_title"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in GAME.team:
            athlete_button = CharacterLayout(
                image_source=athlete.image,
                is_hurt=athlete.is_hurt,
                character_name=athlete.first_name,
                size_hint=(1/3, None),
                height=120*self.font_ratio,
                font_ratio=self.font_ratio,
                release_function=partial(self.go_to_athlete, athlete)
            )
            scrollview_layout.add_widget(athlete_button)

    def go_to_athlete(self, athlete: Athlete):
        print(athlete)
