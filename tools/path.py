"""
Module to store all the paths used for the app files and folders
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy.utils import platform
from kivy.app import App

#################
### Constants ###
#################

ANDROID_MODE = platform == "android"
IOS_MODE = platform == "ios"

if ANDROID_MODE:
    from android.storage import app_storage_path  # pylint: disable=import-error # type: ignore
    PATH_APP_FOLDER = app_storage_path() + "/"
elif IOS_MODE:
    my_app = App()
    PATH_APP_FOLDER = my_app.user_data_dir
else:
    PATH_APP_FOLDER = "./"

# Path for the folders
PATH_RESOURCES = "resources/"

# Path for the user data
PATH_USER_DATA = PATH_APP_FOLDER + "data.json"

# Path for the screen
PATH_SCREENS = "screens/"

# Path for the resources
PATH_IMAGES = PATH_RESOURCES + "images/"
PATH_ICONS = PATH_IMAGES + "icons/"
PATH_CHARACTERS_IMAGES = PATH_IMAGES + "characters/"
PATH_BACKGROUNDS = PATH_IMAGES + "backgrounds/"
PATH_MEDALS = PATH_IMAGES + "medals/"
PATH_FONTS = PATH_RESOURCES + "fonts/"
PATH_DIALOGS_DICT = PATH_RESOURCES + "dialogs.json"

# Path for the fonts
PATH_TEXT_FONT = PATH_FONTS + "Oxanium-Bold.ttf"
PATH_TITLE_FONT = PATH_FONTS + "Oxanium-ExtraBold.ttf"
