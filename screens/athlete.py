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
    CharacterWithMainInfoFireLayout
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
    TEXT
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
        self.my_text = TEXT.athlete

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        ### Main information card ###

        is_hurt = self.athlete.is_hurt
        health = TEXT.injuries[self.athlete.health["type_injury"]]
        if is_hurt:
            time_absent = self.athlete.health["time_absent"]
            if time_absent > 1:
                health += " - " + time_absent + " " + TEXT.general["trimesters"].lower()
            else:
                health += " - " + time_absent + " " + TEXT.general["trimester"].lower()

        self.main_info_card = CharacterWithMainInfoFireLayout(
            image_source=self.athlete.image,
            salary=self.athlete.salary,
            age=self.my_text["age"].replace("@", str(self.athlete.age)),
            fatigue=self.my_text["fatigue"].replace("@", str(self.athlete.fatigue)),
            health=health,
            font_ratio=self.font_ratio,
            fire_text=self.my_text["fire"],
            is_hurt=is_hurt,
            fire_athlete_function=self.ask_fire_athlete,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=200*self.font_ratio
        )
        scrollview_layout.add_widget(self.main_info_card)

    def ask_fire_athlete(self):
        print("TODO")

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
