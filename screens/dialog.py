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
    launch_new_phase,
    finish_dialog
)

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    dialog_code = ""
    name_athlete = ""
    dev_mode = BooleanProperty()

    def reload_kwargs(self, dict_kwargs):
        self.dialog_code = dict_kwargs["dialog_code"]
        next_screen = dict_kwargs["next_screen"]
        next_dict_kwargs = dict_kwargs["next_dict_kwargs"]
        self.name_athlete = dict_kwargs.get("name_athlete", "")

        self.on_dialog_end = partial(
            self.dialog_end_function,
            self.dialog_code,
            next_screen,
            next_dict_kwargs
        )

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.dev_mode = DEV_MODE

        # Reset the variables and start the dialog
        self.dialog_frame_counter = -1
        self.dialog_content_list = DIALOGS_DICT[TEXT.language][self.dialog_code]
        self.post_treat_dialog_text()

        dialog_layout: DialogLayout = self.ids.dialog_layout
        dialog_layout.reload(
            talking_speed=TALKING_SPEED,
            on_dialog_end=self.on_dialog_end,
            color_thought=COLOR_THOUGHT,
            path_character_images=PATH_CHARACTERS_IMAGES,
            character_dict=CHARACTERS_DICT[TEXT.language],
            dialog_content_list=self.dialog_content_list,
            talking_speed_dict=TALKING_SPEED_DICT,
            sound_mixer=sound_mixer,
            music_mixer=music_mixer
        )

    def post_treat_dialog_text(self):
        # Replace the between [] codes by their true value
        for counter_frame in range(len(self.dialog_content_list)):
            frame = self.dialog_content_list[counter_frame]

            # First sport of category 1
            if "[NEW_SPORT]" in frame["text"]:
                self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                    "[NEW_SPORT]", TEXT.sports[self.GAME.first_sport]["name"].lower())
            
            # Corresponding athlete
            if "[NAME_ATHLETE]" in frame["text"]:
                self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                    "[NAME_ATHLETE]", self.name_athlete)

    def dialog_end_function(self, dialog_code, next_screen, next_dict_kwargs):

        finish_dialog(GAME=self.GAME, dialog_code=dialog_code)

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
