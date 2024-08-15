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
    ListProperty,
    BooleanProperty
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
    PATH_ICONS,
    PATH_BACKGROUNDS
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    USER_DATA,
    SHARED_DATA
)
from tools.data_structures import (
    Athlete
)
from tools.olympe import (
    generate_athlete,
    generate_and_add_first_athlete,
    EVENTS_DICT
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
        SCREEN_BACK_ARROW: "backwards",
        SCREEN_MONEY_RIGHT: True
    }
    launch_main_action_label = StringProperty()
    main_action = "plan"  # can be "plan" or "begin_competition_{mode}"
    our_country_label = StringProperty()
    notifications_list = ListProperty([])
    planification_unlocked = BooleanProperty(True)

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.game
        self.main_action = self.GAME.get_main_action()
        self.launch_main_action_label = self.my_text[self.main_action]
        self.our_country_label = TEXT.countries["our_country"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # # TODO TEMP
        # if self.GAME.recrutable_athletes == []:
        #     first_athlete = generate_athlete(GAME=self.GAME)
        #     self.GAME.update_recrutable_athletes(new_athletes_list=[first_athlete])
        #     USER_DATA.save_changes()

        # Update main_action
        self.main_action = self.GAME.get_main_action()
        
        # Fill the back space with all menus
        self.fill_grid_layout()

        # Update the list of notifications
        self.notifications_list = self.GAME.notifications_list
        self.ids.notification_button.trigger_icon_flashing()
        self.update_notification_panel()

    def go_backwards(self):
        self.GAME.set_last_time_played()
        USER_DATA.save_changes()
        self.go_to_next_screen(
            screen_name="save"
        )

    def update_notification_panel(self):

        # Update the notification panel
        if self.notifications_list != []:
            dialog_id = self.notifications_list[0]
            character = dialog_id.split("_")[0]
            self.ids.notification_button.image_source = PATH_CHARACTERS_IMAGES + \
                character + "/neutral.png"

        # Hide the planification button at the beginning of the story
        if self.GAME.year == 3 and self.GAME.trimester == 1:
            if len(self.notifications_list) > 0:
                if len(self.notifications_list) == 1:
                    self.set_back_image_path(self.GAME.get_background_image())
                # Olympe's office at the beginning of the story
                elif len(self.notifications_list) == 2:
                    self.set_back_image_path(PATH_BACKGROUNDS + "office.jpg")
                self.planification_unlocked = False
            else:
                self.planification_unlocked = True

    def fill_grid_layout(self):
        # Menus to display
        if SHARED_DATA.god_mode:
            list_buttons = ["team", "recruit", "sports_complex",
                "sports_menu", "activities_menu", "medals", "shop"]
        else:
            list_buttons = self.GAME.unlocked_menus

        max_icons = 7
        max_lines = (max_icons // 2) + 1

        grid_layout: GridLayout = self.ids["grid_layout"]
        grid_layout.size_hint = (0.9, 0.45)
        grid_layout.padding = (0.05 * self.width, 20 * self.font_ratio)
        grid_layout.spacing = (0.05 * self.width, 20 * self.font_ratio)
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
        elif "begin_competition" in self.main_action:
            self.go_to_next_screen(screen_name="competition_inscriptions")

    def launch_dialog(self):
        dialog_id = self.notifications_list[0]
        name_athlete = ""

        # Get the dict of details of the dialog
        story_events = EVENTS_DICT["story"]
        if dialog_id in story_events:
            dialog_dict = story_events[dialog_id]

            if "first_athlete" in dialog_dict["effects"] and self.GAME.team == []:
                generate_and_add_first_athlete(
                    GAME=self.GAME,
                    main_sport=self.GAME.first_sport)
        
            if "pass_athlete_name" in dialog_dict:
                if dialog_dict["pass_athlete_name"] == "first_athlete":
                    name_athlete = self.GAME.team[0].full_name

        self.go_to_next_screen(
            screen_name="dialog",
            next_dict_kwargs={
                "dialog_code": dialog_id,
                "name_athlete": name_athlete,
                "next_screen": "game",
                "next_dict_kwargs": {}
            }
        )

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.grid_layout.children[:]
        for element in list_widgets:
            self.ids.grid_layout.remove_widget(element)

        self.ids.notification_button.stop_icon_flashing()
