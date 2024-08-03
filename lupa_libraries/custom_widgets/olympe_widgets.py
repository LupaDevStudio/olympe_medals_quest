"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import (
    BooleanProperty,
    StringProperty,
    NumericProperty,
    ColorProperty,
    ObjectProperty,
    ListProperty
)

### Local imports ###

from tools.constants import (
    FPS,
    TEXT
)
from tools.data_structures import (
    Medal,
    convert_points_to_tier_rank
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    HEADER_HEIGHT,
    LARGE_LINE_WIDTH,
    BUTTON_LINE_WIDTH,
    SUBTITLE_HEIGHT,
    LABEL_HEIGHT,
    MEDAL_HEIGHT,
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    SKILL_HEIGHT,
    MARGIN,
    BUTTON_HEIGHT
)
from tools.path import (
    PATH_TITLE_FONT,
    PATH_TEXT_FONT,
    PATH_ICONS,
    PATH_CHARACTERS_IMAGES
)

#######################
### General widgets ###
#######################


class CharacterButtonWithIcon(ButtonBehavior, RelativeLayout):
    """
    A button with a character on it.
    """

    ### Image settings ###

    image_source = StringProperty()

    ### Icon settings ###

    icon_mode = BooleanProperty(False)
    icon_flashing_mode = BooleanProperty(False)
    icon_position = ObjectProperty({"x": 0.05, "top": 0.95})
    icon_source = StringProperty(PATH_ICONS + "idea.png")

    ### Colors ###

    icon_color = ColorProperty(COLORS.white)
    background_color = ColorProperty(COLORS.transparent_black)
    line_color = ColorProperty(COLORS.white)

    ### Button behavior ###

    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)

    size_hint_character = ObjectProperty((None, 0.9))
    line_width = NumericProperty(LARGE_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kwargs):
        self.always_release = True
        super().__init__(**kwargs)

    def trigger_icon_flashing(self):
        if not self.icon_mode:
            self.ids.icon.opacity = 0
        else:
            self.ids.icon.opacity = 1

        if self.icon_flashing_mode:
            self.opacity_state = -1
            self.opacity_rate = 0.05

            self.stop_icon_flashing()
            # Schedule the update for the text opacity effect
            Clock.schedule_interval(self.update_icon_opacity, 1 / FPS)

    def stop_icon_flashing(self):
        try:
            # Unschedule the clock update
            Clock.unschedule(self.update_icon_opacity, 1 / FPS)
            if self.icon_mode:
                self.ids.icon.opacity = 1
            else:
                self.ids.icon.opacity = 0
        except:
            pass

    def update_icon_opacity(self, *args):
        self.ids.icon.opacity += self.opacity_state * self.opacity_rate
        if self.ids.icon.opacity < 0 or self.ids.icon.opacity > 1:
            self.opacity_state = -self.opacity_state

    def on_press(self):
        pass

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y) and not self.disable_button:
            self.stop_icon_flashing()
            self.release_function()


class OlympeCard(RelativeLayout):

    header_mode = BooleanProperty(False)
    icon_mode = BooleanProperty(False)
    foldable_mode = BooleanProperty(False)
    image_mode = BooleanProperty(False)
    money_mode = BooleanProperty(False)
    button_mode = BooleanProperty(False)
    left_surrounded_label_mode = BooleanProperty(False)
    first_icon_mode = BooleanProperty(False)
    right_surrounded_label_mode = BooleanProperty(False)

    header_height = NumericProperty(HEADER_HEIGHT)
    header_text = StringProperty()

    icon_source = StringProperty()
    icon_function = ObjectProperty(lambda: 1 + 1)
    icon_button_color = ColorProperty(COLORS.blue_olympe)
    icon_button_color_pressed = ColorProperty(COLORS.blue_pressed_olympe)
    size_hint_y_icon = NumericProperty(0.6)

    is_folded = BooleanProperty(False)
    keep_line_folded = BooleanProperty(False)

    image_source = StringProperty()
    has_icon_in_image = BooleanProperty(False)
    icon_in_image_source = StringProperty()
    icon_in_image_position = ObjectProperty({"x": 0.05, "top": 0.95})
    image_release_function = ObjectProperty(lambda: 1 + 1)

    money_amount = NumericProperty()
    money_size_hint = ObjectProperty((0.25, 0.5))
    money_minus_mode = BooleanProperty(False)
    money_plus_mode = BooleanProperty(False)

    button_text = StringProperty()
    button_release_function = ObjectProperty(lambda: 1 + 1)
    button_disable_button = BooleanProperty(False)
    button_color = ColorProperty(COLORS.blue_olympe)
    button_pressed_color = ColorProperty(COLORS.blue_pressed_olympe)

    left_label = StringProperty()
    right_label = StringProperty()

    first_icon_source = StringProperty()
    first_icon_color = ColorProperty(COLORS.white)

    font_ratio = NumericProperty(1)

    line_offset_vertical = NumericProperty(8)
    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    background_color = ColorProperty(COLORS.transparent_black)

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.bind(foldable_mode=self.apply_foldable_mode)
        self.bind(is_folded=self.apply_foldable_mode)

    def apply_foldable_mode(self, *args):
        if self.foldable_mode:
            self.icon_mode = True
            if self.is_folded:
                self.icon_source = PATH_ICONS + "plus.png"
                self.size_hint_y_icon = 0.5
            else:
                self.icon_source = PATH_ICONS + "minus.png"
                self.size_hint_y_icon = 0.5
            self.icon_function = self.parent.ask_redraw


