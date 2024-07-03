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
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.home
        self.play_label = my_text["play"]

    def go_to_game(self):
        self.go_to_next_screen(
            screen_name="game"
        )

    def go_to_dialog(self):
        self.go_to_next_screen(
            screen_name="dialog",
            next_dict_kwargs={
                "dialog_code": "introduction",
                "next_screen": "home",
                "next_dict_kwargs": {}
            }
        )

    def go_to_planification(self):
        self.go_to_next_screen(screen_name="planification")

    def go_to_competition_inscriptions(self):
        self.go_to_next_screen(screen_name="competition_inscriptions")

    def go_to_settings(self):
        self.go_to_next_screen(screen_name="settings")
