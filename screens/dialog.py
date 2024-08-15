"""
Module to create the dialog screen.
"""

###############
### Imports ###
###############

### Python imports ###

from functools import partial

### Kivy imports ###

from kivy.properties import (
    BooleanProperty
)

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    OlympeAthletePopup
)
from tools.constants import (
    DIALOGS_DICT,
    CHARACTERS_DICT,
    TEXT,
    TALKING_SPEED_DICT,
    SHARED_DATA,
    TALKING_SPEED
)
from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CHARACTERS_IMAGES
)
from tools.graphics import (
    COLOR_THOUGHT
)
from lupa_libraries.dialog_generator.dialog_layout import (
    DialogLayout
)
from tools import (
    sound_mixer,
    music_mixer
)
from tools.data_structures import (
    Athlete,
    Sport,
    SPORTS
)
from tools.olympe import (
    finish_dialog
)

#############
### Class ###
#############


class DialogScreen(OlympeScreen):
    """
    Class to manage the screen of dialogs of the game.
    """

    dialog_code = ""
    name_athlete = ""
    dev_mode = BooleanProperty()

    def reload_kwargs(self, dict_kwargs):
        self.dialog_code = dict_kwargs["dialog_code"]
        next_screen = dict_kwargs["next_screen"]
        next_dict_kwargs = dict_kwargs["next_dict_kwargs"]
        self.name_athlete = dict_kwargs.get("name_athlete", "")

        self.on_dialog_end = partial(
            self.dialog_end_function,
            self.dialog_code,
            next_screen,
            next_dict_kwargs
        )

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.dev_mode = SHARED_DATA.dev_mode

        # Reset the variables and start the dialog
        self.dialog_frame_counter = -1
        self.dialog_content_list = DIALOGS_DICT[TEXT.language][self.dialog_code]
        self.post_treat_dialog_text()

        dialog_layout: DialogLayout = self.ids.dialog_layout
        dialog_layout.reload(
            talking_speed=TALKING_SPEED,
            on_dialog_end=self.on_dialog_end,
            color_thought=COLOR_THOUGHT,
            path_character_images=PATH_CHARACTERS_IMAGES,
            character_dict=CHARACTERS_DICT[TEXT.language],
            dialog_content_list=self.dialog_content_list,
            talking_speed_dict=TALKING_SPEED_DICT,
            sound_mixer=sound_mixer,
            music_mixer=music_mixer
        )

    def post_treat_dialog_text(self):
        # Replace the between [] codes by their true value
        for counter_frame in range(len(self.dialog_content_list)):
            frame = self.dialog_content_list[counter_frame]
            mode = frame.get("mode", "")

            if mode == "":
                # First sport of category 1
                if "[THE_NEW_SPORT]" in frame["text"]:
                    self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                        "[THE_NEW_SPORT]", TEXT.sports[self.GAME.first_sport]["the_name"])
                
                # First sport of category 1 with capitale at the beginning
                if "[THE_NEW_SPORT_CAPITALIZE]" in frame["text"]:
                    sport_name = TEXT.sports[self.GAME.first_sport]["the_name"].capitalize()
                    self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                        "[THE_NEW_SPORT_CAPITALIZE]", sport_name)

                # First sport of category 1
                if "[A_NEW_SPORT]" in frame["text"]:
                    self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                        "[A_NEW_SPORT]", TEXT.sports[self.GAME.first_sport]["a_name"])

                # Skill of the first sport
                if "[SKILL_NEW_SPORT]" in frame["text"]:
                    sport: Sport = SPORTS[self.GAME.first_sport]
                    self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                        "[SKILL_NEW_SPORT]", TEXT.stats[sport.stats[0]].lower())

                # Corresponding athlete
                if "[NAME_ATHLETE]" in frame["text"]:
                    self.dialog_content_list[counter_frame]["text"] = frame["text"].replace(
                        "[NAME_ATHLETE]", self.name_athlete)

    def dialog_end_function(self, dialog_code, next_screen, next_dict_kwargs):

        finish_dialog(GAME=self.GAME, dialog_code=dialog_code)

        self.go_to_next_screen(
            screen_name=next_screen,
            current_dict_kwargs={
                "dialog_code": dialog_code,
                "next_screen": next_screen,
                "next_dict_kwargs": next_dict_kwargs},
            next_dict_kwargs=next_dict_kwargs
        )

    def set_background(self, background: str):
        """
        Set the background of the screen to the given image.

        Parameters
        ----------
        background : str
            Name of the background to set.

        Returns
        -------
        """

        if background == "sports_complex":
            path_background = self.GAME.get_background_image()
        else:
            path_background = PATH_BACKGROUNDS + f"{background}.jpg"

        self.set_back_image_path(path_background)

    def skip_dialog(self):
        self.ids.dialog_layout.on_dialog_end()

    def create_first_athlete_popup(self):
        first_athlete: Athlete = self.GAME.team[0]
        stats_dict = first_athlete.stats
        sports_dict = first_athlete.sports
        athlete_skills = dict(reversed(list(stats_dict.items())))
        athlete_skills.update(sports_dict)
        popup = OlympeAthletePopup(
            font_ratio=self.font_ratio,
            title=first_athlete.full_name,
            path_background=self.back_image_path,
            image=first_athlete.image,
            age=TEXT.general["age"].replace("@", str(first_athlete.age)),
            salary=first_athlete.salary,
            title_skills=TEXT.general["skills"],
            skills_dict=athlete_skills,
            confirm_function=self.ids.dialog_layout.go_to_next_frame
        )
        popup.open()
