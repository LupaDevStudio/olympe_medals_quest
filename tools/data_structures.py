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
    "time_absent": 0
}
DEFAULT_STAT_DICT = {
    "points": 0,
    "learning_rate": 1
}
DEFAULT_STATS_DICT = {
    "strength": copy.deepcopy(DEFAULT_STAT_DICT),
    "speed": copy.deepcopy(DEFAULT_STAT_DICT),
    "technique": copy.deepcopy(DEFAULT_STAT_DICT),
    "precision": copy.deepcopy(DEFAULT_STAT_DICT),
    "charm": copy.deepcopy(DEFAULT_STAT_DICT)
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

def convert_characteristic_to_display(stat_dict: dict) -> dict:
    value_characteristic = stat_dict["points"]
    learning_rate = stat_dict["learning_rate"]
    tier_rank = value_characteristic // 10
    rest = value_characteristic - 10 * tier_rank
    # Exception for S-10
    if tier_rank == 7:
        return {
            "rank": "S",
            "level": 10,
            "learning_rate": learning_rate}
    return {
        "rank": TIER_RANK_DICT[tier_rank],
        "level": rest,
        "learning_rate": learning_rate} 

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

    def __init__(self, dict_to_load: dict):
        self.id = dict_to_load.get("id", "")
        self.name = dict_to_load.get("name", "")
        self.category = dict_to_load.get("category", "")
        self.level_category = dict_to_load.get("level_category", 0)
        self.price = dict_to_load.get("price", 0)
        self.gain = dict_to_load.get("gain", 0)

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "level_category": self.level_category,
            "price": self.price,
            "gain": self.gain,
        }


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

    def __init__(self, dict_to_load: dict):
        self.id = dict_to_load.get("id", "")
        self.name = dict_to_load.get("name", "")
        self.skills = tuple(dict_to_load.get("skills", ()))
        self.mode_summer_winter = dict_to_load.get("mode_summer_winter", "summer")

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "skills": list(self.skills),
            "mode_summer_winter": self.mode_summer_winter,
        }

class Athlete():
    """
    A class to store the data of an athlete.
    """

    id: str
    name: str
    first_name: str
    age: int
    salary: int
    recruit_price: int
    fatigue: int
    health: dict
    reputation: int
    stats: dict[str, int]
    sports: dict[str, int]
    previous_planning: list[Activity]
    current_planning: list[Activity]

    @ property
    def image(self) -> str:
        return PATH_ATHLETES_IMAGES + f"athlete_{self.id}.png"

    @ property
    def is_hurt(self) -> str:
        return self.health["is_hurt"]

    def __init__(self, dict_to_load: dict) -> None:
        self.id = dict_to_load.get("id", generate_id())
        self.name = dict_to_load.get("name", "")
        self.first_name = dict_to_load.get("first_name", "")
        self.age = dict_to_load.get("age", 0)
        self.salary = dict_to_load.get("salary", 0)
        self.recruit_price = dict_to_load.get("recruit_price", 0)
        self.fatigue = dict_to_load.get("fatigue", 0)
        self.health = dict_to_load.get("health", copy.deepcopy(DEFAULT_HEALTH_DICT))
        self.reputation = dict_to_load("reputation", 0)
        self.stats = dict_to_load.get("stats", {})
        self.sports = dict_to_load.get("sports", {})
        self.previous_planning = [
            Activity(activity) for activity in dict_to_load.get("previous_planning", [])]
        self.current_planning = [
            Activity(activity) for activity in dict_to_load.get("current_planning", [])]

    def __str__(self):
        return f"Athlete {self.id}: {self.name} {self.first_name}\n" \
               f"Age: {self.age}, Salary: {self.salary}, Recruit Price: {self.recruit_price}\n" \
               f"Fatigue: {self.fatigue}, Health: {self.health}\n" \
               f"Reputation: {self.reputation}\n" \
               f"Stats: {self.stats}\n" \
               f"Sports: {self.sports}\n" \
               f"Current Planning: {', '.join(str(activity) for activity in self.current_planning)}"

    def convert_stats_to_tier_rank(self):
        tier_rank_dict = {}
        for key in self.stats:
            value = self.stats[key]
            tier_rank_dict[key] = convert_characteristic_to_display(
                stat_dict=value)
        return tier_rank_dict

    def convert_sports_to_tier_rank(self):
        tier_rank_dict = {}
        for key in self.sports:
            value = self.sports[key]
            tier_rank_dict[key] = convert_characteristic_to_display(
                stat_dict=value)
        return tier_rank_dict

    def update_monthly_performance(self):
        # TODO update performance with chosen activities avec plafond à 70
        # TODO lose performance according to their age

        # Heal athletes
        if self.health["is_hurt"]:
            self.health["time_absent"] -= 1
            if self.health["time_absent"] == 0:
                self.health = copy.deepcopy(DEFAULT_HEALTH_DICT)

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "age": self.age,
            "salary": self.salary,
            "recruit_price": self.recruit_price,
            "fatigue": self.fatigue,
            "health": self.health,
            "reputation": self.reputation,
            "stats": self.stats,
            "sports": self.sports,
            "previous_planning": [activity.export_dict() for activity in self.previous_planning],
            "current_planning": [activity.export_dict() for activity in self.current_planning],
        }


