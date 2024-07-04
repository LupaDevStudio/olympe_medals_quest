"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    BooleanProperty,
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty
)

### Local imports ###

from tools.constants import (
    FPS
)
from tools.graphics import(
    FONTS_SIZES,
    COLORS,
    HEADER_HEIGHT,
    LARGE_LINE_WIDTH,
    BUTTON_LINE_WIDTH
)
from tools.path import (
    PATH_TITLE_FONT,
    PATH_ICONS
)

#############
### Class ###
#############

class CharacterButtonWithIcon(ButtonBehavior, RelativeLayout):
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

    line_width = NumericProperty(LARGE_LINE_WIDTH)
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

class OlympeCard(RelativeLayout):

    header_mode = BooleanProperty(False)
    icon_mode = BooleanProperty(False)
    foldable_mode = BooleanProperty(False)
    image_mode = BooleanProperty(False)
    money_mode = BooleanProperty(False)
    button_mode = BooleanProperty(False)

    header_height = NumericProperty(HEADER_HEIGHT)
    header_text = StringProperty()

    icon_source = StringProperty()
    icon_function = ObjectProperty(lambda: 1 + 1)
    size_hint_y_icon = NumericProperty(0.6)

    is_folded = BooleanProperty(False)
    keep_line_folded = BooleanProperty(False)

    image_source = StringProperty()
    has_icon_in_image = BooleanProperty(False)
    icon_in_image_source = StringProperty()
    icon_in_image_position = ObjectProperty({"x": 0.05, "top": 0.95})
    image_release_function = ObjectProperty(lambda: 1 + 1)

    money_amount = NumericProperty()

    button_text = StringProperty()
    button_release_function = ObjectProperty(lambda: 1 + 1)
    button_disable_button = BooleanProperty(False)
    button_color = ColorProperty(COLORS.blue_olympe)
    button_pressed_color = ColorProperty(COLORS.blue_pressed_olympe)

    font_ratio = NumericProperty(1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    background_color = ColorProperty(COLORS.transparent_black)

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.bind(foldable_mode=self.apply_foldable_mode)
        self.bind(is_folded=self.apply_foldable_mode)

    def apply_foldable_mode(self, *args):
        if self.foldable_mode:
            self.icon_mode = True
            if self.is_folded:
                self.icon_source = PATH_ICONS + "plus.png"
                self.size_hint_y_icon = 0.5
            else:
                self.icon_source = PATH_ICONS + "minus.png"
                self.size_hint_y_icon = 0.5
            self.icon_function = self.parent.ask_redraw

class SportLabelButton(ButtonBehavior, RelativeLayout):

    is_selected = BooleanProperty(False)

    text = StringProperty()
    font_ratio = NumericProperty(1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    line_color = ColorProperty(COLORS.white)

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    release_function = ObjectProperty(lambda: 1 + 1)

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y):
            self.release_function()
