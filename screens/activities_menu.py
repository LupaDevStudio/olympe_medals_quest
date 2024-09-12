"""
Module to create the team screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    IconPressedButton
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
    SHARED_DATA
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN
)
from tools.data_structures import (
    Athlete
)
from tools.path import (
    PATH_CATEGORIES_ICONS
)

#############
### Class ###
#############


class ActivitiesMenuScreen(OlympeScreen):
    """
    Class to manage the team screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "activities_menu",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    categories_title = StringProperty()
    activities_unlocked_title = StringProperty()
    current_activity_title = StringProperty()

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.activities_menu
        self.categories_title = my_text["categories"]
        self.activities_unlocked_title = ""
        self.current_activity_title = ""

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_categories_layout()

    def fill_categories_layout(self):
        categories_layout = self.ids["categories_layout"]
        width_button = (
            Window.size[0]*SCROLLVIEW_WIDTH-6*MARGIN*self.font_ratio)/5

        unlocked_activity_categories = self.GAME.unlocked_activity_categories
        if SHARED_DATA.god_mode:
            unlocked_activity_categories = [
                "sports", "stats", "press", "job",
                "secret", "break", "competition", "others"
            ]
        for category in unlocked_activity_categories:
            category_button = IconPressedButton(
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                width=width_button,
                height=width_button,
                icon_source=PATH_CATEGORIES_ICONS+category+".png",
                release_function=partial(self.fill_unlocked_activites_layout, category)
            )
            categories_layout.add_widget(category_button)

    def fill_unlocked_activites_layout(self, category: str):
        pass

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.categories_layout.children[:]
        for element in list_widgets:
            self.ids.categories_layout.remove_widget(element)
