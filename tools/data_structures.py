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
import uuid

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_SPORTS_ICONS,
    PATH_MEDALS_IMAGES,
    PATH_BACKGROUNDS,
    PATH_ATHLETES_IMAGES,
    PATH_SPORTS,
    PATH_ACTIVITIES,
    PATH_SPORTS_COMPLEX_DICT,
    PATH_ROOMS_DICT
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

STRENGTH = "strength"
SPEED = "speed"
TECHNIQUE = "technique"
PRECISION = "precision"
CHARM = "charm"

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
    STRENGTH: copy.deepcopy(DEFAULT_STAT_DICT),
    SPEED: copy.deepcopy(DEFAULT_STAT_DICT),
    TECHNIQUE: copy.deepcopy(DEFAULT_STAT_DICT),
    PRECISION: copy.deepcopy(DEFAULT_STAT_DICT),
    CHARM: copy.deepcopy(DEFAULT_STAT_DICT)
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
# TODO changer les clés
LEVEL_DICT = {
    1000: 1,
    2000: 2,
    3000: 3,
    4000: 4,
    5000: 5,
    6000: 6,
    7000: 7,
    8000: 8,
    9000: 9,
    10000: 10
}
SPORTS_COMPLEX_EVOLUTION_DICT = load_json_file(PATH_SPORTS_COMPLEX_DICT)
ROOMS_EVOLUTION_DICT = load_json_file(PATH_ROOMS_DICT)

NB_YEARS_BETWEEN_EDITION = 4

FACTOR_SPONSOR_REPUTATION = 300

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

### Activities ###

class Activity():
    """
    A class to store the data of an activity.
    """

    id: str
    effects: list
    category: str
    all_trimester: bool
    price: int
    gain: int
    condition: None|int

    def __init__(self, dict_to_load: dict):
        self.id = dict_to_load.get("id", "")
        self.effects = dict_to_load.get("effects", [])
        self.category = dict_to_load.get("category", "")
        self.all_trimester = dict_to_load.get("all_trimester", False)
        self.price = dict_to_load.get("price", 0)
        self.gain = dict_to_load.get("gain", 0)
        self.condition = dict_to_load.get("condition", None)

    def get_gain(self, athlete) -> int:
        return 0

    def apply_activity(self, athlete) -> None:
        for effect in self.effects:
            if effect[0] == "fatigue":
                athlete.fatigue += effect[1]
            elif effect[0] == "injury_risk":
                athlete.injury_risk += effect[1]
            elif effect[0] == "illness":
                if effect[1] == "heal_one_trimester":
                    athlete.health["time_absent"] -= 1
                elif effect[1] == "heal_all":
                    athlete.health = copy.deepcopy(DEFAULT_HEALTH_DICT)

class InterviewActivity(Activity):
    """
    A class to store the data of the interview activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "interview"

    def get_gain_reputation(self, athlete) -> int:
        current_reputation = athlete.reputation
        current_charm = athlete.stats["charm"]["points"]

        # TODO
        gain_reputation = 0

        return gain_reputation

    def apply_activity(self, athlete) -> None:
        gain_reputation = self.get_gain_reputation(athlete=athlete)
        athlete.reputation += gain_reputation

class SponsorActivity(Activity):
    """
    A class to store the data of the sponsors activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "sponsor"

    def get_gain(self, athlete) -> int:
        current_reputation = athlete.reputation
        gain_money = FACTOR_SPONSOR_REPUTATION * current_reputation

        return gain_money