class SeparationLine(RelativeLayout):

    font_ratio = NumericProperty(1)


class SportLabelButton(ButtonBehavior, RelativeLayout):

    is_selected = BooleanProperty(False)

    text = StringProperty()
    font_ratio = NumericProperty(1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    line_color = ColorProperty(COLORS.white)

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    release_function = ObjectProperty(lambda: 1 + 1)

    def on_release(self):
        if self.collide_point(self.last_touch.x, self.last_touch.y):
            self.release_function()


class LabelWithTutorial(RelativeLayout):

    text = StringProperty()
    icon_source = StringProperty(PATH_ICONS + "tutorial.png")

    font_size = NumericProperty(FONTS_SIZES.small_label)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_color = ColorProperty(COLORS.white)
    icon_color = ColorProperty(COLORS.white)

    font_ratio = NumericProperty(1)

    release_function = ObjectProperty(lambda: 1 + 1)


class StatBar(RelativeLayout):
    color = ColorProperty((0, 0, 0, 1))
    font_ratio = NumericProperty(1)
    radius = NumericProperty(2)


#########################
### Character widgets ###
#########################


class CharacterWithNameLayout(RelativeLayout):

    icon_mode = BooleanProperty(False)
    icon_source = StringProperty(PATH_ICONS + "hurt.png")
    image_source = StringProperty()

    ### Name of the character ###

    character_name = StringProperty()
    font_size = NumericProperty(FONTS_SIZES.small_label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Subtitle ###

    subtitle_mode = BooleanProperty(False)
    subtitle_text = StringProperty()

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    release_function = ObjectProperty(lambda: 1 + 1)
    font_ratio = NumericProperty(1)


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
    show_level_up = BooleanProperty(False)

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    skill_height = NumericProperty(SKILL_HEIGHT)

    ### Colors ###

    font_color = ColorProperty(COLORS.white)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        idx = 0
        total_height = len(self.skills_dict) * \
            self.skill_height * self.font_ratio

        for skill in self.skills_dict:
            pos_y = (idx + 0.5) * self.skill_height * \
                self.font_ratio / total_height
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
                height=(self.skill_height - 5) * self.font_ratio,
                pos_hint={"x": 0, "center_y": pos_y},
                halign="left",
                valign="middle"
            )
            skill_label.bind(size=skill_label.setter('text_size'))
            self.add_widget(skill_label)

            if self.show_level_up:
                pos_hint = {"center_x": 0.7, "center_y": pos_y}
            else:
                pos_hint = {"x": 0.4 + 0.6 * 0.17, "center_y": pos_y}

            skill_widget = CharacterStats(
                stat_dict=self.skills_dict[skill],
                size_hint=(0.6, None),
                height=(self.skill_height - 5) * self.font_ratio,
                pos_hint=pos_hint,
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
            pos_hint={"x": 0.05},
            y=MARGIN * self.font_ratio,
            size_hint=(0.9, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
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
            total_height = (MARGIN * 2 + HEADER_HEIGHT + len(
                self.medals_list) * MEDAL_HEIGHT) * self.font_ratio

            medal: Medal
            for medal in self.medals_list:
                pos_y = (MARGIN + (idx + 0.5) * MEDAL_HEIGHT) * \
                    self.font_ratio / total_height

                year: str = TEXT.general["year"]
                sport: str = TEXT.sports[medal.sport_id]["name"]
                text = sport + " - " + year.capitalize() + " " + str(medal.year)

                width = (MEDAL_HEIGHT - 5) * self.font_ratio
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
                    height=(MEDAL_HEIGHT - 5) * self.font_ratio,
                    pos_hint={"center_y": pos_y},
                    x=width + 10 * self.font_ratio * 2,
                    halign="left",
                    valign="middle"
                )
                medal_label.bind(size=medal_label.setter('text_size'))
                self.add_widget(medal_label)

                idx += 1

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
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
            total_height = SKILL_HEIGHT * \
                len(self.skills_dict) * self.font_ratio

            character_skills_layout = CharacterSkillsLayout(
                skills_dict=self.skills_dict,
                font_ratio=self.font_ratio,
                pos_hint={"x": 0.05},
                y=MARGIN * self.font_ratio,
                size_hint=(0.9, None),
                height=total_height
            )
            self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

###########################
### Recrutement widgets ###
###########################


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
            pos_hint={"x": 0.05},
            y=(MARGIN * 2 + self.recruit_button_height) * self.font_ratio,
            size_hint=(0.9, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

###########################
### Inscription widgets ###
###########################


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
    button_color = ColorProperty(COLORS.blue_olympe)
    button_pressed_color = ColorProperty(COLORS.blue_pressed_olympe)

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
            pos_hint={"x": 0.05},
            y=(MARGIN * 2 + self.button_height) * self.font_ratio,
            size_hint=(0.9, None),
            height=total_height
        )
        self.add_widget(character_skills_layout)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
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
    button_color = ColorProperty(COLORS.blue_olympe)
    button_pressed_color = ColorProperty(COLORS.blue_pressed_olympe)

    button_text = StringProperty()
    disable_button = BooleanProperty(False)
    release_function = ObjectProperty(lambda: 1 + 1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

#############################
### Planification widgets ###
#############################


class CompletePlanificationCard(RelativeLayout):

    ### Information on the athlete ###

    title_card = StringProperty()
    image_source = StringProperty()
    is_hurt = BooleanProperty()
    total_price = NumericProperty(0)
    minus_mode = BooleanProperty()
    planning_text = StringProperty()
    list_activities = ListProperty([])

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    ### Sizes ###

    character_height = NumericProperty(CHARACTER_HEIGHT)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)
    release_function = ObjectProperty(lambda: 1 + 1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)


class SmallPlanificationCard(RelativeLayout):

    ### Information on the athlete ###

    title_card = StringProperty()
    image_source = StringProperty()
    is_hurt = BooleanProperty()
    total_price = NumericProperty()
    minus_mode = BooleanProperty()

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    ### Sizes ###

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

#####################
### Rooms widgets ###
#####################


class SmallRoomCard(RelativeLayout):

    title_card = StringProperty()

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)


class CompleteRoomCard(FloatLayout):

    title_card = StringProperty()

    image_source = StringProperty()
    price = NumericProperty()
    button_text = StringProperty()

    current_level_title = StringProperty()
    current_level_details = ListProperty()
    next_level_title = StringProperty()
    next_level_details = ListProperty()

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    buy_function = ObjectProperty(lambda: 1 + 1)
    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.fill_scrollview()

    def set_label_text_width(self, widget, value):
        """
        Function called when creating the labels to set correctly their size.
        """
        widget.text_size = (value[0], None)

    def fill_scrollview_level_content(self, scrollview_layout, title, list_content):

        ### Title ###

        title = Label(
            text=title,
            font_name=PATH_TITLE_FONT,
            font_size=FONTS_SIZES.subtitle * self.font_ratio,
            size_hint=(1, None),
            height=self.font_ratio * SUBTITLE_HEIGHT
        )
        scrollview_layout.add_widget(title)

        ### Content ###

        for element in list_content:
            text = "  - " + element["text"]
            if "release_function" in element:
                release_function = element["release_function"]
                content = LabelWithTutorial(
                    text=text,
                    size_hint=(1, None),
                    height=self.font_ratio * LABEL_HEIGHT,
                    release_function=release_function,
                    font_ratio=self.font_ratio
                )

            else:
                content = Label(
                    text=text,
                    font_name=PATH_TEXT_FONT,
                    font_size=FONTS_SIZES.small_label * self.font_ratio,
                    size_hint=(1, None),
                    height=self.font_ratio * LABEL_HEIGHT,
                    halign="left",
                    valign="middle"
                )
                content.bind(size=self.set_label_text_width)

            scrollview_layout.add_widget(content)

    def fill_scrollview(self, *args):
        scrollview_layout = self.ids["scrollview_layout_2"]

        ### Next level ###

        self.fill_scrollview_level_content(
            scrollview_layout=scrollview_layout,
            title=self.next_level_title,
            list_content=self.next_level_details
        )

        if self.current_level_details != []:

            ### Separation line ###

            separation_line = SeparationLine(
                size_hint=(1, None),
                height=0,
                font_ratio=self.font_ratio
            )
            scrollview_layout.add_widget(separation_line)

            ### Current level ###

            self.fill_scrollview_level_content(
                scrollview_layout=scrollview_layout,
                title=self.current_level_title,
                list_content=self.current_level_details
            )

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

######################
### Medals widgets ###
######################


class CompleteMedalsCard(FloatLayout):

    title_card = StringProperty()
    icon_mode = BooleanProperty(False)
    icon_source = StringProperty()

    medals_list = ListProperty([])

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    card_width = NumericProperty(1)
    card_height = NumericProperty(1)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fill_card()

    def fill_card(self):
        grid_layout = self.ids.grid_layout

        for medal_dict in self.medals_list:
            medal_card = CharacterWithNameLayout(
                font_ratio=self.font_ratio,
                subtitle_mode=True,
                icon_mode=True,
                icon_source=medal_dict["icon"],
                image_source=medal_dict["image"],
                character_name=medal_dict["title"],
                subtitle_text=medal_dict["label"],
                size_hint=(None, None),
                height=self.card_height,
                width=self.card_width
            )
            grid_layout.add_widget(medal_card)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)


