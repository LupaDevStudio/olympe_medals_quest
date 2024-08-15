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
from screens.competition_inscriptions import CompetitionInscriptionsScreen
from screens.competition_results import CompetitionResultsScreen
from screens.competition_presentation import CompetitionPresentationScreen
from screens.planification import PlanificationScreen
from screens.sports_complex import SportsComplexScreen
from screens.sports_menu import SportsMenuScreen
from screens.activities_menu import ActivitiesMenuScreen
from screens.medals import MedalsScreen
from screens.schedule import ScheduleScreen
from screens.save import SaveScreen

### Reference dict to create the screens ###

SCREENS_DICT = {
    "home": HomeScreen,
    "dialog": DialogScreen,
    "settings": SettingsScreen,
    "game": GameScreen,
    "team": TeamScreen,
    "recruit": RecruitScreen,
    "athlete": AthleteScreen,
    "competition_inscriptions": CompetitionInscriptionsScreen,
    "competition_results": CompetitionResultsScreen,
    "competition_presentation": CompetitionPresentationScreen,
    "planification": PlanificationScreen,
    "sports_complex": SportsComplexScreen,
    "sports_menu": SportsMenuScreen,
    "activities_menu": ActivitiesMenuScreen,
    "medals": MedalsScreen,
    "schedule": ScheduleScreen,
    "save": SaveScreen
}
