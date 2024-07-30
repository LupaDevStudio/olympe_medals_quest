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
    NumericProperty,
    ObjectProperty
)

### Local imports ###

from lupa_libraries.screen_manager import (
    ImprovedScreen
)
from tools.constants import (
    SCREEN_MONEY_RIGHT,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    SCREEN_TITLE_ICON,
    SCREEN_BACK_ARROW,
    SCREEN_CUSTOM_TITLE,
    TEXT,
    USER_DATA
)
from tools.path import (
    PATH_ICONS,
    PATH_BACKGROUNDS
)
from tools.data_structures import (
    Game
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
    GAME = Game()

    def __init__(self, back_image_path=None, **kw):
        if back_image_path is None:
            path_sports_complex = self.GAME.get_background_image()
            super().__init__(
                back_image_path=path_sports_complex,
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
                if code == "edition":
                    self.title_screen = TEXT.general["edition"].replace(
                        "@", str(self.GAME.current_edition))
                else:
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
                if self.dict_type_screen[SCREEN_BACK_ARROW] != "backwards":
                    self.ids.back_arrow.release_function = partial(
                        self.go_to_next_screen,
                        self.dict_type_screen[SCREEN_BACK_ARROW])
                else:
                    self.ids.back_arrow.release_function = self.go_backwards

            # Display the money frame or not
            if SCREEN_MONEY_RIGHT in self.dict_type_screen:
                self.money_amount = self.GAME.money
                self.ids.money_frame.spend_mode = False
                self.ids.money_frame.size_hint = (0.25, 0.7)
            elif SCREEN_SPEND_MONEY_RIGHT in self.dict_type_screen:
                self.money_amount = self.GAME.money
                self.ids.money_frame.spend_mode = True
                self.ids.money_frame.size_hint = (0.35, 0.7)
                self.ids.money_frame.spent_coins_count = self.spent_coins
                self.bind(spent_coins=self.update_money_frame)

                if SCREEN_CUSTOM_TITLE or SCREEN_TITLE_YEAR in self.dict_type_screen:
                    self.ids.title.pos_hint = {"center_x":0.375, "center_y":0.5}
                elif SCREEN_TITLE_ICON in self.dict_type_screen:
                    self.ids.title_icon.pos_hint = {"center_x":0.375, "center_y":0.5}
            else:
                top_bar.remove_widget(self.ids.money_frame)

        else:
            self.remove_widget(self.ids.top_bar)

        self.reload_language()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        id_game = self.manager.id_game
        if id_game == 1:
            self.GAME = USER_DATA.game_1
        elif id_game == 2:
            self.GAME = USER_DATA.game_2
        else:
            self.GAME = USER_DATA.game_3

        self.reload_language()
        if SCREEN_MONEY_RIGHT in self.dict_type_screen:
            self.money_amount = self.GAME.money

        # Fill vertical scrollview if it exists
        if "scrollview_layout_vertical" in self.ids:
            self.fill_scrollview_vertical()

        # Fill scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.fill_scrollview()

    def get_title_year(self):
        year = TEXT.general["year"] + " "
        trimester = TEXT.general["trimester"] + " "
        return year + str(self.GAME.year) + "\n" + trimester + str(self.GAME.trimester)

    def update_money_frame(self, *args):
        self.ids.money_frame.spent_coins_count = self.spent_coins

    def reload_language(self):
        if SCREEN_TITLE_YEAR in self.dict_type_screen:
            self.title_screen = self.get_title_year()

        elif SCREEN_CUSTOM_TITLE in self.dict_type_screen:
            code = self.dict_type_screen[SCREEN_CUSTOM_TITLE]
            if code == "edition":
                self.title_screen = TEXT.general["edition"].replace(
                    "@", str(self.GAME.current_edition))
            else:
                self.title_screen = TEXT.general[code]

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.ids.scrollview_layout.reset_scrollview()

        # Reset vertical scrollview if it exists
        if "scrollview_layout_vertical" in self.ids:
            self.ids.scrollview_layout_vertical.reset_scrollview()
