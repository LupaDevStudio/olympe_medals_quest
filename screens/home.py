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

#############
### Class ###
#############


class HomeScreen(OlympeScreen):
    """
    Class to manage the home screen of the game.
    """

    def go_to_dialog(self):
        self.go_to_next_screen(
            screen_name="dialog",
            current_dict_kwargs={},
            next_dict_kwargs={
                "dialog_code": "test"
            }
        )
