"""
Module to create sound effect for character talking.
"""

###############
### Imports ###
###############

### Python imports ###

import os
from functools import partial
import random

### Kivy imports ###

from kivy.core.audio import SoundLoader, Sound

#################
### Constants ###
#################

__version__ = "1.0.0"

### Paths ###

CURRENT_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = os.path.join(CURRENT_FOLDER, "resources")
BASE_SOUND_FILE = os.path.join(RESOURCES_FOLDER, "base_6.wav")

#################
### Functions ###
#################

sound: Sound = SoundLoader.load(BASE_SOUND_FILE)


if __name__ == "__main__":
    dialog_speed = 20  # letter per second
    test_sentence = "Votre manière de raisonner est décidement très intéressante... Je vous embauche !"

    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.clock import Clock

    class DemoApp(App):

        index_scrolling_label = 0
        dialog_text = test_sentence

        def build(self):
            print("build")
            label = Label(text="", color=(1, 1, 1, 1))
            self.label = label
            Clock.schedule_once(
                self.update_label, 1)
            return label

        def on_start(self):

            return super().on_start()

        def update_label(self, *_):
            self.index_scrolling_label += 1

            # Update the content of the label
            self.label.text = self.dialog_text[0:self.index_scrolling_label]

            current_letter = self.dialog_text[self.index_scrolling_label - 1]
            if current_letter not in [" ", "."]:
                if current_letter in ["a", "e", "i", "o", "u", "y"]:
                    sound.pitch = 1.5
                else:
                    sound.pitch = 1.
                sound.stop()
                sound.play()

            if current_letter in [".", ",", "!"]:
                next_delay = (1 / dialog_speed) * 4
            else:
                next_delay = (1 / dialog_speed)

            # End condition
            if self.index_scrolling_label < len(self.dialog_text):
                Clock.schedule_once(
                    self.update_label, next_delay)

            # if sound.state != "play":
            #     sound.play()

    root = DemoApp()
    root.run()
