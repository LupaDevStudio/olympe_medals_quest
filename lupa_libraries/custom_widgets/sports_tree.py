"""
Module to create the tree of sports.
"""

###############
### Imports ###
###############

# Python imports #

from typing import Literal

# Kivy imports #

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty,
)

# Local imports #

from tools.path import (
    PATH_TITLE_FONT,
    PATH_SPORTS_ICONS
)
from tools.graphics import (
    COLORS,
    FONTS_SIZES,
    BUTTON_LINE_WIDTH
)
from tools.data_structures import (
    SPORTS,
    Sport
)
from tools.constants import (
    TEXT
)
from ._common import hide_widget


#################
### Constants ###
#################

X_SPACING_SPORT_CARDS = 25
Y_SPACING_SPORT_CARDS = 30
X_SIZE_SPORT_CARD = 200
Y_SIZE_SPORT_CARD = 120

#################
### Functions ###
#################


def compute_sport_card_position(sport_class_id: int, sport_id_in_class: int, font_ratio: float):
    x = sport_class_id * (X_SIZE_SPORT_CARD + X_SPACING_SPORT_CARDS) / \
        2 + sport_id_in_class * (X_SIZE_SPORT_CARD +
                                 X_SPACING_SPORT_CARDS) + X_SPACING_SPORT_CARDS
    y = sport_class_id * (Y_SPACING_SPORT_CARDS +
                          Y_SIZE_SPORT_CARD) + Y_SPACING_SPORT_CARDS
    return x * font_ratio, y * font_ratio


def get_sport_state(sport_id, sports_unlocking_progress):
    if sport_id not in sports_unlocking_progress:
        unlocking_progress = 0
    else:
        unlocking_progress = sports_unlocking_progress[sport_id]
    if unlocking_progress == 1:
        return "unlocked"
    elif unlocking_progress > 0:
        return "in_research"
    else:
        # List the requirements
        requirements = SPORTS[sport_id].requirements
        for requirement in requirements:
            if requirement not in sports_unlocking_progress or sports_unlocking_progress[requirement] < 1:
                return "unknown"
        return "locked"

###############
### Classes ###
###############


class SportCard(RelativeLayout):
    """
    Sport card for the sport tree.
    """

    sport_id: str
    state = StringProperty()
    sport_skills: list
    sport_class = NumericProperty()
    first_skill_color = ColorProperty(COLORS.blue_olympe)
    second_skill_color = ColorProperty(COLORS.blue_olympe)
    third_skill_color = ColorProperty(COLORS.blue_olympe)
    sport_icon_source = StringProperty()

    # Text
    unlock_button_text = StringProperty()
    sport_name_text = StringProperty()
    unlocked_text = StringProperty()

    # Font
    font_size = FONTS_SIZES.button
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)
    font_ratio = NumericProperty(1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)

    def __init__(
            self,
            sport_id: str,
            sport_skills: list[str],
            state: Literal["unknown", "in_research", "unlocked", "locked"],
            **kwargs):
        super().__init__(**kwargs)

        # Store the parameters
        self.sport_id = sport_id
        self.sport_skills = sport_skills
        self.state = state
        self.sport_class: Literal[1, 2, 3] = len(sport_skills)

        # Set the colors for the skill rectangles
        self.first_skill_color = COLORS.__getattribute__(
            f"stats_{sport_skills[0]}")
        if self.sport_class >= 2:
            self.second_skill_color = COLORS.__getattribute__(
                f"stats_{sport_skills[1]}")
        if self.sport_class == 3:
            self.third_skill_color = COLORS.__getattribute__(
                f"stats_{sport_skills[2]}")

        self.unlock_button_text = TEXT.general["unlock"]
        self.unlocked_text = TEXT.general["unlocked"]
        self.sport_icon_source = PATH_SPORTS_ICONS + sport_id + ".png"

        self.update_sport_name_text()
        self.update_display_unlock_button()

    def start_researching(self):
        pass

    def unlock(self):
        pass

    def update_sport_name_text(self):
        if self.state == "unknown":
            self.sport_name_text = "???"
        else:
            self.sport_name_text = TEXT.sports[self.sport_id]["name"]

    def remove_unknow(self):
        pass

    def update_display_unlock_button(self):
        if self.state == "unknown":
            hide_widget(self.ids.unlock_button, do_hide=True)
            hide_widget(self.ids.info_button, do_hide=True)
            hide_widget(self.ids.sport_icon, do_hide=True)
        else:
            if self.state == "unlocked":
                hide_widget(self.ids.unlock_button, do_hide=True)
            else:
                hide_widget(self.ids.unlock_button, do_hide=False)
            hide_widget(self.ids.info_button, do_hide=False)
            hide_widget(self.ids.sport_icon, do_hide=False)

    def update_display_info_button(self):
        pass

    def open_info(self):
        pass


