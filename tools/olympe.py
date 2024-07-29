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
    TEXT,
    USER_DATA
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
        main_sport = "buoy_racing"
    if second_sport is None:
        second_sport = "cheese_rolling"

    sports_dict = {
        main_sport: copy.deepcopy(DEFAULT_STAT_DICT)
    }
    if second_sport is not None:
        sports_dict[second_sport] = copy.deepcopy(DEFAULT_STAT_DICT)

    # Choose randomly the learning rates for the both sports
    sports_dict[main_sport]["learning_rate"] = generate_learning_rates(
        double_proba=0.2, simple_proba=0.5)
    if second_sport is not None:
        sports_dict[second_sport]["learning_rate"] = generate_learning_rates()

    # Choose randomly the values (points) according to level
    # TODO

    return sports_dict


def generate_reputation(charm_dict: dict) -> int:
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

def generate_recruit_price(salary: int, level: int) -> int:
    # Random margin between -10.000 and 10.000 depending on level
    multiplying_factor = 10
    if level == 2:
        multiplying_factor = 50
    elif level == 3:
        multiplying_factor = 100
    elif level == 4:
        multiplying_factor = 500
    else:
        multiplying_factor = 1000
    random_margin = rd.randint(-10, 10)

    recruit_price = salary * 10 + random_margin * multiplying_factor
    if recruit_price <= 0:
        recruit_price = salary = 10

    return recruit_price

def generate_athlete(
        country: str = "our_country",
        age: int | None = None,
        time_for_recruit: int | None = None,
        max_level: int | None = None, # between 1 and 5
        main_sport: str | None = None,
        second_sport: str | None = None) -> Athlete:

    ### Athlete identity ###

    gender = rd.choice(["male", "female"])
    first_name = rd.choice(first_names_dict[country][gender])
    name = rd.choice(names_dict[country])
    # Don't generate the age for the first athlete of the game
    if age is None:
        age = generate_age()

    # Choose the time for recruit
    if time_for_recruit is None:
        time_for_recruit = rd.randint(2, 5)

    if max_level is None:
        max_level = GAME.compute_average_level()

    level = rd.randint(1, max_level)

    ### Stats and sports ###

    stats = generate_stats(level)
    sports = generate_sports(main_sport, second_sport, level)
    reputation = generate_reputation(stats["charm"])

    # Generate the portrait of the athlete
    portrait = Portrait(gender=gender)

    # Salary and recruit price
    salary = compute_salary(stats=stats, reputation=reputation)
    recruit_price = generate_recruit_price(
        salary=salary,
        level=level)

    dict_to_load = {
        "first_name": first_name,
        "name": name,
        "age": age,
        "salary": salary,
        "time_for_recruit": time_for_recruit,
        "recruit_price": recruit_price,
        "portrait": portrait.get_dict(),
        "reputation": reputation,
        "stats": stats,
        "sports": sports
    }

    # Create the athlete and its associated image
    athlete = Athlete(dict_to_load=dict_to_load)
    portrait.export_as_png(os.path.join(
        PATH_ATHLETES_IMAGES, f"athlete_{athlete.id}.png"))
    portrait.export_as_json(os.path.join(
        PATH_ATHLETES_IMAGES, f"athlete_{athlete.id}.json"))

    return athlete

############
### Game ###
############

def launch_new_phase(mode_new_phase: str | None = None) -> str:
    # TODO check if recruit mode is unlocked in the GAME
    if True:
        new_athletes_list = []
        # Classic generation at random when no particular event
        if mode_new_phase is None:
            number_sports_unlocked = len(GAME.sports_unlocked)
            if number_sports_unlocked < 3:
                number_athletes_to_add = rd.randint(0, 2)
            elif number_sports_unlocked < 8:
                number_athletes_to_add = rd.randint(2, 6)
            elif number_sports_unlocked < 13:
                number_athletes_to_add = rd.randint(4, 8)
            elif number_sports_unlocked < 20:
                number_athletes_to_add = rd.randint(6, 10)
            else:
                number_athletes_to_add = rd.randint(8, 12)
            for counter in range(number_athletes_to_add):
                new_athletes_list.append(generate_athlete())

        # When we unlock recruit mode, three new athletes of the starting sport with basic level are added
        elif mode_new_phase == "unlock_recruit_mode":
            for counter in range(3):
                new_athletes_list.append(generate_athlete(max_level=1))

        # When we just unlock a sport, three new athletes of this sport are added
        elif "sport_" in mode_new_phase:
            for counter in range(3):
                new_athletes_list.append(generate_athlete(
                    main_sport=mode_new_phase.replace("sport_", "")
                ))

    main_action = GAME.go_to_next_trimester()
    GAME.update_recrutable_athletes(
        new_athletes_list=new_athletes_list)
    
    USER_DATA.save_changes()

    return main_action

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
