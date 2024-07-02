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
from tools.constants import (
    TEXT,
    USER_DATA,
    SCREEN_CUSTOM_TITLE,
    SCREEN_BACK_ARROW
)

#############
### Class ###
#############


class SettingsScreen(OlympeScreen):
    """
    Class to manage the settings screen of the game.
    """

    dict_type_screen = {
        SCREEN_CUSTOM_TITLE : "settings",
        SCREEN_BACK_ARROW : "home"
    }

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)

    def change_language(self):
        # TODO
        code_language = "french"

        # Change the language and save it
        TEXT.change_language(code_language)
        USER_DATA.settings["language"] = code_language
        # TODO uncomment when function implemented
        # USER_DATA.save_changes()

        # Update the labels of the screen
        self.reload_language()
