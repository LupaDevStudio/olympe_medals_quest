"""
Package to manage the screens of the application.
"""

###############
### Imports ###
###############

### Import the screens ###

from screens.home import HomeScreen
from screens.dialog import DialogScreen
from screens.settings import SettingsScreen
from screens.game import GameScreen
from screens.team import TeamScreen
from screens.recruit import RecruitScreen
from screens.athlete import AthleteScreen

### Reference dict to create the screens ###

SCREENS_DICT = {
    "home": HomeScreen,
    "dialog": DialogScreen,
    "settings": SettingsScreen,
    "game": GameScreen,
    "team": TeamScreen,
    "recruit": RecruitScreen,
    "athlete": AthleteScreen
}
