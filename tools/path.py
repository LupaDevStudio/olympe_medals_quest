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
PATH_ATHLETES_IMAGES = PATH_APP_FOLDER + "athletes/"
# Create the directory if it does not exist
if not os.path.exists(PATH_ATHLETES_IMAGES):
    os.mkdir(PATH_ATHLETES_IMAGES)

# Path for the screen
PATH_SCREENS = "screens/"

# Path for the resources
PATH_IMAGES = PATH_RESOURCES + "images/"
PATH_ICONS = PATH_IMAGES + "icons/"
PATH_SPORTS_ICONS = PATH_ICONS + "sports/"
PATH_ACTIVITIES_ICONS = PATH_ICONS + "activities/"
PATH_CHARACTERS_IMAGES = PATH_IMAGES + "characters/"
PATH_BACKGROUNDS = PATH_IMAGES + "backgrounds/"
PATH_MEDALS_IMAGES = PATH_IMAGES + "medals/"
PATH_FLAGS_IMAGES = PATH_IMAGES + "flags/"

PATH_FONTS = PATH_RESOURCES + "fonts/"
PATH_SOUNDS = PATH_RESOURCES + "sounds/"
PATH_MUSICS = PATH_RESOURCES + "musics/"
PATH_COUNTRIES = PATH_RESOURCES + "countries.json"
PATH_SPORTS_COMPLEX_DICT = PATH_RESOURCES + "sports_complex.json"
PATH_TALKING_SPEED_DICT = PATH_RESOURCES + "talking_speed.json"
PATH_ROOMS_DICT = PATH_RESOURCES + "rooms.json"
PATH_SPORTS = PATH_RESOURCES + "sports.json"
PATH_ACTIVITIES = PATH_RESOURCES + "activities.json"

# Path for the languages
PATH_LANGUAGE = PATH_RESOURCES + "languages/"

# Path for the fonts
PATH_TEXT_FONT = PATH_FONTS + "Oxanium-Bold.ttf"
PATH_TITLE_FONT = PATH_FONTS + "Oxanium-ExtraBold.ttf"
