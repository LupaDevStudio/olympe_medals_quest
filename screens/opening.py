"""
Module for the opening screen.
"""

###############
### Imports ###
###############

### Python imports ###

import os
from threading import Thread

### Kivy imports ###

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label

### Local imports ###

from lupa_libraries import (
    ImprovedScreen
)
from tools.path import (
    PATH_IMAGES
)
from tools.constants import (
    USER_DATA
)

#############
### Class ###
#############

class OpeningScreen(ImprovedScreen):
    """
    Screen of Opening.
    """

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "opening.jpg",
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03
        self.label = Label(text="", pos_hint={
            "bottom": 1, "left": 1})
        self.add_widget(self.label)

    def update(self, *args):
        self.label.opacity += self.opacity_state * self.opacity_rate
        if self.label.opacity < 0 or self.label.opacity > 1:
            self.opacity_state = -self.opacity_state

    def on_enter(self, *args):
        print("Enter opening screen")
        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / 60)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / 60)

        return super().on_leave(*args)

    def launch_thread(self, *_):
        thread = Thread(target=self.load_kv_files)
        thread.start()

    def load_kv_files(self, *_):
        from screens import (
            SCREENS_DICT
        )
        self.screens_class_dict = SCREENS_DICT

        files_to_load_list = [
            "lupa_libraries/screen_manager/",
            "lupa_libraries/custom_widgets/",
            "lupa_libraries/dialog_generator/",
            "screens/"
        ]
        for type_file in files_to_load_list:
            screen_files = [file for file in os.listdir(
                type_file) if file.endswith(".kv")]
            # Force the load of the screen first
            if "screen.kv" in screen_files:
                screen_files.remove("screen.kv")
                screen_files.insert(0, "screen.kv")
            for file in screen_files:
                print(file)
                Builder.load_file(f"{type_file}{file}", encoding="utf-8")

        Clock.schedule_once(self.load_other_screens)

    def switch_to_menu(self, *args):
        self.manager.current = "home"

    def load_other_screens(self, *args):

        ### Load the kv files of the screens ###

        for screen_name in self.screens_class_dict:
            temp_screen = self.screens_class_dict[screen_name](
                name=screen_name)
            self.manager.add_widget(temp_screen)

        Clock.schedule_once(self.switch_to_menu)
