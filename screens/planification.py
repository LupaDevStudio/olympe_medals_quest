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
    PlanificationCard
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
    folded_dict = {}

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.planification
        self.validate_label = TEXT.general["validate"]
        self.header_text = my_text["planification"]

    def get_information_planification_card(self, athlete: Athlete):

        if self.folded_dict[athlete.id][0]:
            height = self.font_ratio * BIG_HEADER_HEIGHT

        else:
            height = self.font_ratio * (
                HEADER_HEIGHT + CHARACTER_HEIGHT + SKILL_HEIGHT + 3*MARGIN)

        return height

    def update_planification_card(self, athlete: Athlete):

        height = self.get_information_planification_card(athlete=athlete)

        self.folded_dict[athlete.id][1].height = height
        self.folded_dict[athlete.id][1].is_folded = self.folded_dict[athlete.id][0]

    def fill_scrollview(self):
        self.spent_coins = - self.GAME.get_trimester_gained_total_money()
        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in self.GAME.team:

            if athlete.id not in self.folded_dict:
                self.folded_dict[athlete.id] = [False, None]

            height = self.get_information_planification_card(athlete=athlete)

            athlete_card = PlanificationCard(
                font_ratio=self.font_ratio,
                size_hint=(SCROLLVIEW_WIDTH, None),
                height=height,
                is_folded=self.folded_dict[athlete.id][0],
                athlete=athlete,
                planification_unlocked="planification" in self.GAME.unlocked_modes,
                planification_release_function=partial(self.open_schedule_screen, athlete)
            )

            self.folded_dict[athlete.id][1] = athlete_card
            scrollview_layout.add_widget(athlete_card)

    def ask_redraw(self, widget):
        for athlete_id in self.folded_dict:
            if widget == self.folded_dict[athlete_id][1]:
                self.folded_dict[athlete_id][0] = not self.folded_dict[athlete_id][0]
                athlete: Athlete = self.GAME.get_athlete_from_id(athlete_id=athlete_id)
                self.update_planification_card(athlete=athlete)
                break
        
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
