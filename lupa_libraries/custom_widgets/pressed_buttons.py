"""
Module to create widgets with the pressed style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty,
    ListProperty
)
from kivy.compat import string_types
from kivy.factory import Factory

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


class PressedSpinnerOption(ButtonBehavior, Label):

    font_ratio = NumericProperty(1)
    background_color = ColorProperty((0.5, 0.5, 0.5, 1))
    radius = NumericProperty(RADIUS)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        self.color = self.background_color
        # sound_mixer.play("click")
        return super().on_press()

    def on_release(self):
        self.color = self.parent.parent.text_color
        return super().on_release()


class PressedDropDown(DropDown):

    font_ratio = NumericProperty(1)
    radius = NumericProperty(RADIUS)
    background_color = ColorProperty((0, 0, 0, 1))
    background_disabled_color = ColorProperty((1, 1, 1, 1))
    pressed_color = ColorProperty((1, 1, 1, 1))
    pressed_disabled_color = ColorProperty((1, 1, 1, 1))
    text_color = ColorProperty((0, 0, 0, 1))
    disable_button = BooleanProperty(False)
    press_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container.spacing = 2

    def on_dismiss(self):
        self.scroll_y = 1
        return super().on_dismiss()


class PressedSpinner(ButtonBehavior, RelativeLayout):

    font_ratio = NumericProperty(1)
    text_color = ColorProperty((1, 1, 1, 1))
    radius = NumericProperty(RADIUS)
    font_size = NumericProperty(FONTS_SIZES.button)
    text = StringProperty()

    ### Colors ###

    background_color = ColorProperty(COLORS.blue_olympe)
    pressed_color = ColorProperty(COLORS.blue_pressed_olympe)
    background_disabled_color = ColorProperty(COLORS.gray_disable)
    pressed_disabled_color = ColorProperty(COLORS.gray_pressed_disable)
    dropdown_color = ColorProperty(COLORS.light_blue_olympe)

    ### Button behavior ###

    press_button = BooleanProperty(False)
    disable_button = BooleanProperty(False)
    confirm_function = ObjectProperty(lambda: 1 + 1)

    ### Spinner variables ###

    values = ListProperty()
    text_autoupdate = BooleanProperty(False)
    option_cls = ObjectProperty(PressedSpinnerOption)
    dropdown_cls = ObjectProperty(PressedDropDown)
    is_open = BooleanProperty(False)
    sync_height = BooleanProperty(False)

    def __init__(self, **kwargs):
        self._dropdown = None
        super().__init__(**kwargs)
        fbind = self.fbind
        build_dropdown = self._build_dropdown
        fbind('on_release', self._toggle_dropdown)
        fbind('dropdown_cls', build_dropdown)
        fbind('option_cls', build_dropdown)
        fbind('values', self._update_dropdown)
        fbind('size', self._update_dropdown_size)
        fbind('text_autoupdate', self._update_dropdown)
        build_dropdown()

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.unbind(on_select=self._on_dropdown_select)
            self._dropdown.unbind(on_dismiss=self._close_dropdown)
            self._dropdown.dismiss()
            self._dropdown = None
        cls = self.dropdown_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._dropdown = cls()
        self._dropdown.bind(on_select=self._on_dropdown_select)
        self._dropdown.bind(on_dismiss=self._close_dropdown)
        self._update_dropdown()

    def _update_dropdown_size(self, *largs):
        if not self.sync_height:
            return
        dp = self._dropdown
        if not dp:
            return

        container = dp.container
        if not container:
            return
        h = self.height
        for item in container.children[:]:
            item.height = h

    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()
        for value in values:
            item = cls(text=value)
            item.height = self.height if self.sync_height else item.height
            item.bind(on_release=lambda option: dp.select(option.text))
            dp.add_widget(item)
        if text_autoupdate:
            if values:
                if not self.text or self.text not in values:
                    self.text = values[0]
            else:
                self.text = ''

    def _toggle_dropdown(self, *largs):
        if self.values:
            self.is_open = not self.is_open

    def _close_dropdown(self, *largs):
        self.is_open = False
        self.confirm_function(self.text)

    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False

    def on_is_open(self, instance, value):

        if value:
            self._dropdown.open(self)
            self.press_button = True
            self.ids.background.height = self.size[1] + self._dropdown.height
            self.ids.background.y = self.pos[1] - self._dropdown.height

        else:
            if self._dropdown.attach_to:
                self._dropdown.dismiss()
            self.press_button = False
            self.ids.background.height = self.size[1]
            self.ids.background.y = self.pos[1]
