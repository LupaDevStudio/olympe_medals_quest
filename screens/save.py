"""
Module to create the save screen.
"""

###############
### Imports ###
###############

### Python imports ###

from typing import Literal
from functools import partial
from datetime import datetime

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    SaveCard
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
    TOP_BAR_HEIGHT,
    BOTTOM_BAR_HEIGHT,
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
    number_saves = 0

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "office.jpg",
            **kw)

    def reload_language(self):
        super().reload_language()
        self.new_game_label = TEXT.save["new_game"]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.can_start_new_game: bool = USER_DATA.can_start_new_game()
        self.number_saves = 0

        self.fill_save_cards()

    def fill_save_cards(self):
        if USER_DATA.game_1 is not None:
            self.add_save_card(id_save=1)
        if USER_DATA.game_2 is not None:
            self.add_save_card(id_save=2)
        if USER_DATA.game_3 is not None:
            self.add_save_card(id_save=3)

    def add_save_card(self, id_save: int):
        save_layout = self.ids.save_layout

        if id_save == 1:
            game: Game = USER_DATA.game_1
        elif id_save == 2:
            game: Game = USER_DATA.game_2
        else:
            game: Game = USER_DATA.game_3

        height_card = (Window.size[1] * (0.95 - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT) - \
            MARGIN*2*self.font_ratio) / 3
        
        date = game.last_time_played
        if TEXT.language == "french":

            date_en_format = '%m/%d/%Y - %H:%M'
            date_fr_format = '%d/%m/%Y - %Hh%M'

            date_en_datetime = datetime.strptime(date, date_en_format)
            date = date_en_datetime.strftime(date_fr_format)

        information = TEXT.save["information"].replace(
            "[YEAR]", str(game.year)).replace(
            "[TRIMESTER]", str(game.trimester)).replace(
            "[DATE]", date)
        number_athletes = game.number_athletes
        if number_athletes > 1:
            number_athletes_label = str(number_athletes) + TEXT.team["athletes"]
        else:
            number_athletes_label = str(number_athletes) + TEXT.team["athlete"]

        save_card = SaveCard(
            font_ratio=self.font_ratio,
            title_card=TEXT.save["save"].replace(
                "@", str(id_save)).replace("€", TEXT.save[game.difficulty]),
            delete_function=partial(self.delete_game, id_save),
            launch_function=partial(self.launch_game, id_save),
            size_hint=(None, None),
            width=Window.size[0]*SCROLLVIEW_WIDTH,
            height=height_card,
            y=height_card*(2-self.number_saves)+MARGIN*self.font_ratio*(2-self.number_saves),
            load_text=TEXT.save["load"],
            best_athlete_image=game.get_best_athlete_image(),
            information=information,
            number_athletes_label=number_athletes_label,
            money=game.money,
            characters_list=game.unlocked_characters
        )

        save_layout.add_widget(save_card)
        self.number_saves += 1

    def ask_to_ask_delete_game(self, id_game: int):
        print("TODO popup 1")
        self.ask_delete_game(id_game=id_game)

    def ask_delete_game(self, id_game: int):
        print("TODO popup 2")
        self.delete_game(id_game=id_game)

    def delete_game(self, id_game: int):
        USER_DATA.delete_game(id_game=id_game)
        USER_DATA.save_changes()

        # Reset the layout of save cards
        list_widgets = self.ids.save_layout.children[:]
        for element in list_widgets:
            self.ids.save_layout.remove_widget(element)
        self.number_saves = 0
        self.can_start_new_game: bool = USER_DATA.can_start_new_game()
        # Rebuild the layout of save cards
        self.fill_save_cards()

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

    def on_leave(self, *args):
        # Reset the layout of save cards
        list_widgets = self.ids.save_layout.children[:]
        for element in list_widgets:
            self.ids.save_layout.remove_widget(element)

        super().on_leave(*args)
