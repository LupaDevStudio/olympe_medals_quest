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
    SCREEN_TITLE_YEAR
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

        # TODO
        athletes_list = ["Agathe", "Babou", "Gatho", "D", "E", "Miamour", "Paul", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C"]

        for athlete in athletes_list:
            athlete_button = CharacterLayout(
                image_source=PATH_CHARACTERS_IMAGES + "olympe/olympe_face_neutral.png", # TODO
                is_hurt=False, # TODO
                character_name=athlete, # TODO
                size_hint=(1/3, None),
                height=120*self.font_ratio,
                font_ratio=self.font_ratio,
                release_function=partial(self.go_to_athlete, athlete) # TODO id of the athlete
            )
            scrollview_layout.add_widget(athlete_button)

    def go_to_athlete(self, athlete_id: str):
        print(athlete_id)
