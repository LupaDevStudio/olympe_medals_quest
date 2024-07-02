"""
Module to create the recruit screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial
import time

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    BooleanProperty
)
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterInfoWithMainSportsLayout,
    CompleteRecruitCard
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
    GAME
)
from tools.graphics import (
    MARGIN_HEIGHT,
    BUTTON_HEIGHT,
    HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    SCROLLVIEW_WIDTH
)
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class RecruitScreen(OlympeScreen):
    """
    Class to manage the recruit screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "recruit",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    recruit_title = StringProperty()
    team_label = StringProperty()
    folded_dict = {}

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.recruit

        self.team_label = my_text["team"]

        number_athletes_current = GAME.number_athletes
        if number_athletes_current <= 1:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athlete"]
        else:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                GAME.max_athletes) + my_text["athletes"]

    def on_pre_enter(self, *args):
        self.start_time = time.time()
        athlete: Athlete
        for athlete in GAME.recrutable_athletes:
            if athlete.id not in self.folded_dict:
                self.folded_dict[athlete.id] = [True, None]
        return super().on_pre_enter(*args)

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        athlete: Athlete
        for athlete in GAME.recrutable_athletes:

            if self.folded_dict[athlete.id][0]:
                athlete_skills = athlete.get_best_sports()
                height = self.font_ratio * (
                    BIG_HEADER_HEIGHT + len(athlete_skills) * SKILL_HEIGHT + MARGIN_HEIGHT*2) 

                character_card = CharacterInfoWithMainSportsLayout(
                    image_source=athlete.image,
                    is_hurt=athlete.is_hurt,
                    title_card=athlete.first_name + "\n" + athlete.name,
                    salary=athlete.salary,
                    skills_dict=athlete_skills,
                    font_ratio=self.font_ratio,
                    size_hint=(0.9, None),
                    height=height,
                    foldable_mode=True
                )

            else:

                stats_dict = athlete.stats
                sports_dict = athlete.sports
                athlete_skills = dict(stats_dict)
                athlete_skills.update(sports_dict)
                if len(athlete_skills) > 0:
                    height = self.font_ratio * (
                        HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN_HEIGHT*4 + BUTTON_HEIGHT + SKILL_HEIGHT * len(athlete_skills))
                else:
                    height = self.font_ratio * (
                        HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN_HEIGHT*3 + BUTTON_HEIGHT)

                # Sort reverse
                athlete_skills = dict(reversed(athlete_skills.items()))

                character_card = CompleteRecruitCard(
                    image_source=athlete.image,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=height,
                    font_ratio=self.font_ratio,
                    skills_dict=athlete_skills,
                    title_card=athlete.first_name + " " + athlete.name,
                    salary=athlete.salary,
                    age=TEXT.general["age"].replace("@", str(athlete.age)),
                    reputation=TEXT.general["reputation"].replace("@", str(athlete.reputation)),
                    recruit_price=athlete.recruit_price,
                    disable_button=not(GAME.can_recruit_athlete(athlete=athlete)),
                    recruit_release_function=partial(self.recruit_athlete, athlete)
                )

            self.folded_dict[athlete.id][1] = character_card
            scrollview_layout.add_widget(character_card)

    def ask_redraw(self, widget):
        for athlete_id in self.folded_dict:
            if widget == self.folded_dict[athlete_id][1]:
                self.folded_dict[athlete_id][0] = not self.folded_dict[athlete_id][0]
                break

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def recruit_athlete(self, athlete: Athlete):
        print("TODO")

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
