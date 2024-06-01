"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.path import (
    PATH_BACKGROUNDS
)

#############
### Class ###
#############


class HomeScreen(OlympeScreen):
    """
    Class to manage the home screen of the game.
    """

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.png",
            **kw)

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
        # TODO go to settings
        pass
