"""
Module to create widgets with the pressed style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty,
    ListProperty
)

### Local imports ###

from tools.constants import (
    TEXT
)
from tools.data_structures import (
    Medal
)
from tools.graphics import (
    COLORS,
    BUTTON_LINE_WIDTH,
    BUTTON_HEIGHT,
    FONTS_SIZES,
    SKILL_HEIGHT,
    MARGIN_HEIGHT,
    HEADER_HEIGHT,
    MEDAL_HEIGHT,
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT
)
from tools.path import (
    PATH_TEXT_FONT,
    PATH_TITLE_FONT,
)
from tools.data_structures import (
    convert_points_to_tier_rank
)

#############
### Class ###
#############

class CharacterWithNameLayout(RelativeLayout):

    is_hurt = BooleanProperty(False)
    image_source = StringProperty()

    ### Name of the character ###

    character_name = StringProperty()
    font_size = NumericProperty(FONTS_SIZES.small_label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    release_function = ObjectProperty(lambda: 1 + 1)
    font_ratio = NumericProperty(1)


class StatBar(RelativeLayout):
    color = ColorProperty((0, 0, 0, 1))
    font_ratio = NumericProperty(1)
    radius = NumericProperty(2)


class CharacterWithMainInfoFireLayout(RelativeLayout):

    is_hurt = BooleanProperty(False)
    image_source = StringProperty()

    ### Information on the character ###

    salary = NumericProperty()
    age = StringProperty()
    reputation = StringProperty()
    fire_text = StringProperty()
    fatigue = StringProperty()
    health = StringProperty()

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    ### Function ###
    fire_athlete_function = ObjectProperty(lambda: 1 + 1)


class CharacterStats(RelativeLayout):

    learning_rate = NumericProperty()
    will_level_up = BooleanProperty()
    rank_letter = StringProperty()
    rank_color = ColorProperty()
    font_ratio = NumericProperty(1)
    radius = NumericProperty(2)

    def __init__(
            self,
            stat_dict: dict,
            expected_points_after_training: float | None = None,
            ** kw):
        super().__init__(**kw)

        # Store the parameters
        self.learning_rate = stat_dict["learning_rate"]

        # Determine if the athlete will level up
        self.current_rank, self.current_level = convert_points_to_tier_rank(
            stat_dict["points"])
        if expected_points_after_training is not None:
            self.expected_rank, self.expected_level = convert_points_to_tier_rank(
                expected_points_after_training)
        else:
            self.expected_rank = self.current_rank
            self.expected_level = self.current_level
        if self.expected_rank != self.current_rank:
            self.will_level_up = True
        else:
            self.will_level_up = False

        # Set the rank color and letter
        self.rank_letter = self.expected_rank
        self.rank_color = COLORS.tier_ranks[self.expected_rank]

        for i in range(1, 11):
            for i in range(1, 11):
                if i <= self.current_level and not self.will_level_up:
                    color = COLORS.white
                elif i <= self.expected_level:
                    color = COLORS.blue_pressed_olympe
                else:
                    color = COLORS.black
                current_bar = StatBar(
                    pos_hint={"center_x": 0.35 + 0.05 * i, "center_y": 0.5},
                    size_hint=(0.1, 1),
                    color=color,
                    font_ratio=self.font_ratio
                )
                self.add_widget(current_bar)

class CharacterSkillsLayout(RelativeLayout):

    ### Information on the skills ###

    skills_dict = ObjectProperty({})

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    skill_height = NumericProperty(SKILL_HEIGHT)

    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        idx = 0
        total_height = len(self.skills_dict) * self.skill_height * self.font_ratio

        for skill in self.skills_dict:
            pos_y = (idx+0.5) * self.skill_height *self.font_ratio / total_height
            if skill in TEXT.stats:
                text = TEXT.stats[skill]
            elif skill in TEXT.sports:
                text = TEXT.sports[skill]["name"]

            skill_label = Label(
                text=text,
                font_size=FONTS_SIZES.label * self.font_ratio,
                font_name=PATH_TITLE_FONT,
                color=COLORS.white,
                size_hint=(0.5, None),
                height=(self.skill_height-5)*self.font_ratio,
                pos_hint={"x": 0, "center_y": pos_y},
                halign="left",
                valign="middle"
            )
            skill_label.bind(size=skill_label.setter('text_size'))
            self.add_widget(skill_label)

            skill_widget = CharacterStats(
                stat_dict=self.skills_dict[skill],
                size_hint=(0.6, None),
                height=(self.skill_height-5)*self.font_ratio,
                pos_hint={"center_x": 0.7, "center_y": pos_y},
                font_ratio=self.font_ratio
            )
            self.add_widget(skill_widget)
            idx += 1

class CharacterInfoWithMainSportsLayout(RelativeLayout):

    ### Information on the athlete ###

    skills_dict = ObjectProperty({})
    title_card = StringProperty()
    foldable_mode = BooleanProperty(False)
    is_folded = BooleanProperty(True)
    is_hurt = BooleanProperty(False)
    image_source = StringProperty()
    image_release_function = ObjectProperty(lambda: 1 + 1)
    salary = NumericProperty()
    header_height = NumericProperty(BIG_HEADER_HEIGHT)

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        total_height = SKILL_HEIGHT * len(self.skills_dict) * self.font_ratio

        character_skills_layout = CharacterSkillsLayout(
            skills_dict=self.skills_dict,
            font_ratio=self.font_ratio,
            pos_hint={"x":0.025},
            y=MARGIN_HEIGHT * self.font_ratio,
            size_hint=(0.95, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)

class MedalsCard(RelativeLayout):

    ### Information on the skills ###

    medals_list = ListProperty([])
    title_card = StringProperty(TEXT.general["medals"])
    is_folded = BooleanProperty(False)

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        if not self.is_folded:

            idx = 0
            total_height = (MARGIN_HEIGHT*2 + HEADER_HEIGHT + len(
                self.medals_list) * MEDAL_HEIGHT) * self.font_ratio

            medal: Medal
            for medal in self.medals_list:
                pos_y = (MARGIN_HEIGHT + (idx+0.5) * MEDAL_HEIGHT)*self.font_ratio / total_height
                
                year: str = TEXT.general["year"]
                sport: str = TEXT.sports[medal.sport_id]["name"]
                text = sport + " - " + year.capitalize() + " " + str(medal.year)

                width = (MEDAL_HEIGHT-5)*self.font_ratio
                medal_image = Image(
                    source=medal.image,
                    size_hint=(None, None),
                    height=width,
                    width=width,
                    pos_hint={"x": 0.03, "center_y": pos_y}
                )
                self.add_widget(medal_image)

                medal_label = Label(
                    text=text,
                    font_size=FONTS_SIZES.label * self.font_ratio,
                    font_name=PATH_TITLE_FONT,
                    color=COLORS.white,
                    size_hint=(0.5, None),
                    height=(MEDAL_HEIGHT-5)*self.font_ratio,
                    pos_hint={"center_y": pos_y},
                    x=width+10*self.font_ratio*2,
                    halign="left",
                    valign="middle"
                )
                medal_label.bind(size=medal_label.setter('text_size'))
                self.add_widget(medal_label)

                idx += 1

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)

class SkillsCard(RelativeLayout):

    ### Information on the skills ###

    skills_dict = ObjectProperty({})
    title_card = StringProperty(TEXT.general["skills"])
    is_folded = BooleanProperty(False)

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        if not self.is_folded:
            total_height = SKILL_HEIGHT * len(self.skills_dict) * self.font_ratio

            character_skills_layout = CharacterSkillsLayout(
                skills_dict=self.skills_dict,
                font_ratio=self.font_ratio,
                pos_hint={"x":0.025},
                y=MARGIN_HEIGHT * self.font_ratio,
                size_hint=(0.95, None),
                height=total_height
            )
            self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)

class CompleteRecruitCard(RelativeLayout):

    ### Information on the athlete ###

    skills_dict = ObjectProperty({})
    title_card = StringProperty()
    image_source = StringProperty()
    age = StringProperty()
    reputation = StringProperty()
    salary = NumericProperty()
    recruit_price = NumericProperty()

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    ### Sizes ###

    recruit_button_height = NumericProperty(BUTTON_HEIGHT)
    character_height = NumericProperty(CHARACTER_HEIGHT)

    disable_button = BooleanProperty(False)
    recruit_release_function = ObjectProperty(lambda: 1 + 1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        total_height = SKILL_HEIGHT * len(self.skills_dict) * self.font_ratio

        character_skills_layout = CharacterSkillsLayout(
            skills_dict=self.skills_dict,
            font_ratio=self.font_ratio,
            pos_hint={"x":0.025},
            y=(MARGIN_HEIGHT*2 + self.recruit_button_height) * self.font_ratio,
            size_hint=(0.95, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)

class CompleteInscriptionCard(RelativeLayout):


    ### Information on the athlete ###

    skills_dict = ObjectProperty({})
    title_card = StringProperty()
    image_source = StringProperty()
    best_medal_source = StringProperty()
    fatigue_evolution = StringProperty()
    health = StringProperty()
    wound_risk = StringProperty()

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    ### Sizes ###

    button_height = NumericProperty(BUTTON_HEIGHT)
    character_height = NumericProperty(CHARACTER_HEIGHT)

    button_text = StringProperty()
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        total_height = SKILL_HEIGHT * len(self.skills_dict) * self.font_ratio

        character_skills_layout = CharacterSkillsLayout(
            skills_dict=self.skills_dict,
            font_ratio=self.font_ratio,
            pos_hint={"x":0.025},
            y=(MARGIN_HEIGHT*2 + self.button_height) * self.font_ratio,
            size_hint=(0.95, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)

class SmallInscriptionCard(RelativeLayout):

    ### Information on the athlete ###

    title_card = StringProperty()
    image_source = StringProperty()
    best_medal_source = StringProperty()

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    ### Sizes ###

    button_text = StringProperty()
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(current_screen_name)
        screen.ask_redraw(self)
