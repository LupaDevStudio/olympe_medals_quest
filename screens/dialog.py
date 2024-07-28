"""
Module to create the dialog screen.
"""

###############
### Imports ###
###############

### Kivy properties ###

from kivy.clock import Clock
from kivy.properties import (
    StringProperty
)
from kivy.animation import Animation

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.constants import (
    DIALOGS_DICT,
    CHARACTERS_DICT,
    USER_DATA,
    TEXT,
    GAME,
    TALKING_SPEED_DICT
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from lupa_libraries.dialog_generator.dialog_layout import get_shake_animation

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    dialog_code: str
    dialog_frame_counter: int
    dialog_content_list: list

    ### Current dialog frame property ###

    character_name = StringProperty()
    character_title = StringProperty()
    character_image = StringProperty()
    dialog_text: str
    index_scrolling_label: int
    dialog_text_label = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.dialog_code = dict_kwargs["dialog_code"]
        self.next_screen = dict_kwargs["next_screen"]
        self.next_dict_kwargs = dict_kwargs["next_dict_kwargs"]

        # Reset the variables and start the dialog
        self.dialog_frame_counter = -1
        self.dialog_content_list = DIALOGS_DICT[TEXT.language][self.dialog_code]
        self.go_to_next_frame()

    def pass_current_frame(self):
        """
        Finish the display of the current frame or go to the next frame of the dialog.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Finish the display of the current frame if not finished
        if self.index_scrolling_label < len(self.dialog_text) + 1:
            Clock.unschedule(self.update_label)
            self.dialog_text_label = self.dialog_text
            self.index_scrolling_label = len(self.dialog_text) + 1

        # Go to the next frame if finished
        else:
            self.go_to_next_frame()

    def go_to_next_frame(self):
        """
        Go to the next dialog, by setting again the character details and dialog text.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.dialog_frame_counter += 1

        # Change screen if the dialog is finished
        if self.dialog_frame_counter == len(self.dialog_content_list):
            self.go_to_next_screen(
                screen_name=self.next_screen,
                current_dict_kwargs={
                    "dialog_code": self.dialog_code,
                    "next_screen": self.next_screen,
                    "next_dict_kwargs": self.next_dict_kwargs},
                next_dict_kwargs=self.next_dict_kwargs
            )
            return

        current_dialog_dict: dict = self.dialog_content_list[self.dialog_frame_counter]

        # Set the background of the screen
        # TODO faire une transition smooth entre les différents backgrounds
        background: str = current_dialog_dict["background"]
        if background == "sports_complex":
            path_background = GAME.get_background_image()
        else:
            path_background = PATH_BACKGROUNDS + f"{background}.jpg"
        self.set_back_image_path(
            back_image_path=path_background)

        # Set the character details
        character_id: str = current_dialog_dict["character"]
        expression: str = current_dialog_dict["expression"]
        self.character_image = PATH_CHARACTERS_IMAGES + \
            f"{character_id}/{expression}.png"

        # Hide the name and the title of the character if necessary
        mystery: bool = current_dialog_dict["mystery"]
        if mystery:
            self.character_title = "???"
            self.character_name = "???"
        else:
            self.character_name = CHARACTERS_DICT[TEXT.language][character_id]["name"]
            self.character_title = CHARACTERS_DICT[TEXT.language][character_id]["title"]

        # Set the content of the scrolling dialog
        self.dialog_text = current_dialog_dict["text"]
        self.dialog_text_label = ""
        self.index_scrolling_label = 0
        talking_speed = USER_DATA.settings["text_scrolling_speed"] / \
            TALKING_SPEED_DICT["characters"][character_id] / \
            TALKING_SPEED_DICT["emotions"][expression]
        Clock.schedule_interval(
            self.update_label, talking_speed)

        # Apply the animation if needed
        if "shake" in current_dialog_dict:
            shake_type = current_dialog_dict["shake"]
            shake_animation: Animation = get_shake_animation(
                self, shake_type=shake_type)
            shake_animation.start(self)

    def update_label(self, *args):
        """
        Update the content of the dialog to make it scroll.

        Parameters
        ----------
        *args : optional

        Returns
        -------
        None
        """
        self.index_scrolling_label += 1

        # End condition
        if self.index_scrolling_label == len(self.dialog_text) + 1:
            Clock.unschedule(self.update_label)
            return

        # Update the content of the label
        self.dialog_text_label = self.dialog_text[0:self.index_scrolling_label]
