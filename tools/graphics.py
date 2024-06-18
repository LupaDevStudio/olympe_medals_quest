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

        self.big_button = 18
        self.button = 16

        self.coins_count = 15

FONTS_SIZES = FontSize()

### Colors ###

class Colors():
    def __init__(self) -> None:
        self.blue_olympe = (36 / 255, 122 / 255, 145 / 255, 1)
        self.blue_pressed_olympe = (22 / 255, 74 / 255, 87 / 255, 1)
        self.gray_disable = (128 / 255, 128 / 255, 128 / 255, 1)
        self.gray_pressed_disable = (102 / 255, 102 / 255, 102 / 255, 1)

        self.white = (1, 1, 1, 1)
        self.black = (0, 0, 0, 1)
        self.transparent_black = (0, 0, 0, 0.5)
        self.very_transparent_black = (0, 0, 0, 0.3)

        self.tier_rank_s = (255 / 255, 126 / 255, 126 / 255, 1)
        self.tier_rank_a = (254 / 255, 191 / 255, 127 / 255, 1)
        self.tier_rank_b = (254 / 255, 254 / 255, 129 / 255, 1)
        self.tier_rank_c = (189 / 255, 254 / 255, 129 / 255, 1)
        self.tier_rank_d = (125 / 255, 254 / 255, 130 / 255, 1)
        self.tier_rank_e = (126 / 255, 254 / 255, 255 / 255, 1)
        self.tier_rank_f = (127 / 255, 191 / 255, 253 / 255, 1)

COLORS = Colors()

### Sizes ###

ICON_BUTTON_SIZE = 0.1
TOP_BAR_HEIGHT = 0.09
RADIUS_SMALL = 12
SCROLLVIEW_WIDTH = 0.96

### Outlines ###

BUTTON_OUTLINE_WIDTH = 1

### Positions ###

POS_HINT_LEFT_TOP_BUTTON = {"x": 0.05, "top": 0.975}
POS_HINT_LEFT_BOTTOM_BUTTON = {"x": 0.05, "y": 0.025}
POS_HINT_RIGHT_TOP_BUTTON = {"right": 0.95, "top": 0.975}
POS_HINT_RIGHT_BOTTOM_BUTTON = {"right": 0.95, "y": 0.025}
