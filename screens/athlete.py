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
from tools.constants import (
    TEXT,
    SCREEN_BACK_ARROW,
    SCREEN_MONEY_RIGHT,
    SCREEN_TITLE_ICON,
    GAME,
    USER_DATA
)
from tools.graphics import (
    SCROLLVIEW_WIDTH,
    HEADER_HEIGHT,
    MARGIN_HEIGHT,
    MEDAL_HEIGHT,
    SKILL_HEIGHT
)
from tools.data_structures import (
    Athlete
)
from tools.olympe import (
    get_health_string
)

#############
### Class ###
#############


class AthleteScreen(OlympeScreen):
    """
    Class to manage the athlete screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON: "team",
        SCREEN_BACK_ARROW: "backwards",
        SCREEN_MONEY_RIGHT: True
    }
    athlete_title = StringProperty()
    team_label = StringProperty()
    medals_folded = BooleanProperty(False)
    skills_folded = BooleanProperty(False)

    def reload_kwargs(self, dict_kwargs):
        self.athlete: Athlete = dict_kwargs["athlete"]
        self.athlete_title = self.athlete.first_name + " " + self.athlete.name

    def reload_language(self):
        super().reload_language()
        self.my_text = TEXT.athlete

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        ### Main information card ###

        self.main_info_card = CharacterWithMainInfoFireLayout(
            image_source=self.athlete.image,
            salary=self.athlete.salary,
            age=TEXT.general["age"].replace("@", str(self.athlete.age)),
            reputation=TEXT.general["reputation"].replace("@", str(self.athlete.reputation)),
            fatigue=self.my_text["fatigue"].replace(
                "@", str(self.athlete.fatigue)),
            health=get_health_string(athlete=self.athlete),
            font_ratio=self.font_ratio,
            fire_text=self.my_text["fire"],
            is_hurt=self.athlete.is_hurt,
            fire_athlete_function=self.ask_fire_athlete,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=250 * self.font_ratio
        )
        scrollview_layout.add_widget(self.main_info_card)

        ### Medals ###

        if not self.medals_folded:
            athlete_medals = GAME.get_medals_from_athlete(
                athlete_id=self.athlete.id)
            if len(athlete_medals) > 0:
                height = self.font_ratio * (
                    HEADER_HEIGHT + MARGIN_HEIGHT*2 + MEDAL_HEIGHT * len(athlete_medals))
            else:
                height = self.font_ratio * HEADER_HEIGHT * 2
        else:
            athlete_medals = []
            height = self.font_ratio * HEADER_HEIGHT

        self.medals_card = MedalsCard(
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=height,
            medals_list=athlete_medals,
            is_folded=self.medals_folded
        )
        scrollview_layout.add_widget(self.medals_card)

        ### Skills ###

        if not self.skills_folded:
            stats_dict = self.athlete.stats
            sports_dict = self.athlete.sports
            athlete_skills = dict(stats_dict)
            athlete_skills.update(sports_dict)

            # Sort reverse
            athlete_skills = dict(reversed(athlete_skills.items()))

            if len(athlete_skills) > 0:
                height = self.font_ratio * (
                    HEADER_HEIGHT + MARGIN_HEIGHT*2 + SKILL_HEIGHT * len(athlete_skills))
            else:
                height = self.font_ratio * HEADER_HEIGHT * 2
        else:
            athlete_skills = {}
            height = self.font_ratio * HEADER_HEIGHT

        self.skills_card = SkillsCard(
            font_ratio=self.font_ratio,
            size_hint=(SCROLLVIEW_WIDTH, None),
            height=height,
            skills_dict=athlete_skills,
            is_folded=self.skills_folded
        )
        scrollview_layout.add_widget(self.skills_card)

    def ask_fire_athlete(self):
        print("TODO fire athlete")

    def fire_athlete(self):
        GAME.fire_athlete(athlete_id=self.athlete.id)
        USER_DATA.save_changes()

    def ask_redraw(self, widget):
        if widget == self.medals_card:
            self.medals_folded = not self.medals_folded
        elif widget == self.skills_card:
            self.skills_folded = not self.skills_folded

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()
