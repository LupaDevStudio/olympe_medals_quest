"""
Module to create an improved Kivy screen for Lemon Energy application.
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

from lupa_libraries.screen_manager import (
    ImprovedScreen
)
from tools.constants import (
    SCREEN_TITLE,
    SCREEN_BACK_ARROW
)
from tools.path import (
    PATH_BACKGROUNDS
)
from tools.graphics import (
    TOP_BAR_HEIGHT
)

#############
### Class ###
#############


class OlympeScreen(ImprovedScreen):
    """
    Improved screen class for Olympe's Medals Quest.
    """

    # Configuration of the main widgets
    dict_type_screen: dict = {}
    title_screen = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "sport_complex.png",
            **kw)