class Room():
    """
    A class to store the data of a room.
    """

    id: str
    name: str
    current_level: int
    activities_unlocked: list[Activity]
    effects: list

    @ property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"{self.id}_{self.current_level}.png"

    def __init__(self, dict_to_load: dict) -> None:
        self.id = dict_to_load.get("id", "")
        self.name = dict_to_load.get("name", ROOMS_EVOLUTION_DICT[self.id])
        self.current_level = dict_to_load.get("current_level", 1)
        self.activities_unlocked = [
            Activity(activity) for activity in dict_to_load.get("activities_unlocked", [])]
        self.effects = dict_to_load.get("effects", [])

    def update_according_to_level(self) -> None:
        self.activities_unlocked = ROOMS_EVOLUTION_DICT[self.id]["levels"][
            self.current_level]["activities_unlocked"]
        self.effects = ROOMS_EVOLUTION_DICT[self.id]["levels"][
            self.current_level]["effects"]

    def increase_level(self) -> None:
        self.current_level += 1
        self.update_according_to_level()

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "current_level": self.current_level,
            "activities_unlocked": [
                activity.export_dict() for activity in self.activities_unlocked],
            "effects": self.effects
        }


class SportsComplex():
    """
    A class to store the data of the sports complex.
    """

    current_level: int
    rooms_bought: dict[str, Room]  # id room and associated Room

    @property
    def max_number_athletes(self):
        return GYMNASIUM_EVOLUTION_DICT[
            self.current_level]["max_number_athletes"]
    
    @property
    def rooms_unlocked(self):
        list_rooms = []
        for element in GYMNASIUM_EVOLUTION_DICT[self.current_level]["rooms_unlocked"]:
            list_rooms.append(element)
        return list_rooms

    def __init__(self, dict_to_load: dict) -> None:
        self.current_level = dict_to_load.get('current_level', 1)
        self.rooms_bought = {
            room_id: Room(dict_to_load=room_dict) for room_id, room_dict in dict_to_load.get('rooms_bought', {}).items()}

    @property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"sport_complex_{self.current_level}.png"

    def increase_level(self):
        self.current_level += 1

    def buy_room(self, room_id: str) -> Room:
        if room_id in self.rooms_bought:
            current_room: Room = self.rooms_bought[room_id]
            current_room.increase_level()
        else:
            current_room = Room(id=room_id)
        return current_room

    def export_dict(self):
        return {
            "current_level": self.current_level,
            "rooms_bought": {
                room_id: room.export_dict() for room_id, room in self.rooms_bought.items()},
        }


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

    def __init__(self, dict_to_load: dict) -> None:
        self.type_medal = dict_to_load.get("type_medal", "gold")
        self.edition = dict_to_load.get("edition", 0)
        self.athlete_id = dict_to_load.get("athlete_id", "")
        self.sport_id = dict_to_load.get("sport_id", "")

    def export_dict(self):
        return {
            "type_medal": self.type_medal,
            "edition": self.edition,
            "athlete_id": self.athlete_id,
            "sport_id": self.sport_id,
        }