class SmallMedalsCard(FloatLayout):

    title_card = StringProperty()
    icon_mode = BooleanProperty(False)
    icon_source = StringProperty()

    label = StringProperty()

    font_size = NumericProperty(FONTS_SIZES.subtitle)
    text_font_name = StringProperty(PATH_TITLE_FONT)
    font_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    def ask_redraw(self):
        current_screen_name = self.get_root_window().children[0].current
        screen = self.get_root_window().children[0].get_screen(
            current_screen_name)
        screen.ask_redraw(self)

####################
### Save widgets ###
####################


class SaveCard(FloatLayout):

    title_card = StringProperty()
    load_text = StringProperty()
    information = StringProperty()
    number_athletes_label = StringProperty()
    money = NumericProperty()

    best_athlete_image = StringProperty()

    characters_list = ListProperty([])

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    font_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_LINE_WIDTH)
    font_ratio = NumericProperty(1)

    delete_function = ObjectProperty(lambda: 1 + 1)
    launch_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fill_unlocked_characters()

    def fill_unlocked_characters(self):
        max_characters = 8
        margin_between_char = 3
        character_height = self.ids.number_athletes_label.height
        character_width = (self.width - self.ids.button.x * 3 - margin_between_char *
                           self.font_ratio * (max_characters - 1) - self.ids.button.width) / max_characters
        character_y = self.ids.number_athletes_label.y + \
            character_height + self.ids.button.y
        first_character_x = self.ids.number_athletes_label.x

        # Add each character
        for counter in range(len(self.characters_list)):
            character_id = self.characters_list[counter]
            character_x = first_character_x + counter * \
                (margin_between_char * self.font_ratio + character_width)

            character_card = CharacterButtonWithIcon(
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                height=character_height,
                width=character_width,
                x=self.x + character_x,
                y=self.y + character_y,
                image_source=PATH_CHARACTERS_IMAGES +
                f"{character_id}/neutral.png",
                disable_button=True,
                line_width=self.line_width
            )

            self.add_widget(character_card)
