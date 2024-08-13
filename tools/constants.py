"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_LANGUAGE,
    PATH_TALKING_SPEED_DICT
)
from tools.basic_tools import (
    save_json_file,
    load_json_file
)
from tools.data_structures import (
    UserData
)
from tools.language import (
    Text
)

#################
### Constants ###
#################

### Version ###

__version__ = "0.0.7"

### Mode ###

GOD_MODE = True # Change this value
if GOD_MODE:
    DEV_MODE = True
else:
    DEV_MODE = True # Change this value
FPS = 30
MSAA_LEVEL = 2

### Data loading ###

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "settings": {
            "sound_volume": 0.5,
            "music_volume": 0.3,
            "language": "english"
        }
    }
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the data of the user
USER_DATA = UserData()

class SharedData():
    id_game: int # 1, 2, 3
    
    @property
    def GAME(self):
        if self.id_game == 1:
            return USER_DATA.game_1
        elif self.id_game == 2:
            return USER_DATA.game_2
        else:
            return USER_DATA.game_3

    def __init__(self, id_game: int = 1) -> None:
        self.id_game = id_game

SHARED_DATA = SharedData()

### Language ###

DICT_LANGUAGE_CODE_TO_NAME = {
    "french": "Français",
    "english": "English"
}
DICT_LANGUAGE_NAME_TO_CODE = {
    "Français": "french",
    "English": "english"
}
LANGUAGES_LIST = tuple(DICT_LANGUAGE_CODE_TO_NAME.values())
TEXT = Text(language=USER_DATA.settings["language"])

### Game data ###

DIALOGS_DICT = {}
for language_code in DICT_LANGUAGE_CODE_TO_NAME:
    DIALOGS_DICT[language_code] = load_json_file(
        PATH_LANGUAGE + "dialogs_" + language_code + ".json")

CHARACTERS_DICT = {}
for language_code in DICT_LANGUAGE_CODE_TO_NAME:
    CHARACTERS_DICT[language_code] = load_json_file(
        PATH_LANGUAGE + "characters_" + language_code + ".json")

TALKING_SPEED = 35
TALKING_SPEED_DICT = load_json_file(PATH_TALKING_SPEED_DICT)

### Screens ###

SCREEN_CUSTOM_TITLE = "custom_title"
SCREEN_TITLE_YEAR = "title_year"
SCREEN_TITLE_ICON = "title_icon"
SCREEN_MONEY_RIGHT = "money_right"
SCREEN_SPEND_MONEY_RIGHT = "spend_money_right"
SCREEN_BACK_ARROW = "back_arrow"
