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
from lupa_libraries.custom_widgets import (
    OlympeMessagePopup,
    OlympeYesNoPopup,
    OlympeSpinnerPopup
)
from tools.constants import (
    SCREEN_MONEY_RIGHT,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_TITLE_YEAR,
    SCREEN_TITLE_ICON,
    SCREEN_BACK_ARROW,
    SCREEN_CUSTOM_TITLE,
    TEXT,
    USER_DATA,
    SHARED_DATA
)
from tools.graphics import (
    SCROLLVIEW_WIDTH
)
from tools.path import (
    PATH_ICONS
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
                self.ids.money_frame.size_hint = (0.25, 0.65)
            elif SCREEN_SPEND_MONEY_RIGHT in self.dict_type_screen:
                self.money_amount = self.GAME.money
                self.ids.money_frame.spend_mode = True
                self.ids.money_frame.size_hint = (0.35, 0.65)
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
        if self.name not in ["home", "settings", "save"]:
            self.set_game()
        self.reload_language()
        if SCREEN_MONEY_RIGHT in self.dict_type_screen or SCREEN_SPEND_MONEY_RIGHT in self.dict_type_screen:
            self.money_amount = self.GAME.money

        # Fill vertical scrollview if it exists
        if "scrollview_layout_vertical" in self.ids:
            self.fill_scrollview_vertical()

        # Fill scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.fill_scrollview()

    def set_game(self):
        self.GAME = SHARED_DATA.GAME

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

        elif SCREEN_MONEY_RIGHT in self.dict_type_screen:
            self.money_amount = self.GAME.money

    def set_label_text_width(self, widget, value):
        """
        Function called when creating the labels to set correctly their size.
        """
        widget.text_size = (value[0], None)

    def create_message_popup(self, code: str | None = None, confirm_function = lambda: 1 + 1, title: str | None = None, text: str | None = None):
        if text is None:
            text = TEXT.popup[code]["text"]
        if title is None:
            title = TEXT.popup[code]["title"]

        if len(text) > 450:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.8)
        elif len(text) > 300:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.6)
        else:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.4)
        popup = OlympeMessagePopup(
            title=title,
            text=text,
            font_ratio=self.font_ratio,
            path_background=self.back_image_path,
            confirm_function=confirm_function,
            popup_size_hint=popup_size_hint
        )
        popup.open()

    def create_yes_no_popup(self, code: str | None = None, title: str | None = None, text: str | None = None, confirm_function = lambda: 1 + 1, cancel_function = lambda: 1 + 1):
        if code is not None:
            text = TEXT.popup[code]["text"]
            title = TEXT.popup[code]["title"]
        if len(text) > 450:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.8)
        elif len(text) > 300:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.6)
        else:
            popup_size_hint = (SCROLLVIEW_WIDTH, 0.4)
        popup = OlympeYesNoPopup(
            title=title,
            text=text,
            font_ratio=self.font_ratio,
            path_background=self.back_image_path,
            confirm_function=confirm_function,
            cancel_function=cancel_function,
            popup_size_hint=popup_size_hint
        )
        popup.open()

    def create_spinner_popup(self, code: str, confirm_function = lambda: 1 + 1, default_value = None, values = None, sort_values: bool = True):
        if values is None:
            values = TEXT.popup[code]["values"]
        if default_value is None:
            default_value = TEXT.popup[code]["default_value"]
        if sort_values:
            values = sorted(values)
        popup = OlympeSpinnerPopup(
            popup_size_hint=(SCROLLVIEW_WIDTH, 0.4),
            title=TEXT.popup[code]["title"],
            text=TEXT.popup[code]["text"],
            font_ratio=self.font_ratio,
            path_background=self.back_image_path,
            confirm_function=confirm_function,
            values=values,
            default_value=default_value
        )
        popup.open()

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset scrollview if it exists
        if "scrollview_layout" in self.ids:
            self.ids.scrollview_layout.reset_scrollview()

        # Reset vertical scrollview if it exists
        if "scrollview_layout_vertical" in self.ids:
            self.ids.scrollview_layout_vertical.reset_scrollview()
