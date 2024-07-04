"""
Module with the class of the TEXT.
"""

###############
### Imports ###
###############

### Local imports ###

from tools.basic_tools import (
    load_json_file
)
from tools.path import (
    PATH_LANGUAGE
)

#############
### Class ###
#############

class Text():
    def __init__(self, language) -> None:
        self.language = language
        self.change_language(language)

    def change_language(self, language):
        """
        Change the language of the text contained in the class.

        Parameters
        ----------
        language : str
            Code of the desired language.

        Returns
        -------
        None
        """
        # Change the language
        self.language = language

        # Load the json file
        data = load_json_file(PATH_LANGUAGE + language + ".json")

        # Split the text contained in the screens
        self.home = data["home"]
        self.game = data["game"]
        self.sports_complex = data["sports_complex"]
        self.planification = data["planification"]
        self.team = data["team"]
        self.athlete = data["athlete"]
        self.settings = data["settings"]
        self.sports_menu = data["sports_menu"]
        self.activities_menu = data["activities_menu"]
        self.competition_results = data["competition_results"]
        self.competition_inscriptions = data["competition_inscriptions"]
        self.recruit = data["recruit"]

        self.general = data["general"]
        self.injuries = data["injuries"]
        self.sports = data["sports"]
        self.countries = data["countries"]
        self.stats = data["stats"]
        self.rooms = data["rooms"]
        self.activities = data["activities"]

        self.tutorial = data["tutorial"]
        self.popup = data["popup"]
