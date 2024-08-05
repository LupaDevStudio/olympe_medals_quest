"""
Module to create the dialog screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial


### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.constants import (
    DIALOGS_DICT,
    CHARACTERS_DICT,
    USER_DATA,
    TEXT,
    TALKING_SPEED_DICT
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.graphics import (
    COLOR_THOUGHT
)
from lupa_libraries.dialog_generator.dialog_layout import (
    get_shake_animation,
    DialogLayout
)

from tools import sound_mixer, music_mixer

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    def reload_kwargs(self, dict_kwargs):
        dialog_code = dict_kwargs["dialog_code"]
        next_screen = dict_kwargs["next_screen"]
        next_dict_kwargs = dict_kwargs["next_dict_kwargs"]

        on_dialog_end = partial(
            self.go_to_next_screen,
            screen_name=next_screen,
            current_dict_kwargs={
                "dialog_code": dialog_code,
                "next_screen": next_screen,
                "next_dict_kwargs": next_dict_kwargs},
            next_dict_kwargs=next_dict_kwargs
        )

        # Reset the variables and start the dialog
        self.dialog_frame_counter = -1
        self.dialog_content_list = DIALOGS_DICT[TEXT.language][dialog_code]

        dialog_layout: DialogLayout = self.ids.dialog_layout
        dialog_layout.reload(
            talking_speed=USER_DATA.settings["talking_speed"],
            on_dialog_end=on_dialog_end,
            color_thought=COLOR_THOUGHT,
            path_character_images=PATH_CHARACTERS_IMAGES,
            character_dict=CHARACTERS_DICT[TEXT.language],
            dialog_content_list=self.dialog_content_list,
            talking_speed_dict=TALKING_SPEED_DICT,
            sound_mixer=sound_mixer,
            music_mixer=music_mixer
        )

    def set_background(self, background: str):
        """
        Set the background of the screen to the given image.

        Parameters
        ----------
        background : str
            Name of the background to set.

        Returns
        -------
        """

        if background == "sports_complex":
            path_background = self.GAME.get_background_image()
        else:
            path_background = PATH_BACKGROUNDS + f"{background}.jpg"

        self.set_back_image_path(path_background)
