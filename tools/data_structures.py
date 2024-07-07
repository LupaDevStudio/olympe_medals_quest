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
    PATH_ATHLETES_IMAGES,
    PATH_SPORTS
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

MAX_ATHLETES_TO_SELECT = 3
PRICES_SELECTION = {
    1: 5000,
    2: 10000,
    3: 15000
}
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


def convert_points_to_tier_rank(points):
    tier_rank = points // 10
    rest = points - 10 * tier_rank
    if tier_rank == 7:
        level = 10
        rank = "S"
    else:
        level = rest
        rank = TIER_RANK_DICT[tier_rank]
    return rank, level


def convert_characteristic_to_display(stat_dict: dict) -> dict:
    value_characteristic = stat_dict["points"]
    learning_rate = stat_dict["learning_rate"]
    tier_rank, level = convert_points_to_tier_rank(value_characteristic)

    return {
        "rank": tier_rank,
        "level": level,
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
    stats: list[str]
    requirements: list[str]
    mode_summer_winter: Literal["summer", "winter"]

    @ property
    def category(self) -> int:
        return len(self.stats)

    def __init__(self, dict_to_load: dict):
        self.id = dict_to_load.get("id", "")
        self.stats = list(dict_to_load.get("stats", ()))
        self.requirements = list(dict_to_load.get("requirements", ()))
        self.mode_summer_winter = dict_to_load.get(
            "mode_summer_winter", "summer")

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
    stats: dict[str, dict]
    sports: dict[str, dict]
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
        self.health = dict_to_load.get(
            "health", copy.deepcopy(DEFAULT_HEALTH_DICT))
        self.reputation = dict_to_load.get("reputation", 0)
        self.stats = dict_to_load.get("stats", {})
        self.sports = dict_to_load.get("sports", {})
        self.previous_planning = [
            Activity(activity) for activity in dict_to_load.get("previous_planning", [])]
        self.current_planning = [
            Activity(activity) for activity in dict_to_load.get("current_planning", [])]

    def get_best_sports(self, number_sports: int = 2):
        # Sort the sports by decreasing points
        sorted_sports = sorted(
            self.sports.items(), key=lambda x: x[1]['points'], reverse=True)

        # Extract the first sports
        best_sports = dict(sorted_sports[:number_sports])
        return dict(reversed(best_sports.items()))

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
        return PATH_BACKGROUNDS + f"sport_complex_{self.current_level}.jpg"

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

    type_medal: Literal["gold", "silver", "bronze"]
    edition: int
    type_edition: Literal["summer", "winter"]
    athlete_id: str
    sport_id: str

    @property
    def image(self) -> str:
        return PATH_MEDALS_IMAGES + self.type_medal + ".png"

    @property
    def year(self) -> int:
        if self.type_edition == "summer":
            return self.edition * NB_YEARS_BETWEEN_EDITION
        elif self.type_edition == "winter":
            return self.edition * NB_YEARS_BETWEEN_EDITION - NB_YEARS_BETWEEN_EDITION//2

    def __init__(self, dict_to_load: dict) -> None:
        self.type_medal = dict_to_load.get("type_medal", "gold")
        self.edition = dict_to_load.get("edition", 0)
        self.athlete_id = dict_to_load.get("athlete_id", "")
        self.type_edition = dict_to_load.get("type_edition", "summer")
        self.sport_id = dict_to_load.get("sport_id", "")

    def export_dict(self):
        return {
            "type_medal": self.type_medal,
            "edition": self.edition,
            "athlete_id": self.athlete_id,
            "sport_id": self.sport_id,
            "type_edition": self.type_edition
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
    # Retired athletes (we still need them for the display of medals)
    retired_team: list[Athlete]
    # Recrutable athletes for the current trimester
    recrutable_athletes: list[Athlete]
    countries: dict[str, Country]
    sports_complex: SportsComplex
    medals: list[Medal]
    sports_unlocking_progress: dict[str, float]
    # Sport id with athlete ids
    selected_athletes_summer: dict[str, list[str]]
    selected_athletes_winter: dict[str, list[str]]

    @property
    def sports_unlocked(self) -> list[str]:
        sports_unlocked = []
        for key in self.sports_unlocking_progress:
            value = self.sports_unlocking_progress[key]
            if value == 1:
                sports_unlocked.append(key)
        return sports_unlocked

    @property
    def number_athletes(self) -> int:
        return len(self.team)

    @property
    def max_athletes(self) -> int:
        return self.sports_complex.max_number_athletes

    @property
    def current_edition(self, type_edition: Literal["summer", "winter"] = "summer") -> int:
        if type_edition == "summer":
            if self.year % NB_YEARS_BETWEEN_EDITION == 0:
                return self.year // NB_YEARS_BETWEEN_EDITION
            return self.year // NB_YEARS_BETWEEN_EDITION + 1
        elif type_edition == "winter":
            if self.year % NB_YEARS_BETWEEN_EDITION == NB_YEARS_BETWEEN_EDITION//2:
                return self.year // NB_YEARS_BETWEEN_EDITION
            return (self.year + NB_YEARS_BETWEEN_EDITION//2) // NB_YEARS_BETWEEN_EDITION

    def __init__(self, dict_to_load: dict) -> None:

        self.money = dict_to_load.get("money", 0)
        self.year = dict_to_load.get("year", 3)
        self.trimester = dict_to_load.get("trimester", 1)
        self.team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("team", [])]
        self.fired_team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("fired_team", [])]
        self.retired_team = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("retired_team", [])]
        self.recrutable_athletes = [
            Athlete(dict_to_load=athlete_dict) for athlete_dict in dict_to_load.get("recrutable_athletes", [])]
        self.countries = {
            country_id: Country(dict_to_load=country_dict) for country_id, country_dict in dict_to_load.get("countries", {}).items()}
        self.sports_complex = SportsComplex(
            dict_to_load=dict_to_load.get("sports_complex", {}))
        self.medals = [
            Medal(dict_to_load=medal_dict) for medal_dict in dict_to_load.get("medals", [])]
        self.sports_unlocking_progress = dict_to_load.get(
            "sports_unlocking_progress", {})
        self.selected_athletes_summer = dict_to_load.get(
            "selected_athletes_summer", {})
        self.selected_athletes_winter = dict_to_load.get(
            "selected_athletes_winter", {})

    def get_background_image(self) -> int:
        return self.sports_complex.image

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

    def update_recrutable_athletes(self, new_athletes_list: list[Athlete]) -> None:
        # TODO call this function each month after having some new athetes
        # Diminish the time left to recruit and remove those with 0 time left
        # TODO

        # Add the new athletes
        for athlete in new_athletes_list:
            self.recrutable_athletes.append(athlete)

    def can_recruit_athlete(self, athlete: Athlete):
        # If the user has enough money
        if self.money >= athlete.recruit_price:
            # If the user has still place in its gymnasium
            if self.sports_complex.max_number_athletes > len(self.team):
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
        if room_id == "sports_complex":
            self.sports_complex.increase_level()
            self.money -= GYMNASIUM_EVOLUTION_DICT[self.sports_complex.current_level]["price"]
        else:
            bought_room: Room = self.sports_complex.buy_room(room_id=room_id)
            self.money -= ROOMS_EVOLUTION_DICT[room_id][bought_room.current_level]["price"]

    def get_medals_from_athlete(self, athlete_id: str) -> Medal:
        list_medals = []
        for medal in self.medals:
            if medal.athlete_id == athlete_id:
                list_medals.append(medal)

        # Sort the list of medals first by sport_id and then by edition
        list_medals.sort(key=lambda medal: (medal.sport_id, medal.edition), reverse=True)

        return list_medals

    def get_medals_from_sport(self, sport_id: str) -> Medal:
        list_medals = []
        for medal in self.medals:
            if medal.sport_id == sport_id:
                list_medals.append(medal)

        # Sort the list of medals first by athlete_id and then by edition
        list_medals.sort(key=lambda medal: (medal.athlete_id, medal.edition), reverse=True)

        return list_medals

    def get_best_medal_source_from_athlete_in_sport(self, athlete_id: str, sport_id: str) -> str:
        order_medals = ["", "bronze", "silver", "gold"]
        best_medal_type = ""
        best_medal = None
        for medal in self.medals:
            if medal.athlete_id == athlete_id and medal.sport_id == sport_id:
                ref = order_medals.index(best_medal_type)
                current = order_medals.index(medal.type_medal)
                if current > ref:
                    best_medal_type = medal.type_medal
                    best_medal = medal
        if best_medal is None:
            return ""
        return best_medal.image

    def win_medal(self, sport_id, athlete_id, type: Literal["gold", "silver", "bronze"], edition: int, type_edition: Literal["summer", "winter"]="summer"):
        new_medal = Medal(
            dict_to_load={
                "sport_id": sport_id,
                "athlete_id": athlete_id,
                "type": type,
                "edition": edition,
                "type_edition": type_edition
            }
        )
        self.medals.append(new_medal)

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

    def compute_total_spent_money_selection(self, mode: Literal["summer", "winter"] = "summer") -> int:
        total_money_spent = 0

        if mode == "summer":
            for sport_id in self.selected_athletes_summer:
                sport: Sport = SPORTS[sport_id]
                sport_category = sport.category
                price_sport = PRICES_SELECTION[sport_category]
                total_money_spent += price_sport * len(self.selected_athletes_summer[sport_id])

        elif mode == "winter":
            for sport_id in self.selected_athletes_winter:
                sport: Sport = SPORTS[sport_id]
                sport_category = sport.category
                price_sport = PRICES_SELECTION[sport_category]
                total_money_spent += price_sport * len(self.selected_athletes_winter[sport_id])
        
        return total_money_spent

    def get_price_selection_for_sport(self, sport_id: str, mode: Literal["summer", "winter"] = "summer") -> int:
        number_athletes_selected = self.get_number_athletes_selected_for_sport(
            sport_id=sport_id, mode=mode
        )
        sport: Sport = SPORTS[sport_id]
        return number_athletes_selected*PRICES_SELECTION[sport.category]

    def get_number_athletes_selected_for_sport(self, sport_id: str, mode: Literal["summer", "winter"] = "summer") -> int:
        if mode == "summer":
            return len(self.selected_athletes_summer[sport_id])
        return len(self.selected_athletes_winter[sport_id])

    def can_select_athlete(self, athlete: Athlete, sport_id: str, mode: Literal["summer", "winter"] = "summer") -> dict[str, bool]:
        dict_return = {
            "already_selected": False,
            "can_select": False
        }
        
        # If the athlete is not hurt
        if not athlete.is_hurt:
            athlete_id = athlete.id
            sport: Sport = SPORTS[sport_id]
            total_spends = self.compute_total_spent_money_selection(mode=mode)
            price_sport = PRICES_SELECTION[sport.category]
            number_athletes_selected = self.get_number_athletes_selected_for_sport(
                sport_id=sport_id, mode=mode
            )

            # If the number of athletes to select is not reached for summer
            if mode == "summer":
                if athlete_id in self.selected_athletes_summer[sport_id]:
                    dict_return["already_selected"] = True
                    dict_return["can_select"] = True
                else:
                    if number_athletes_selected < MAX_ATHLETES_TO_SELECT:
                        # If enough money to select another athlete
                        if self.money - total_spends - price_sport >= 0:
                            dict_return["can_select"] = True

            # If the number of athletes to select is not reached for winter
            if mode == "winter":
                if athlete_id in self.selected_athletes_winter[sport_id]:
                    dict_return["already_selected"] = True
                    dict_return["can_select"] = True
                else:
                    if number_athletes_selected < MAX_ATHLETES_TO_SELECT:
                        # If enough money to select another athlete
                        if self.money - total_spends - price_sport >= 0:
                            dict_return["can_select"] = True

        return dict_return

    def select_unselect_athlete(self, athlete_id: str, sport_id: str, mode: Literal["summer", "winter"] = "summer"):
        if mode == "summer":
            if athlete_id in self.selected_athletes_summer[sport_id]:
                self.selected_athletes_summer[sport_id].remove(athlete_id)
            else:
                self.selected_athletes_summer[sport_id].append(athlete_id)
        if mode == "winter":
            if athlete_id in self.selected_athletes_winter[sport_id]:
                self.selected_athletes_winter[sport_id].remove(athlete_id)
            else:
                self.selected_athletes_winter[sport_id].append(athlete_id)

    def export_dict(self):
        return {
            "money": self.money,
            "year": self.year,
            "trimester": self.trimester,
            "team": [
                athlete.export_dict() for athlete in self.team],
            "fired_team": [
                athlete.export_dict() for athlete in self.fired_team],
            "retired_team": [
                athlete.export_dict() for athlete in self.retired_team],
            "recrutable_athletes": [
                athlete.export_dict() for athlete in self.recrutable_athletes],
            "countries": {
                country_id: country.export_dict() for country_id, country in self.countries.items()},
            "sports_complex": self.sports_complex.export_dict(),
            "medals": [
                medal.export_dict() for medal in self.medals],
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
        self.game = Game(
            dict_to_load=data["game"]) if "game" in data else Game()
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

SPORTS = load_json_file(PATH_SPORTS)
for sport_id in SPORTS:
    SPORTS[sport_id] = Sport(
        dict_to_load={
            "id": sport_id,
            "stats": SPORTS[sport_id]["stats"],
            "requirements": SPORTS[sport_id]["requirements"]
        }
    ) 
