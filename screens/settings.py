"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ListProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen
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

    language_label = StringProperty()
    current_language_label = StringProperty()
    list_languages = ListProperty()
    configuration_label = StringProperty()
    achievements_label = StringProperty()
    tutorial_label = StringProperty()
    see_tutorial_label = StringProperty()
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
        self.achievements_label = my_text["achievements"]
        self.tutorial_label = my_text["tutorial"]
        self.see_tutorial_label = my_text["see_tutorial"]
        self.credits_label = my_text["credits"]
        self.see_credits_label = my_text["see_credits"]

    def change_language(self, name_language: str):
        # Get the code of the selected language
        code_language: str = DICT_LANGUAGE_NAME_TO_CODE[name_language]

        # Change the language and save it
        TEXT.change_language(code_language)
        USER_DATA.settings["language"] = code_language
        USER_DATA.save_changes()

        # Update the labels of the screen
        self.reload_language()

    def go_to_achievements(self):
        print("TODO create the achievements screen")

    def launch_credits(self):
        print("TODO launch the generic")

    def launch_tutorial(self):
        print("TODO launch the tutorial")
