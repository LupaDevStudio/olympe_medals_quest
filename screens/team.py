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


class TeamScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "team",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    team_title = StringProperty()
    grid_view = BooleanProperty(False) # detailed view by default
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
                athlete_button = CharacterWithNameLayout(
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    character_name=athlete.first_name,
                    size_hint=(None, None),
                    height=width,
                    width=width,
                    font_ratio=self.font_ratio,
                    release_function=partial(self.go_to_athlete, athlete)
                )

            # Display the characters in a list
            else:
                skills_dict = athlete.get_best_sports()
                height = self.font_ratio * (
                    BIG_HEADER_HEIGHT + len(skills_dict) * SKILL_HEIGHT + MARGIN_HEIGHT*2) 

                athlete_button = CharacterInfoWithMainSportsLayout(
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    title_card=athlete.first_name + "\n" + athlete.name,
                    salary=athlete.salary,
                    skills_dict=skills_dict,
                    font_ratio=self.font_ratio,
                    size_hint=(0.9, None),
                    height=height,
                    image_release_function=partial(self.go_to_athlete, athlete)
                )
            
            scrollview_layout.add_widget(athlete_button)

    def change_view_mode(self):
        self.grid_view = not self.grid_view

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def go_to_athlete(self, athlete: Athlete):
        self.go_to_next_screen(
            screen_name="athlete",
            next_dict_kwargs={"athlete": athlete}
        )

    def go_to_recruit(self):
        self.go_to_next_screen(screen_name="recruit")
