"""
Module to handle all the backend of the game.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
import os
from typing import Literal
import copy
if __name__ == "__main__":
    import sys
    sys.path.append("../")
    sys.path.append("./")
    import matplotlib.pyplot as plt

### Local imports ###

from lupa_libraries.face_generator.face_generator import (
    Portrait
)
from tools.basic_tools import (
    load_json_file
)
from tools.constants import (
    GAME,
    TEXT
)
from tools.data_structures import (
    Athlete,
    DEFAULT_STATS_DICT,
    DEFAULT_STAT_DICT
)
from tools.path import (
    PATH_COUNTRIES,
    PATH_ATHLETES_IMAGES
)

#################
### Constants ###
#################

COUNTRY_NAME = "our_country"

countries_dict = load_json_file(PATH_COUNTRIES)

### First names and names ###

first_names_dict = {}
names_dict = {}
for country in countries_dict:
    first_names_dict[country] = countries_dict[country]["athletes_first_names"]
    names_dict[country] = countries_dict[country]["athletes_names"]

first_names_dict[COUNTRY_NAME] = {
    "male": [],
    "female": []
}
for key in first_names_dict:
    if key != COUNTRY_NAME:
        for first_name in first_names_dict[key]["male"]:
            first_names_dict[COUNTRY_NAME]["male"].append(first_name)
        for first_name in first_names_dict[key]["female"]:
            first_names_dict[COUNTRY_NAME]["female"].append(first_name)

names_dict[COUNTRY_NAME] = []
for key in first_names_dict:
    if key != COUNTRY_NAME:
        for name in names_dict[key]:
            names_dict[COUNTRY_NAME].append(name)

#################
### Functions ###
#################


def compute_salary(stats, reputation) -> int:
    # TODO
    return 1200

def get_health_string(athlete: Athlete) -> str:
    is_hurt = athlete.is_hurt

    health = TEXT.injuries[athlete.health["type_injury"]]
    if is_hurt:
        time_absent = athlete.health["time_absent"]
        if time_absent > 1:
            health += " - " + time_absent + " " + \
                TEXT.general["trimesters"].lower()
        else:
            health += " - " + time_absent + " " + \
                TEXT.general["trimester"].lower()
            
    return health

##########################
### Athlete generation ###
##########################


def generate_age() -> int:
    # Probabilities for each age 16-19 / 20-24 / 25-29 / 30-35 / 36-40
    weights = [1, 1.5, 2, 3] + [4, 5, 5, 5, 4] + [3.5, 3, 2.5, 2, 1.5] + [
        1] * 6 + [0.75, 0.75, 0.5, 0.5, 0.25]
    age = rd.choices(range(16, 41), weights=weights)
    return age[0]


def generate_learning_rates(double_proba=0.15, simple_proba=0.4):
    random_number = rd.random()
    if random_number < double_proba:
        return 2
    elif random_number < simple_proba:
        return 1.5
    return 1


def generate_stats(level) -> dict:
    stats = copy.deepcopy(DEFAULT_STATS_DICT)
    for key in stats:
        # Choose randomly the learning rates (talent = flams)
        stats[key]["learning_rate"] = generate_learning_rates()

        # Choose randomly the stats
        # TODO
    return stats


def generate_sports(main_sport: str | None, second_sport: str | None, level) -> dict:
    # TODO choisir un principal sport parmi les sports débloqués
    if main_sport is None:
        main_sport = ...
    if second_sport is None:
        second_sport = ...

    sports_dict = {
        main_sport: copy.deepcopy(DEFAULT_STAT_DICT),
        second_sport: copy.deepcopy(DEFAULT_STAT_DICT)
    }

    # Choose randomly the learning rates for the both sports
    sports_dict[main_sport]["learning_rate"] = generate_learning_rates(
        double_proba=0.2, simple_proba=0.5)
    sports_dict[second_sport]["learning_rate"] = generate_learning_rates()

    # Choose randomly the values (points) according to level
    # TODO

    return sports_dict


def generate_reputation(charm_dict: dict):
    charm = charm_dict["points"]
    basis_reputation = charm * 100 / 70
    random_number = rd.random() * 5
    plus_mode = rd.randint(0, 1) == 1
    if plus_mode:
        reputation = basis_reputation + random_number
    else:
        reputation = basis_reputation - random_number
    if reputation < 0:
        return 0
    elif reputation > 100:
        return 100
    return reputation


def generate_recruit_price(salary: int):
    # TODO
    return 0


def generate_athlete(
        country: str = "our_country",
        age: int | None = None,
        level: int = None,
        main_sport: str = None,
        second_sport: str = None) -> Athlete:

    ### Athlete identity ###

    gender = rd.choice(["male", "female"])
    first_name = rd.choice(first_names_dict[country][gender])
    name = rd.choice(names_dict[country])
    # Don't generate the age for the first athlete of the game
    if age is None:
        age = generate_age()

    # TODO remplacer les None en fonction du niveau de notre pays
    if level is None:
        ...

    ### Stats and sports ###

    stats = generate_stats(level)
    sports = generate_sports(main_sport, second_sport, level)
    reputation = generate_reputation(stats["charm"])

    # Generate the portrait of the athlete
    portrait = Portrait(gender=gender)

    # Salary and recruit price
    salary = compute_salary(stats=stats, reputation=reputation)
    recruit_price = generate_recruit_price(salary=salary)

    dict_to_load = {
        "first_name": first_name,
        "name": name,
        "age": age,
        "salary": salary,
        "recruit_price": recruit_price,
        # "portrait": portrait.export_as_dict(), #TODO uncomment
        "reputation": reputation,
        "stats": stats,
        "sports": sports
    }

    # Create the athlete and its associated image
    athlete = Athlete(dict_to_load=dict_to_load)
    portrait.export_as_png(os.path.join(
        PATH_ATHLETES_IMAGES, f"{athlete.id}.png"))

    return athlete

#################
### Main code ###
#################


if __name__ == "__main__":
    dict_age = {}

    DEBUG_AGE = False
    if DEBUG_AGE:
        for country in range(10000):
            athlete = generate_athlete()
            if athlete.age not in dict_age:
                dict_age[athlete.age] = 1
            else:
                dict_age[athlete.age] += 1
        x = list(dict_age.keys())
        y = list(dict_age.values())
        plt.bar(x, y)
        plt.xlabel('Âge')
        plt.ylabel('Fréquence')
        plt.title('Fréquence des âges')
        plt.show()
