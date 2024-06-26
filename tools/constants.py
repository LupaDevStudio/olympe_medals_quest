"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

ANDROID_MODE : bool
    Whether the application is launched on mobile or not.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_LANGUAGE
)
from tools.basic_tools import (
    save_json_file,
    load_json_file
)
from tools.data_structures import (
    UserData,
    Game
)
from tools.language import (
    Text
)

#################
### Constants ###
#################

### Version ###

__version__ = "0.0.1"

### Mode ###

DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2

### Data loading ###

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "settings": {
            "sound_volume": 0.5,
            "music_volume": 0.5,
            "language": "english",
            "text_scrolling_speed": 0.03
        },
        "tutorial": {},
        "game": {}
    }
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the data of the user
USER_DATA = UserData()
GAME = USER_DATA.game

### Language ###

DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English"
}
DICT_LANGUAGE_NAME_TO_CODE = {
    "Français": "french",
    "English": "english"
}
LANGUAGES_LIST = tuple(DICT_LANGUAGE_CORRESPONDANCE.values())
TEXT = Text(language=USER_DATA.settings["language"])

### Game data ###

DIALOGS_DICT = {}
for language_code in DICT_LANGUAGE_CORRESPONDANCE:
    DIALOGS_DICT[language_code] = load_json_file(
        PATH_LANGUAGE + "dialogs_" + language_code + ".json")

CHARACTERS_DICT = {
    "olympe": {
        "name": "Olympe",
        "title": "Présidente de NOM PAYS"
    },
    "president_competition": {
        "name": "Président",
        "title": "Président de la compétition TODO"
    },
    "journalist": {
        "name": "Journaliste",
        "title": "Journaliste de NOM JOURNAL"
    }
}

### Screens ###

SCREEN_CUSTOM_TITLE = "custom_title"
SCREEN_TITLE_YEAR = "title_year"
SCREEN_TITLE_ICON = "title_icon"
SCREEN_MONEY_RIGHT = "money_right"
SCREEN_BACK_ARROW = "back_arrow"
