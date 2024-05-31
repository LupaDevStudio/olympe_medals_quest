"""
Package to manage the screens of the application.
"""

###############
### Imports ###
###############

### Import the screens ###

from screens.home import HomeScreen
from screens.dialog import DialogScreen

### Reference dict to create the screens ###

SCREENS_DICT = {
    "home": HomeScreen,
    "dialog": DialogScreen
}
