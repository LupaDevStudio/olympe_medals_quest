"""
Module to create the dialog screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    BooleanProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.constants import (
    DIALOGS_DICT,
    CHARACTERS_DICT,
    USER_DATA,
    TEXT,
    TALKING_SPEED_DICT,
    DEV_MODE,
    TALKING_SPEED
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.graphics import (
    COLOR_THOUGHT
)
from lupa_libraries.dialog_generator.dialog_layout import (
    DialogLayout
)
from tools import (
    sound_mixer,
    music_mixer
)
from tools.olympe import (
    launch_new_phase
)

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    dev_mode = BooleanProperty()

    def reload_kwargs(self, dict_kwargs):
        dialog_code = dict_kwargs["dialog_code"]
        next_screen = dict_kwargs["next_screen"]
        next_dict_kwargs = dict_kwargs["next_dict_kwargs"]

        on_dialog_end = partial(
            self.dialog_end_function,
            dialog_code,
            next_screen,
            next_dict_kwargs
        )

        # Reset the variables and start the dialog
        self.dialog_frame_counter = -1
        self.dialog_content_list = DIALOGS_DICT[TEXT.language][dialog_code]

        dialog_layout: DialogLayout = self.ids.dialog_layout
        dialog_layout.reload(
            talking_speed=TALKING_SPEED,
            on_dialog_end=on_dialog_end,
            color_thought=COLOR_THOUGHT,
            path_character_images=PATH_CHARACTERS_IMAGES,
            character_dict=CHARACTERS_DICT[TEXT.language],
            dialog_content_list=self.dialog_content_list,
            talking_speed_dict=TALKING_SPEED_DICT,
            sound_mixer=sound_mixer,
            music_mixer=music_mixer
        )

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.dev_mode = DEV_MODE

    def dialog_end_function(self, dialog_code, next_screen, next_dict_kwargs):

        USER_DATA.finish_dialog(dialog_code, self.manager.id_game)
        # Special case for the introduction
        if dialog_code == "introduction":
            launch_new_phase(GAME=self.GAME)

        USER_DATA.save_changes()
        self.go_to_next_screen(
            screen_name=next_screen,
            current_dict_kwargs={
                "dialog_code": dialog_code,
                "next_screen": next_screen,
                "next_dict_kwargs": next_dict_kwargs},
            next_dict_kwargs=next_dict_kwargs
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

    def skip_dialog(self):
        self.ids.dialog_layout.on_dialog_end()
