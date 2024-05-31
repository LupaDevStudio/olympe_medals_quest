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
        self.blue_olympe = (18 / 255, 56 / 255, 89 / 255, 1), # TODO
        self.white = (1, 1, 1, 1)
        self.black = (0, 0, 0, 1)
        self.transparent_black = (0, 0, 0, 0.5)

COLORS = Colors()

### Sizes ###

BACK_ARROW_SIZE = 0.2
TOP_BAR_HEIGHT = 0.09
SAVE_PUBLISH_BUTTON_SIZE_HINT = (0.5, 0.075)

### Positions ###

### Opacity ###

OPACITY_ON_BUTTON_PRESS = 0.8
