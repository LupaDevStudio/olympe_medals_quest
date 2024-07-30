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
    MARGIN
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

    def get_info_from_sport_complex_level(self, sports_complex_level: int):

        level_details = []
        max_number_athletes = TEXT.sports_complex["max_number_athletes"].replace(
            "[NB_ATHLETES]", str(SPORTS_COMPLEX_EVOLUTION_DICT[
                str(sports_complex_level)]["max_number_athletes"])
        )
        level_details.append({
            "text": max_number_athletes
        })

        for element in SPORTS_COMPLEX_EVOLUTION_DICT[str(sports_complex_level)]["rooms_unlocked"]:
            room_id = element[0]
            room_level = element[1]
            text = TEXT.sports_complex["room"].replace(
                "[ROOM]", TEXT.rooms[room_id]["name"])
            text = text.replace("[LEVEL]", str(room_level))
            level_details.append(
                {
                    "text": text,
                    "release_function": partial(
                        self.open_tutorial_popup_room, room_id)
                }
            )

        return level_details

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        ### Sports complex ###

        sports_complex_level = GAME.sports_complex.current_level

        # If the sports complex is not at its maximum level
        if sports_complex_level != len(SPORTS_COMPLEX_EVOLUTION_DICT):

            # Init the folded dictionary
            if "sports_complex" not in self.rooms_folded_dict:
                self.rooms_folded_dict["sports_complex"] = [False, None]

            next_level = sports_complex_level + 1
            sports_complex_title = TEXT.sports_complex[
                "sports_complex"] + " - " + TEXT.general[
                    "level"] + " " + str(next_level)
            
            # Small view
            if self.rooms_folded_dict["sports_complex"][0]:

                sports_complex_card = SmallRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=sports_complex_title,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=HEADER_HEIGHT*self.font_ratio
                )

            # Complete view
            else:

                # Details of the current level of the sports complex
                current_level_details = self.get_info_from_sport_complex_level(
                    sports_complex_level=sports_complex_level
                )

                # Details of the next level of the sports complex
                next_level_details = self.get_info_from_sport_complex_level(
                    sports_complex_level=next_level
                )

                sports_complex_card = CompleteRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=sports_complex_title,
                    price=SPORTS_COMPLEX_EVOLUTION_DICT[str(next_level)]["price"],
                    button_text=TEXT.sports_complex["expand"],
                    image_source=PATH_BACKGROUNDS + f"sport_complex_{next_level}.jpg",
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=(HEADER_HEIGHT+BIG_BUTTON_HEIGHT+ROOM_HEIGHT+3*MARGIN)*self.font_ratio,
                    current_level_title=TEXT.general["level"] + " " + str(sports_complex_level),
                    current_level_details=current_level_details,
                    next_level_title=TEXT.general["level"] + " " + str(next_level),
                    next_level_details=next_level_details
                )

            self.rooms_folded_dict["sports_complex"][1] = sports_complex_card
            scrollview_layout.add_widget(sports_complex_card)

        ### Rooms ###

        # Add the unlocked rooms not bought in the scrollview
        for room_id in GAME.sports_complex.rooms_unlocked:

            # Init the folded dictionary
            if room_id not in self.rooms_folded_dict:
                self.rooms_folded_dict[room_id] = [False, None]

            room: Room = GAME.sports_complex.rooms_unlocked[room_id]
            room_title: str = TEXT.rooms[room_id]["name"] + " - " + TEXT.general[
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
                    current_level_details = []
                    # TODO parcourir les activités et effets DANS UNE FONCTION

                # Fill next details
                next_level_title = TEXT.general["level"] + " " + str(next_level)
                next_level_details = []
                # TODO parcourir les activités et effets DANS UNE FONCTION

                room_card = CompleteRoomCard(
                    font_ratio=self.font_ratio,
                    title_card=room_title,
                    price=ROOMS_EVOLUTION_DICT[room_id][str(next_level)]["price"],
                    button_text=button_text,
                    image_source=room.image,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=(HEADER_HEIGHT+BIG_BUTTON_HEIGHT+ROOM_HEIGHT+3*MARGIN)*self.font_ratio,
                    current_level_title=current_level_title,
                    current_level_details=current_level_details,
                    next_level_title=next_level_title,
                    next_level_details=next_level_details
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

    def open_tutorial_popup_room(self, room_id: str):
        print("Open popup room")

    def open_tutorial_popup_activity(self, activity_id: str):
        print("Open popup activity")

    def open_tutorial_popup_effect(self, effect_id: str):
        print("Open popup effect")