class JobActivity(Activity):
    """
    A class to store the data of the job activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "job"

    def get_can_access_gain_money_gain_stats(self, athlete) -> dict:

        # Activities not based on stats
        if self.id in ["basic_job", "best_job"]:
            return {
                "can_access": True,
                "gain_money": self.gain
            }
        
        # Activities based on a stat

        fix_part = self.gain
        stat = self.id.replace("_job", "")
        athlete_stat = athlete.stats[stat]["points"]

        # The athlete is not skilled enough to perform the job
        condition = self.condition
        if athlete_stat < condition:
            return {"can_access": False}
        
        variable_part = int(fix_part * athlete_stat / 70)

        return {
                "can_access": True,
                "gain_money": fix_part + variable_part,
                "gain_stats": {} # TODO
            }

    def get_gain(self, athlete) -> int:
        dict_effects = self.get_can_access_gain_money_gain_stats(athlete=athlete)
        return dict_effects.get("gain_money", 0)

    def apply_activity(self, athlete) -> None:
        dict_effects = self.get_can_access_gain_money_gain_stats(athlete=athlete)
        dict_effects_stats = dict_effects.get("gain_stats", {})

        for key in dict_effects_stats:
            athlete.stats[key]["points"] += dict_effects_stats[key]

### Sports ###

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

    @ property
    def icon(self) -> str:
        return PATH_SPORTS_ICONS + self.id + ".png"

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
    time_for_recruit: int
    fatigue: int
    injury_risk: float
    health: dict
    reputation: int
    stats: dict[str, dict]
    sports: dict[str, dict]
    current_planning: list[str]

    @ property
    def image(self) -> str:
        return PATH_ATHLETES_IMAGES + f"athlete_{self.id}.png"

    @ property
    def global_score(self) -> str:
        # TODO prendre en compte le type de sport
        score = 0
        for stat in self.stats:
            score += self.stats[stat]["points"]
        for sport in self.sports:
            score += self.sports[sport]["points"]
        return score

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
        self.time_for_recruit = dict_to_load.get("time_for_recruit", 0)
        self.fatigue = dict_to_load.get("fatigue", 0)
        self.injury_risk = dict_to_load.get("injury_risk", 0)
        self.health = dict_to_load.get(
            "health", copy.deepcopy(DEFAULT_HEALTH_DICT))
        self.reputation = dict_to_load.get("reputation", 0)
        self.stats = dict_to_load.get("stats", {})
        self.sports = dict_to_load.get("sports", {})
        self.current_planning = dict_to_load.get("current_planning", ["vacation", "vacation", "vacation"])

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
               f"Current Planning: {', '.join(activity_id for activity_id in self.current_planning)}"

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

    def update_trimester_performance(self):
        # TODO lose performance according to their age

        # Heal athletes
        if self.health["is_hurt"]:
            self.health["time_absent"] -= 1
            if self.health["time_absent"] <= 0:
                self.health = copy.deepcopy(DEFAULT_HEALTH_DICT)

    def get_trimester_gained_money(self) -> int:
        # Salary of the athlete
        trimester_payment = - self.salary

        for activity_id in self.current_planning:
            activity: Activity = ACTIVITIES[activity_id]

            # Potential price of the activity
            trimester_payment -= activity.price
            # Potential gain of the activity
            trimester_payment += activity.get_gain(athlete=self)

        return trimester_payment

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "age": self.age,
            "salary": self.salary,
            "time_for_recruit": self.time_for_recruit,
            "recruit_price": self.recruit_price,
            "fatigue": self.fatigue,
            "health": self.health,
            "reputation": self.reputation,
            "stats": self.stats,
            "sports": self.sports,
            "current_planning": [activity_id for activity_id in self.current_planning]
        }


class Room():
    """
    A class to store the data of a room.
    """

    id: str
    current_level: int

    @ property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"{self.id}.jpg"

    @ property
    def activities_unlocked(self) -> list[str]:
        return ROOMS_EVOLUTION_DICT[self.id][str(self.current_level)]["activities_unlocked"]
    
    @ property
    def effects(self) -> list:
        return ROOMS_EVOLUTION_DICT[self.id][str(self.current_level)]["effects"]

    def __init__(self, dict_to_load: dict) -> None:
        self.id = dict_to_load.get("id", "")
        self.current_level = dict_to_load.get("current_level", 1)

    def increase_level(self) -> None:
        self.current_level += 1

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "current_level": self.current_level,
        }


class SportsComplex():
    """
    A class to store the data of the sports complex.
    """

    current_level: int
    rooms_bought: dict[str, Room]  # id room and associated Room

    @ property
    def image(self) -> str:
        return PATH_BACKGROUNDS + f"sport_complex_{self.current_level}.jpg"

    @ property
    def max_number_athletes(self):
        return SPORTS_COMPLEX_EVOLUTION_DICT[
            str(self.current_level)]["max_number_athletes"]

    @ property
    def rooms_unlocked(self) -> dict[str, Room]:
        dict_rooms = {}
        for level in range(1, self.current_level+1):
            for element in SPORTS_COMPLEX_EVOLUTION_DICT[str(level)]["rooms_unlocked"]:
                room_id = element[0]

                # Add only the minimum level the user has not bought
                room_level = element[1]
                has_already_bought = self.check_has_already_bought_room(
                    room_id=room_id,
                    room_level=room_level
                )
                if room_id not in dict_rooms and not has_already_bought:
                    dict_rooms[room_id] = Room(
                        dict_to_load={
                            "id": room_id,
                            "current_level": room_level
                        }
                    )
        return dict_rooms

    def __init__(self, dict_to_load: dict) -> None:
        self.current_level = dict_to_load.get('current_level', 1)
        self.rooms_bought = {
            room_id: Room(dict_to_load=room_dict) for room_id, room_dict in dict_to_load.get('rooms_bought', {}).items()}

    def check_has_already_bought_room(self, room_id: str, room_level: str):
        for room_id_ref in self.rooms_bought:
            if room_id == room_id_ref:
                return self.rooms_bought[room_id].current_level >= room_level
        return False

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

    def get_athlete_from_id(self, athlete_id) -> Athlete:
        for athlete in self.team:
            if athlete.id == athlete_id:
                return athlete

    def get_trimester_gained_total_money(self) -> int:
        trimester_payment = 0
        for athlete in self.team:
            trimester_payment += athlete.get_trimester_gained_money()
        return trimester_payment

    def update_recrutable_athletes(self, new_athletes_list: list[Athlete]) -> None:
        # Diminish the time left to recruit and remove those with 0 time left
        list_athletes_to_remove = []
        athlete: Athlete
        for athlete in self.recrutable_athletes:
            athlete.time_for_recruit -= 1
            if athlete.time_for_recruit == 0:
                list_athletes_to_remove.append(athlete)
        for athlete in list_athletes_to_remove:
            self.recrutable_athletes.remove(athlete)

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
        self.recrutable_athletes.remove(athlete)

    def fire_athlete(self, athlete_id: str):
        for athlete in self.team:
            if athlete.id == athlete_id:
                break

        # Remove the athlete from the current team and put it in the fired team
        self.team.remove(athlete)
        self.fired_team.append(athlete)

    def buy_sports_complex(self, room_id: str):
        if room_id == "sports_complex":
            self.sports_complex.increase_level()
            self.money -= SPORTS_COMPLEX_EVOLUTION_DICT[str(self.sports_complex.current_level)]["price"]
        else:
            bought_room: Room = self.sports_complex.buy_room(room_id=room_id)
            self.money -= ROOMS_EVOLUTION_DICT[room_id][str(bought_room.current_level)]["price"]

    def get_medals_from_edition(self, edition: int) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.edition == edition:
                list_medals.append(medal)

        # Sort the list of medals first by sport_id and then by athlete_id
        list_medals.sort(key=lambda medal: (medal.sport_id, medal.athlete_id), reverse=True)

        return list_medals

    def get_medals_from_athlete(self, athlete_id: str) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.athlete_id == athlete_id:
                list_medals.append(medal)

        # Sort the list of medals first by sport_id and then by edition
        list_medals.sort(key=lambda medal: (medal.sport_id, medal.edition), reverse=True)

        return list_medals

    def get_medals_from_sport(self, sport_id: str) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.sport_id == sport_id:
                list_medals.append(medal)

        # Sort the list of medals first by edition and then by athlete_id
        list_medals.sort(key=lambda medal: (medal.edition, medal.athlete_id), reverse=True)

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

    def go_to_next_trimester(self):
        if self.trimester != 4:
            self.trimester += 1
        else:
            self.trimester = 1
            self.year += 1
            self.begin_new_year()

        # Update the stats of the athletes and the game depending on the activities performed
        for athlete in self.team:
            for activity_id in athlete.current_planning:
                activity: Activity = ACTIVITIES[activity_id]
                activity.apply_activity(athlete=athlete)

        # Update the amount of money due to salaries and activities
        self.money += self.get_trimester_gained_total_money()

        # Update the stats of the athletes according to their age and ill state
        for athlete in self.team:
            athlete.update_trimester_performance()

    def compute_average_level(self) -> int:
        if self.team == []:
            return 1

        # Take the average of the 5 best athletes
        list_athletes_scores = []
        for athlete in self.team:
            list_athletes_scores.append(athlete.global_score)
        list_athletes_scores.sort(reverse=True)

        list_five_best_athletes = list_athletes_scores
        if len(list_athletes_scores) > 5:
            list_five_best_athletes = list_athletes_scores[:5]
    
        average_score = sum(list_five_best_athletes) / len(list_five_best_athletes)
        
        for score_ref in LEVEL_DICT:
            if average_score <= score_ref:
                return LEVEL_DICT[score_ref]
        return 10

    def get_main_action(self) -> str:

        main_action = "plan" # or "being_competition_{mode}"

        # Summer competition trimester 2 each 4 years
        if self.year % NB_YEARS_BETWEEN_EDITION == 0:
            if self.trimester == 2:
                main_action = "being_competition_summer"

        return main_action

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

ACTIVITIES = load_json_file(PATH_ACTIVITIES)
for activity_id in ACTIVITIES:
    activity_dict = ACTIVITIES[activity_id]

    # Job activities
    if "_job" in activity_id:
        ACTIVITIES[activity_id] = JobActivity(
            dict_to_load={
                "id": activity_id,
                "condition": activity_dict.get("condition", None),
                "gain": activity_dict["gain"]
            }
        )
    
    # Other activities
    else:
        ACTIVITIES[activity_id] = Activity(
            dict_to_load={
                "id": activity_id,
                "effects": activity_dict.get("effects", []),
                "category": activity_dict.get("category", ""),
                "all_trimester": activity_dict.get("all_trimester", False),
                "price": activity_dict.get("price", 0),
                "gain": activity_dict.get("gain", 0),
                "condition": activity_dict.get("condition", None)
            }
        )