class SportLink(Widget):
    font_ratio = NumericProperty(1)


class SportsScrollView(ScrollView):
    """
    Class containing the scrollview to scroll over the tree.
    """

    sports_unlocking_progress = ObjectProperty({})
    font_ratio = NumericProperty(1)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.bar_color = COLORS.blue_olympe
        self.bar_inactive_color = COLORS.blue_pressed_olympe


class SportsTreeContent(Widget):
    sports_unlocking_progress = ObjectProperty({})
    font_ratio = NumericProperty(1)
    line_width = NumericProperty(BUTTON_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)

    def build_tree(self, sports_unlocking_progress: dict):
        self.sports_unlocking_progress = sports_unlocking_progress

        # Iterate over the sports to divide them in the categories
        sport_classes = [[]]
        for sport in SPORTS:
            if len(SPORTS[sport].requirements) == 0:
                sport_classes[0].append(sport)
            else:
                print(sport_classes)
                print(sport)
                requirement = SPORTS[sport].requirements[0]
                for i in range(len(sport_classes)):
                    if requirement in sport_classes[i]:
                        class_id = i + 1
                if class_id > len(sport_classes) - 1:
                    sport_classes.append([])
                sport_classes[class_id].append(sport)

        # Duplicate the first and last sport of each category except the last one
        for i in range(len(sport_classes) - 1):
            sport_classes[i].append(sport_classes[i][0])

        # Create the sport cards
        for i in range(len(sport_classes)):
            for j, sport in enumerate(sport_classes[i]):
                pos = compute_sport_card_position(i, j, self.font_ratio)
                size = (X_SIZE_SPORT_CARD * self.font_ratio,
                        Y_SIZE_SPORT_CARD * self.font_ratio)
                state = get_sport_state(
                    sport_id=sport, sports_unlocking_progress=self.sports_unlocking_progress)
                current_sport_card = SportCard(
                    sport_skills=SPORTS[sport].stats,
                    state=state,
                    pos=pos,
                    size=size,
                    font_ratio=self.font_ratio,
                    sport_id=sport
                )
                self.add_widget(current_sport_card)

        # Set the size of the widget
        x_size, _ = compute_sport_card_position(
            sport_class_id=0, sport_id_in_class=len(sport_classes[0]), font_ratio=self.font_ratio)
        _, y_size = compute_sport_card_position(
            sport_class_id=len(sport_classes), sport_id_in_class=0, font_ratio=self.font_ratio)
        self.size = (x_size + (X_SIZE_SPORT_CARD +
                     X_SPACING_SPORT_CARDS) * self.font_ratio / 2, y_size - Y_SPACING_SPORT_CARDS * self.font_ratio / 2)


class SportTree(Widget):
    """
    Class to create the entire sports tree.
    """

    sports_unlocking_progress: dict

    # Font
    font_size = FONTS_SIZES.button
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)
    font_ratio = NumericProperty(1)

    def __init__(self, sports_unlocking_progress: dict, **kwargs):
        super().__init__(**kwargs)
        self.sports_unlocking_progress = sports_unlocking_progress
