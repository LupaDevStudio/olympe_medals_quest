"""
Module to create the schedule screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterSkillsLayout
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_CUSTOM_TITLE,
    GAME
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    HEADER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN_HEIGHT
)
from tools.data_structures import (
    Athlete
)
from tools.path import (
    PATH_ICONS
)

#############
### Class ###
#############


class ScheduleScreen(OlympeScreen):
    """
    Class to manage the schedule screen of the game (for one athlete).
    """

    dict_type_screen = {
        SCREEN_BACK_ARROW : "backwards",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    athlete: Athlete
    validate_label = StringProperty()
    header_text = StringProperty()
    spent_coins = NumericProperty()
    spent_coins_for_athlete = NumericProperty()
    progression_label = StringProperty()
    change_text = StringProperty()
    fatigue_label = StringProperty()
    injury_label = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.athlete = dict_kwargs["athlete"]
        self.header_text = self.athlete.first_name + " " + self.athlete.name

        self.reload_info()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.schedule
        self.validate_label = TEXT.general["validate"]
        self.progression_label = my_text["progression"]
        self.change_text = my_text["change"]

    def reload_info(self):
        self.fatigue_label = TEXT.general["fatigue_evolution"].replace(
            " : ", "\n").replace("@", "5").replace("€", "10") # TODO
        self.injury_label = TEXT.general["injury_evolution"].replace(
            " : ", "\n").replace("@", "5") # TODO

        ### Stats ###

        stats_dict = self.athlete.stats
        sports_dict = self.athlete.sports
        athlete_skills = dict(stats_dict)
        athlete_skills.update(sports_dict)

        self.fill_stats_scrollview(athlete_skills=athlete_skills)

    def fill_stats_scrollview(self, athlete_skills):
        scrollview_layout = self.ids.stats_scrollview_layout

        total_height = self.font_ratio * (
            SKILL_HEIGHT * len(athlete_skills)
        )

        skills_layout = CharacterSkillsLayout(
            skills_dict=athlete_skills,
            font_ratio=self.font_ratio,
            pos_hint={"x": 0.05},
            size_hint=(0.9, None),
            height=total_height,
            show_level_up=True
        )

        scrollview_layout.add_widget(skills_layout)

    def change_first_activity(self):
        self.open_planning_popup(1)

    def change_second_activity(self):
        self.open_planning_popup(2)

    def change_third_activity(self):
        self.open_planning_popup(3)

    def open_planning_popup(self, number_activity: int):
        print("Planning")

    def validate_planning(self):
        print("TODO validate planning")
        self.go_to_next_screen(
            screen_name="planification",
            current_dict_kwargs={"athlete": self.athlete}
        )
