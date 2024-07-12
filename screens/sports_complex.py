"""
Module to create the team screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    SmallRoomCard,
    CompleteRoomCard
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
    GAME
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    HEADER_HEIGHT,
    BIG_BUTTON_HEIGHT,
    ROOM_HEIGHT,
    MARGIN_HEIGHT
)
from tools.data_structures import (
    Room,
    SPORTS_COMPLEX_EVOLUTION_DICT,
    ROOMS_EVOLUTION_DICT
)
from tools.path import (
    PATH_BACKGROUNDS
)

#############
### Class ###
#############


class SportsComplexScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "sports_complex",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    sports_complex_title = StringProperty()
    rooms_folded_dict = {}

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.sports_complex
        self.sports_complex_title = my_text["title"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        if self.rooms_folded_dict == {}:
            self.rooms_folded_dict["sports_complex"] = [False, None]
            for room_id in GAME.sports_complex.rooms_unlocked:
                self.rooms_folded_dict[room_id] = [False, None]

        # If the sports complex is not at its maximum level
        sports_complex_level = GAME.sports_complex.current_level
        if sports_complex_level != len(SPORTS_COMPLEX_EVOLUTION_DICT):
            next_level = sports_complex_level+1
            sports_complex_title = TEXT.sports_complex[
                "sports_complex"] + " - " + TEXT.general[
                    "level"] + " " + str(next_level)
            if self.rooms_folded_dict["sports_complex"][0]:
                sports_complex_card = SmallRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=sports_complex_title,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=HEADER_HEIGHT*self.font_ratio
                )
            else:
                sports_complex_card = CompleteRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=sports_complex_title,
                    price=SPORTS_COMPLEX_EVOLUTION_DICT[str(next_level)]["price"],
                    button_text=TEXT.sports_complex["expand"],
                    image_source=PATH_BACKGROUNDS + f"sport_complex_{next_level}.jpg",
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=(HEADER_HEIGHT+BIG_BUTTON_HEIGHT+ROOM_HEIGHT+3*MARGIN_HEIGHT)*self.font_ratio,
                    current_level_title=TEXT.general["level"] + " " + str(sports_complex_level),
                    current_level_details=[
                        {
                            "text": "Test",
                            "release_function": partial(self.open_tutorial_popup, "test")
                        },
                        {
                            "text": "Test2",
                            "release_function": partial(self.open_tutorial_popup, "test")
                        },
                        {
                            "text": "Test3",
                            "release_function": partial(self.open_tutorial_popup, "test")
                        },
                        {
                            "text": "Test"
                        },
                        {
                            "text": "Test2"
                        },
                        {
                            "text": "Test3"
                        }
                    ],# TODO
                    next_level_title=TEXT.general["level"] + " " + str(next_level),
                    next_level_details=[
                        {
                            "text": "Test"
                        },
                        {
                            "text": "Test2"
                        },
                        {
                            "text": "Test3"
                        },
                        {
                            "text": "Test"
                        },
                        {
                            "text": "Test2"
                        },
                        {
                            "text": "Test3"
                        }
                    ]
                )

            self.rooms_folded_dict["sports_complex"][1] = sports_complex_card
            scrollview_layout.add_widget(sports_complex_card)

        # Add the unlocked rooms in the scrollview
        for room_id in GAME.sports_complex.rooms_unlocked:
            room: Room = GAME.sports_complex.rooms_unlocked[room_id]
            room_title: str = TEXT.rooms[room_id] + " - " + TEXT.general[
                "level"] + " " + str(room.current_level)
            
            if self.rooms_folded_dict[room_id][0]:
                room_card = SmallRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=room_title,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=HEADER_HEIGHT*self.font_ratio
                )
            else:
                button_text = TEXT.sports_complex["buy"]
                current_level_details = []
                current_level_title = ""
                if room.current_level != 1:
                    button_text = TEXT.sports_complex["expand"]
                    current_level_title = TEXT.general["level"] + " " + str(next_level-1)
                    current_level_details = [] # TODO

                room_card = CompleteRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=room_title,
                    price=ROOMS_EVOLUTION_DICT[room_id][str(next_level)]["price"],
                    button_text=button_text,
                    image_source=room.image,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=(HEADER_HEIGHT+BIG_BUTTON_HEIGHT+ROOM_HEIGHT+3*MARGIN_HEIGHT)*self.font_ratio,
                    current_level_title=current_level_title,
                    current_level_details=current_level_details,
                    next_level_title=TEXT.general["level"] + " " + str(next_level),
                    next_level_details=[]# TODO
                )

            self.rooms_folded_dict[room_id][1] = room_card
            scrollview_layout.add_widget(room_card)

    def ask_redraw(self, widget):
        for room_id in self.rooms_folded_dict:
            if widget == self.rooms_folded_dict[room_id][1]:
                self.rooms_folded_dict[room_id][0] = not self.rooms_folded_dict[room_id][0]
                break
        
        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def open_tutorial_popup(self, activity_id: str):
        print("Open popup")
