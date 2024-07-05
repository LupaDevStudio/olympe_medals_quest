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
    PlanificationCard
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
        scrollview_layout = self.ids["scrollview_layout"]

        if self.athlete_folded_dict == {}:
            for athlete in GAME.team:
                self.athlete_folded_dict[athlete.id] = [False, None]

        athlete: Athlete
        for athlete in GAME.team:

            if self.athlete_folded_dict[athlete.id][0]:
                athlete_card = SmallPlanificationCard(
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=self.font_ratio * BIG_HEADER_HEIGHT,
                    title_card=athlete.first_name + "\n" + athlete.name,
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    total_price=abs(-1200), # TODO
                    minus_mode=True # TODO
                )

            else:
                height = self.font_ratio * (
                    HEADER_HEIGHT + CHARACTER_HEIGHT + SKILL_HEIGHT + 3*MARGIN_HEIGHT
                )

                athlete_card = PlanificationCard(
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=height,
                    title_card=athlete.first_name + " " + athlete.name,
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    total_price=abs(-1200), # TODO
                    minus_mode=True, # TODO
                    planning_text=TEXT.planification["planning"],
                    list_activities=[],
                    release_function=partial(self.open_planning_popup, athlete)
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

    def open_planning_popup(self, athlete: Athlete):
        print("Planning")

    def ask_validate_planning(self):
        print("TODO ask validation planing")

    def validate_planning(self):
        print("TODO validate planning")
