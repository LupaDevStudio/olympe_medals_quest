"""
Module to create widgets with the pressed style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.graphics import (
    COLORS,
    FONTS_SIZES,
    RADIUS
)
from tools.path import (
    PATH_TITLE_FONT
)

#############
### Class ###
#############


class PressedThemeBackground(Widget):

    ### Colors ###

    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Button behavior ###

    press_button = BooleanProperty(False)
    disable_button = BooleanProperty(False)
    
    radius = NumericProperty(RADIUS)
    font_ratio = NumericProperty(1)


class PressedButton(ButtonBehavior, RelativeLayout):
    """
    A customizable button with the Pressed theme.
    """

    ### Label settings ###

    text = StringProperty()
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(FONTS_SIZES.button)
    text_font_name = StringProperty(PATH_TITLE_FONT)

    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    disabled_font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.press_button = True

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        if not self.disable_button:
            self.press_button = False


class IconPressedButton(ButtonBehavior, RelativeLayout):
    """
    A customizable button with an icon on the Pressed theme.
    """

    ### Icon settings ###

    icon_source = StringProperty()
    size_hint_y_icon = NumericProperty(0.5)

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    disabled_icon_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.press_button = True

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        if not self.disable_button:
            self.press_button = False


class PressedWithIconButton(ButtonBehavior, RelativeLayout):
    """
    A customizable button with a text and an icon on the left on the Pressed theme.
    """

    ### Icon settings ###

    icon_source = StringProperty()
    size_hint_y_icon = NumericProperty(0.5)

    ### Label settings ###

    text = StringProperty()
    font_size = NumericProperty(FONTS_SIZES.button)
    text_font_name = StringProperty(PATH_TITLE_FONT)

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    disabled_icon_color = ColorProperty(COLORS.white)
    font_color = ColorProperty(COLORS.white)
    disabled_font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.press_button = True

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        if not self.disable_button:
            self.press_button = False

class TextMoneyLayoutPressedButton(ButtonBehavior, RelativeLayout):
    """
    A customizable button with a text and the money layout on the right on the Pressed theme.
    """

    ### Money layout settings ###

    coins_amount = NumericProperty()

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    disabled_icon_color = ColorProperty(COLORS.white)
    font_color = ColorProperty(COLORS.white)
    disabled_font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.press_button = True

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        if not self.disable_button:
            self.press_button = False

class TextMoneyLayoutUnderPressedButton(ButtonBehavior, RelativeLayout):
    """
    A customizable button with a text and the money layout under on the Pressed theme.
    """

    ### Content settings ###

    text = StringProperty()
    coins_amount = NumericProperty()

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    disabled_icon_color = ColorProperty(COLORS.white)
    font_color = ColorProperty(COLORS.white)
    disabled_font_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)

    ### Label settings ###

    font_size = NumericProperty(FONTS_SIZES.button)
    text_font_name = StringProperty(PATH_TITLE_FONT)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def on_press(self):
        if not self.disable_button:
            self.press_button = True

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.release_function()
        if not self.disable_button:
            self.press_button = False
