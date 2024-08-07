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
    NumericProperty,
    ListProperty
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
    USER_DATA
)
from tools.graphics import (
    SKILL_HEIGHT
)
from tools.data_structures import (
    Athlete
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
    athlete_money_gain = NumericProperty()
    progression_label = StringProperty()
    change_text = StringProperty()
    fatigue_label = StringProperty()
    injury_label = StringProperty()
    activities_ids_list = ListProperty([])

    def reload_kwargs(self, dict_kwargs):
        self.athlete = dict_kwargs["athlete"]
        self.header_text = self.athlete.first_name + " " + self.athlete.name

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.schedule
        self.validate_label = TEXT.general["validate"]
        self.progression_label = my_text["progression"]
        self.change_text = my_text["change"]

    def reload_info(self):
        # Money
        self.spent_coins = - self.GAME.get_trimester_gained_total_money()
        self.athlete_money_gain = self.athlete.get_trimester_gained_money()

        self.fatigue_label = TEXT.general["fatigue_evolution"].replace(
            " : ", "\n").replace("@", str(self.athlete.fatigue)).replace("€", "10") # TODO
        self.injury_label = TEXT.general["injury_evolution"].replace(
            " : ", "\n").replace("@", "5") # TODO

        ### Stats ###

        stats_dict = self.athlete.stats
        sports_dict = self.athlete.sports
        athlete_skills = dict(stats_dict)
        athlete_skills.update(sports_dict)

        self.fill_stats_scrollview(athlete_skills=athlete_skills)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.bind(activities_ids_list=self.update_activities_label)
        self.activities_ids_list = self.athlete.current_planning
        self.reload_info()

    def update_activities_label(self, *args):
        self.ids.first_activity.text = TEXT.activities[self.activities_ids_list[0]]["name"]
        self.ids.second_activity.text = TEXT.activities[self.activities_ids_list[1]]["name"]
        self.ids.third_activity.text = TEXT.activities[self.activities_ids_list[2]]["name"]

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

        # update activities_ids_list[number_activity]

    def validate_planning(self):
        # Validate the new planning of the athlete
        self.athlete.current_planning = self.activities_ids_list
        USER_DATA.save_changes()

        self.go_to_next_screen(
            screen_name="planification",
            current_dict_kwargs={"athlete": self.athlete}
        )
