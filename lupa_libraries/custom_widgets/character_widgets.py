"""
Module to create widgets with the pressed style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.constants import (
    FPS
)
from tools.graphics import (
    COLORS,
    LARGE_OUTLINE_WIDTH,
    BUTTON_OUTLINE_WIDTH,
    FONTS_SIZES
)
from tools.path import (
    PATH_ICONS,
    PATH_TEXT_FONT
)

#############
### Class ###
#############


class CharacterButton(ButtonBehavior, RelativeLayout):
    """
    A button with a character on it.
    """

    ### Image settings ###

    image_source = StringProperty()

    ### Icon settings ###

    icon_mode = BooleanProperty(False)
    icon_flashing_mode = BooleanProperty(False)
    icon_position = ObjectProperty({"x": 0.05, "top": 0.95})
    icon_source = StringProperty(PATH_ICONS + "idea.png")

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.transparent_black)
    line_color = ColorProperty(COLORS.white)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)

    outline_width = NumericProperty(LARGE_OUTLINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def trigger_icon_flashing(self):
        if not self.icon_mode:
            self.ids.icon.opacity = 0
        else:
            self.ids.icon.opacity = 1

        if self.icon_flashing_mode:
            self.opacity_state = -1
            self.opacity_rate = 0.05

            self.stop_icon_flashing()
            # Schedule the update for the text opacity effect
            Clock.schedule_interval(self.update_icon_opacity, 1 / FPS)

    def stop_icon_flashing(self):
        try:
            # Unschedule the clock update
            Clock.unschedule(self.update_icon_opacity, 1 / FPS)
            if self.icon_mode:
                self.ids.icon.opacity = 1
            else:
                self.ids.icon.opacity = 0
        except:
            pass

    def update_icon_opacity(self, *args):
        self.ids.icon.opacity += self.opacity_state * self.opacity_rate
        if self.ids.icon.opacity < 0 or self.ids.icon.opacity > 1:
            self.opacity_state = -self.opacity_state

    def on_press(self):
        pass

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.stop_icon_flashing()
            self.release_function()

class CharacterLayout(RelativeLayout):

    is_hurt = BooleanProperty(False)
    image_source = StringProperty()

    ### Name of the character ###

    character_name = StringProperty()
    font_size = NumericProperty(FONTS_SIZES.small_label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_OUTLINE_WIDTH)
    release_function = ObjectProperty(lambda: 1 + 1)
    font_ratio = NumericProperty(1)