class Country():

    id: str
    name: str
    team: list[Athlete]
    medals: list[Medal]

    @property
    def flag(self):
        # TODO
        return ...

    def __init__(self, dict_to_load: dict) -> None:
        self.id = dict_to_load.get("id", "")
        self.name = dict_to_load.get("name", "")
        self.team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("team", [])]
        self.medals = [
            Medal(dict_to_load=medal_dict) for medal_dict in dict_to_load.get("medals", [])]

    def export_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "team": [athlete.export_dict() for athlete in self.team],
            "medals": [medal.export_dict() for medal in self.medals],
        }


class Game():
    """
    A class to store the data of the game.
    """

    money: int
    year: int
    trimester: int
    team: list[Athlete]
    # Fired athletes (we still need them for the display of medals)
    fired_team: list[Athlete]
    countries: dict[str, Country]
    gymnasium: SportsComplex
    medals: list[Medal]
    sports: dict[str, Sport]
    sports_unlocking_progress: dict[str, float]
    # Sport id with athlete ids
    selected_athletes_summer: dict[str, list[str]]
    selected_athletes_winter: dict[str, list[str]]

    @property
    def sports_unlocked(self) -> list[Sport]:
        sports_unlocked = []
        for key in self.sports_unlocking_progress:
            value = self.sports_unlocking_progress[key]
            if value >= 1:
                sports_unlocked.append(self.sports[key])
        return sports_unlocked

    @property
    def number_athletes(self) -> int:
        return len(self.team)
    
    @property
    def max_athletes(self) -> int:
        return self.gymnasium.max_number_athletes

    def __init__(self, dict_to_load: dict) -> None:

        self.money = dict_to_load.get("money", 0)
        self.year = dict_to_load.get("year", 3)
        self.trimester = dict_to_load.get("trimester", 1)
        self.team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("team", [])]
        self.fired_team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("fired_team", [])]
        self.countries = {
            country_id: Country(dict_to_load=country_dict) for country_id, country_dict in dict_to_load.get("countries", {}).items()}
        self.gymnasium = SportsComplex(dict_to_load=dict_to_load.get("gymnasium", {}))
        self.medals = [
            Medal(dict_to_load=medal_dict) for medal_dict in dict_to_load.get("medals", [])]
        self.sports = {
            sport_id: Sport(dict_to_load=sport_dict) for sport_id, sport_dict in dict_to_load.get("sports", {}).items()}
        self.sports_unlocking_progress = dict_to_load.get("sports_unlocking_progress", {})
        self.selected_athletes_summer = dict_to_load.get("selected_athletes_summer", {})
        self.selected_athletes_winter = dict_to_load.get("selected_athletes_winter", {})

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

        # Remove the athlete from the current team and put it in the fired team
        self.team.remove(athlete)
        self.fired_team.append(athlete)

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

    def export_dict(self):
        return {
            "money": self.money,
            "year": self.year,
            "trimester": self.trimester,
            "team": [
                athlete.export_dict() for athlete in self.team],
            "fired_team": [
                athlete.export_dict() for athlete in self.fired_team],
            "countries": {
                country_id: country.export_dict() for country_id, country in self.countries.items()},
            "gymnasium": self.gymnasium.export_dict(),
            "medals": [
                medal.export_dict() for medal in self.medals],
            "sports": {
                sport_id: sport.export_dict() for sport_id, sport in self.sports.items()},
            "sports_unlocking_progress": self.sports_unlocking_progress,
            "selected_athletes_summer": self.selected_athletes_summer,
            "selected_athletes_winter": self.selected_athletes_winter,
        }


class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.settings = data["settings"]
        self.tutorial = data["tutorial"]
        self.game = Game(dict_to_load=data["game"]) if "game" in data else Game()
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
        data = {
            "settings": self.settings,
            "tutorial": self.tutorial,
            "game": self.game.export_dict(),
        }

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)
