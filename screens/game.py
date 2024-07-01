"""
Module to create the game screen.
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

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    PressedWithIconButton
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_ICONS
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    GAME,
    USER_DATA
)
from tools.olympe import (
    generate_athlete
)

#############
### Class ###
#############


class GameScreen(OlympeScreen):
    """
    Class to manage the game screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR: True,
        SCREEN_BACK_ARROW: "home",
        SCREEN_MONEY_RIGHT: True
    }
    launch_main_action_label = StringProperty()
    main_action = "plan"  # can be "plan" or "begin_competition"
    has_notifications_olympe = BooleanProperty(True)
    has_notifications_minister = BooleanProperty(False)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # TODO update the has_notifications depending if Olympe or the minister has notifications
        # TODO update main_action

        if self.has_notifications_olympe:
            self.ids.olympe_button.trigger_icon_flashing()
        if self.has_notifications_minister:
            self.ids.minister_button.trigger_icon_flashing()

        # TODO TEMP
        if GAME.team == []:
            first_athlete = generate_athlete()
            GAME.recruit_athlete(athlete=first_athlete)
            USER_DATA.save_changes()
        # TODO TEMP
        if GAME.medals == []:
            GAME.win_medal(
                sport_id="cheese_rolling",
                athlete_id=GAME.team[0].id,
                type="gold",
                edition=1
            )
            USER_DATA.save_changes()

    def on_enter(self, *args):
        super().on_enter(*args)

        self.fill_grid_layout()

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.game
        self.launch_main_action_label = self.my_text[self.main_action]

    def fill_grid_layout(self):
        # TODO insert in this list only the buttons unlocked depending on tutorial
        list_buttons = [
            "team",
            "recruit",
            "sports_complex",
            "sports_menu",
            "activities_menu",
            "medals",
            "shop"
        ]
        max_icons = 7
        max_lines = (max_icons // 2) + 1

        grid_layout = self.ids["grid_layout"]
        grid_layout.size_hint = (0.9, 0.45)
        grid_layout.padding = (0.05 * self.width, 20 * self.font_ratio)
        grid_layout.spacing = 20 * self.font_ratio
        height_button = (
            grid_layout.size_hint[1] * self.height - grid_layout.padding[1] * 2 - (max_lines - 1) * grid_layout.spacing[1]) // max_lines

        for element in list_buttons:

            pressed_button = PressedWithIconButton(
                icon_source=PATH_ICONS + element + ".png",
                text=self.my_text[element],
                font_ratio=self.font_ratio,
                release_function=partial(self.go_to_next_screen, element),
                size_hint=(0.45, None),
                height=height_button,
            )

            grid_layout.add_widget(pressed_button)

    def launch_main_action(self):
        if self.main_action == "plan":
            ...
            # TODO go to planning screen
        elif self.main_action == "begin_competition":
            ...
            # TODO go to competition

    def launch_dialog_olympe(self):
        print("TODO olympe")

    def launch_dialog_minister(self):
        print("TODO minister")

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.grid_layout.children[:]
        for element in list_widgets:
            self.ids.grid_layout.remove_widget(element)

        if self.has_notifications_olympe:
            self.ids.olympe_button.stop_icon_flashing()
        if self.has_notifications_minister:
            self.ids.minister_button.stop_icon_flashing()
