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
    TEXT
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
            back_image_path=PATH_BACKGROUNDS + "office.png",
            **kw)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.reload_language()

    def reload_language(self):
        my_text = TEXT.home
        self.play_label = my_text["play"]

    def go_to_dialog(self):
        self.go_to_next_screen(
            screen_name="dialog",
            current_dict_kwargs={},
            next_dict_kwargs={
                "dialog_code": "introduction",
                "next_screen": "home",
                "next_dict_kwargs": {}
            }
        )

    def go_to_settings(self):
        self.go_to_next_screen(screen_name="settings")
