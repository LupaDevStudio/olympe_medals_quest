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
from kivy.uix.label import Label

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    IconPressedButton,
    OlympeCard,
    LabelWithTutorial
)
from lupa_libraries.custom_widgets import (
    CustomScrollview,
    MyScrollViewLayout
)
from tools.basic_tools import (
    load_json_file
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
    HEADER_HEIGHT,
    COLORS,
    SCROLL_VIEW_SPACING_VERTICAL,
    LABEL_HEIGHT,
    MARGIN,
    FONTS_SIZES,
    TOP_BAR_HEIGHT
)
from tools.data_structures import (
    ACTIVITIES,
    SPORTS
)
from tools.olympe import (
    get_list_full_activity_ids,
    get_activity_name_or_description
)
from tools.path import (
    PATH_CATEGORIES_ICONS,
    PATH_TEXT_FONT,
    PATH_ACTIVITIES
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

    activities_card = None
    activity_details_card = None

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
                "secrets", "break", "competition", "others"
            ]
        for category in unlocked_activity_categories:
            category_button = IconPressedButton(
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                width=width_button,
                height=width_button,
                icon_source=PATH_CATEGORIES_ICONS+category+".png",
                release_function=partial(self.fill_unlocked_activities_layout, category)
            )
            categories_layout.add_widget(category_button)

    def fill_unlocked_activities_layout(self, category: str):
        if self.activities_card is not None:
            self.remove_widget(self.activities_card)
        if self.activity_details_card is not None:
            self.remove_widget(self.activity_details_card)

        # Build the olympe card with the scrollview
        height = Window.size[1]*(0.95-TOP_BAR_HEIGHT) - self.ids.categories_card.height*1.85 - \
            2*MARGIN*self.font_ratio
        pos_y = self.ids.categories_card.y - MARGIN*self.font_ratio - height
        self.activities_card = OlympeCard(
            header_mode=True,
            header_text=TEXT.activity_categories[category]["name"],
            first_icon_mode=True,
            first_icon_source=PATH_CATEGORIES_ICONS+category+".png",
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=height,
            pos_hint={"center_x": 0.5},
            y=pos_y
        )
        activities_scrollview = CustomScrollview(
            bar_width=5*self.font_ratio,
            bar_color=COLORS.blue_olympe,
            bar_inactive_color=COLORS.blue_pressed_olympe,
            size_hint=(1, None),
            height=height-HEADER_HEIGHT*self.font_ratio-SCROLL_VIEW_SPACING_VERTICAL*self.font_ratio,
            bar_margin=8*self.font_ratio
        )
        my_scrollview_layout = MyScrollViewLayout(
            cols=1,
            spacing=10*self.font_ratio,
            padding=(10*self.font_ratio, 5*self.font_ratio, 20*self.font_ratio, SCROLL_VIEW_SPACING_VERTICAL*self.font_ratio)
        )

        # Add the elements in the scrollview
        list_activities = self.GAME.get_unlocked_activities_from_category(
            category=category,
            god_mode=SHARED_DATA.god_mode)
        if SHARED_DATA.god_mode:
            list_sports = list(SPORTS.keys())
        else:
            list_sports = self.GAME.unlocked_sports
        list_activities = get_list_full_activity_ids(
            list_activities=list_activities,
            list_sports=list_sports
        )
        for full_activity_id in list_activities:
            activity_label = LabelWithTutorial(
                font_ratio=self.font_ratio,
                text=get_activity_name_or_description(full_activity_id=full_activity_id),
                size_hint=(1, None),
                height=LABEL_HEIGHT*self.font_ratio,
                release_function=partial(self.show_activities_details, full_activity_id),
                font_size=FONTS_SIZES.label
            )
            my_scrollview_layout.add_widget(activity_label)

        activities_scrollview.add_widget(my_scrollview_layout)
        self.activities_card.add_widget(activities_scrollview)
        self.add_widget(self.activities_card)

    def show_activities_details(self, full_activity_id: str):
        if self.activity_details_card is not None:
            self.remove_widget(self.activity_details_card)

        height = self.ids.categories_card.height*0.85
        self.activity_details_card = OlympeCard(
            header_mode=True,
            header_text=get_activity_name_or_description(full_activity_id=full_activity_id),
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=height,
            pos_hint={"center_x":0.5, "y": 0.025}
        )

        # Add the label of description of the activity
        description_label = Label(
            text=get_activity_name_or_description(
                full_activity_id=full_activity_id,
                mode="description"
            ),
            font_name=PATH_TEXT_FONT,
            font_size=FONTS_SIZES.label * self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            pos_hint={"center_x": 0.5},
            height=height-HEADER_HEIGHT*self.font_ratio-2*MARGIN*self.font_ratio,
            y=MARGIN*self.font_ratio,
            halign="left",
            valign="top"
        )
        description_label.bind(size=description_label.setter('text_size'))
        self.activity_details_card.add_widget(description_label)

        self.add_widget(self.activity_details_card)

    def on_leave(self, *args):
        super().on_leave(*args)

        # Reset grid layout
        list_widgets = self.ids.categories_layout.children[:]
        for element in list_widgets:
            self.ids.categories_layout.remove_widget(element)

        # Reset activities scrollview
        if self.activities_card is not None:
            self.remove_widget(self.activities_card)
            self.activities_card = None
        
        # Reset activity details card
        if self.activity_details_card is not None:
            self.remove_widget(self.activity_details_card)
            self.activity_details_card = None
