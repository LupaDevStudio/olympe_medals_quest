"""
Module to create the competition inscriptions screen.
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
    ListProperty,
    ObjectProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    SportLabelButton,
    CompleteInscriptionCard,
    SmallInscriptionCard
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_SPEND_MONEY_RIGHT,
    SCREEN_CUSTOM_TITLE,
    GAME
)
from tools.graphics import (
    HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    MARGIN_HEIGHT,
    BUTTON_HEIGHT,
    SKILL_HEIGHT,
    SCROLLVIEW_WIDTH,
    BIG_HEADER_HEIGHT,
    COLORS
)
from tools.data_structures import (
    Athlete,
    Sport,
    SPORTS,
    MAX_ATHLETES_TO_SELECT
)
from tools.olympe import (
    get_health_string
)

#############
### Class ###
#############


class CompetitionInscriptionsScreen(OlympeScreen):
    """
    Class to manage the competition inscriptions screen of the game.
    """

    dict_type_screen = {
        SCREEN_CUSTOM_TITLE: "edition",
        SCREEN_BACK_ARROW : "game",
        SCREEN_SPEND_MONEY_RIGHT : True
    }
    cancel_label = StringProperty()
    previous_label = StringProperty()
    next_label = StringProperty()
    validate_label = StringProperty()
    list_sports = ListProperty([])
    selected_sport_counter = NumericProperty(0)
    athlete_folded_dict = ObjectProperty({})
    spent_coins = NumericProperty()
    spent_coins_in_current_sport = NumericProperty(0)
    left_label = StringProperty()

    def reload_language(self):
        super().reload_language()
        self.cancel_label = TEXT.general["cancel"]
        self.previous_label = TEXT.general["previous"]
        self.next_label = TEXT.general["next"]
        self.validate_label = TEXT.general["validate"]

        self.change_previous_next_buttons_text()

    def change_previous_next_buttons_text(self):
        if self.selected_sport_counter == 0:
            self.ids.previous_button.text = self.cancel_label
        else:
            self.ids.previous_button.text = self.previous_label

        if self.selected_sport_counter == len(self.list_sports) - 1:
            self.ids.next_button.text = self.validate_label
        else:
            self.ids.next_button.text = self.next_label

    def on_pre_enter(self, *args):
        self.list_sports = GAME.sports_unlocked

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
                is_selected=counter_sport == self.selected_sport_counter,
                release_function=partial(self.select_sport, counter_sport)
            )

            if counter_sport == self.selected_sport_counter:
                self.ids.scrollview_vertical.scroll_to(sport_button)

            scrollview_layout.add_widget(sport_button)

    def fill_scrollview(self):

        selected_sport_id = self.list_sports[self.selected_sport_counter]
        sport: Sport = SPORTS[selected_sport_id]
        sport_stats = sport.stats

        self.left_label = TEXT.competition_inscriptions["number_athletes"].replace(
            "@", str(GAME.get_number_athletes_selected_for_sport(sport_id=selected_sport_id))).replace(
                "€", str(MAX_ATHLETES_TO_SELECT))
        self.spent_coins_in_current_sport = GAME.get_price_selection_for_sport(
            sport_id=selected_sport_id
        )

        if self.athlete_folded_dict == {}:
            for athlete in GAME.team:
                if selected_sport_id in athlete.sports:
                    self.athlete_folded_dict[athlete.id] = [False, None]

        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in GAME.team:
            if selected_sport_id in athlete.sports:
                athlete_skills = {
                    selected_sport_id: athlete.sports[selected_sport_id]
                }
                for stat in sport_stats:
                    athlete_skills[stat] = athlete.stats[stat]

                best_medal_source = GAME.get_best_medal_source_from_athlete_in_sport(
                            athlete_id=athlete.id, sport_id=selected_sport_id)
                
                selection_information = GAME.can_select_athlete(
                    athlete=athlete,
                    sport_id=selected_sport_id
                )
                if selection_information["already_selected"]:
                    button_text = TEXT.competition_inscriptions["unselect"]
                    button_color = COLORS.red
                    button_pressed_color = COLORS.red_pressed
                else:
                    button_text = TEXT.competition_inscriptions["select"]
                    button_color = COLORS.blue_olympe
                    button_pressed_color = COLORS.blue_pressed_olympe
                disable_button = not selection_information["can_select"]

                if self.athlete_folded_dict[athlete.id][0]:
                    inscription_card = SmallInscriptionCard(
                        title_card=athlete.first_name + "\n" + athlete.name,
                        image_source=athlete.image,
                        font_ratio=self.font_ratio,
                        best_medal_source=best_medal_source,
                        disable_button=disable_button,
                        release_function=partial(self.select_athlete, athlete),
                        button_text=button_text,
                        button_color=button_color,
                        button_pressed_color=button_pressed_color,
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=BIG_HEADER_HEIGHT*self.font_ratio,
                    )
                
                else:

                    if len(athlete_skills) > 0:
                        height = self.font_ratio * (
                            HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN_HEIGHT*4 + BUTTON_HEIGHT + SKILL_HEIGHT * len(athlete_skills))
                    else:
                        height = self.font_ratio * (
                            HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN_HEIGHT*3 + BUTTON_HEIGHT)

                    inscription_card = CompleteInscriptionCard(
                        title_card=athlete.first_name + " " + athlete.name,
                        font_ratio=self.font_ratio,
                        skills_dict=athlete_skills,
                        image_source=athlete.image,
                        health=get_health_string(athlete=athlete),
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=height,
                        fatigue_evolution="TODO",
                        wound_risk="TODO",
                        button_text=button_text,
                        button_color=button_color,
                        button_pressed_color=button_pressed_color,
                        best_medal_source=best_medal_source,
                        disable_button=disable_button,
                        release_function=partial(self.select_athlete, athlete)
                    )

                self.athlete_folded_dict[athlete.id][1] = inscription_card
                scrollview_layout.add_widget(inscription_card)

    def select_athlete(self, athlete: Athlete):
        GAME.select_unselect_athlete(
            athlete_id=athlete.id,
            sport_id=self.list_sports[self.selected_sport_counter]
        )
        self.spent_coins = GAME.compute_total_spent_money_selection()
        self.ids.money_frame.spent_coins_count = self.spent_coins

        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def ask_redraw(self, widget):
        for athlete_id in self.athlete_folded_dict:
            if widget == self.athlete_folded_dict[athlete_id][1]:
                self.athlete_folded_dict[athlete_id][0] = not self.athlete_folded_dict[athlete_id][0]
                break
        
        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def reset_screen(self):
        self.athlete_folded_dict = {}

        # Reset scrollviews
        self.ids.scrollview_layout.reset_scrollview()
        self.ids.scrollview_layout_vertical.reset_scrollview()

        # Rebuild scrollviews
        self.fill_scrollview_vertical()
        self.fill_scrollview()
    
    def select_sport(self, sport_counter):
        self.selected_sport_counter = sport_counter
        self.reset_screen()

    def go_to_previous_sport(self):
        if self.selected_sport_counter != 0:
            self.selected_sport_counter -= 1
            self.change_previous_next_buttons_text()
            self.reset_screen()
        else:
            self.go_to_next_screen(screen_name="game")

    def go_to_next_sport(self):
        if self.selected_sport_counter != len(self.list_sports) - 1:
            self.selected_sport_counter += 1
            self.change_previous_next_buttons_text()
            self.reset_screen()
        else:
            ... # TODO validate
