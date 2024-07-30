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
    CompleteMedalsCard,
    SmallMedalsCard
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
    HEADER_HEIGHT,
    CHARACTER_HEIGHT,
    MARGIN
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
    medals_per_sport_folded_dict = {}
    medals_per_edition_folded_dict = {}

    def reload_language(self):
        super().reload_language()
        my_text = TEXT.medals
        self.medals_title = my_text["title"]

    def fill_scrollview(self):
        scrollview_layout = self.ids["scrollview_layout"]

        card_width = (Window.size[0]*(SCROLLVIEW_WIDTH**2) - \
            4*MARGIN*self.font_ratio - \
            (scrollview_layout.padding[2]-scrollview_layout.padding[0])/2) / 3
        card_height = 1.25*card_width

        ### Sports view ###

        if self.sports_view:

            for sport_id in GAME.sports_unlocked:

                # Initialisation of the folded dictionary
                if sport_id not in self.medals_per_sport_folded_dict:
                    self.medals_per_sport_folded_dict[sport_id] = [False, None]

                # Build the list of medals obtained for each sport
                list_medals = GAME.get_medals_from_sport(sport_id=sport_id)
                number_medals = len(list_medals)

                if self.medals_per_sport_folded_dict[sport_id][0]:
                    if number_medals > 1:
                        label = TEXT.medals["medals"].replace("@", str(number_medals))
                    else:
                        label = TEXT.medals["medal"].replace("@", str(number_medals))
                    medals_card = SmallMedalsCard(
                        title_card=TEXT.sports[sport_id]["name"],
                        icon_mode=True,
                        icon_source=SPORTS[sport_id].icon,
                        font_ratio=self.font_ratio,
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=HEADER_HEIGHT*self.font_ratio,
                        label=label
                    )

                else:
                    list_content = []
                    medal: Medal
                    for medal in list_medals:
                        athlete = GAME.get_athlete_from_id(athlete_id=medal.athlete_id)
                        list_content.append({
                            "title": athlete.first_name,
                            "image": athlete.image,
                            "icon": medal.image,
                            "label": TEXT.general["edition"].replace(
                                "@", str(medal.edition))
                        })

                    number_lines = (number_medals-1) // 3 + 1
                    height = self.font_ratio * (
                        HEADER_HEIGHT + \
                        MARGIN * (number_lines + 1)
                    ) + card_height * number_lines

                    medals_card = CompleteMedalsCard(
                        title_card=TEXT.sports[sport_id]["name"],
                        icon_mode=True,
                        icon_source=SPORTS[sport_id].icon,
                        medals_list=list_content,
                        font_ratio=self.font_ratio,
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=height,
                        card_height=card_height,
                        card_width=card_width
                    )

                self.medals_per_sport_folded_dict[sport_id][1] = medals_card
                scrollview_layout.add_widget(medals_card)

        ### Editions view ###

        else:

            for edition in range(1, GAME.current_edition+1):

                # Initialisation of the folded dictionary
                if edition not in self.medals_per_edition_folded_dict:
                    self.medals_per_edition_folded_dict[edition] = [False, None]

                # Build the list of medals obtained for each edition
                list_medals = GAME.get_medals_from_edition(edition=edition)
                number_medals = len(list_medals)

                if self.medals_per_edition_folded_dict[edition][0]:
                    if number_medals > 1:
                        label = TEXT.medals["medals"].replace("@", str(number_medals))
                    else:
                        label = TEXT.medals["medal"].replace("@", str(number_medals))
                    medals_card = SmallMedalsCard(
                        title_card=TEXT.general["edition"].replace(
                            "@", str(edition)),
                        font_ratio=self.font_ratio,
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=HEADER_HEIGHT*self.font_ratio,
                        label=label
                    )

                else:
                    list_content = []
                    medal: Medal
                    for medal in list_medals:
                        athlete = GAME.get_athlete_from_id(athlete_id=medal.athlete_id)
                        list_content.append({
                            "title": athlete.first_name,
                            "image": athlete.image,
                            "icon": medal.image,
                            "label": TEXT.sports[medal.sport_id]["name"]
                        })

                    number_lines = (number_medals-1) // 3 + 1
                    height = self.font_ratio * (
                        HEADER_HEIGHT + \
                        MARGIN * (number_lines + 1)
                    ) + card_height * number_lines

                    medals_card = CompleteMedalsCard(
                        title_card=TEXT.general["edition"].replace(
                            "@", str(medal.edition)),
                        medals_list=list_content,
                        font_ratio=self.font_ratio,
                        size_hint=(SCROLLVIEW_WIDTH, None),
                        height=height,
                        card_height=card_height,
                        card_width=card_width
                    )

                self.medals_per_edition_folded_dict[edition][1] = medals_card
                scrollview_layout.add_widget(medals_card)


    def change_view_mode(self):
        self.sports_view = not self.sports_view

        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()

    def ask_redraw(self, widget):
        if self.sports_view:
            for sport_id in self.medals_per_sport_folded_dict:
                if widget == self.medals_per_sport_folded_dict[sport_id][1]:
                    self.medals_per_sport_folded_dict[sport_id][0] = not self.medals_per_sport_folded_dict[sport_id][0]
                    break

        else:
            for edition in self.medals_per_edition_folded_dict:
                if widget == self.medals_per_edition_folded_dict[edition][1]:
                    self.medals_per_edition_folded_dict[edition][0] = not self.medals_per_edition_folded_dict[edition][0]
                    break
        
        # Rebuild scrollview
        self.ids.scrollview_layout.reset_scrollview()
        self.fill_scrollview()
