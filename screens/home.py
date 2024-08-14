"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    TEXT,
    USER_DATA,
    DICT_LANGUAGE_NAME_TO_CODE,
    DICT_LANGUAGE_CODE_TO_NAME
)

#############
### Class ###
#############


class HomeScreen(OlympeScreen):
    """
    Class to manage the home screen of the game.
    """

    play_label = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)
        
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # Launch automatically the game the first time
        if USER_DATA.game_1 is None and USER_DATA.game_2 is None and USER_DATA.game_3 is None:
            # Choose the language
            self.create_spinner_popup(
                code="choose_language",
                default_value=DICT_LANGUAGE_CODE_TO_NAME[TEXT.language],
                values=list(DICT_LANGUAGE_NAME_TO_CODE.keys()),
                confirm_function=self.change_language_and_go_to_save)

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.home
        self.play_label = my_text["play"]

    def change_language_and_go_to_save(self, name_language: str, *args):
        # Get the code of the selected language
        code_language: str = DICT_LANGUAGE_NAME_TO_CODE[name_language]

        # Change the language and save it
        TEXT.change_language(code_language)
        USER_DATA.settings["language"] = code_language
        USER_DATA.save_changes()
        self.go_to_save()

    def go_to_save(self):
        self.go_to_next_screen(
            screen_name="save"
        )

    def go_to_competition_inscriptions(self):
        self.go_to_next_screen(screen_name="competition_inscriptions")

    def go_to_competition_results(self):
        self.go_to_next_screen(screen_name="competition_results")

    def go_to_settings(self):
        self.go_to_next_screen(screen_name="settings")
