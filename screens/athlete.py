"""
Module to create the athlete screen.
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

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CharacterWithMainInfoFireLayout,
    SkillsCard,
    MedalsCard
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
    SCROLLVIEW_WIDTH,
    HEADER_HEIGHT
)
from tools.data_structures import (
    Athlete
)

#############
### Class ###
#############


class AthleteScreen(OlympeScreen):
    """
    Class to manage the athlete screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "team",
        SCREEN_BACK_ARROW : "backwards",
        SCREEN_MONEY_RIGHT : True
    }
    athlete_title = StringProperty()
    team_label = StringProperty()
    is_folded = BooleanProperty()

    def reload_kwargs(self, dict_kwargs):
        self.athlete: Athlete = dict_kwargs["athlete"]
        self.athlete_title = self.athlete.first_name + " " + self.athlete.name

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.athlete

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        ### Main information card ###

        is_hurt = self.athlete.is_hurt
        health = TEXT.injuries[self.athlete.health["type_injury"]]
        if is_hurt:
            time_absent = self.athlete.health["time_absent"]
            if time_absent > 1:
                health += " - " + time_absent + " " + TEXT.general["trimesters"].lower()
            else:
                health += " - " + time_absent + " " + TEXT.general["trimester"].lower()

        self.main_info_card = CharacterWithMainInfoFireLayout(
            image_source=self.athlete.image,
            salary=self.athlete.salary,
            age=self.my_text["age"].replace("@", str(self.athlete.age)),
            fatigue=self.my_text["fatigue"].replace("@", str(self.athlete.fatigue)),
            health=health,
            font_ratio=self.font_ratio,
            fire_text=self.my_text["fire"],
            is_hurt=is_hurt,
            fire_athlete_function=self.ask_fire_athlete,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=200*self.font_ratio
        )
        scrollview_layout.add_widget(self.main_info_card)

        ### Medals ###

        if not self.is_folded:
            athlete_medals = GAME.get_medals_from_athlete(athlete_id=self.athlete.id)
            height = self.font_ratio*(HEADER_HEIGHT*2) + 100*len(athlete_medals)
        else:
            athlete_medals = {}
            height = self.font_ratio*HEADER_HEIGHT

        self.medals_card = MedalsCard(
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=height,
            medals_dict=athlete_medals,
            is_folded=self.is_folded
        )
        scrollview_layout.add_widget(self.medals_card)

        ### Skills ###

        stats_dict = self.athlete.stats
        sports_dict = self.athlete.sports
        athlete_skills = dict(stats_dict)
        athlete_skills.update(sports_dict)

        self.skills_card = SkillsCard(
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=self.font_ratio*(HEADER_HEIGHT*2) + 70*len(athlete_skills),
            skills_dict=athlete_skills
        )
        scrollview_layout.add_widget(self.skills_card)

    def ask_fire_athlete(self):
        print("TODO")

    def ask_redraw(self, widget):
        self.is_folded = not self.is_folded
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def go_to_team(self):
        self.go_to_next_screen(screen_name="team")
