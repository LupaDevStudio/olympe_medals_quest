"""
Module with the class of the USER_DATA.
"""

###############
### Imports ###
###############

### Python imports ###

import copy
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    sys.path.append("./")
from typing import Literal

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_MEDALS
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

default_health_dict = {
    "is_hurt": False,
    "type_injury": "",
    "months_absent": 0
}
tier_rank_dict = {
    0: "F",
    1: "E",
    2: "D",
    3: "C",
    4: "B",
    5: "A",
    6: "S"
}

###############
### Classes ###
###############

class Athlete():
    """
    A class to store the data of an athlete.
    """

    def __init__(self, id: int, name: str, age: int, salary: int,
            strength: int, speed: int, technique: int, precision: int,
            charisma: int, sports: list[int]) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.salary = salary
        self.fatigue = 0
        self.health = copy.deepcopy(default_health_dict)
        self.medals = []
        self.strength = strength
        self.speed = speed
        self.technique = technique
        self.precision = precision
        self.charisma = charisma
        self.sports = sports

    def convert_charateristic_to_display(self, value_characteristic: int):
        tier_rank = value_characteristic // 10
        rest = value_characteristic - 10 * tier_rank
        return [tier_rank_dict[tier_rank], rest]

class Room():
    """
    A class to store the data of a room.
    """

    name: str
    current_level: int
    image: str
    activities_unlocked: list
    effects: list

class Gymnasium():
    """
    A class to store the data of the gymnasium.
    """

    current_level: int
    image: str
    max_number_athletes: int
    rooms_unlocked: list[Room]
    rooms_buyed: list[Room]

class Medal():
    """
    A class to store the data of a medal.
    """

    type_medal: Literal["gold", "silver", "copper"]
    image: str
    year: int
    athlete: Athlete

    def get_image_from_type(self, type_medal: Literal["gold", "silver", "copper"]) -> str:
        return PATH_MEDALS + type_medal + ".png"

class Game():
    """
    A class to store the data of the game.
    """

    def __init__(self) -> None:
        self.money: int = 0
        self.team: list[Athlete] = []
        self.gymnasium: Gymnasium = None
        self.medals: list[Medal] = []

    def get_monthly_salary(self) -> int:
        monthly_salary = 0
        for athlete in self.team:
            monthly_salary += athlete.salary
        return monthly_salary

    def recruit_athlete(self, athlete: Athlete):
        self.team.append(athlete)

    def fire_athlete(self, athlete_id: Athlete):
        for athlete in self.team:
            if athlete.id == athlete_id:
                break
        self.team.remove(athlete)

class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)

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

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)

#################
### Functions ###
#################

def generate_athlete() -> Athlete:
    return Athlete(
        id=1,
        name="A",
        age=20,
        salary=1200,
        strength=10,
        speed=2,
        technique=15,
        precision=60,
        charisma=29,
        sports=[]
    )

if __name__ == "__main__":
    my_athlete_a = Athlete(
        id=1,
        name="A",
        age=20,
        salary=1200,
        strength=10,
        speed=2,
        technique=15,
        precision=60,
        charisma=29,
        sports=[]
    )
    assert my_athlete_a.convert_charateristic_to_display(my_athlete_a.strength) == ["E", 0]
    assert my_athlete_a.convert_charateristic_to_display(my_athlete_a.speed) == ["F", 2]
    assert my_athlete_a.convert_charateristic_to_display(my_athlete_a.technique) == ["E", 5]
    assert my_athlete_a.convert_charateristic_to_display(my_athlete_a.precision) == ["S", 0]
    assert my_athlete_a.convert_charateristic_to_display(my_athlete_a.charisma) == ["D", 9]
