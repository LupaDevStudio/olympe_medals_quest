"""
Module to create the credits screen.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    StatBar,
    OlympeMessagePopup
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT
)
from tools.constants import (
    TEXT
)
from tools.graphics import (
    COLORS,
    FONTS_SIZES
)
from tools import (
    sound_mixer,
    music_mixer
)

#############
### Class ###
#############


class CreditsScreen(OlympeScreen):
    """
    Class to manage the settings screen of the game.
    """

    dict_type_screen = {}
    mode: Literal["normal", "olympe", "ariane"]

    credits_label = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.mode = dict_kwargs.get("mode", "normal")
        if self.mode == "normal":
            background_image = PATH_BACKGROUNDS + "office.jpg"
        elif self.mode == "ariane":
            background_image = PATH_BACKGROUNDS + "ariane_ending.jpg"
        else:
            background_image = PATH_BACKGROUNDS + "olympe_ending.jpg"
        self.set_back_image_path(back_image_path=background_image)

    def reload_language(self):
        super().reload_language()

        self.credits_label = "TEST de label déroulant\ntest de label déroulant"*60

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.build_scrolling_label()
        
    def build_scrolling_label(self):
        scrolling_label = Label(
            text=self.credits_label,
            font_size=FONTS_SIZES.small_label*self.font_ratio,
            color=COLORS.white,
            font_name=PATH_TEXT_FONT,
            size_hint=(None, None),
            width=Window.size[0]*0.8,
            pos_hint={"center_x": 0.5},
            halign='center',
            valign='middle'
        )
        scrolling_label.bind(size=scrolling_label.setter('text_size'))
        
        self.ids.relative_layout.add_widget(scrolling_label)
        
        # Crée une animation pour faire défiler le texte de bas en haut
        anim = Animation(y=Window.height, duration=5)
        anim.start(scrolling_label)
