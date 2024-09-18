"""
Module to create the credits screen.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal
import os

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.constants import (
    TEXT,
    CREDITS_DICT
)
from tools.graphics import (
    FONTS_SIZES
)
from tools import (
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
    thanks_for_playing = StringProperty()

    def reload_kwargs(self, dict_kwargs):
        self.mode = dict_kwargs.get("mode", "normal")
        if self.mode == "normal":
            background_image = PATH_BACKGROUNDS + "office.jpg"
        elif self.mode == "ariane":
            background_image = PATH_BACKGROUNDS + "ariane_ending.png"
        else:
            background_image = PATH_BACKGROUNDS + "olympe_ending.jpg"
        self.set_back_image_path(back_image_path=background_image)

    def reload_language(self):
        super().reload_language()

        my_text = TEXT.credits
        self.thanks_for_playing = my_text["conclusion"]

        ### Title ###

        self.credits_label = f"[size={int(FONTS_SIZES.title*self.font_ratio)}]" + my_text["title"] + "[/size]" + "\n\n\n\n\n\n"

        ### Lupa ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["lupa"] + "[/size]" + "\n\n"
        self.credits_label += my_text["lupa_text"] + "\n\n\n\n"

        ### Licenses ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["licenses"] + "[/size]" + "\n\n"
        self.credits_label += my_text["licenses_text"] + "\n\n\n\n"

        ### Images ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["images"] + "[/size]" + "\n\n"
        for image in CREDITS_DICT["images"]:
            if image in TEXT.rooms:
                title = TEXT.rooms[image]["name"]
            else:
                title = TEXT.credits[image]
            author = CREDITS_DICT["images"][image]["author"]
            self.credits_label += f"[size={int(FONTS_SIZES.label*self.font_ratio)}]" + title + "[/size]\n" + author + "\n\n"
        self.credits_label += "\n\n"

        ### Icons ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["icons"] + "[/size]" + "\n\n"
        dict_authors = {}
        for icon in CREDITS_DICT["icons"]:
            author = CREDITS_DICT["icons"][icon]["author"]
            if author not in dict_authors:
                dict_authors[author] = 1
            else:
                dict_authors[author] += 1
        list_authors = sorted(dict_authors, key=dict_authors.get, reverse=True)
        for author in list_authors:
            self.credits_label += author + "\n"
        self.credits_label += "\n\n\n"

        ### Musics ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["musics"] + "[/size]" + "\n\n"
        for music in CREDITS_DICT["musics"]:
            title_in_game = CREDITS_DICT["musics"][music]["title_in_game"]
            title = CREDITS_DICT["musics"][music]["title"]
            author = CREDITS_DICT["musics"][music]["author"]
            self.credits_label += f"[size={int(FONTS_SIZES.label*self.font_ratio)}]" + title_in_game + "[/size]\n" + title + "\n" + author + "\n\n"
        self.credits_label += "\n\n"

        ### Sounds effects ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["sound_effects"] + "[/size]" + "\n\n"
        self.credits_label += my_text["sound_effects_text"] + "\n\n\n\n"

        ### Voices ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["voices"] + "[/size]" + "\n\n"
        self.credits_label += my_text["voices_text"] + "\n\n\n\n"

        ### Testing ###

        self.credits_label += f"[size={int(FONTS_SIZES.subtitle*self.font_ratio)}]" + my_text["testing"] + "[/size]" + "\n\n"
        self.credits_label += my_text["testing_text"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        music_mixer.play(name="generic")

    def on_enter(self, *args):
        super().on_enter(*args)
        self.launch_generic()
        
    def launch_generic(self):
        
        scrolling_label = self.ids.scrolling_label
        anim = Animation(y=Window.size[1]+10*self.font_ratio, duration=81)
        anim.start(scrolling_label)
        anim.on_complete = self.finish_animation

        list_characters = [d for d in os.listdir(PATH_CHARACTERS_IMAGES) if os.path.isdir(os.path.join(PATH_CHARACTERS_IMAGES, d))]
        for character in list_characters:
            character_image = self.ids[character]
            anim = Animation(y=Window.size[1]+10*self.font_ratio+scrolling_label.height+character_image.y, duration=81)
            anim.start(character_image)

    def finish_animation(self, *args):
        self.ids.thanks_for_playing_label.opacity = 1
        Clock.schedule_once(self.leave_screen, 5)

    def leave_screen(self, *args):
        self.ids.thanks_for_playing_label.opacity = 0
        self.go_to_next_screen(screen_name="home")
