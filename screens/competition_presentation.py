"""
Module to create the competition presentation screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    BooleanProperty,
    StringProperty
)
from kivy.clock import Clock

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from lupa_libraries.dialog_generator.dialog_layout import (
    VOICE_MIXER
)
from tools.constants import (
    TEXT,
    DEV_MODE,
    TALKING_SPEED
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_SOUNDS
)
from tools import (
    sound_mixer,
    music_mixer
)


#############
### Class ###
#############


class CompetitionPresentationScreen(OlympeScreen):
    """
    Class to manage the screen of the results presentation of the game.
    """

    dev_mode = BooleanProperty()
    text = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "stadium.jpg",
            **kw)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.dev_mode = DEV_MODE

        self.dialog_frame_counter = -1
        self.dialog_content_list = TEXT.fight
        self.go_to_next_frame()

    def on_enter(self, *args):
        super().on_enter(*args)

        # Launch the music of the FIGHT
        music_mixer.play("fight")

    def go_to_next_frame(self, *args):
        self.dialog_frame_counter += 1
        self.index_scrolling_label = 0

        # End of the presentation
        if self.dialog_frame_counter >= len(self.dialog_content_list):
            self.finish_presentation()
            return
        
        self.frame_text = self.dialog_content_list[self.dialog_frame_counter]

        self.text_delay = 1 / TALKING_SPEED
        self.voice_delay = self.text_delay * 2
        Clock.schedule_once(
            self.update_label, self.text_delay)
        Clock.schedule_once(
            self.update_voice, self.text_delay)

    def update_label(self, *args):
        self.index_scrolling_label += 1

        # Update the content of the label
        self.text = self.frame_text[0:self.index_scrolling_label]

        if self.index_scrolling_label < len(self.frame_text):
            current_letter = self.frame_text[self.index_scrolling_label - 1]
        else:
            Clock.schedule_once(
                self.go_to_next_frame, 0.8)
            return
        if current_letter in [".", ",", "!"]:
            next_delay = self.text_delay * 4
        else:
            next_delay = self.text_delay

        # End condition
        if self.index_scrolling_label < len(self.frame_text):
            Clock.schedule_once(
                self.update_label, next_delay)

    def update_voice(self, *_):
        if self.index_scrolling_label < len(self.frame_text):
            current_letter = self.frame_text[self.index_scrolling_label - 1]
        else:
            return

        # Extract the sound
        sound = VOICE_MIXER.musics["masculine_thoughts_medium"]

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

        if self.index_scrolling_label < len(self.frame_text):
            Clock.schedule_once(
                self.update_voice, next_delay)

    def finish_presentation(self):
        self.go_to_next_screen(
            screen_name="competition_results"
        )
