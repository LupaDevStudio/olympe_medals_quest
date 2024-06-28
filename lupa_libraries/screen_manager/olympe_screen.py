"""
Module to create an improved Kivy screen for Lemon Energy application.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from lupa_libraries.screen_manager import (
    ImprovedScreen
)
from tools.constants import (
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    SCREEN_TITLE_ICON,
    SCREEN_BACK_ARROW,
    SCREEN_CUSTOM_TITLE,
    TEXT,
    USER_DATA
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_ICONS
)

#############
### Class ###
#############


class OlympeScreen(ImprovedScreen):
    """
    Improved screen class for Olympe's Medals Quest.
    """

    # Configuration of the main widgets
    dict_type_screen: dict = {}
    title_screen = StringProperty()
    title_icon_source = StringProperty()
    money_amount = NumericProperty()

    def __init__(self, back_image_path=None, **kw):
        if back_image_path is None:
            super().__init__(
                back_image_path=PATH_BACKGROUNDS + "sport_complex.png",
                **kw)
        else:
            super().__init__(
                back_image_path=back_image_path,
                **kw)

        # Display the top bar
        if self.dict_type_screen != {}:

            top_bar = self.ids.top_bar

            # Display the title or not
            if SCREEN_TITLE_YEAR in self.dict_type_screen:
                self.title_screen = self.get_title_year()
            elif SCREEN_CUSTOM_TITLE in self.dict_type_screen:
                code = self.dict_type_screen[SCREEN_CUSTOM_TITLE]
                self.title_screen = TEXT.general[code]
            else:
                top_bar.remove_widget(self.ids.title)

            # Display the title in shape of icon or not
            if SCREEN_TITLE_ICON in self.dict_type_screen:
                self.title_icon_source = PATH_ICONS + self.dict_type_screen[
                    SCREEN_TITLE_ICON] + ".png"
            else:
                top_bar.remove_widget(self.ids.title_icon)
                
            # Display the back arrow or not
            if not SCREEN_BACK_ARROW in self.dict_type_screen:
                top_bar.remove_widget(self.ids.back_arrow)
            else:
                self.ids.back_arrow.release_function = partial(
                    self.go_to_next_screen,
                    self.dict_type_screen[SCREEN_BACK_ARROW])

            # Display the money frame or not
            if not SCREEN_MONEY_RIGHT in self.dict_type_screen:
                top_bar.remove_widget(self.ids.money_frame)
            else:
                self.money_amount = USER_DATA.game.money

        else:
            self.remove_widget(self.ids.top_bar)

        self.reload_language()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.reload_language()
        self.money_amount = USER_DATA.game.money

        # Fill scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.fill_scrollview()

    def get_title_year(self):
        year = TEXT.general["year"] + " "
        trimester = TEXT.general["trimester"] + " "
        return year + str(USER_DATA.game.year) + "\n" + trimester + str(USER_DATA.game.trimester)

    def reload_language(self):
        if SCREEN_TITLE_YEAR in self.dict_type_screen:
            self.title_screen = self.get_title_year()

        if SCREEN_CUSTOM_TITLE in self.dict_type_screen:
            code = self.dict_type_screen[SCREEN_CUSTOM_TITLE]
            self.title_screen = TEXT.general[code]

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.ids.scrollview_layout.reset_scrollview()
