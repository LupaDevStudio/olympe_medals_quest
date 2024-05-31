"""
Module to create the dialog screen.
"""

###############
### Imports ###
###############

### Kivy properties ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    dialog_code = ""
    dialog_frame_counter = 0

    ### Current dialog frame property ###

    character_name = StringProperty("Olympe")
    character_title = StringProperty("Présidente")
    character_image = StringProperty(PATH_CHARACTERS_IMAGES + "Olympe/olympe_face_neutral.png")
    dialog_text = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.dialog_code = dict_kwargs["dialog_code"]
        self.dialog_frame_counter = 0
        # TODO update variables
        self.set_back_image_path(
            back_image_path=PATH_BACKGROUNDS + "sport_complex.png")
        self.dialog_text = "Je m'appelle Olympe.\n\nJe vais faire une très longue phrase pour que je puisse voir si cela loge bien dans le cadre, merci pour votre compréhension !"

    def next_dialog_frame(self):
        """
        Go to the next dialog, by setting again the character details and dialog text.
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.dialog_frame_counter += 1
        # TODO update with the dictionary
