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
    PATH_USER_DATA
)
from tools.basic_tools import (
    save_json_file
)
from tools.manage_data import (
    UserData
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
    default_user_data = {}
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the data of the user
USER_DATA = UserData()

### Screens ###

SCREEN_TITLE = "title"
SCREEN_MONEY_RIGHT = "money_right"
SCREEN_BACK_ARROW = "back_arrow"
