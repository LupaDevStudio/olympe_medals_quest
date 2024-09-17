"""
Module to create the competition results screen.
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
    ListProperty
)
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    SportLabelButton,
    SeparationLine,
    CharacterButtonWithIcon,
    FramedImage,
    OlympeCard
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_CUSTOM_TITLE
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    SCROLLVIEW_WIDTH,
    HEADER_HEIGHT,
    LARGE_LINE_WIDTH,
    BUTTON_LINE_WIDTH,
    MARGIN
)
from tools.data_structures import (
    Athlete,
    COUNTRY_NAME
)
from tools.path import (
    PATH_TEXT_FONT,
    PATH_MEDALS_IMAGES,
    PATH_FLAGS_IMAGES
)

#############
### Class ###
#############


class CompetitionResultsScreen(OlympeScreen):
    """
    Class to manage the competition results screen of the game.
    """

    dict_type_screen = {
        SCREEN_CUSTOM_TITLE: "edition",
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    previous_label = StringProperty()
    next_label = StringProperty()
    validate_label = StringProperty()
    list_sports = ListProperty([])
    selected_sport_id = NumericProperty(0)
    spent_coins = NumericProperty()

    def reload_language(self):
        super().reload_language()
        self.previous_label = TEXT.general["previous"]
        self.next_label = TEXT.general["next"]
        self.validate_label = TEXT.general["validate"]

        self.change_previous_next_buttons_text()

    def change_previous_next_buttons_text(self):
        if self.selected_sport_id == 0:
            self.ids.previous_button.opacity = 0
        else:
            self.ids.previous_button.opacity = 1
            self.ids.previous_button.text = self.previous_label

        if self.selected_sport_id == len(self.list_sports) - 1:
            self.ids.next_button.text = self.validate_label
        else:
            self.ids.next_button.text = self.next_label

    def on_pre_enter(self, *args):
        self.list_sports = self.GAME.unlocked_sports

        super().on_pre_enter(*args)

    def fill_scrollview_vertical(self):
        scrollview_layout = self.ids["scrollview_layout_vertical"]
        margin_label = 10
        total_label_width = 0

        for counter_sport in range(len(self.list_sports)):
            sport_id = self.list_sports[counter_sport]

            pos_x = self.font_ratio * (
                total_label_width + margin_label * (counter_sport+1))
            
            sport_name = TEXT.sports[sport_id]["name"]
            width_label = 11 * len(sport_name)
            if len(sport_name) <= 7:
                width_label += 8
            elif len(sport_name) >= 22:
                width_label -= 28
            elif len(sport_name) >= 17:
                width_label -= 15
            elif len(sport_name) >= 13:
                width_label -= 7
            number_long_letters = sport_name.count("m") + sport_name.count("w")
            if number_long_letters >= 2:
                width_label += 2.5 * number_long_letters
            total_label_width += width_label

            sport_button = SportLabelButton(
                text=sport_name,
                size_hint=(None, 1),
                x=pos_x,
                width=width_label*self.font_ratio,
                pos_hint={"center_y": 0.5},
                font_ratio=self.font_ratio,
                is_selected=counter_sport == self.selected_sport_id,
                release_function=partial(self.select_sport, counter_sport)
            )

            if counter_sport == self.selected_sport_id:
                self.ids.scrollview_vertical.scroll_to(sport_button)

            scrollview_layout.add_widget(sport_button)

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        list_results: list[Athlete] = self.GAME.compute_results_fight_from_sport(
            sport_id=self.list_sports[self.selected_sport_id])

        for counter in range(len(list_results)):
            athlete: Athlete = list_results[counter]
            result_athlete = counter + 1

            ### Information on the current athlete ###

            if athlete.nationality == COUNTRY_NAME:
                background_color = COLORS.transparent_blue_olympe
            else:
                background_color = COLORS.transparent
            relative_layout = OlympeCard(
                size_hint=(1, None),
                height=self.font_ratio*HEADER_HEIGHT,
                background_color=background_color,
                font_ratio=self.font_ratio
            )
            
            # Add a medal for the three first ones
            results_width = 0.085*(SCROLLVIEW_WIDTH*Window.size[0]-20*self.font_ratio)
            if result_athlete <= 3:
                type_image = "gold" if result_athlete == 1 else "silver" if result_athlete == 2 else "bronze"
                number_image = Image(
                    source=PATH_MEDALS_IMAGES+type_image+".png",
                    size_hint=(None, None),
                    height=results_width,
                    width=results_width,
                    pos_hint={"center_y": 0.5},
                    x=MARGIN*self.font_ratio
                )
                relative_layout.add_widget(number_image)
            # Just the position of the athlete
            else:
                number_label = Label(
                    text=str(result_athlete),
                    size_hint=(None, 1),
                    width=results_width,
                    pos_hint={"center_y": 0.5},
                    font_size=FONTS_SIZES.subtitle*self.font_ratio,
                    font_name=PATH_TEXT_FONT,
                    color=COLORS.white,
                    x=MARGIN*self.font_ratio
                )
                relative_layout.add_widget(number_label)
            
            # Image of the athlete
            
            image_width = self.font_ratio*HEADER_HEIGHT*0.8
            athlete_image = CharacterButtonWithIcon(
                image_source=athlete.image,
                disable_button=True,
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                height=image_width,
                width=image_width,
                pos_hint={"center_y": 0.5},
                x=results_width+2*MARGIN*self.font_ratio,
                line_width=BUTTON_LINE_WIDTH
            )
            relative_layout.add_widget(athlete_image)

            # Name of the athlete and country

            flag_height = self.font_ratio*HEADER_HEIGHT*0.5
            flag_width = 1.73*flag_height
            label_width = SCROLLVIEW_WIDTH*Window.size[0] - results_width - image_width - flag_width - MARGIN*6*self.font_ratio - 20*self.font_ratio
            name_label = Label(
                text=athlete.full_name + " - " + TEXT.countries[athlete.nationality],
                size_hint=(None, 1),
                width=label_width,
                pos_hint={"center_y": 0.5},
                x=results_width+image_width+MARGIN*3*self.font_ratio,
                font_size=FONTS_SIZES.label*self.font_ratio,
                font_name=PATH_TEXT_FONT,
                color=COLORS.white,
                halign="left",
                valign="middle"
            )
            name_label.bind(size=name_label.setter('text_size'))
            relative_layout.add_widget(name_label)

            # Image of the flag

            flag_image = FramedImage(
                image_source=PATH_FLAGS_IMAGES+athlete.nationality+".jpg",
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                height=flag_height,
                width=flag_width,
                pos_hint={"center_y": 0.5},
                x=name_label.x+label_width+MARGIN*self.font_ratio
            )
            relative_layout.add_widget(flag_image)

            # Add the layout in the scrollview
            scrollview_layout.add_widget(relative_layout)

            ### Separation line ###

            if counter != len(list_results) - 1:

                separation_line = SeparationLine(
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=LARGE_LINE_WIDTH*self.font_ratio,
                    line_width=LARGE_LINE_WIDTH
                )
                scrollview_layout.add_widget(separation_line)

    def reset_screen(self):
        # Reset scrollviews
        self.ids.scrollview_layout.reset_scrollview()
        self.ids.scrollview_layout_vertical.reset_scrollview()

        # Rebuild scrollviews
        self.fill_scrollview_vertical()
        self.fill_scrollview()
    
    def select_sport(self, sport_counter):
        self.selected_sport_id = sport_counter
        self.reset_screen()

    def go_to_previous_sport(self):
        if self.selected_sport_id != 0:
            self.selected_sport_id -= 1
            self.change_previous_next_buttons_text()
            self.reset_screen()

    def go_to_next_sport(self):
        if self.selected_sport_id != len(self.list_sports) - 1:
            self.selected_sport_id += 1
            self.change_previous_next_buttons_text()
            self.reset_screen()
        else:
            ... # TODO validate
