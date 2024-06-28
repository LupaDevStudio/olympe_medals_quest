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


class TeamScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR : True,
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    team_title = StringProperty()
    grid_view = BooleanProperty(True) # TODO change to False
    recruit_label = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.team

        self.recruit_label = my_text["recruit"]

        number_athletes_current = GAME.number_athletes
        if number_athletes_current <= 1:
            self.team_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athlete"]
        else:
            self.team_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athletes"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in GAME.team:

            # Display the characters in a grid
            if self.grid_view:
                width = (Window.size[0]*SCROLLVIEW_WIDTH - \
                    2*scrollview_layout.spacing[0] - \
                    2*scrollview_layout.padding[0]) / 3
                athlete_button = CharacterLayout(
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    character_name=athlete.first_name,
                    size_hint=(None, None),
                    height=width,
                    width=width,
                    font_ratio=self.font_ratio,
                    release_function=partial(self.go_to_athlete, athlete)
                )
                scrollview_layout.add_widget(athlete_button)

            # Display the characters in a list
            else:
                # TODO
                ...

    def change_view_mode(self):
        self.grid_view = not self.grid_view

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def go_to_athlete(self, athlete: Athlete):
        print(athlete)

    def go_to_recruit(self):
        self.go_to_next_screen(screen_name="recruit")
