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
    TEXT
)

#############
### Class ###
#############


class SettingsScreen(OlympeScreen):
    """
    Class to manage the settings screen of the game.
    """

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.png",
            **kw)

    def change_language(self):
        # TODO
        TEXT.change_language("french")
