"""
Module to create widgets with the pressed style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.graphics import (
    Color,
    RoundedRectangle
)
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.constants import (
    FPS,
    TEXT
)
from tools.graphics import (
    COLORS,
    LARGE_OUTLINE_WIDTH,
    BUTTON_OUTLINE_WIDTH,
    FONTS_SIZES
)
from tools.path import (
    PATH_ICONS,
    PATH_TEXT_FONT
)
from tools.data_structures import (
    convert_points_to_tier_rank
)

#############
### Class ###
#############


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

    outline_width = NumericProperty(LARGE_OUTLINE_WIDTH)
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

    line_width = NumericProperty(BUTTON_OUTLINE_WIDTH)
    release_function = ObjectProperty(lambda: 1 + 1)
    font_ratio = NumericProperty(1)


class CharacterStats(RelativeLayout):

    learning_rate = NumericProperty()
    will_level_up = BooleanProperty()
    rank_letter = StringProperty()
    rank_color = ColorProperty()

    def __init__(
            self,
            stat_dict: dict,
            expected_points_after_training: float | None = None,
            ** kw):
        super().__init__(**kw)

        # Store the parameters
        self.learning_rate = stat_dict["learning_rate"]

        # Determine if the athlete will level up
        current_rank, current_level = convert_points_to_tier_rank(
            stat_dict["points"])
        if expected_points_after_training is not None:
            expected_rank, expected_level = convert_points_to_tier_rank(
                expected_points_after_training)
        else:
            expected_rank = current_rank
            expected_level = current_level
        if expected_rank != current_rank:
            self.will_level_up = True

        # Set the rank color and letter
        self.rank_letter = expected_rank
        self.rank_color = COLORS.tier_ranks[expected_rank]

        with self.canvas:
            Color(0, 0, 0, 1)
            for i in range(1, 11):
                if i <= current_level and not self.will_level_up:
                    Color(1, 1, 1, 1)
                elif i <= expected_level:
                    Color(22 / 255, 74 / 255, 87 / 255, 1)
                else:
                    Color(0, 0, 0, 1)
                RoundedRectangle(
                    pos=(self.width * (0.35 + i * 0.5)), radius=(20, 20, 20, 20), size=(0.05 * self.width, self.width / 7.9))


class CharacterWithMainInfoFireLayout(RelativeLayout):

    is_hurt = BooleanProperty(False)
    image_source = StringProperty()

    ### Information on the character ###

    salary = NumericProperty()
    age = StringProperty()
    fire_text = StringProperty()
    fatigue = StringProperty()
    health = StringProperty()

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_OUTLINE_WIDTH)
    font_ratio = NumericProperty(1)

    ### Function ###
    fire_athlete_function = ObjectProperty(lambda: 1 + 1)

class MedalsCard(RelativeLayout):
    
    ### Information on the skills ###

    medals_dict = ObjectProperty({})
    title_card = StringProperty(TEXT.general["medals"])
    is_folded = BooleanProperty(False)

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_OUTLINE_WIDTH)
    font_ratio = NumericProperty(1)

class SkillsCard(RelativeLayout):

    ### Information on the skills ###

    skills_dict = ObjectProperty({})
    title_card = StringProperty(TEXT.general["skills"])

    font_size = NumericProperty(FONTS_SIZES.label)
    text_font_name = StringProperty(PATH_TEXT_FONT)

    ### Colors ###

    background_color = ColorProperty(COLORS.transparent_black)
    font_color = ColorProperty(COLORS.white)
    line_color = ColorProperty(COLORS.white)

    line_width = NumericProperty(BUTTON_OUTLINE_WIDTH)
    font_ratio = NumericProperty(1)
