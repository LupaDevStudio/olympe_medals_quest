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
from datetime import datetime
import time
import random as rd

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
    PATH_ROOMS_DICT,
    PATH_EVENTS
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

COUNTRY_NAME = "our_country"

MAX_ATHLETES_TO_SELECT = 3
PRICE_FIGHT_SELECTION = {
    1: 10000,
    2: 50000,
    3: 100000
}
REWARD_FIGHT = {
    1: {
        "gold": 100000,
        "silver": 70000,
        "bronze": 50000
    },
    2: {
        "gold": 500000,
        "silver": 200000,
        "bronze": 100000
    },
    3: {
        "gold": 1000000,
        "silver": 700000,
        "bronze": 500000
    }
}
REWARD_COMPETITION = {
    "national": {
        3: {
            1: 1000000,
            2: 700000,
            3: 500000
        }
    },
    "continental": {
        2: {
            1: 1000000,
            2: 700000,
            3: 500000
        },
        3: {
            1: 1000000,
            2: 700000,
            3: 500000
        }
    },
    "world": {
        1: {
            1: 50000,
            2: 35000,
            3: 25000
        },
        2: {
            1: 1000000,
            2: 700000,
            3: 500000
        },
        3: {
            1: 1000000,
            2: 700000,
            3: 500000
        }
    }
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
MIN_LEVEL_ATHLETE = 0.2
MIN_LEVEL_SPECIALIST = 0.4
MIN_LEVEL_BI_SPECIALIST = 0.6

### Experience ###

MAX_XP: int = 70
FACTOR_XP_SPORT_COMPETITION = 0.3
FACTOR_XP_SPORT_SPORT = 1
FACTOR_XP_STAT_SPORT = 0.3
FACTOR_XP_STAT_STAT = 1.2
FACTOR_XP_FIRST_STAT_STAT = 0.9
FACTOR_XP_SECOND_STAT_STAT = 0.6
FACTOR_XP_STAT_JOB_1 = 0.3
FACTOR_XP_STAT_JOB_2 = 0.5

SPORTS_COMPLEX_EVOLUTION_DICT = load_json_file(PATH_SPORTS_COMPLEX_DICT)
ROOMS_EVOLUTION_DICT = load_json_file(PATH_ROOMS_DICT)

NB_YEARS_BETWEEN_EDITION = 4

FACTOR_SPONSOR_REPUTATION = 300
MAX_REPUTATION = 1000

# 3 years
TIME_NUMBER_TRIMESTERS_LOBBYING_SPORTS_1 = 3 * 4
# 5 years
TIME_NUMBER_TRIMESTERS_LOBBYING_SPORTS_2 = 5 * 4

##############
### Events ###
##############

EVENTS_DICT = load_json_file(PATH_EVENTS)

#################
### Functions ###
#################


def generate_id() -> str:
    unique_id = uuid.uuid4()
    return str(unique_id)


def generate_learning_rates(double_proba=0.05, simple_proba=0.2):
    random_number = rd.random()
    if random_number < double_proba:
        return 2
    elif random_number < simple_proba:
        return 1.5
    return 1


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

def compute_xp_gain(current_xp: float, fatigue: float, factor: int, learning_rate: float, level_activity: int | None = None):
    """
    Compute the gain in experience after an activity.
    
    Parameters
    ----------
    current_xp : float
        Current experience of the athlete in the corresponding skill.
    fatigue : float
        Current fatigue of the athlete. The more the athlete is tired, the less the training will be efficient.
    factor : int
        Factor to multiply the gain in experience. The reference is the gain in sport for activities for sports.
    level_activity : int | None, optional (default is None)
        Level of the activity, when the activity is a sports or stats training.
    
    Returns
    -------
    float
        Gain in experience in the current skill.
    """

    def f(x: float, pow: float, y0: float) -> float:
        return y0 * (1 - (x / MAX_XP)**pow)

    # Take into account the fatigue
    FATIGUE_FACTOR: float = 0.5

    if level_activity is not None:

        # Set the quality of the training depending of the level of the activity
        if level_activity == 1:
            n = 0.5
            y0 = 2.5
            # The first level activity is not useful to train a skill that is above 40.
            if current_xp >= 50:
                return 0
        elif level_activity == 2:
            n = 1
            y0 = 2
            if current_xp < 10 or current_xp >= 60:
                return 0
        elif level_activity == 3:
            n = 1.5
            y0 = 1.75
            if current_xp < 20:
                return 0
        else:
            n = 2
            y0 = 1.5
            if current_xp < 30:
                return 0

    else:
        n = 1
        y0 = 2

    gross_xp: float = f(current_xp, n, level_activity*y0)
    gain_xp = factor * learning_rate * gross_xp * (1 - FATIGUE_FACTOR * fatigue)
    return round(gain_xp, 3)

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
    category: str  # "sports", "stats", "press", "job", "secrets", "break", "competition", "others"
    all_trimester: bool
    price: int
    gain: int
    condition: int
    can_be_done_when_ill: bool
    can_be_done_when_hurt: bool

    def __init__(self, dict_to_load: dict):
        self.id = dict_to_load.get("id", "")
        self.effects = dict_to_load.get("effects", [])
        self.category = dict_to_load.get("category", "")
        self.all_trimester = dict_to_load.get("all_trimester", False)
        self.price = dict_to_load.get("price", 0)
        self.gain = dict_to_load.get("gain", 0)
        self.condition = dict_to_load.get("condition", 0)
        self.can_be_done_when_ill = dict_to_load.get(
            "can_be_done_when_ill", False)
        self.can_be_done_when_hurt = dict_to_load.get(
            "can_be_done_when_hurt", False)

    def compute_virtual_progress_previous_activities(self, athlete, activity_pos_in_planning: int) -> dict:
        stats_dict = {}
        sports_dict = {}
        fatigue = athlete.fatigue

        for stat in athlete.stats:
            stats_dict[stat] = athlete.stats[stat]["points"]
        for sport in athlete.sports:
            sports_dict[sport] = athlete.sports[sport]["points"]

        # Apply the virtual effects of the previous activities of the planning
        if activity_pos_in_planning >= 1:
            previous_activity_id = athlete.current_planning[activity_pos_in_planning - 1]
            previous_activity: Activity = ACTIVITIES[previous_activity_id]

            # Gain in stats
            gain_stats = previous_activity.get_gain_stats(
                athlete=athlete,
                activity_pos_in_planning=activity_pos_in_planning - 1
            )
            for stat in gain_stats:
                stats_dict[stat] += gain_stats[stat]

            # Gain in sports
            gain_sports = previous_activity.get_gain_sports(
                athlete=athlete,
                activity_pos_in_planning=activity_pos_in_planning - 1
            )
            for sport in gain_sports:
                sports_dict[sport] += gain_sports[sport]

            # TODO fatigue

            if activity_pos_in_planning >= 2:
                previous_activity_id = athlete.current_planning[activity_pos_in_planning - 2]
                previous_activity: Activity = ACTIVITIES[previous_activity_id]

                # Gain in stats
                gain_stats = previous_activity.get_gain_stats(
                    athlete=athlete,
                    activity_pos_in_planning=activity_pos_in_planning - 2
                )
                for stat in gain_stats:
                    stats_dict[stat] += gain_stats[stat]

                # Gain in sports
                gain_sports = previous_activity.get_gain_sports(
                    athlete=athlete,
                    activity_pos_in_planning=activity_pos_in_planning - 2
                )
                for sport in gain_sports:
                    sports_dict[sport] += gain_sports[sport]

                # TODO fatigue
        return {
            "stats": stats_dict,
            "sports": sports_dict,
            "fatigue": fatigue
        }


    def get_gain_stats(self, athlete, activity_pos_in_planning: int) -> dict:
        return {}
    
    def get_gain_sports(self, athlete, activity_pos_in_planning: int) -> dict:
        return {}

    def get_gain(self, athlete, activity_pos_in_planning: int) -> int:
        return 0

    def get_effects(self, athlete) -> dict:
        dict_effects = {}
        for effect in self.effects:

            # For fatigue
            if effect[0] == "fatigue":
                final_fatigue = athlete.fatigue + effect[1]
                if final_fatigue > 1:
                    dict_effects["fatigue"] = 1
                elif final_fatigue < 0:
                    dict_effects["fatigue"] = 0
                else:
                    dict_effects["fatigue"] = final_fatigue

            # For injury risk
            elif effect[0] == "injury_risk":
                final_injury_risk = athlete.injury_risk + effect[1]
                if final_injury_risk > 1:
                    dict_effects["injury_risk"] = 1
                elif final_injury_risk < 0:
                    dict_effects["injury_risk"] = 0
                else:
                    dict_effects["injury_risk"] = final_injury_risk

            # For illness and injuries
            elif effect[0] in ["illness", "injury"]:
                if effect[0] in athlete.health["type_injury"]:
                    if effect[1] == "heal_one_trimester":
                        dict_effects["health"] = copy.deepcopy(athlete.health)
                        dict_effects["health"]["time_absent"] -= 1
                    elif effect[1] == "heal_all":
                        dict_effects["health"] = copy.deepcopy(
                            DEFAULT_HEALTH_DICT)

        return dict_effects

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        dict_effects = self.get_effects(athlete=athlete)
        for key_effect in dict_effects:
            consequence = dict_effects[key_effect]
            if key_effect == "fatigue":
                athlete.fatigue = consequence
            elif key_effect == "injury_risk":
                athlete.injury_risk = consequence
            elif key_effect == "illness":
                athlete.health = copy.deepcopy(consequence)


class InterviewActivity(Activity):
    """
    A class to store the data of the interview activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "press"

    def get_gain_reputation(self, athlete) -> int:
        current_reputation = athlete.reputation
        current_charm = athlete.stats["charm"]["points"]

        # TODO
        gain_reputation = 0

        return gain_reputation

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        gain_reputation = self.get_gain_reputation(athlete=athlete)
        athlete.reputation += gain_reputation


class SponsorActivity(Activity):
    """
    A class to store the data of the sponsors activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "press"

    def get_gain(self, athlete, activity_pos_in_planning: int) -> int:
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
        self.level_job = dict_to_load.get("level_job", 1)

    def get_can_access_gain_money_gain_stats(self, athlete, activity_pos_in_planning: int) -> dict:

        ### Activities not based on stats ###

        if self.id in ["basic_job", "best_job"]:
            return {
                "can_access": True,
                "gain_money": self.gain
            }

        ### Activities based on a stat ###

        fix_part = self.gain
        stat = self.id.split("_")[0]

        current_skills = self.compute_virtual_progress_previous_activities(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning
        )
        current_stats = current_skills["stats"]
        current_fatigue = current_skills["fatigue"]
        athlete_stat = current_stats[stat]

        # The athlete is not skilled enough to perform the job
        if athlete_stat < self.condition:
            return {"can_access": False}

        variable_part = int(fix_part * athlete_stat / MAX_XP)

        gain_stat = compute_xp_gain(
            current_xp=athlete_stat,
            factor=FACTOR_XP_STAT_JOB_1 if self.level_job == 1 else FACTOR_XP_STAT_JOB_2,
            fatigue=current_fatigue,
            learning_rate=athlete.stats[stat]["learning_rate"]
        )

        return {
            "can_access": True,
            "gain_money": fix_part + variable_part,
            "gain_stats": {stat : gain_stat}
        }

    def get_gain(self, athlete, activity_pos_in_planning: int) -> int:
        dict_effects = self.get_can_access_gain_money_gain_stats(
            athlete=athlete, activity_pos_in_planning=activity_pos_in_planning)
        return dict_effects.get("gain_money", 0)

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        dict_effects = self.get_can_access_gain_money_gain_stats(
            athlete=athlete, activity_pos_in_planning=activity_pos_in_planning)
        dict_effects_stats = dict_effects.get("gain_stats", {})

        for key in dict_effects_stats:
            athlete.stats[key]["points"] += dict_effects_stats[key]


class TribuneActivity(Activity):
    """
    A class to store the data of the research sports activities.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "press"
        self.type_sport = int(self.id.replace("tribune_", ""))

    def gain_research_in_sport(self, game):
        researching_sport_id: str = game.get_current_unlocking_sport()
        if researching_sport_id is None:
            return 0

        researching_sport: Sport = SPORTS[researching_sport]
        if self.type_sport == 1 and researching_sport.category == 1:
            return 1 / TIME_NUMBER_TRIMESTERS_LOBBYING_SPORTS_1
        elif self.type_sport == 2 and researching_sport.category == 2:
            return 1 / TIME_NUMBER_TRIMESTERS_LOBBYING_SPORTS_2

        return 0

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        researching_sport_id = game.get_current_unlocking_sport()
        gain_research = self.gain_research_in_sport(game=game)
        game.sports_unlocking_progress[researching_sport_id] += gain_research


class CompetitionActivity(Activity):
    """
    A class to store the data of the competition activities.
    """

    type_competition: Literal["national", "continental", "world"]
    sport_id: str
    category_sport: int

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "competition"
        self.type_competition = dict_to_load["type_competition"]
        self.sport_id = dict_to_load["sport_id"]
        self.category_sport = dict_to_load["category_sport"]

    def get_gain_sports(self, athlete, activity_pos_in_planning: int):
        current_skills = self.compute_virtual_progress_previous_activities(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning
        )
        current_sports = current_skills["sports"]
        current_fatigue = current_skills["fatigue"]

        gain_sport = compute_xp_gain(
            current_xp=current_sports[self.sport_id],
            factor=FACTOR_XP_SPORT_COMPETITION,
            fatigue=current_fatigue,
            learning_rate=athlete.sports[self.sport_id]["learning_rate"]
        )
        return {self.sport_id : gain_sport}

    def get_result(self, athlete) -> int:
        # TODO
        return 1

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        # TODO rajouter la fatigue et risque de blessure aussi

        # Gain of the competition
        result = self.get_result(athlete=athlete)
        # TODO
        # if result == 1:
        #     if

        # Gain in sports
        dict_gain_sports = self.get_gain_sports(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning)
        for key in dict_gain_sports:
            athlete.sports[key]["points"] += dict_gain_sports[key]


class SportsActivity(Activity):
    """
    A class to store the data of the sports activities.
    """

    sport_id: str
    category_sport: int
    level: int

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "sports"
        self.level = dict_to_load["level"]
        self.sport_id = dict_to_load["sport_id"]
        self.category_sport = dict_to_load["category_sport"]

    def get_gain_sports(self, athlete, activity_pos_in_planning: int):
        current_skills = self.compute_virtual_progress_previous_activities(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning
        )
        current_sports = current_skills["sports"]
        current_fatigue = current_skills["fatigue"]
        gain_sport = compute_xp_gain(
            current_xp=current_sports[self.sport_id],
            factor=FACTOR_XP_SPORT_SPORT,
            fatigue=current_fatigue,
            level_activity=self.level,
            learning_rate=athlete.sports[self.sport_id]["learning_rate"]
        )
        return {self.sport_id : gain_sport}

    def get_gain_stats(self, athlete, activity_pos_in_planning: int):
        current_skills = self.compute_virtual_progress_previous_activities(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning
        )
        current_stats = current_skills["stats"]
        current_fatigue = current_skills["fatigue"]
        dict_stats = {}
        for stat in SPORTS[self.sport_id].stats:
            dict_stats[stat] = compute_xp_gain(
                current_xp=current_stats[stat],
                factor=FACTOR_XP_STAT_SPORT,
                fatigue=current_fatigue,
                level_activity=self.level,
                learning_rate=athlete.stats[stat]["learning_rate"]
            )
        return dict_stats

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        # TODO rajouter la fatigue et risque de blessure aussi

        # Gain in sports
        dict_gain_sports = self.get_gain_sports(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning)
        for key in dict_gain_sports:
            athlete.sports[key]["points"] += dict_gain_sports[key]

        # Gain in stats
        dict_gain_stats = self.get_gain_stats(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning)
        for key in dict_gain_stats:
            athlete.stats[key]["points"] += dict_gain_stats[key]


class StatsActivity(Activity):
    """
    A class to store the data of the stats activities.
    """

    level: int
    first_stat: str
    second_stat: str | None

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "stats"
        self.level = dict_to_load.get("level", 1)
        self.first_stat = dict_to_load["first_stat"]
        self.second_stat = dict_to_load.get("second_stat", None)

    def get_gain_stats(self, athlete, activity_pos_in_planning: int):
        dict_stats = {}

        current_skills = self.compute_virtual_progress_previous_activities(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning
        )
        current_stats = current_skills["stats"]
        current_fatigue = current_skills["fatigue"]

        # Compute the gain for the main stat involved
        first_factor = FACTOR_XP_STAT_STAT if self.second_stat is None else FACTOR_XP_FIRST_STAT_STAT
        dict_stats[self.first_stat] = compute_xp_gain(
            current_xp=current_stats[self.first_stat],
            factor=first_factor,
            fatigue=current_fatigue,
            level_activity=self.level,
            learning_rate=athlete.stats[self.first_stat]["learning_rate"]
        )

        # Compute the gain for the second stat involved if some
        if self.second_stat is not None:
            dict_stats[self.second_stat] = compute_xp_gain(
                current_xp=current_stats[self.second_stat],
                factor=FACTOR_XP_SECOND_STAT_STAT,
                fatigue=current_fatigue,
                level_activity=self.level,
                learning_rate=athlete.stats[self.second_stat]["learning_rate"]
            )

        return dict_stats

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        # TODO rajouter la fatigue et risque de blessure aussi

        # Gain in stats
        dict_gain_stats = self.get_gain_stats(
            athlete=athlete,
            activity_pos_in_planning=activity_pos_in_planning)
        for key in dict_gain_stats:
            athlete.stats[key]["points"] += dict_gain_stats[key]


class TransferSportActivity(Activity):
    """
    A class to store the data of the transfer activity.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "others"
        self.sport_id = dict_to_load["sport_id"]

    def get_dict_new_sport(self, athlete):
        new_dict_sport = copy.deepcopy(DEFAULT_STAT_DICT)
        new_sport: Sport = SPORTS[self.sport_id]
        requirements = new_sport.requirements

        best_learning_rate = 1
        points_from_previous_sports = []
        for required_sport_id in requirements:
            if required_sport_id in athlete.sports:
                points_from_previous_sports.append(
                    athlete.sports[required_sport_id]["points"])
                learning_rate = athlete.sports[required_sport_id]["learning_rate"]

                # Take the best learning rate from the two below sports
                if learning_rate > best_learning_rate:
                    best_learning_rate = learning_rate

        # If 1 sport learned => 60% from this sport transferred
        points = 0
        if len(points_from_previous_sports) == 1:
            points = points_from_previous_sports[0] * 0.6

        # If 2 sports learned => 60% from the best sports then 20% of the other
        elif len(points_from_previous_sports) == 2:
            points_from_previous_sports.sort()
            points = points_from_previous_sports[0] * 0.2 + \
                points_from_previous_sports[1] * 0.6

        new_dict_sport["points"] = points
        new_dict_sport["learning_rate"] = best_learning_rate

        return new_dict_sport

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        # Apply fatigue and injury risk
        super().apply_activity(athlete, game)

        # Unlock the new sport
        athlete.sports[self.sport_id] = self.get_dict_new_sport(
            athlete=athlete)


class StartNewSportActivity(Activity):
    """
    A class to store the data of the start a new sport activity.
    """

    def __init__(self, dict_to_load: dict):
        super().__init__(dict_to_load)

        self.category = "others"
        self.sport_id = dict_to_load["sport_id"]

    def get_dict_new_sport(self, athlete):
        new_dict_sport = copy.deepcopy(DEFAULT_STAT_DICT)
        new_sport: Sport = SPORTS[self.sport_id]

        # Generate the learning rate
        learning_rate = generate_learning_rates()
        # Generate the points related to the stats of the sport
        points = 0
        for stat in new_sport.stats:
            if athlete.stats[stat]["points"] > 20:
                points += 5
            elif athlete.stats[stat]["points"] > 30:
                points += 10
            elif athlete.stats[stat]["points"] > 40:
                points += 15
            elif athlete.stats[stat]["points"] > 50:
                points += 20
            else:
                points += 25
        points /= len(new_sport.stats)

        new_dict_sport["points"] = points
        new_dict_sport["learning_rate"] = learning_rate

        return new_dict_sport

    def apply_activity(self, athlete, game, activity_pos_in_planning: int) -> None:
        # Apply fatigue and injury risk
        super().apply_activity(athlete, game)

        # Unlock the new sport
        athlete.sports[self.sport_id] = self.get_dict_new_sport(
            athlete=athlete)

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
    nationality: str # name of the country
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
    def full_name(self) -> str:
        return self.first_name + " " + self.name

    @ property
    def image(self) -> str:
        return PATH_ATHLETES_IMAGES + f"athlete_{self.id}.png"

    @ property
    def global_score_for_salary(self) -> float:
        skills_part = 0

        # Stats part
        for stat in self.stats:
            skills_part += self.stats[stat]["points"]

        # Sports part with the two best sports
        all_sports = []
        for sport_id in self.sports:
            sport: Sport = SPORTS[sport_id]
            all_sports.append(
                [sport.category, self.sports[sport_id]["points"]])
        all_sports = sorted(all_sports)

        number_sports_to_take = min(len(all_sports), 2)
        for counter in range(number_sports_to_take):
            skills_part += all_sports[counter][1]

        skills_part = skills_part / (MAX_XP * (5+number_sports_to_take))

        # Reputation for half the score
        reputation_part = self.reputation / MAX_REPUTATION
        score = 0.5*skills_part + 0.5*reputation_part

        return score

    @ property
    def global_score(self) -> float:
        """
        Global score of the athlete that only takes the stats into account not the reputation.
        
        Parameters
        ----------
        
        Returns
        -------
        float
            Score of the athlete.
        """
        score = 0

        # Stats part
        for stat in self.stats:
            score += self.stats[stat]["points"]

        # Sports part with the two best sports
        all_sports = []
        for sport_id in self.sports:
            sport: Sport = SPORTS[sport_id]
            all_sports.append(
                [sport.category, self.sports[sport_id]["points"]])
        all_sports = sorted(all_sports)

        number_sports_to_take = min(len(all_sports), 2)
        for counter in range(number_sports_to_take):
            score += all_sports[counter][1]

        score = score / (MAX_XP * (5+number_sports_to_take))

        return score

    @ property
    def is_hurt(self) -> str:
        return self.health["is_hurt"]

    def __init__(self, dict_to_load: dict) -> None:
        self.id = dict_to_load.get("id", generate_id())
        self.nationality = dict_to_load.get("nationality", COUNTRY_NAME)
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
        self.current_planning = dict_to_load.get(
            "current_planning", self.generate_default_planning())

    def generate_default_planning(self) -> list[str]:
        main_sport_id = list(self.sports.keys())[0]
        main_sport: Sport = SPORTS[main_sport_id]
        sport_category = main_sport.category
        activity_id = f"sports_{sport_category}_{main_sport_id}_training_1"
        return [activity_id, activity_id, activity_id]

    def get_best_sports(self, number_sports: int = 2):
        # Sort the sports by decreasing points
        sorted_sports = sorted(
            self.sports.items(), key=lambda x: x[1]['points'], reverse=True)

        # Extract the first sports
        best_sports = dict(sorted_sports[:number_sports])
        return dict(reversed(best_sports.items()))

    def set_salary(self, salary: int):
        self.salary = salary

    def set_recruit_price(self, recruit_price: int):
        self.recruit_price = recruit_price

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

        for counter in range(len(self.current_planning)):
            activity_id = self.current_planning[counter]
            activity: Activity = ACTIVITIES[activity_id]

            # Potential price of the activity
            trimester_payment -= activity.price
            # Potential gain of the activity
            trimester_payment += activity.get_gain(
                athlete=self,
                activity_pos_in_planning=counter)

        return trimester_payment

    def export_dict(self) -> dict:
        return {
            "id": self.id,
            "nationality": self.nationality,
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
    def unlocked_activities(self) -> list[str]:
        return ROOMS_EVOLUTION_DICT[self.id][str(self.current_level)].get("unlocked_activities", [])

    @ property
    def effects(self) -> list:
        return ROOMS_EVOLUTION_DICT[self.id][str(self.current_level)].get("effects", [])

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
        for level in range(1, self.current_level + 1):
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
            return self.edition * NB_YEARS_BETWEEN_EDITION - NB_YEARS_BETWEEN_EDITION // 2

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

    difficulty: Literal["easy", "medium", "difficult"]
    total_time_played: float  # in seconds
    last_time_played: str
    unlocked_characters: list[str]
    notifications_list: list[str]
    # "team", "recruit", "sports_complex", "sports_menu", "activities_menu", "medals", "shop"
    unlocked_menus: list[str]
    # "retirement", "grow_old", "fire", "reputation", "injury", "illness", "fatigue", "salary_augmentation", "unlock_sports"
    unlocked_modes: list[str]
    unlocked_activities: list[str]
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
    seen_dialogs: list[str]
    first_sport: str  # Id of the first sport

    @property
    def unlocked_sports(self) -> list[str]:
        unlocked_sports = []
        for key in self.sports_unlocking_progress:
            value = self.sports_unlocking_progress[key]
            if value == 1:
                unlocked_sports.append(key)
        return unlocked_sports

    @property
    def unlocked_activity_categories(self) -> list[str]:
        unlocked_activity_categories = []
        print("UNLOCKED ACTIVITIES", self.unlocked_activities)
        for activity_id in self.unlocked_activities:
            print(activity_id)

            # Special case for sports
            if "sports_" in activity_id:
                category = "sports"
            # Special case for competitions
            elif "competition_" in activity_id:
                category = "competition"
            else:
                activity: Activity = ACTIVITIES[activity_id]
                category = activity.category

            if category not in unlocked_activity_categories:
                unlocked_activity_categories.append(category)
        return unlocked_activity_categories

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
            if self.year % NB_YEARS_BETWEEN_EDITION == NB_YEARS_BETWEEN_EDITION // 2:
                return self.year // NB_YEARS_BETWEEN_EDITION
            return (self.year + NB_YEARS_BETWEEN_EDITION // 2) // NB_YEARS_BETWEEN_EDITION

    def __init__(self, dict_to_load: dict = {}) -> None:

        self.difficulty = dict_to_load.get("difficulty", "medium")
        self.total_time_played = dict_to_load.get("total_time_played", 0)
        self.last_time_played = dict_to_load.get(
            "last_time_played", self.set_last_time_played())
        self.unlocked_characters = dict_to_load.get("unlocked_characters", [])
        self.notifications_list = dict_to_load.get("notifications_list", [])
        self.unlocked_menus = dict_to_load.get("unlocked_menus", [])
        self.unlocked_modes = dict_to_load.get("unlocked_modes", [])
        self.unlocked_activities = dict_to_load.get("unlocked_activities", [])
        self.money = dict_to_load.get("money", 0)
        self.year = dict_to_load.get("year", 2)
        self.trimester = dict_to_load.get("trimester", 4)
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
        self.seen_dialogs = dict_to_load.get("seen_dialogs", [])
        self.first_sport = dict_to_load.get("first_sport", "")
        if self.first_sport == "":
            self.first_sport = self.generate_first_sport()

    def get_background_image(self) -> int:
        return self.sports_complex.image

    def get_athlete_from_id(self, athlete_id) -> Athlete:
        # For the main team
        for athlete in self.team:
            if athlete.id == athlete_id:
                return athlete
        # For the athletes to recruit
        for athlete in self.recrutable_athletes:
            if athlete.id == athlete_id:
                return athlete
        # For the retired team
        for athlete in self.retired_team:
            if athlete.id == athlete_id:
                return athlete

    def get_unlocked_activities_from_category(self, category: str, god_mode: bool = False) -> list[str]:
        if god_mode:
            all_activities = list(load_json_file(PATH_ACTIVITIES).keys())
        else:
            all_activities = self.unlocked_activities
        list_activities = []
        for activity_id in all_activities:
            if "sports_" in activity_id:
                activity_category = "sports"
            elif "competition_" in activity_id:
                activity_category = "competition"
            elif activity_id in ["start_new_sport", "transfer_sport"]:
                activity_category = "others"
            else:
                activity: Activity = ACTIVITIES[activity_id]
                activity_category = activity.category
            if activity_category == category:
                list_activities.append(activity_id)
        return list_activities

    def get_trimester_gained_total_money(self) -> int:
        trimester_payment = 0
        for athlete in self.team:
            trimester_payment += athlete.get_trimester_gained_money()
        return trimester_payment

    def get_current_sports_category(self) -> int:
        current_category = 1
        for athlete in self.team:
            for sport_id in athlete.sports:
                sport: Sport = SPORTS[sport_id]
                if sport.category > current_category:
                    current_category = sport.category
                    if current_category == 3:
                        return current_category
        return current_category

    def get_all_sports_from_current_category_or_less(self) -> list[str]:
        current_category = self.get_current_sports_category()
        list_sports: list[str] = []
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            if sport.category <= current_category:
                list_sports.append(sport_id)
        return list_sports

    def get_current_unlocking_sport(self) -> str | None:
        for sport_id in self.sports_unlocking_progress:
            if 1 > self.sports_unlocking_progress[sport_id] > 0:
                return sport_id
        return None

    def compute_results_fight_from_sport(self, sport_id: str) -> list[Athlete]:
        return [self.team[0], self.team[0], self.team[0], self.team[0], self.team[0], self.team[0], self.team[0], self.team[0], self.team[0], self.team[0]]

    def generate_first_sport(self) -> str:
        list_possible_sports = []
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            # Take only sports of first category
            if sport.category == 1:
                # Remove sports with charm
                if CHARM not in sport.stats:
                    list_possible_sports.append(sport_id)
        first_sport = rd.choice(list_possible_sports)
        self.unlock_new_sport(sport_id=first_sport)
        return first_sport

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
            self.money -= SPORTS_COMPLEX_EVOLUTION_DICT[str(
                self.sports_complex.current_level)]["price"]
        else:
            bought_room: Room = self.sports_complex.buy_room(room_id=room_id)
            self.money -= ROOMS_EVOLUTION_DICT[room_id][str(
                bought_room.current_level)]["price"]

            # Add the activities unlocked with this new room
            for activity in bought_room.unlocked_activities:
                self.unlocked_activities.append(activity)

    def get_medals_from_edition(self, edition: int) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.edition == edition:
                list_medals.append(medal)

        # Sort the list of medals first by sport_id and then by athlete_id
        list_medals.sort(key=lambda medal: (
            medal.sport_id, medal.athlete_id), reverse=True)

        return list_medals

    def get_medals_from_athlete(self, athlete_id: str) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.athlete_id == athlete_id:
                list_medals.append(medal)

        # Sort the list of medals first by sport_id and then by edition
        list_medals.sort(key=lambda medal: (
            medal.sport_id, medal.edition), reverse=True)

        return list_medals

    def get_medals_from_sport(self, sport_id: str) -> list[Medal]:
        list_medals = []
        for medal in self.medals:
            if medal.sport_id == sport_id:
                list_medals.append(medal)

        # Sort the list of medals first by edition and then by athlete_id
        list_medals.sort(key=lambda medal: (
            medal.edition, medal.athlete_id), reverse=True)

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

    def get_best_athlete_image(self) -> str:
        best_score: int = 0
        best_athlete: Athlete | None = None
        for athlete in self.team:
            if athlete.global_score_for_salary >= best_score:
                best_score = athlete.global_score_for_salary
                best_athlete = athlete
        if best_athlete is None:
            return ""
        return best_athlete.image

    def win_medal(self, sport_id, athlete_id, type: Literal["gold", "silver", "bronze"], edition: int, type_edition: Literal["summer", "winter"] = "summer"):
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
            counter_activity = 0
            for activity_id in athlete.current_planning:
                activity: Activity = ACTIVITIES[activity_id]
                activity.apply_activity(
                    athlete=athlete,
                    game=self,
                    activity_pos_in_planning=counter_activity)
                counter_activity += 1

        # Update the amount of money due to salaries and activities
        self.money += self.get_trimester_gained_total_money()

        # Update the stats of the athletes according to their age and ill state
        for athlete in self.team:
            athlete.update_trimester_performance()

    def compute_average_level(self) -> int:
        if self.team == []:
            return MIN_LEVEL_ATHLETE

        # Take the average of the 5 best athletes
        list_athletes_scores = []
        for athlete in self.team:
            list_athletes_scores.append(athlete.global_score)
        list_athletes_scores.sort(reverse=True)

        list_five_best_athletes = list_athletes_scores
        if len(list_athletes_scores) > 5:
            list_five_best_athletes = list_athletes_scores[:5]

        average_score = sum(list_five_best_athletes) / \
            len(list_five_best_athletes)

        return max(average_score, MIN_LEVEL_ATHLETE)

    def get_main_action(self) -> str:

        main_action = "plan"  # or "begin_competition_{mode}"

        # Summer competition trimester 3 each 4 years
        if self.year % NB_YEARS_BETWEEN_EDITION == 0:
            if self.trimester == 3:
                main_action = "begin_competition_summer"

        return main_action

    def begin_new_year(self):
        for athlete in self.team:
            athlete.age += 1

    def unlock_new_sport(self, sport_id: str, mode: Literal["summer", "winter"] = "summer"):
        self.sports_unlocking_progress[sport_id] = 1
        if mode == "summer":
            self.selected_athletes_summer[sport_id] = []
        elif mode == "winter":
            self.selected_athletes_winter[sport_id] = []

    def compute_total_spent_money_selection(self, mode: Literal["summer", "winter"] = "summer") -> int:
        total_money_spent = 0

        if mode == "summer":
            for sport_id in self.selected_athletes_summer:
                sport: Sport = SPORTS[sport_id]
                sport_category = sport.category
                price_sport = PRICE_FIGHT_SELECTION[sport_category]
                total_money_spent += price_sport * \
                    len(self.selected_athletes_summer[sport_id])

        elif mode == "winter":
            for sport_id in self.selected_athletes_winter:
                sport: Sport = SPORTS[sport_id]
                sport_category = sport.category
                price_sport = PRICE_FIGHT_SELECTION[sport_category]
                total_money_spent += price_sport * \
                    len(self.selected_athletes_winter[sport_id])

        return total_money_spent

    def get_price_selection_for_sport(self, sport_id: str, mode: Literal["summer", "winter"] = "summer") -> int:
        number_athletes_selected = self.get_number_athletes_selected_for_sport(
            sport_id=sport_id, mode=mode
        )
        sport: Sport = SPORTS[sport_id]
        return number_athletes_selected * PRICE_FIGHT_SELECTION[sport.category]

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
            price_sport = PRICE_FIGHT_SELECTION[sport.category]
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

    def set_last_time_played(self):
        self.last_time_played = datetime.now().strftime("%m/%d/%Y - %H:%M")

    def export_dict(self):
        return {
            "difficulty": self.difficulty,
            "total_time_played": self.total_time_played,
            "last_time_played": self.last_time_played,
            "unlocked_characters": self.unlocked_characters,
            "notifications_list": self.notifications_list,
            "unlocked_modes": self.unlocked_modes,
            "unlocked_menus": self.unlocked_menus,
            "unlocked_activities": self.unlocked_activities,
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
            "seen_dialogs": self.seen_dialogs,
            "first_sport": self.first_sport
        }

    def get_sport_in_research(self):
        for sport in self.sports_unlocking_progress:
            if 1 > self.sports_unlocking_progress[sport] > 0:
                return sport
        return None


class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.settings = data["settings"]
        self.tutorial = data.get("tutorial", {})
        self.seen_dialogs = data.get("seen_dialogs", [])
        self.total_time_played = data.get("total_time_played", 0)
        self.session_start_time = time.time()
        self.game_1 = Game(
            dict_to_load=data["game_1"]) if \
            "game_1" in data and data["game_1"] is not None else None
        self.game_2 = Game(
            dict_to_load=data["game_2"]) if \
            "game_2" in data and data["game_2"] is not None else None
        self.game_3 = Game(
            dict_to_load=data["game_3"]) if \
            "game_3" in data and data["game_3"] is not None else None
        self.save_changes()

    def get_game(self, id_game: int) -> Game:
        if id_game == 1:
            return self.game_1
        elif id_game == 2:
            return self.game_2
        else:
            return self.game_3

    def start_new_game(self, difficulty: Literal["easy", "medium", "difficult"]) -> int:
        new_game = Game(
            dict_to_load={"difficulty": difficulty}
        )

        if self.game_1 is None:
            self.game_1 = new_game
            return 1
        elif self.game_2 is None:
            self.game_2 = new_game
            return 2
        else:
            self.game_3 = new_game
            return 3

    def can_start_new_game(self):
        return self.game_1 is None or self.game_2 is None or self.game_3 is None

    def delete_game(self, id_game: int):
        if id_game == 1:
            self.game_1 = None
        elif id_game == 2:
            self.game_2 = None
        else:
            self.game_3 = None

    def stop_game(self, id_game: int | None):
        self.total_time_played += time.time() - self.session_start_time
        if id_game is not None:
            current_game = self.get_game(id_game=id_game)
            current_game.set_last_time_played()

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
            "game_1": self.game_1.export_dict() if self.game_1 is not None else None,
            "game_2": self.game_2.export_dict() if self.game_2 is not None else None,
            "game_3": self.game_3.export_dict() if self.game_3 is not None else None,
            "seen_dialogs": self.seen_dialogs,
            "total_time_played": self.total_time_played
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
SPORTS: dict[str, Sport]

temp_activities = load_json_file(PATH_ACTIVITIES)
ACTIVITIES = {}
for activity_id in temp_activities:
    activity_dict = temp_activities[activity_id]

    dict_to_load = {
        "id": activity_id,
        "effects": activity_dict.get("effects", []),
        "category": activity_dict.get("category", ""),
        "type_activity": activity_dict.get("type_activity", ""),
        "all_trimester": activity_dict.get("all_trimester", False),
        "price": activity_dict.get("price", 0),
        "gain": activity_dict.get("gain", 0),
        "condition": activity_dict.get("condition", None),
        "can_be_done_when_hurt": activity_dict.get("can_be_done_when_hurt", False),
        "can_be_done_when_ill": activity_dict.get("can_be_done_when_ill", False)
    }

    # Job activities
    if "_job" in activity_id:
        ACTIVITIES[activity_id] = JobActivity(
            dict_to_load=dict_to_load)

    # Interview activities
    elif activity_id == "interview":
        ACTIVITIES[activity_id] = InterviewActivity(
            dict_to_load=dict_to_load)

    # Sponsor activities
    elif activity_id == "sponsor":
        ACTIVITIES[activity_id] = SponsorActivity(
            dict_to_load=dict_to_load)

    # Tribune activities
    elif "tribune" in activity_id:
        ACTIVITIES[activity_id] = TribuneActivity(
            dict_to_load=dict_to_load)

    # Competition activities
    elif "competition" in activity_id:
        list_infos = activity_id.split("_")
        type_competition = list_infos[1]
        category_sport = list_infos[2]
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            if str(sport.category) == category_sport:
                new_activity_id = f"competition_{type_competition}_{sport_id}_{category_sport}"
                new_dict_to_load = copy.deepcopy(dict_to_load)
                new_dict_to_load["id"] = new_activity_id
                new_dict_to_load["type_competition"] = type_competition
                new_dict_to_load["sport_id"] = sport_id
                new_dict_to_load["category_sport"] = int(category_sport)
                ACTIVITIES[new_activity_id] = CompetitionActivity(
                    dict_to_load=new_dict_to_load)

    # Sports activities
    elif "sports_" in activity_id:
        list_infos = activity_id.split("_")  # "sports_2_training_4"
        category_sport = list_infos[1]
        level_activity = list_infos[3]
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            if str(sport.category) == category_sport:
                new_activity_id = f"sports_{category_sport}_{sport_id}_training_{level_activity}"
                new_dict_to_load = copy.deepcopy(dict_to_load)
                new_dict_to_load["id"] = new_activity_id
                new_dict_to_load["level"] = int(level_activity)
                new_dict_to_load["sport_id"] = sport_id
                new_dict_to_load["category_sport"] = int(category_sport)
                ACTIVITIES[new_activity_id] = SportsActivity(
                    dict_to_load=new_dict_to_load)

    # Stats activities
    elif "stats_" in activity_id:
        # "stats_speed_2", "stats_speed_strength"
        list_infos = activity_id.split("_")
        first_stat = list_infos[1]
        second_element = list_infos[2]
        try:
            level = int(second_element)
            new_dict_to_load = copy.deepcopy(dict_to_load)
            new_dict_to_load["level"] = level
            new_dict_to_load["first_stat"] = first_stat
        except:
            second_stat = second_element
            new_dict_to_load = copy.deepcopy(dict_to_load)
            new_dict_to_load["first_stat"] = first_stat
            new_dict_to_load["second_stat"] = second_stat
            new_dict_to_load["level"] = 3
        ACTIVITIES[activity_id] = StatsActivity(
            dict_to_load=new_dict_to_load)

    # Transfer sport activities
    elif "transfer_sport" in activity_id:
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            if sport.category > 1:
                new_activity_id = f"transfer_sport_{sport_id}"
                new_dict_to_load = copy.deepcopy(dict_to_load)
                new_dict_to_load["id"] = new_activity_id
                new_dict_to_load["sport_id"] = sport_id
                ACTIVITIES[new_activity_id] = TransferSportActivity(
                    dict_to_load=new_dict_to_load)

    # Start new sport activities
    elif "start_new_sport" in activity_id:
        for sport_id in SPORTS:
            sport: Sport = SPORTS[sport_id]
            new_activity_id = f"start_new_sport_{sport_id}"
            new_dict_to_load = copy.deepcopy(dict_to_load)
            new_dict_to_load["id"] = new_activity_id
            new_dict_to_load["sport_id"] = sport_id
            ACTIVITIES[new_activity_id] = StartNewSportActivity(
                dict_to_load=new_dict_to_load)

    # Other activities
    else:
        ACTIVITIES[activity_id] = Activity(
            dict_to_load=dict_to_load)
