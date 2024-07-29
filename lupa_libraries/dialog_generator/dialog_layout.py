"""
Module to manage the dialogs.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
from random import random
from math import pi, sin, cos

### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ColorProperty
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation, AnimationTransition
from kivy.uix.widget import Widget

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_TITLE_FONT
)
from tools.graphics import (
    COLORS,
    FONTS_SIZES,
    BUTTON_LINE_WIDTH
)

#################
### Constants ###
#################


def get_flash_animation(animation: Animation | None = None, number_blinks: int = 1, blink_delay: float = 0.1) -> Animation:

    # First flash
    new_animation = Animation(opacity=0,
                            transition="linear", duration=blink_delay / 2)
    new_animation += Animation(opacity=1,
                            transition="linear", duration=blink_delay / 2)

    for counter in range(number_blinks - 1):
        random_added_delay = rd.randint(0, 2) / 10
        new_animation += Animation(
            opacity=0,
            transition="linear",
            duration=(blink_delay+random_added_delay) / 2)
        new_animation += Animation(
            opacity=1,
            transition="linear",
            duration=(blink_delay+random_added_delay) / 2)

    if animation is None:
        animation = new_animation
    else:
        animation += new_animation

    return animation

def get_shake_animation(widget: Widget, shake_type: str) -> Animation:
    """
    Return a shake animation of the given type.

    Parameters
    ----------
    shake_type : str
        Type of shake animation.

    Returns
    -------
    kivy.Animation
    """
    # For flash animations
    if shake_type == "flash":
        return get_flash_animation(
            number_blinks=3,
            blink_delay=0.2)

    original_x = widget.x
    original_y = widget.y

    if shake_type == "strong":
        shake_distance = 20
        nb_shakes = 5
        shake_speed = 200  # in px per sec
    elif shake_type == "medium":
        shake_distance = 15
        nb_shakes = 4
        shake_speed = 150  # in px per sec
    elif shake_type == "weak":
        shake_distance = 10
        nb_shakes = 2
        shake_speed = 100  # in px per sec
    animation = None

    for i in range(nb_shakes):
        if i < nb_shakes - 1:
            # Shake in a random direction
            shake_angle = random() * 4 * pi - 2 * pi
            new_x = original_x + shake_distance * cos(shake_angle)
            new_y = original_y + shake_distance * sin(shake_angle)
        else:
            # Return to original position for the last shake
            new_x = original_x
            new_y = original_y
        new_animation = Animation(pos=(
            new_x, new_y), transition="in_out_back", duration=shake_distance / shake_speed)
        if animation is None:
            animation = new_animation
        else:
            animation += new_animation

        # Add blinking for strong shakes
        if shake_type == "strong":
            animation += get_flash_animation(animation=animation)

    return animation

#############
### Class ###
#############


class DialogLayout(RelativeLayout):

    mode = StringProperty("left")  # can be "left" or "right"

    ### Content ###

    character_name = StringProperty()
    character_title = StringProperty()
    character_image = StringProperty()
    text = StringProperty()

    ### Fonts ###

    font_size_title = NumericProperty(FONTS_SIZES.subtitle)
    font_size_text = NumericProperty(FONTS_SIZES.label)
    font_ratio = NumericProperty(1)
    font_name_title = StringProperty(PATH_TITLE_FONT)
    font_name_text = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.dark_transparent_black)
    frame_color = ColorProperty(COLORS.white)

    frame_width = NumericProperty(BUTTON_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
