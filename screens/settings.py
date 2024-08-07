"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ListProperty,
    NumericProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    StatBar,
    OlympeMessagePopup
)
from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    TEXT,
    USER_DATA,
    SCREEN_TITLE_ICON,
    SCREEN_BACK_ARROW,
    DICT_LANGUAGE_CODE_TO_NAME,
    DICT_LANGUAGE_NAME_TO_CODE
)
from tools.graphics import (
    COLORS,
    SKILL_HEIGHT,
    MARGIN
)

#############
### Class ###
#############


class SettingsScreen(OlympeScreen):
    """
    Class to manage the settings screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "settings",
        SCREEN_BACK_ARROW : "home"
    }

    ### Language ###

    language_label = StringProperty()
    current_language_label = StringProperty()
    list_languages = ListProperty()

    ### Configuration ###

    configuration_label = StringProperty()
    music_label = StringProperty()
    music_level = NumericProperty(int(USER_DATA.settings["music_volume"]*10))
    sound_effects_label = StringProperty()
    sound_effects_level = NumericProperty(int(USER_DATA.settings["sound_volume"]*10))
    talking_speed_label = StringProperty()
    talking_speed_level = NumericProperty(int((USER_DATA.settings["talking_speed"]-20)/3))
    list_bars = []

    ### Achievements ###

    achievements_label = StringProperty()

    ### Tutorial ###

    tutorial_label = StringProperty()
    see_tutorial_label = StringProperty()

    ### Credits ###

    credits_label = StringProperty()
    see_credits_label = StringProperty()

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)
        
        self.list_languages = sorted(list(DICT_LANGUAGE_NAME_TO_CODE.keys()))

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.settings

        self.language_label = my_text["language"]
        self.current_language_label = DICT_LANGUAGE_CODE_TO_NAME[TEXT.language]
        self.configuration_label = my_text["configuration"]
        self.music_label = my_text["music"]
        self.sound_effects_label = my_text["sound_effects"]
        self.talking_speed_label = my_text["talking_speed"]
        self.achievements_label = my_text["achievements"]
        self.tutorial_label = my_text["tutorial"]
        self.see_tutorial_label = my_text["see_tutorial"]
        self.credits_label = my_text["credits"]
        self.see_credits_label = my_text["see_credits"]

    def on_enter(self, *args):
        super().on_enter(*args)

        self.build_configuration_bars()

    def build_configuration_bars(self):
        list_content = [
            {
                "y": self.ids.music_minus_button.y,
                "level": self.music_level
            },
            {
                "y": self.ids.sound_effects_minus_button.y,
                "level": self.sound_effects_level
            },
            {
                "y": self.ids.talking_speed_minus_button.y,
                "level": self.talking_speed_level
            }
        ]
        offset_x = self.ids.music_minus_button.x + self.ids.music_minus_button.width
        width = (self.ids.music_plus_button.x - offset_x - 2*MARGIN*self.font_ratio)/10
        small_margin = width / 2
        width = width - small_margin

        for dict_content in list_content:
            y_pos = dict_content["y"]
            level = dict_content["level"]
            for i in range(0, 10):
                if (i+1) <= level:
                    color = COLORS.white
                else:
                    color = COLORS.black
                current_bar = StatBar(
                    y=y_pos,
                    x=offset_x+i*width+self.font_ratio*MARGIN+i*small_margin,
                    size_hint=(None, None),
                    height=SKILL_HEIGHT*self.font_ratio,
                    width=width*4,
                    color=color,
                    font_ratio=self.font_ratio
                )
                self.list_bars.append(current_bar)
                self.add_widget(current_bar)

    def rebuild_configuration_bars(self):
        # Remove the bars
        for widget in self.list_bars:
            self.remove_widget(widget)

        # Build the bars
        self.build_configuration_bars()

    def change_language(self, name_language: str):
        # Get the code of the selected language
        code_language: str = DICT_LANGUAGE_NAME_TO_CODE[name_language]

        # Change the language and save it
        TEXT.change_language(code_language)
        USER_DATA.settings["language"] = code_language
        USER_DATA.save_changes()

        # Update the labels of the screen
        self.reload_language()

    def reduce_music(self):
        self.music_level -= 1
        USER_DATA.settings["music_volume"] = self.music_level/10
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def increase_music(self):
        self.music_level += 1
        USER_DATA.settings["music_volume"] = self.music_level/10
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def reduce_sound_effects(self):
        self.sound_effects_level -= 1
        USER_DATA.settings["sound_volume"] = self.sound_effects_level/10
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def increase_sound_effects(self):
        self.sound_effects_level += 1
        USER_DATA.settings["sound_volume"] = self.sound_effects_level/10
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def reduce_talking_speed(self):
        self.talking_speed_level -= 1
        USER_DATA.settings["talking_speed"] = 20+self.talking_speed_level*3
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def increase_talking_speed(self):
        self.talking_speed_level += 1
        USER_DATA.settings["talking_speed"] = 20+self.talking_speed_level*3
        USER_DATA.save_changes()
        self.rebuild_configuration_bars()

    def go_to_achievements(self):
        print("TODO create the achievements screen")

    def launch_credits(self):
        print("TODO launch the generic")

    def launch_tutorial(self):
        print("TODO launch the tutorial")
