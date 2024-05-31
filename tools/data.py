"""
Module with the class of the USER_DATA.
"""

###############
### Imports ###
###############

### Local imports ###

from tools.path import (
    PATH_USER_DATA
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#############
### Class ###
#############

class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)

    def save_changes(self) -> None:
        """
        Save the changes in the data.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the dictionary of data
        data = {}

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)
