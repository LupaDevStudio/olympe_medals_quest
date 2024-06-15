"""
Module with the class of the USER_DATA.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import copy
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    sys.path.append("./")
from typing import Literal
import uuid

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_MEDALS_IMAGES,
    PATH_BACKGROUNDS,
    PATH_ATHLETES_IMAGES
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

DEFAULT_HEALTH_DICT = {
    "is_hurt": False,
    "type_injury": "",
    "months_absent": 0
}
DEFAULT_STATS_DICT = {
    "strength": 0,
    "speed": 0,
    "technique": 0,
    "precision": 0,
    "charm": 0,
}
TIER_RANK_DICT = {
    0: "F",
    1: "E",
    2: "D",
    3: "C",
    4: "B",
    5: "A",
    6: "S"
}
ROOMS_EVOLUTION_DICT = {
    "id_room_1": {
        "name": "Name of room 1",
        "price": 1000,
        "levels": {
            1: {
                "activities_unlocked": [],
                "effects": []
            }
        }
    }
}
GYMNASIUM_EVOLUTION_DICT = {
    1: {
        "max_number_athletes": 5,
        "rooms_unlocked": [["id_room_1", 1], ["id_room_2", 1]],
        "price": 0
    },
    2: {
        "max_number_athletes": 10,
        "rooms_unlocked": [["id_room_1", 2], ["id_room_2", 2]],
        "price": 20000
    },
    3: {
        "max_number_athletes": 20,
        "rooms_unlocked": [["id_room_1", 3], ["id_room_3", 1]],
        "price": 30000
    },
    4: {
        "max_number_athletes": 50,
        "rooms_unlocked": [["id_room_1", 4], ["id_room_4", 1]],
        "price": 40000
    },
    5: {
        "max_number_athletes": 100,
        "rooms_unlocked": [["id_room_1", 5], ["id_room_5", 1]],
        "price": 50000
    }
}

NB_YEARS_BETWEEN_EDITION = 4


#################
### Functions ###
#################

def generate_id() -> str:
    unique_id = uuid.uuid4()
    return str(unique_id)

def convert_characteristic_to_display(value_characteristic: int):
    tier_rank = value_characteristic // 10
    rest = value_characteristic - 10 * tier_rank
    # Exception for S-10
    if tier_rank == 7:
        return ("S", 10)
    return (TIER_RANK_DICT[tier_rank], rest)

###############
### Classes ###
###############


class Activity():
    """
    A class to store the data of an activity.
    """

    id: str
    name: str
    category: str
    level_category: int
    price: int
    gain: int


class Sport():
    """
    A class to store the data of a sport.
    """

    id: str
    name: str
    skills: tuple[str]
    mode_summer_winter: Literal["summer", "winter"]

    @ property
    def category(self) -> int:
        return len(self.skills)

class Athlete():
    """
    A class to store the data of an athlete.
    """

    def __init__(self, name: str, age: int, salary: int,
                 recruit_price: int, stats: dict[str, int], sports: dict[str, int]) -> None:
        self.id = generate_id()
        self.name = name
        self.age = age
        self.salary = salary
        self.recruit_price = recruit_price
        self.fatigue = 0
        self.health = copy.deepcopy(DEFAULT_HEALTH_DICT)
        self.stats: dict[str, int] = stats
        self.sports: dict[str, int] = sports
        self.current_planning: list[Activity] = []

    @ property
    def image(self) -> str:
        return PATH_ATHLETES_IMAGES + f"athlete_{self.id}.png"

    def convert_stats_to_tier_rank(self):
        tier_rank_dict = {}
        for key in self.stats:
            value = self.stats[key]
            tier_rank_dict[key] = convert_characteristic_to_display(
                value_characteristic=value)
        return tier_rank_dict

    def convert_sports_to_tier_rank(self):
        tier_rank_dict = {}
        for key in self.sports:
            value = self.sports[key]
            tier_rank_dict[key] = convert_characteristic_to_display(
                value_characteristic=value)
        return tier_rank_dict

    def update_monthly_performance(self):
        # TODO update performance with chosen activities avec plafond à 70
        # TODO lose performance according to their age

        # Heal athletes
        if self.health["is_hurt"]:
            self.health["months_absent"] -= 1
            if self.health["months_absent"] == 0:
                self.health = copy.deepcopy(DEFAULT_HEALTH_DICT)


class Room():
    """
    A class to store the data of a room.
    """

    id: str
    name: str
    current_level: int
    activities_unlocked: list[Activity]
    effects: list

    def __init__(self, id: str) -> None:
        self.id = id
        self.name = ROOMS_EVOLUTION_DICT[self.id]
        self.current_level = 1
        self.activities_unlocked = []
        self.effects = []
        self.update_according_to_level()

    @ property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"{self.id}_{self.current_level}.png"

    def update_according_to_level(self):
        self.activities_unlocked = ROOMS_EVOLUTION_DICT[self.id]["levels"][
            self.current_level]["activities_unlocked"]
        self.effects = ROOMS_EVOLUTION_DICT[self.id]["levels"][
            self.current_level]["effects"]

    def increase_level(self):
        self.current_level += 1
        self.update_according_to_level()


class SportsComplex():
    """
    A class to store the data of the sports complex.
    """

    current_level: int
    max_number_athletes: int
    rooms_unlocked: list[list[str, int]]  # id room and level room
    rooms_bought: dict[str, Room]  # id room and associated Room

    def __init__(self) -> None:
        self.current_level = 1
        self.rooms_unlocked = []
        self.rooms_bought = {}
        self.update_according_to_level()

    @property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"sport_complex_{self.current_level}.png"

    def update_according_to_level(self):
        self.max_number_athletes = GYMNASIUM_EVOLUTION_DICT[
            self.current_level]["max_number_athletes"]
        for element in GYMNASIUM_EVOLUTION_DICT[self.current_level]["rooms_unlocked"]:
            self.rooms_unlocked.append(element)

    def increase_level(self):
        self.current_level += 1
        self.update_according_to_level()

    def buy_room(self, room_id: str) -> Room:
        if room_id in self.rooms_bought:
            current_room: Room = self.rooms_bought[room_id]
            current_room.increase_level()
        else:
            current_room = Room(id=room_id)
        return current_room


class Medal():
    """
    A class to store the data of a medal.
    """

    type_medal: Literal["gold", "silver", "copper"]
    edition: int
    athlete_id: str
    sport_id: str

    @property
    def image(self) -> str:
        return PATH_MEDALS_IMAGES + self.type_medal + ".png"

    @property
    def year(self) -> int:
        return self.edition * NB_YEARS_BETWEEN_EDITION


class Game():
    """
    A class to store the data of the game.
    """

    def __init__(self, dict_to_load = None) -> None:
        if not dict_to_load is None:
            self.load_dict(dict_to_load = dict_to_load)
        else:
            self.money: int = 0
            self.year: int = 3
            self.trimester: int = 1
            self.team: list[Athlete] = []
            self.gymnasium: SportsComplex = SportsComplex()
            self.medals: list[Medal] = []
            self.sports: dict[str, Sport] = {}
            self.sports_unlocking_progress: dict[str, float] = {}
            # Sport id with athlete ids
            self.selected_athletes_summer: dict[str, list[str]] = {}
            # Sport id with athlete ids
            self.selected_athletes_winter: dict[str, list[str]] = {}

    @property
    def sports_unlocked(self) -> list[Sport]:
        sports_unlocked = []
        for key in self.sports_unlocking_progress:
            value = self.sports_unlocking_progress[key]
            if value >= 1:
                sports_unlocked.append(self.sports[key])
        return sports_unlocked

    def get_monthly_salaries(self) -> int:
        monthly_salaries = 0
        for athlete in self.team:
            monthly_salaries += athlete.salary
        return monthly_salaries

    def get_monthly_activities_payment(self) -> int:
        monthly_payment = 0
        for athlete in self.team:
            for activity in athlete.current_planning:
                monthly_payment += activity.price
        return monthly_payment

    def get_monthly_payment(self) -> int:
        monthly_salaries = self.get_monthly_salaries()
        monthly_activities = self.get_monthly_activities_payment()
        return monthly_activities + monthly_salaries

    def can_recruit_athlete(self, athlete: Athlete):
        # If the user has enough money
        if self.money >= athlete.recruit_price:
            # If the user has still place in its gymnasium
            if self.gymnasium.max_number_athletes > len(self.team):
                return True
        return False

    def recruit_athlete(self, athlete: Athlete):
        self.money -= athlete.recruit_price
        self.team.append(athlete)

    def fire_athlete(self, athlete_id: str):
        for athlete in self.team:
            if athlete.id == athlete_id:
                break
        # Remove the image of the athlete
        athlete_image = athlete.get_image()
        os.remove(athlete_image)
        self.team.remove(athlete)

    def buy_sport_complex(self, room_id: str):
        if room_id == "gymnasium":
            self.gymnasium.increase_level()
            self.money -= GYMNASIUM_EVOLUTION_DICT[self.gymnasium.current_level]["price"]
        else:
            bought_room: Room = self.gymnasium.buy_room(room_id=room_id)
            self.money -= ROOMS_EVOLUTION_DICT[room_id][bought_room.current_level]["price"]

    def get_medals_from_athlete(self, athlete_id: str) -> Medal:
        list_medals = []
        for medal in self.medals:
            if medal.athlete_id == athlete_id:
                list_medals.append(medal)
        return list_medals

    def get_medals_from_sport(self, sport_id: str) -> Medal:
        list_medals = []
        for medal in self.medals:
            if medal.sport_id == sport_id:
                list_medals.append(medal)
        return list_medals

    def go_to_next_month(self):
        if self.trimester != 4:
            self.trimester += 1
        else:
            self.trimester = 0
            self.year += 1
            self.begin_new_year()

        # Update the amount of money
        self.money -= self.get_monthly_payment()

        # Update the stats of the athletes according to their activities and age
        for athlete in self.team:
            athlete.update_monthly_performance()

    def begin_new_year(self):
        for athlete in self.team:
            athlete.age += 1

    def load_dict(self, dict_to_load):
        # TODO finish function by loading the other classes
        self.money = dict_to_load["money"]
        self.year = dict_to_load["year"]
        self.trimester = dict_to_load["trimester"]
        self.team = dict_to_load["team"]
        self.gymnasium = dict_to_load["gymnasium"]
        self.medals = dict_to_load["medals"]
        self.sports = dict_to_load["sports"]
        self.sports_unlocking_progress = dict_to_load["sports_unlocking_progress"]
        self.selected_athletes_summer = dict_to_load["selected_athletes_summer"]
        self.selected_athletes_winter = dict_to_load["selected_athletes_winter"]

    def export_dict(self):
        # TODO finish function
        dict_to_export = {
            "money": self.money,
            "year": self.year,
            "trimester": self.trimester,
            "team": [],
            "gymnasium": [],
            "medals": [],
            "sports": [],
            "sports_unlocking_progress": [],
            "selected_athletes_summer": [],
            "selected_athletes_winter": []
        }
        return dict_to_export


class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.settings = data["settings"]
        self.tutorial = data["tutorial"]
        if not "game" in data:
            self.game = Game()
        else:
            self.game = Game(dict_to_load=data["game"])
        self.save_changes()

    def save_changes(self) -> None:
        """
        Save the changes in the data.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the dictionary of data
        data = {}

        data["settings"] = self.settings
        data["tutorial"] = self.tutorial
        data["game"] = self.game.export_dict()

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)

#################
### Functions ###
#################


def generate_athlete() -> Athlete:
    return Athlete(
        id="Ariel_1",
        name="A",
        age=20,
        salary=1200,
        recruit_price=20000,
        strength=10,
        speed=2,
        technique=15,
        precision=60,
        charm=29,
        sports=[]
    )


if __name__ == "__main__":
    my_athlete_a = Athlete(
        name="A",
        age=20,
        salary=1200,
        recruit_price=20000,
        strength=10,
        speed=2,
        technique=70,
        precision=60,
        charm=29,
        sports=[]
    )
    assert my_athlete_a.convert_characteristic_to_display(
        my_athlete_a.strength) == ["E", 0]
    assert my_athlete_a.convert_characteristic_to_display(my_athlete_a.speed) == [
        "F", 2]
    assert my_athlete_a.convert_characteristic_to_display(
        my_athlete_a.technique) == ["S", 10]
    assert my_athlete_a.convert_characteristic_to_display(
        my_athlete_a.precision) == ["S", 0]
    assert my_athlete_a.convert_characteristic_to_display(my_athlete_a.charm) == [
        "D", 9]
