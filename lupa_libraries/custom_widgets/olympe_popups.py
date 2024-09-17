"""
Module to create popups for the game.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.popup import Popup
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
    TEXT
)
from tools.graphics import (
    FONTS_SIZES,
    COLORS,
    SCROLLVIEW_WIDTH,
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
    PATH_BACKGROUNDS
)
from tools.data_structures import (
    Athlete,
    Sport,
    Activity,
    SPORTS,
    ACTIVITIES
)
from tools.olympe import (
    get_activity_name_or_description
)
from lupa_libraries.custom_widgets import (
    OlympeCard,
    SeparationLine,
    CharacterSkillsLayout
)

###############
### Classes ###
###############


class OlympePopup(Popup):
    # Colors
    true_background_color = ColorProperty(COLORS.transparent_black)
    border_color = ColorProperty(COLORS.white)
    path_background = StringProperty()

    popup_size_hint = ObjectProperty((SCROLLVIEW_WIDTH, 0.8))

    # Font
    font_color = ColorProperty(COLORS.white)
    text_font_name = StringProperty(PATH_TEXT_FONT)
    title_font_name = StringProperty(PATH_TITLE_FONT)
    font_size = NumericProperty(FONTS_SIZES.subtitle)

    # Font ratio
    font_ratio = NumericProperty(1)

    # Width for the border
    border_width = NumericProperty(LARGE_LINE_WIDTH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.black_background = OlympeCard(
            font_ratio=self.font_ratio,
            header_mode=True,
            size_hint=(None, None),
            size=(self.popup_size_hint[0]*Window.size[0], self.popup_size_hint[1]*Window.size[1]),
            x=(1-self.popup_size_hint[0])/2*Window.size[0],
            y=(1-self.popup_size_hint[1])/2*Window.size[1],
            header_text=self.title
        )
        self.ids.popup_layout.add_widget(self.black_background, 100)

        background_image = Image(
            source=self.path_background,
            size_hint=(None, None),
            size=Window.size,
            pos=(0, 0),
            fit_mode="cover"
        )
        self.ids.popup_layout.add_widget(background_image, 100)

        buttons_separation_line = SeparationLine(
            font_ratio=self.font_ratio,
            size_hint=(None, None),
            width=self.popup_size_hint[0]*Window.size[0]-16*self.font_ratio,
            x=((1-self.popup_size_hint[0])/2)*Window.size[0]+8*self.font_ratio,
            y=(1-self.popup_size_hint[1])/2*Window.size[1]+(BUTTON_HEIGHT+2*MARGIN)*self.font_ratio,
            line_width=LARGE_LINE_WIDTH
        )
        self.ids.popup_layout.add_widget(buttons_separation_line)

class OlympeMessagePopup(OlympePopup):
    """
    Class to create a popup with a message and a confirm button.
    """

    text = StringProperty()
    font_size_text = StringProperty(FONTS_SIZES.label)
    text_filling_ratio = NumericProperty(0.98)

    button_text = StringProperty()

    confirm_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_text = TEXT.popup["close"]

    def confirm(self):
        self.dismiss()
        self.confirm_function()

class OlympeYesNoPopup(OlympePopup):
    """
    Class to create a popup with a message and two buttons.
    """

    text = StringProperty()
    font_size_text = StringProperty(FONTS_SIZES.label)
    text_filling_ratio = NumericProperty(0.98)

    cancel_button_text = StringProperty()
    confirm_button_text = StringProperty()

    cancel_function = ObjectProperty(lambda: 1 + 1)
    confirm_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confirm_button_text = TEXT.popup["yes"]
        self.cancel_button_text = TEXT.popup["no"]

    def confirm(self):
        self.dismiss()
        self.confirm_function()

    def cancel(self):
        self.dismiss()
        self.cancel_function()

class OlympeSpinnerPopup(OlympePopup):
    """
    Class to create a popup with a message, a spinner and a confirm button.
    """

    ### Text options ###

    text = StringProperty()
    font_size_text = StringProperty(FONTS_SIZES.label)
    text_filling_ratio = NumericProperty(0.98)

    ### Spinner options ###

    default_value = StringProperty()
    values = ListProperty()

    ### Button options ###

    button_text = StringProperty()
    confirm_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_text = TEXT.popup["validate"]

    def confirm(self):
        self.dismiss()
        self.confirm_function(self.ids.spinner.text)

class OlympePlanificationPopup(OlympePopup):
    """
    Class to create a popup for the planification.
    """

    athlete: Athlete = ObjectProperty()

    ### Money options ###

    gain = NumericProperty(0)
    money_amount = NumericProperty(0)
    money_minus_mode = BooleanProperty(False)
    money_plus_mode = BooleanProperty(False)

    ### Texts options ###

    category_title = StringProperty()
    activity_title = StringProperty()
    font_size_text = StringProperty(FONTS_SIZES.label)
    take_all_trimester_text = StringProperty()

    ### Spinners options ###

    code_default_category = StringProperty() # code of the default category
    default_category = StringProperty() # name of the default category
    code_values_category = ListProperty() # code values of the categories
    values_category = ListProperty() # name values of the categories

    all_unlocked_activities = ListProperty() # code of all unlocked activities
    code_default_activity = StringProperty() # code of the default activity
    default_activity = StringProperty() # name of the default activity
    code_values_activity = ListProperty() # code values of the activities
    values_activity = ListProperty() # name values of the activities

    create_message_popup_function = ObjectProperty(lambda : 1 + 1) # function to open a message popup like in the Olympe screen

    ### Button options ###

    number_activity = NumericProperty()
    cancel_button_text = StringProperty()
    confirm_button_text = StringProperty()
    confirm_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confirm_button_text = TEXT.popup["validate"]
        self.cancel_button_text = TEXT.popup["cancel"]

        # Update the values of the spinners

        self.default_category = TEXT.activity_categories[self.code_default_category]["name"]
        self.values_category = []
        for id in self.code_values_category:
            self.values_category.append(TEXT.activity_categories[id]["name"])

        self.default_activity = get_activity_name_or_description(
            full_activity_id=self.code_default_activity)
        self.build_values_activity()
        self.choose_activity(activity=self.default_activity)

        # Update the money

        self.black_background.money_mode = True
        self.update_cost()

    def build_values_activity(self):
        self.values_activity = []
        self.code_values_activity = []
        for activity_id in self.all_unlocked_activities:
            activity: Activity = ACTIVITIES[activity_id]
            # If it's the right category
            if activity.category == self.code_default_category:
                self.code_values_activity.append(activity_id)
                self.values_activity.append(
                    get_activity_name_or_description(full_activity_id=activity_id))

    def update_cost(self):
        self.money_amount = abs(self.gain)
        if self.gain > 0:
            self.money_minus_mode = False
            self.money_plus_mode = True
        elif self.gain < 0:
            self.money_minus_mode = True
            self.money_plus_mode = False
        else:
            self.money_minus_mode = False
            self.money_plus_mode = False

        self.black_background.money_amount = self.money_amount
        self.black_background.money_minus_mode = self.money_minus_mode
        self.black_background.money_plus_mode = self.money_plus_mode

    def open_details_category(self):
        category_index = self.values_category.index(self.ids.category_spinner.text)
        category_id: str = self.code_values_category[category_index]
        self.create_message_popup_function(
            title=TEXT.activity_categories[category_id]["name"],
            text=TEXT.activity_categories[category_id]["description"]
        )

    def open_details_activity(self):
        activity_index = self.values_activity.index(self.ids.activity_spinner.text)
        full_activity_id: str = self.code_values_activity[activity_index]
        self.create_message_popup_function(
            title=self.ids.activity_spinner.text,
            text=get_activity_name_or_description(
                full_activity_id=full_activity_id,
                mode="description")
        )

    def choose_category(self, category: str):
        # Get the default category
        category_index = self.values_category.index(category)
        self.code_default_category = self.code_values_category[category_index]

        # Update the spinner of activities
        self.build_values_activity()
        self.default_activity = self.values_activity[0]
        self.choose_activity(activity=self.default_activity)

    def choose_activity(self, activity: str):
        activity_index = self.values_activity.index(self.ids.activity_spinner.text)
        activity: Activity = ACTIVITIES[self.code_values_activity[activity_index]]
        
        # Indicate if it lasts all trimester or not
        if activity.all_trimester:
            self.take_all_trimester_text = TEXT.schedule["take_all_trimester"]
        else:
            self.take_all_trimester_text = ""

        # Update the counter of money
        self.gain = activity.gain - activity.price
        self.update_cost()

        # Show the effects of this activity
        print("TODO")

    def confirm(self):
        self.dismiss()
        activity_index = self.values_activity.index(self.ids.activity_spinner.text)
        activity_chosen: str = self.code_values_activity[activity_index]
        self.confirm_function(
            self.number_activity,
            activity_chosen)

    def cancel(self):
        self.dismiss()

class OlympeAthletePopup(OlympePopup):
    """
    Class to create a popup with an athlete card and a confirm button.
    """

    ### Athlete information ###

    title_skills = StringProperty()
    age = StringProperty()
    salary = NumericProperty()
    image = StringProperty()
    skills_dict = ObjectProperty({})

    ### Text options ###

    font_size_text = StringProperty(FONTS_SIZES.label)

    ### Button options ###

    button_text = StringProperty()
    confirm_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_text = TEXT.popup["close"]

        skills_card = CharacterSkillsLayout(
            font_ratio=self.font_ratio,
            skills_dict=self.skills_dict,
            size_hint=(0.9, None),
            height=(SKILL_HEIGHT*6 + MARGIN*5)*self.font_ratio,
            pos_hint={"center_x": 0.5},
            y=((1-self.popup_size_hint[1])/2)*Window.size[1]+8*self.font_ratio + self.ids.confirm_button.height + 3*MARGIN*self.font_ratio
        )
        self.ids.popup_layout.add_widget(skills_card)

    def confirm(self):
        self.dismiss()
        self.confirm_function()
