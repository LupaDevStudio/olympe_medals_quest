"""
Module to create the competition results screen.
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
    SportLabelButton
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_CUSTOM_TITLE
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS
)
from tools.data_structures import (
    Athlete
)
from tools.path import (
    PATH_TITLE_FONT
)

#############
### Class ###
#############


class CompetitionResultsScreen(OlympeScreen):
    """
    Class to manage the competition results screen of the game.
    """

    dict_type_screen = {
        SCREEN_CUSTOM_TITLE: "edition",
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    previous_label = StringProperty()
    next_label = StringProperty()
    validate_label = StringProperty()
    list_sports = ListProperty([])
    selected_sport_id = NumericProperty(0)
    spent_coins = NumericProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.competition_results
        self.previous_label = TEXT.general["previous"]
        self.next_label = TEXT.general["next"]
        self.validate_label = TEXT.general["validate"]

        self.change_previous_next_buttons_text()

    def change_previous_next_buttons_text(self):
        if self.selected_sport_id == 0:
            self.ids.previous_button.opacity = 0
        else:
            self.ids.previous_button.opacity = 1
            self.ids.previous_button.text = self.previous_label

        if self.selected_sport_id == len(self.list_sports) - 1:
            self.ids.next_button.text = self.validate_label
        else:
            self.ids.next_button.text = self.next_label

    def on_pre_enter(self, *args):
        self.list_sports = self.GAME.unlocked_sports

        super().on_pre_enter(*args)

    def fill_scrollview_vertical(self):
        scrollview_layout = self.ids["scrollview_layout_vertical"]
        margin_label = 10
        total_label_width = 0

        for counter_sport in range(len(self.list_sports)):
            sport_id = self.list_sports[counter_sport]

            pos_x = self.font_ratio * (
                total_label_width + margin_label * (counter_sport+1))
            
            sport_name = TEXT.sports[sport_id]["name"]
            width_label = 11 * len(sport_name)
            if len(sport_name) <= 7:
                width_label += 8
            elif len(sport_name) >= 22:
                width_label -= 28
            elif len(sport_name) >= 17:
                width_label -= 15
            elif len(sport_name) >= 13:
                width_label -= 7
            number_long_letters = sport_name.count("m") + sport_name.count("w")
            if number_long_letters >= 2:
                width_label += 2.5 * number_long_letters
            total_label_width += width_label

            sport_button = SportLabelButton(
                text=sport_name,
                size_hint=(None, 1),
                x=pos_x,
                width=width_label*self.font_ratio,
                pos_hint={"center_y": 0.5},
                font_ratio=self.font_ratio,
                is_selected=counter_sport == self.selected_sport_id,
                release_function=partial(self.select_sport, counter_sport)
            )

            if counter_sport == self.selected_sport_id:
                self.ids.scrollview_vertical.scroll_to(sport_button)

            scrollview_layout.add_widget(sport_button)

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        print("TODO fill scrollview")

    def reset_screen(self):
        # Reset scrollviews
        self.ids.scrollview_layout.reset_scrollview()
        self.ids.scrollview_layout_vertical.reset_scrollview()

        # Rebuild scrollviews
        self.fill_scrollview_vertical()
        self.fill_scrollview()
    
    def select_sport(self, sport_counter):
        self.selected_sport_id = sport_counter
        self.reset_screen()

    def go_to_previous_sport(self):
        if self.selected_sport_id != 0:
            self.selected_sport_id -= 1
            self.change_previous_next_buttons_text()
            self.reset_screen()

    def go_to_next_sport(self):
        if self.selected_sport_id != len(self.list_sports) - 1:
            self.selected_sport_id += 1
            self.change_previous_next_buttons_text()
            self.reset_screen()
        else:
            ... # TODO validate
