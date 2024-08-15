"""
Module to create the recruit screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.uix.label import Label

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterInfoWithMainSportsLayout,
    CompleteRecruitCard
)
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
    USER_DATA,
    GOD_MODE
)
from tools.path import (
    PATH_TEXT_FONT
)
from tools.graphics import (
    MARGIN,
    BUTTON_HEIGHT,
    HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    BIG_HEADER_HEIGHT,
    SKILL_HEIGHT,
    SCROLLVIEW_WIDTH,
    COLORS,
    FONTS_SIZES,
    LABEL_HEIGHT
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

        number_athletes_current = self.GAME.number_athletes
        if number_athletes_current <= 1:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                self.GAME.max_athletes) + my_text["athlete"]
        else:
            self.recruit_title = str(number_athletes_current) + " / " + str(
                self.GAME.max_athletes) + my_text["athletes"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        # No athlete to recruit
        if len(self.GAME.recrutable_athletes) == 0:
            label = Label(
                text=TEXT.recruit["no_athlete"],
                font_size=FONTS_SIZES.label * self.font_ratio,
                font_name=PATH_TEXT_FONT,
                color=COLORS.white,
                size_hint=(0.9, None),
                height=1.5*LABEL_HEIGHT*self.font_ratio,
                halign="left",
                valign="middle"
            )
            label.bind(size=label.setter('text_size'))
            scrollview_layout.add_widget(label)

        athlete: Athlete
        for athlete in self.GAME.recrutable_athletes:

            if athlete.id not in self.folded_dict:
                self.folded_dict[athlete.id] = [True, None]

            if self.folded_dict[athlete.id][0]:
                athlete_skills = athlete.get_best_sports()
                height = self.font_ratio * (
                    BIG_HEADER_HEIGHT + len(athlete_skills) * SKILL_HEIGHT + MARGIN*2) 

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
                athlete_skills = stats_dict
                athlete_skills.update(sports_dict)
                if len(athlete_skills) > 0:
                    height = self.font_ratio * (
                        HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN*4 + BUTTON_HEIGHT + SKILL_HEIGHT * len(athlete_skills))
                else:
                    height = self.font_ratio * (
                        HEADER_HEIGHT + CHARACTER_HEIGHT + MARGIN*3 + BUTTON_HEIGHT)

                # Sort reverse
                athlete_skills = dict(reversed(athlete_skills.items()))
                
                # Display reputation or not
                reputation_unlocked = "reputation" in self.GAME.unlocked_modes
                if GOD_MODE:
                    reputation_unlocked = True

                character_card = CompleteRecruitCard(
                    image_source=athlete.image,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=height,
                    font_ratio=self.font_ratio,
                    skills_dict=athlete_skills,
                    title_card=athlete.full_name,
                    salary=athlete.salary,
                    age=TEXT.general["age"].replace("@", str(athlete.age)),
                    reputation=TEXT.general["reputation"].replace(
                        "@", str(int(athlete.reputation))),
                    recruit_price=athlete.recruit_price,
                    reputation_unlocked=reputation_unlocked,
                    disable_button=not(self.GAME.can_recruit_athlete(athlete=athlete)),
                    recruit_release_function=partial(self.ask_recruit_athlete, athlete)
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

    def ask_recruit_athlete(self, athlete: Athlete):
        self.create_yes_no_popup(
            code="recruit_athlete",
            confirm_function=partial(self.recruit_athlete, athlete)
        )

    def recruit_athlete(self, athlete: Athlete):
        self.GAME.recruit_athlete(athlete=athlete)
        USER_DATA.save_changes()

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()
        self.reload_language()

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
