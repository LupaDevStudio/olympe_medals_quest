"""
Module to manage the dialogs.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd
from typing import Callable
from random import random
from math import pi, sin, cos

### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ColorProperty
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation, AnimationTransition
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_TITLE_FONT,
    PATH_BACKGROUNDS,
    PATH_MUSICS
)
from tools.graphics import (
    COLORS,
    FONTS_SIZES,
    BUTTON_LINE_WIDTH
)
from lupa_libraries.sound_manager import MusicMixer, load_sounds, DynamicMusicMixer

#################
### Constants ###
#################

__version__ = "1.0.0"

### Paths ###

CURRENT_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = os.path.join(CURRENT_FOLDER, "resources")
SOUNDS_EFFECT_FOLDER = os.path.join(RESOURCES_FOLDER, "sound_effects")

### Sounds ###

voice_dict = load_sounds(os.listdir(RESOURCES_FOLDER), RESOURCES_FOLDER, 0.3)
shake_sound_dict = load_sounds(os.listdir(
    SOUNDS_EFFECT_FOLDER), SOUNDS_EFFECT_FOLDER, 1)

VOICE_MIXER = MusicMixer(voice_dict)
SHAKE_SOUND_MIXER = MusicMixer(shake_sound_dict)

SHAKE_SOUND_EFFECTS = {
    "medium": "tchak",
    "strong": "bom",
    "weak": "pat"
}

# TEMP
BASE_SOUND_FILE = os.path.join(
    RESOURCES_FOLDER, "test_y_single.wav")
t_sound: Sound = SoundLoader.load(BASE_SOUND_FILE)


#################
### Functions ###
#################


def get_flash_animation(animation: Animation | None = None, number_blinks: int = 1, blink_delay: float = 0.1) -> Animation:

    # First flash
    new_animation = Animation(opacity=0,
                              transition="linear", duration=blink_delay / 2)
    new_animation += Animation(opacity=1,
                               transition="linear", duration=blink_delay / 2)

    for counter in range(number_blinks - 1):
        random_added_delay = rd.randint(0, 2) / 10
        new_animation += Animation(
            opacity=0,
            transition="linear",
            duration=(blink_delay + random_added_delay) / 2)
        new_animation += Animation(
            opacity=1,
            transition="linear",
            duration=(blink_delay + random_added_delay) / 2)

    if animation is None:
        animation = new_animation
    else:
        animation += new_animation

    return animation


def get_shake_animation(widget: Widget, shake_type: str) -> Animation:
    """
    Return a shake animation of the given type.

    Parameters
    ----------
    shake_type : str
        Type of shake animation.

    Returns
    -------
    kivy.Animation
    """
    # For flash animations
    if shake_type == "flash":
        return get_flash_animation(
            number_blinks=3,
            blink_delay=0.2)

    original_x = widget.x
    original_y = widget.y

    if shake_type == "strong":
        shake_distance = 20
        nb_shakes = 5
        shake_speed = 200  # in px per sec
    elif shake_type == "medium":
        shake_distance = 15
        nb_shakes = 4
        shake_speed = 150  # in px per sec
    elif shake_type in ["weak", "weak_no_sound"]:
        shake_distance = 10
        nb_shakes = 2
        shake_speed = 100  # in px per sec
    animation = None

    for i in range(nb_shakes):
        if i < nb_shakes - 1:
            # Shake in a random direction
            shake_angle = random() * 4 * pi - 2 * pi
            new_x = original_x + shake_distance * cos(shake_angle)
            new_y = original_y + shake_distance * sin(shake_angle)
        else:
            # Return to original position for the last shake
            new_x = original_x
            new_y = original_y
        new_animation = Animation(pos=(
            new_x, new_y), transition="in_out_back", duration=shake_distance / shake_speed)
        if animation is None:
            animation = new_animation
        else:
            animation += new_animation

        # Add blinking for strong shakes
        if shake_type == "strong":
            animation += get_flash_animation(animation=animation)

    return animation

#############
### Class ###
#############


class DialogLayout(RelativeLayout):

    mode = StringProperty("left")  # can be "left" or "right"

    ### Content ###

    character_name = StringProperty()
    character_title = StringProperty()
    character_image = StringProperty()
    text = StringProperty()

    ### Fonts ###

    font_size_character_name = NumericProperty(FONTS_SIZES.subtitle)
    font_size_character_title = NumericProperty(FONTS_SIZES.small_label)
    font_size_text = NumericProperty(FONTS_SIZES.label)
    font_ratio = NumericProperty(1)
    font_name_title = StringProperty(PATH_TITLE_FONT)
    font_name_text = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.dark_transparent_black)
    frame_color = ColorProperty(COLORS.white)

    frame_width = NumericProperty(BUTTON_LINE_WIDTH)

    ### Internal variables ###

    dialog_content_list: list[dict]

    def __init__(
            self,
            **kwargs):
        super().__init__(**kwargs)
        self.is_thinking = False

    def reload(
            self,
            on_dialog_end: Callable,
            color_thought: str | tuple,
            path_character_images: str,
            character_dict: dict,
            talking_speed: float,
            talking_speed_dict: dict,
            sound_mixer: DynamicMusicMixer,
            music_mixer: DynamicMusicMixer,
            dialog_content_list: list[dict]):
        """
        Reload all the necessary variables to play the dialog.

        Parameters
        ----------
        on_dialog_end : Callable
            Function called when the dialog is over.
        color_thought : str | tuple
            Color to use for the thoughts of the characters.
        path_character_images : str
            Path of the folder containing the character images.
        character_dict : dict
            Dictionary containing all the information about the characters.
        talking_speed : float
            Base scrolling speed of the text.
        sound_mixer : MusicMixer
            Class to play the sound effect of the dialog.
        dialog_content_list : list[dict]
            Content of the dialog.
        """

        self.dialog_frame_counter = -1
        self.dialog_content_list = dialog_content_list
        self.on_dialog_end = on_dialog_end
        self.path_character_images = path_character_images
        self.character_dict = character_dict
        self.talking_speed_base = talking_speed
        self.talking_speed_dict = talking_speed_dict
        self.color_thought = color_thought
        self.sound_mixer = sound_mixer
        self.music_mixer = music_mixer

        # Load the required musics for the dialog
        for dialog_dict in dialog_content_list:
            if "music" in dialog_dict:
                if dialog_dict["music"] not in music_mixer.musics:
                    sound_to_add = SoundLoader.load(os.path.join(
                        PATH_MUSICS, dialog_dict["music"] + ".mp3"))
                    music_mixer.add_sound(sound_to_add, dialog_dict["music"])

        self.go_to_next_frame()

    def format_text(self):
        # Insert thoughts in a different color
        self.dialog_text = self.dialog_text.replace(
            "(", f"[color={self.color_thought}](")
        self.dialog_text = self.dialog_text.replace(")", f")[/color]")

    def update_voice(self, *_):
        """
        Play the sound of the voice of the talking character.
        """

        # Extract the info
        current_dialog_dict: dict = self.dialog_content_list[self.dialog_frame_counter]
        if self.index_scrolling_label < len(self.dialog_text):
            current_letter = self.dialog_text[self.index_scrolling_label - 1]
        else:
            return
        character_id: str = current_dialog_dict["character"]
        voice_id = self.character_dict[character_id]["voice"]

        # Change voice if the character is thinking
        if self.is_thinking:
            voice_id = voice_id.replace("voice", "thoughts")

        # Extract the sound
        sound = VOICE_MIXER.musics[voice_id]

        # Play the sound
        if current_letter not in [" ", "."]:
            if current_letter in ["a", "e", "i", "o", "u", "y"]:
                sound.pitch = 1.
            else:
                sound.pitch = 0.8
            sound.play()

        if current_letter in [".", ",", "!"]:
            next_delay = self.voice_delay * 4
        else:
            next_delay = self.voice_delay

        if self.index_scrolling_label < len(self.dialog_text):
            Clock.schedule_once(
                self.update_voice, next_delay)

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
        # Update the display of the label
        if self.dialog_text[self.index_scrolling_label:self.index_scrolling_label + 14] == f"[color={self.color_thought}]":
            self.index_scrolling_label += 15
            self.is_thinking = True
        elif self.dialog_text[self.index_scrolling_label:self.index_scrolling_label + 8] == f"[/color]":
            self.index_scrolling_label += 9
            self.is_thinking = False
        else:
            self.index_scrolling_label += 1

        # Update the content of the label
        self.text = self.dialog_text[0:self.index_scrolling_label]

        if self.index_scrolling_label < len(self.dialog_text):
            current_letter = self.dialog_text[self.index_scrolling_label - 1]
        else:
            return
        if current_letter in [".", ",", "!"]:
            next_delay = self.text_delay * 4
        else:
            next_delay = self.text_delay

        # End condition
        if self.index_scrolling_label < len(self.dialog_text):
            Clock.schedule_once(
                self.update_label, next_delay)

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
            self.on_dialog_end()
            return

        current_dialog_dict: dict = self.dialog_content_list[self.dialog_frame_counter]

        # Set the background of the screen
        background: str = current_dialog_dict["background"]
        self.parent.set_background(background)

        # Get the mode of the current frame (card or simple dialog)
        mode = current_dialog_dict.get("mode", "")
        if mode == "card":

            card_type = current_dialog_dict["card_type"]

            if card_type == "first_athlete":
                self.parent.create_first_athlete_popup()

        else:

            # Set the character details
            character_id: str = current_dialog_dict["character"]
            character_id_for_image: str = character_id
            if character_id == "journalist":
                character_id_for_image = "ariane"
            elif character_id == "phil_coach":
                character_id_for_image = "phil"
            expression: str = current_dialog_dict.get("expression", "neutral")
            self.character_image = self.path_character_images + \
                f"{character_id_for_image}/{expression}.png"

            # Hide the name and the title of the character if necessary
            mystery: bool = current_dialog_dict.get("mystery", [False, False])
            if mystery[0]:
                self.character_name = "???"
            else:
                self.character_name = self.character_dict[character_id]["name"]
            if mystery[1]:
                self.character_title = "???"
            else:
                self.character_title = self.character_dict[character_id]["title"]

            # Set the content of the scrolling dialog
            self.dialog_text = current_dialog_dict["text"]
            self.format_text()
            self.text = ""
            self.index_scrolling_label = 0
            self.text_delay = 1 / self.talking_speed_base / \
                self.talking_speed_dict["characters"][character_id] / \
                self.talking_speed_dict["emotions"][expression]
            self.voice_delay = self.text_delay * 2
            Clock.schedule_once(
                self.update_label, self.text_delay)
            Clock.schedule_once(
                self.update_voice, self.text_delay)

            # Apply the animation if needed
            if "shake" in current_dialog_dict:
                shake_type = current_dialog_dict["shake"]
                shake_animation: Animation = get_shake_animation(
                    self.parent, shake_type=shake_type)
                shake_animation.start(self.parent)
                if shake_type in SHAKE_SOUND_EFFECTS:
                    SHAKE_SOUND_MIXER.play(SHAKE_SOUND_EFFECTS[shake_type])
                self.ids.next_button.press_button = False
                self.ids.next_button.disable_button = True
                shake_animation.on_complete = self.enable_next_button_when_completed

            # Play the sound effect if needed
            if "sound" in current_dialog_dict:
                sound_id = current_dialog_dict["sound"]
                self.sound_mixer.play(sound_id)

            # Play the music if needed
            if "music" in current_dialog_dict:
                music_id = current_dialog_dict["music"]
                self.music_mixer.play(music_id)

            if "volume" in current_dialog_dict:
                self.music_mixer.change_volume(
                    self.music_mixer.default_volume * current_dialog_dict["volume"])

    def enable_next_button_when_completed(self, *args):
        self.ids.next_button.disable_button = False

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

        # Reset variables
        self.sound_mixer.stop()
        self.is_thinking = False

        # Finish the display of the current frame if not finished
        if self.index_scrolling_label < len(self.dialog_text):
            # Clock.unschedule(self.update_label)
            self.text = self.dialog_text
            self.index_scrolling_label = len(self.dialog_text) + 1

        # Go to the next frame if finished
        else:
            self.go_to_next_frame()
