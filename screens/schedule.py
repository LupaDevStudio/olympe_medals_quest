"""
Module to create the schedule screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterSkillsLayout,
    OlympePlanificationPopup
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
    Athlete,
    Activity,
    Sport,
    SPORTS,
    ACTIVITIES
)
from tools.olympe import (
    get_activity_name_or_description,
    get_list_full_activity_ids
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

    fatigue_unlocked = BooleanProperty(False)
    injury_risk_unlocked = BooleanProperty(False)

    def reload_kwargs(self, dict_kwargs):
        self.athlete = dict_kwargs["athlete"]
        self.header_text = self.athlete.full_name

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
        athlete_skills = dict(reversed(list(stats_dict.items())))
        athlete_skills.update(sports_dict)

        # Reset scrollview
        self.ids.stats_scrollview_layout.reset_scrollview()
        # Fill scrollview
        self.fill_stats_scrollview(athlete_skills=athlete_skills)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.fatigue_unlocked = "fatigue" in self.GAME.unlocked_modes
        self.injury_risk_unlocked = "injury" in self.GAME.unlocked_modes

        self.bind(activities_ids_list=self.update_activities_label)
        self.activities_ids_list = self.athlete.current_planning
        self.reload_info()

    def update_activities_label(self, *args):
        self.ids.first_activity.text = get_activity_name_or_description(self.activities_ids_list[0])
        self.ids.second_activity.text = get_activity_name_or_description(self.activities_ids_list[1])
        self.ids.third_activity.text = get_activity_name_or_description(self.activities_ids_list[2])

    def fill_stats_scrollview(self, athlete_skills):
        scrollview_layout = self.ids.stats_scrollview_layout

        total_height = self.font_ratio * (
            SKILL_HEIGHT * len(athlete_skills)
        )

        gain_skills_dict = {}
        for counter_activity in range(len(self.athlete.current_planning)):
            activity_id: str = self.athlete.current_planning[counter_activity]
            activity: Activity = ACTIVITIES[activity_id]

            gain_stats_dict = activity.get_gain_stats(
                athlete=self.athlete,
                activity_pos_in_planning=counter_activity)
            for stat in gain_stats_dict:
                if stat not in gain_skills_dict:
                    gain_skills_dict[stat] = gain_stats_dict[stat]
                else:
                    gain_skills_dict[stat] += gain_stats_dict[stat]

            gain_sports_dict = activity.get_gain_sports(
                athlete=self.athlete,
                activity_pos_in_planning=counter_activity)

            for sport in gain_sports_dict:
                if sport not in gain_skills_dict:
                    gain_skills_dict[sport] = gain_sports_dict[sport]
                else:
                    gain_skills_dict[sport] += gain_sports_dict[sport]

        skills_layout = CharacterSkillsLayout(
            skills_dict=athlete_skills,
            gain_skills_dict=gain_skills_dict,
            font_ratio=self.font_ratio,
            pos_hint={"x": 0.05},
            size_hint=(0.9, None),
            height=total_height,
            show_level_up=True
        )

        scrollview_layout.add_widget(skills_layout)

    def change_first_activity(self):
        self.open_planning_popup(0)

    def change_second_activity(self):
        self.open_planning_popup(1)

    def change_third_activity(self):
        self.open_planning_popup(2)

    def open_planning_popup(self, number_activity: int):
        current_activity: Activity = ACTIVITIES[self.athlete.current_planning[number_activity]]
        current_activity_id = current_activity.id

        list_full_ids_activities = get_list_full_activity_ids(
            list_activities=self.GAME.unlocked_activities,
            list_sports=self.athlete.sports
        )

        popup = OlympePlanificationPopup(
            title=self.athlete.full_name,
            athlete=self.athlete,
            category_title=TEXT.schedule["category"],
            activity_title=TEXT.schedule["activity"],
            font_ratio=self.font_ratio,
            path_background=self.back_image_path,
            confirm_function=self.change_activity,
            number_activity=number_activity,
            code_values_category=self.GAME.unlocked_activity_categories,
            code_default_category=current_activity.category,
            all_unlocked_activities=list_full_ids_activities,
            code_default_activity=current_activity_id,
            create_message_popup_function=self.create_message_popup
        )
        popup.open()

    def change_activity(self, number_activity: int, activity_chosen: str):
        self.activities_ids_list[number_activity] = activity_chosen

        # Save the new activity
        self.athlete.current_planning = self.activities_ids_list
        USER_DATA.save_changes()

        # Change the display of the consequences of this new activity
        self.reload_info()

    def validate_planning(self):
        self.go_to_next_screen(
            screen_name="planification",
            current_dict_kwargs={"athlete": self.athlete}
        )
