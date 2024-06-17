"""
Module to create the game screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    PressedWithIconButton
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_ICONS
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR
)

#############
### Class ###
#############


class GameScreen(OlympeScreen):
    """
    Class to manage the game screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_YEAR : True,
        SCREEN_BACK_ARROW : True,
        SCREEN_MONEY_RIGHT : True
    }

    def on_enter(self, *args):
        super().on_enter(*args)

        self.fill_grid_layout()

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.game

    def fill_grid_layout(self):
        # TODO insert in this list only the buttons unlocked depending on tutorial
        list_buttons = [
            "team",
            "recruit",
            "sports_complex",
            "sports_menu",
            "activities_menu",
            "medals",
            "shop"
        ]

        grid_layout = self.ids["grid_layout"]
        grid_layout.padding = (0.05*self.width, 20*self.font_ratio)
        grid_layout.spacing = 20*self.font_ratio
        height_button = (
            0.5*self.height - grid_layout.padding[1]*2 - 3*grid_layout.spacing[1]) // 4
        for element in list_buttons:

            pressed_button = PressedWithIconButton(
                icon_source = PATH_ICONS + element + ".png",
                text=self.my_text[element],
                font_ratio=self.font_ratio,
                release_function=partial(self.go_to_next_screen, element),
                size_hint=(0.45, None),
                height=height_button*self.font_ratio,
            )

            grid_layout.add_widget(pressed_button)

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.grid_layout.children[:]
        for element in list_widgets:
            self.ids.grid_layout.remove_widget(element)
