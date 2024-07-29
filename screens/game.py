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
    ListProperty
)
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    PressedWithIconButton
)
from tools.path import (
    PATH_CHARACTERS_IMAGES,
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
    generate_athlete,
    generate_and_add_first_athlete,
    launch_new_phase
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
    main_action = "plan"  # can be "plan" or "begin_competition_{mode}"
    our_country_label = StringProperty()
    notifications_list = ListProperty([])

    def reload_kwargs(self, dict_kwargs: dict):
        has_seen_notification = dict_kwargs.get("has_seen_notification", False)
        
        if has_seen_notification:
            # Remove the notification once seen in GAME
            # TODO self.notifications_list.remove(self.notifications_list[0])
            pass

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.game
        self.launch_main_action_label = self.my_text[self.main_action]
        self.our_country_label = TEXT.countries["our_country"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # TODO update the notifications_list depending if one of the characters has something to say
        self.notifications_list = [
            ["olympe", "introduction"]
        ]
        # Update main_action
        self.main_action = GAME.get_main_action()

        self.ids.notification_button.trigger_icon_flashing()

        # TODO TEMP
        if GAME.team == []:
            generate_and_add_first_athlete(main_sport="cheese_rolling")
        # TODO TEMP
        if GAME.recrutable_athletes == []:
            first_athlete = generate_athlete()
            GAME.update_recrutable_athletes(new_athletes_list=[first_athlete])
            USER_DATA.save_changes()
        self.fill_grid_layout()

        self.update_notification_panel()

    def update_notification_panel(self):

        # Update the notification panel
        if self.notifications_list != []:
            character = self.notifications_list[0][0]
            self.ids.notification_button.image_source = PATH_CHARACTERS_IMAGES + \
                character + "/neutral.png"

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

        grid_layout: GridLayout = self.ids["grid_layout"]
        grid_layout.size_hint = (0.9, 0.45)
        grid_layout.padding = (0.05 * self.width, 20 * self.font_ratio)
        grid_layout.spacing = 20 * self.font_ratio
        height_button = (
            grid_layout.size_hint[1] * Window.size[1] - grid_layout.padding[1] * 2 - (max_lines - 1) * grid_layout.spacing[1]) // max_lines

        for element in list_buttons:

            pressed_button = PressedWithIconButton(
                icon_source=PATH_ICONS + element + ".png",
                text=self.my_text[element],
                font_ratio=self.font_ratio,
                release_function=partial(self.go_to_next_screen, element),
                size_hint=(0.4, None),
                height=height_button,
            )

            grid_layout.add_widget(pressed_button)

    def launch_main_action(self):
        if self.main_action == "plan":
            self.go_to_next_screen(screen_name="planification")
        elif self.main_action == "begin_competition":
            self.go_to_next_screen(screen_name="competition_inscriptions")

    def launch_dialog(self):
        event = self.notifications_list[0]
        dialog_id = event[1]

        self.go_to_next_screen(
            screen_name="dialog",
            next_dict_kwargs={
                "dialog_code": dialog_id,
                "next_screen": "game",
                "next_dict_kwargs": {
                    "has_seen_notification": True
                }
            }
        )


    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.grid_layout.children[:]
        for element in list_widgets:
            self.ids.grid_layout.remove_widget(element)

        self.ids.notification_button.stop_icon_flashing()
