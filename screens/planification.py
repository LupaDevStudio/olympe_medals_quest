"""
Module to create the planification screen.
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
    SmallPlanificationCard,
    CompletePlanificationCard
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    HEADER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN
)
from tools.data_structures import (
    Athlete
)
from tools.olympe import (
    launch_new_phase
)

#############
### Class ###
#############


class PlanificationScreen(OlympeScreen):
    """
    Class to manage the planification screen of the game.
    """

    dict_type_screen = {
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    validate_label = StringProperty()
    spent_coins = NumericProperty()
    header_text = StringProperty()
    athlete_folded_dict = {}

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.planification
        self.validate_label = TEXT.general["validate"]
        self.header_text = my_text["planification"]

    def fill_scrollview(self):
        self.spent_coins = - self.GAME.get_trimester_gained_total_money()
        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in self.GAME.team:
            trimester_gain = athlete.get_trimester_gained_money()

            if athlete.id not in self.athlete_folded_dict:
                self.athlete_folded_dict[athlete.id] = [False, None]

            if self.athlete_folded_dict[athlete.id][0]:
                athlete_card = SmallPlanificationCard(
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=self.font_ratio * BIG_HEADER_HEIGHT,
                    title_card=athlete.first_name + "\n" + athlete.name,
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    total_price=abs(trimester_gain),
                    minus_mode=trimester_gain < 0
                )

            else:
                height = self.font_ratio * (
                    HEADER_HEIGHT + CHARACTER_HEIGHT + SKILL_HEIGHT + 3*MARGIN
                )

                list_activities_label = []
                for activity_id in athlete.current_planning:
                    list_activities_label.append(TEXT.activities[activity_id]["name"])

                athlete_card = CompletePlanificationCard(
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=height,
                    title_card=athlete.first_name + " " + athlete.name,
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    total_price=abs(trimester_gain),
                    minus_mode=trimester_gain < 0,
                    planning_text=TEXT.planification["planning"],
                    list_activities=list_activities_label,
                    release_function=partial(self.open_schedule_screen, athlete)
                )

            self.athlete_folded_dict[athlete.id][1] = athlete_card
            scrollview_layout.add_widget(athlete_card)

    def ask_redraw(self, widget):
        for athlete_id in self.athlete_folded_dict:
            if widget == self.athlete_folded_dict[athlete_id][1]:
                self.athlete_folded_dict[athlete_id][0] = not self.athlete_folded_dict[athlete_id][0]
                break
        
        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def open_schedule_screen(self, athlete: Athlete):
        self.go_to_next_screen(
            screen_name="schedule",
            next_dict_kwargs={"athlete": athlete}
        )

    def ask_validate_planning(self):
        self.create_yes_no_popup(
            code="validate_planning",
            confirm_function=self.validate_planning
        )

    def validate_planning(self):
        launch_new_phase(GAME=self.GAME)
        self.go_to_next_screen(
            screen_name="game"
        )
