"""
Module to create the save screen.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterInfoWithMainSportsLayout,
    CompleteRecruitCard
)
from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    USER_DATA
)
from tools.graphics import (
    MARGIN,
    BUTTON_HEIGHT,
    HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    SCROLLVIEW_WIDTH
)
from tools.data_structures import (
    Game
)

#############
### Class ###
#############

class SaveScreen(OlympeScreen):
    """
    Class to manage the save screen of the game.
    """

    dict_type_screen = {
        SCREEN_BACK_ARROW : "home"
    }
    new_game_label = StringProperty()
    can_start_new_game = BooleanProperty(True)

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.save

        self.new_game_label = my_text["new_game"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.can_start_new_game: bool = USER_DATA.can_start_new_game()

    def ask_start_new_game(self):
        # TODO popup launching creation of the new game with difficulty
        print("Popup of difficulty")
        self.start_new_game(difficulty="medium")

    def start_new_game(self, difficulty: Literal["easy", "medium", "difficult"]):
        id_game = USER_DATA.start_new_game(difficulty=difficulty)
        USER_DATA.save_changes()
        self.launch_game(id_game=id_game)

    def launch_game(self, id_game=1):
        self.manager.id_game = id_game
        self.go_to_next_screen(screen_name="game")
