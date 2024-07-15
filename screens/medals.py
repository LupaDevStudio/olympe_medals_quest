"""
Module to create the medals screen.
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
from kivy.core.window import Window

### Local imports ###

from lupa_libraries import (
    OlympeScreen,
    CompleteMedalsCard
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
    BIG_HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    MARGIN_HEIGHT
)
from tools.data_structures import (
    Medal,
    SPORTS
)

#############
### Class ###
#############


class MedalsScreen(OlympeScreen):
    """
    Class to manage the medals screen of the game.
    """

    dict_type_screen = {
        SCREEN_TITLE_ICON : "medals",
        SCREEN_BACK_ARROW : "game",
        SCREEN_MONEY_RIGHT : True
    }
    medals_title = StringProperty()
    sports_view = BooleanProperty(True)

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.medals
        self.medals_title = my_text["title"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        if self.sports_view:
            for sport_id in GAME.sports_unlocked:

                # Build the list of medals obtained for each sport
                list_medals = GAME.get_medals_from_sport(sport_id=sport_id)
                list_content = []
                medal: Medal
                for medal in list_medals:
                    print(medal.athlete_id)
                    athlete = GAME.get_athlete_from_id(athlete_id=medal.athlete_id)
                    list_content.append({
                        "title": athlete.first_name,
                        "image": athlete.image,
                        "icon": medal.type_medal,
                        "label": medal.edition
                    })

                number_lines = (len(list_content)-1) // 3 + 1
                height = self.font_ratio * (
                    CHARACTER_HEIGHT*number_lines + MARGIN_HEIGHT*(number_lines+1)
                )

                medals_card = CompleteMedalsCard(
                    title_card=TEXT.sports[sport_id]["name"],
                    icon_mode=True,
                    icon_source=SPORTS[sport_id].icon,
                    medals_list=list_content,
                    font_ratio=self.font_ratio,
                    size_hint=(SCROLLVIEW_WIDTH, None),
                    height=height
                )

                scrollview_layout.add_widget(medals_card)

        else:
            for edition in range(1, GAME.current_edition+1):
                list_medals = GAME.get_medals_from_edition(edition=edition)

    def change_view_mode(self):
        self.sports_view = not self.sports_view

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()
