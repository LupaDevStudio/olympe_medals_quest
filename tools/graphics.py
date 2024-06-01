"""
Module referencing the main constants for the graphics of the application.

Constants
---------
"""

#################
### Constants ###
#################

### Font sizes ###

class FontSize():
    def __init__(self) -> None:
        self.title = 21
        self.subtitle = 18
        self.small_label = 12
        self.label = 15

        self.button = 16

FONTS_SIZES = FontSize()

### Colors ###

class Colors():
    def __init__(self) -> None:
        self.blue_olympe = (36 / 255, 122 / 255, 145 / 255, 1) # TODO
        self.blue_pressed_olympe = (22 / 255, 74 / 255, 87 / 255, 1) # TODO

        self.gray_disable = (128 / 255, 128 / 255, 128 / 255, 1) # TODO
        self.gray_pressed_disable = (102 / 255, 102 / 255, 102 / 255, 1) # TODO

        self.white = (1, 1, 1, 1)
        self.black = (0, 0, 0, 1)
        self.transparent_black = (0, 0, 0, 0.5)

COLORS = Colors()

### Sizes ###

ICON_BUTTON_SIZE = 0.1
TOP_BAR_HEIGHT = 0.09

### Positions ###

POS_HINT_RIGHT_BOTTOM_BUTTON = {"right": 0.95, "y": 0.025}

### Opacity ###

OPACITY_ON_BUTTON_PRESS = 0.8
