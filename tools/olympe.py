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
    TEXT,
    USER_DATA
)
from tools.data_structures import (
    generate_learning_rates,
    Athlete,
    Game,
    DEFAULT_STATS_DICT,
    DEFAULT_STAT_DICT,
    EVENTS_DICT,
    MIN_LEVEL_ATHLETE,
    MIN_LEVEL_SPECIALIST,
    MIN_LEVEL_BI_SPECIALIST,
    SPORTS,
    MAX_REPUTATION,
    COUNTRY_NAME
)
from tools.path import (
    PATH_COUNTRIES,
    PATH_ATHLETES_IMAGES
)

#################
### Constants ###
#################

### Countries ###

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


def compute_salary(athlete: Athlete, game_difficulty: Literal["easy", "medium", "difficult"]) -> int:
    # Take into account the difficulty of the game
    if game_difficulty == "easy":
        base_salary = 500
        arithmetic_factor_salary = 9
        geometric_factor_salary = 1.9
    elif game_difficulty == "medium":
        base_salary = 1000
        arithmetic_factor_salary = 10
        geometric_factor_salary = 2
    else:
        base_salary = 1500
        arithmetic_factor_salary = 11
        geometric_factor_salary = 2.1

    score_athlete = athlete.global_score_for_salary
    salary = base_salary + ((arithmetic_factor_salary * score_athlete) ** geometric_factor_salary)*1000

    return int(salary)

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


def generate_stats_sports(main_sport: str, second_sport: str | None, level: float, profile: Literal["homogeneous", "specialist", "bi-specialist"]) -> dict:
    """
    Generate the dict of stats and sports for an athlete, given its type of profile.
    
    Parameters
    ----------
    main_sport : str
        Key of the main sport of the athlete.
    second_sport : str | None
        Key of the second sport of the athlete, if it exists.
    level : float
        Level of the athlete, comprised between 0 and 1.
    profile : Literal["homogeneous", "specialist", "bi-specialist"
        Type of the profile of the athlete.
        Homogeneous means the athlete is good/bad in all skills.
        Specialist means the athlete is good in the skills related to its main sport, and bad in the others.
        Bi-specialist means the athlete is good in the skills related to its main and second sports, and bad in the others.
    
    Returns
    -------
    dict, dict
        Dict of stats and dict of sports.
    """

    # Set the bounds for the random generation of points for the skills
    b_homogeneous = min(level+0.25*MIN_LEVEL_ATHLETE, 1)
    a_homogeneous = max(level-1.5*MIN_LEVEL_ATHLETE, 0)
    b_specialist = min(level+0.5*MIN_LEVEL_ATHLETE, 1)
    a_specialist = max(level, 0)
    b_non_specialist = min(level-MIN_LEVEL_ATHLETE, 1)
    a_non_specialist = max(level-2*MIN_LEVEL_ATHLETE, 0)

    ### Sports ###

    sports_dict = {
        main_sport: copy.deepcopy(DEFAULT_STAT_DICT)
    }
    if second_sport is not None:
        sports_dict[second_sport] = copy.deepcopy(DEFAULT_STAT_DICT)

    # Choose randomly the learning rates for the both sports
    sports_dict[main_sport]["learning_rate"] = generate_learning_rates(
        double_proba=0.06, simple_proba=0.25)
    if second_sport is not None:
        sports_dict[second_sport]["learning_rate"] = generate_learning_rates()

    # Choose randomly the values (points) according to level and type of profile
    if profile == "homogeneous":
        sports_dict[main_sport]["points"] = round((rd.random()*(
            b_homogeneous-a_homogeneous)+a_homogeneous)*70, 3)
        if second_sport is not None:
            sports_dict[second_sport]["points"] = round((rd.random()*(
                b_homogeneous-a_homogeneous)+a_homogeneous)*70, 3)
    elif profile == "specialist":
        sports_dict[main_sport]["points"] = round((rd.random()*(
            b_specialist-a_specialist)+a_specialist)*70, 3)
        # Second sport non specialist
        if second_sport is not None:
            sports_dict[second_sport]["points"] = round((rd.random()*(
                b_non_specialist-a_non_specialist)+a_non_specialist)*70, 3)
    elif profile == "bi-specialist":
        sports_dict[main_sport]["points"] = round((rd.random()*(
            b_specialist-a_specialist)+a_specialist)*70, 3)
        if second_sport is not None:
            sports_dict[second_sport]["points"] = round((rd.random()*(
                b_specialist-a_specialist)+a_specialist)*70, 3)

    ### Stats ###

    stats_related_to_main_sport = SPORTS[main_sport].stats
    if second_sport is not None:
        stats_related_to_second_sport = SPORTS[second_sport].stats

    stats_dict = copy.deepcopy(DEFAULT_STATS_DICT)
    for key in stats_dict:
        # Choose randomly the learning rates (talent = flams)
        stats_dict[key]["learning_rate"] = generate_learning_rates()

        # Choose randomly the stats according to the type of profile

        # If the stat is related to the second sport for the bi-specialist profile
        if second_sport is not None and profile == "bi-specialist" and key in stats_related_to_second_sport:
            stats_dict[key]["points"] = round((rd.random()*(
                b_specialist-a_specialist)+a_specialist)*70, 3)
        
        # If the stat is related to the first sport for the specialists profiles
        elif profile in ["specialist", "bi-specialist"] and key in stats_related_to_main_sport:
            stats_dict[key]["points"] = round((rd.random()*(
                b_specialist-a_specialist)+a_specialist)*70, 3)
        
        # If the stat is not related to any sport for specialists profiles
        elif profile in ["specialist", "bi-specialist"]:
            stats_dict[key]["points"] = round((rd.random()*(
                b_non_specialist-a_non_specialist)+a_non_specialist)*70, 3)
        
        # If the profile is homogeneous
        else:
            stats_dict[key]["points"] = round((rd.random()*(
                b_homogeneous-a_homogeneous)+a_homogeneous)*70, 3)

    return stats_dict, sports_dict

def generate_reputation(charm_dict: dict) -> int:
    charm = charm_dict["points"]
    # Maximum 250 points of reputation (to avoid very high salaries at the beginning)
    basis_reputation = 0.25 * charm * MAX_REPUTATION / 70
    random_number = rd.random() * MAX_REPUTATION * 0.05
    plus_mode = rd.randint(0, 1) == 1
    if plus_mode:
        reputation = basis_reputation + random_number
    else:
        reputation = basis_reputation - random_number
    if reputation < 0:
        return 0
    elif reputation > MAX_REPUTATION:
        return MAX_REPUTATION
    return reputation

def generate_recruit_price(salary: int, level: float, game_difficulty: Literal["easy", "medium", "difficult"]) -> int:
    # Basis of the recruit price
    if game_difficulty == "easy":
        basis_factor = 8
    elif game_difficulty == "medium":
        basis_factor = 10
    else:
        basis_factor = 12
    
    # Random margin between -10.000 and 10.000 depending on level
    multiplying_factor = 10
    if level > 0.8:
        multiplying_factor = 1000
    elif level > 0.6:
        multiplying_factor = 500
    elif level > 0.4:
        multiplying_factor = 100
    elif level > 0.2:
        multiplying_factor = 50
    random_margin = rd.randint(-50, 50)

    recruit_price = salary * basis_factor + random_margin * multiplying_factor
    if recruit_price <= 0:
        recruit_price = salary * basis_factor

    return int(recruit_price)

def generate_athlete(
        GAME: Game,
        country: str = COUNTRY_NAME,
        age: int | None = None,
        time_for_recruit: int | None = None,
        recruit_price: int | None = None,
        salary: int | None = None,
        main_sport: str = "random",
        second_sport: str | None = "random",
        gender: Literal["male", "female"] | None = None,
        portrait: Portrait | None = None) -> Athlete:

    ### Athlete identity ###

    if gender is None:
        gender = rd.choice(["male", "female"])
    first_name = rd.choice(first_names_dict[country][gender])
    name = rd.choice(names_dict[country])
    # Don't generate the age for the first athlete of the game
    if age is None:
        age = generate_age()

    # Choose the time for recruit
    if time_for_recruit is None:
        time_for_recruit = rd.randint(2, 4)

    ### Level and profile ###

    # Choose the level
    max_level = GAME.compute_average_level()
    a = max(MIN_LEVEL_ATHLETE, (max_level-MIN_LEVEL_ATHLETE))
    b = min(max_level, 1)
    level = rd.random()*(b-a) + a

    # Change the level of the athlete depending on the difficulty of the game / country
    if country == COUNTRY_NAME:
        if GAME.difficulty == "easy":
            level = min(level*1.05, 1)
        elif GAME.difficulty == "difficult":
            level *= 0.95
    else:
        # TODO change accordingly to the strength of the country
        level = level

    # Choose the profile of the athlete
    list_profiles = ["homogeneous"]
    if level > MIN_LEVEL_SPECIALIST:
        list_profiles.append("specialist")
    if level > MIN_LEVEL_BI_SPECIALIST:
        list_profiles.append("bi-specialist")
    profile = rd.choice(list_profiles)

    ### Stats and sports ###

    if main_sport == "random":
        # Main sport among those unlocked
        main_sport = rd.choice(GAME.unlocked_sports)
    if second_sport == "random":
        # Second sport among all sports of the current category or less
        list_second_sports = GAME.get_all_sports_from_current_category_or_less()
        list_second_sports.remove(main_sport)
        second_sport = rd.choice(list_second_sports)
    
    stats, sports = generate_stats_sports(
        main_sport=main_sport,
        second_sport=second_sport,
        level=level,
        profile=profile)

    ### Reputation ###

    reputation = generate_reputation(stats["charm"])

    ### Portrait ###

    # Generate the portrait of the athlete
    if portrait is None:
        portrait = Portrait(gender=gender)

    ### Athlete ###

    dict_to_load = {
        "first_name": first_name,
        "nationality": country,
        "name": name,
        "age": age,
        "time_for_recruit": time_for_recruit,
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

    ### Costs ###

    # Generate the salary and the recruit price only for the athletes of our country
    if country == COUNTRY_NAME:

        # Salary
        if salary is None:
            salary = compute_salary(athlete=athlete, game_difficulty=GAME.difficulty)
        athlete.set_salary(salary=salary)

        # Recruit price
        if recruit_price is None:
            recruit_price = generate_recruit_price(
                salary=salary,
                level=level,
                game_difficulty=GAME.difficulty)
        athlete.set_recruit_price(recruit_price=recruit_price)

    return athlete

def generate_and_add_first_athlete(GAME: Game, main_sport: str) -> None:

    # Woman athlete at the beginning
    gender = "female"

    portrait = Portrait(
        gender=gender,
        hairs_behind_face=True,
        mouth_shape=rd.choice(["mouth_happy", "mouth_glad"]),
        eyebrow_y_offset=0,
        eyes_x_offset=0,
        eyes_y_offset=0,
        eyes_shape="eye_1"
    )

    first_athlete = generate_athlete(
        GAME=GAME,
        age=rd.randint(16, 22),
        recruit_price=0,
        salary=3500,
        main_sport=main_sport,
        second_sport=None,
        gender=gender,
        portrait=portrait
    )

    GAME.update_recrutable_athletes(new_athletes_list=[first_athlete])
    GAME.recruit_athlete(GAME.recrutable_athletes[0])
    USER_DATA.save_changes()

############
### Game ###
############

def update_notifications(GAME: Game):

    ### For story events ###

    list_events = []
    for event_id in EVENTS_DICT["story"]:
        if event_id not in GAME.seen_dialogs:
            event_dict = EVENTS_DICT["story"][event_id]
            if (event_dict["year"] == GAME.year and GAME.trimester >= event_dict["trimester"]) or GAME.year > event_dict["year"]:
                condition = event_dict.get("condition", {})
                order = event_dict.get("order", 1)
                # TODO treat condition
                list_events.append([order, event_id])

    # Sort the list of events with their order
    list_events = sorted(list_events)

    ### For repeatable events ###
    # TODO

    ### For random events ###
    # TODO

    ### For endings ###
    # TODO choose between Olympe and Ariane

    ### For retirements ###

    if "retirement" in GAME.unlocked_modes:
        print("TODO")

    # Update the list of notifications
    GAME.notifications_list = [element[1] for element in list_events]

def finish_dialog(GAME: Game, dialog_code: str):

    # Update the USER_DATA
    if dialog_code not in USER_DATA.seen_dialogs:
        USER_DATA.seen_dialogs.append(dialog_code)

    # Get the dict of details of the dialog
    story_events = EVENTS_DICT["story"]
    random_events = EVENTS_DICT["random_events"]
    if dialog_code in story_events:
        dialog_dict = story_events[dialog_code]
    elif dialog_code in random_events:
        dialog_dict = random_events[dialog_code]

    # Update the list of seen dialogs
    if dialog_code not in GAME.seen_dialogs:
        GAME.seen_dialogs.append(dialog_code)

    # Apply effects of the dialogs if some
    effects = dialog_dict.get("effects", {})
    for key_effect in effects:
        value_effect = effects[key_effect]
        if key_effect == "money":
            GAME.money += value_effect

        elif key_effect == "unlocked_characters":
            for character_id in value_effect:
                if character_id not in GAME.unlocked_characters:
                    GAME.unlocked_characters.append(character_id)

        elif key_effect == "unlocked_modes":
            for mode_id in value_effect:
                if mode_id not in GAME.unlocked_modes:
                    GAME.unlocked_modes.append(mode_id)

        elif key_effect == "unlocked_menus":
            for mode_id in value_effect:
                if mode_id not in GAME.unlocked_menus:
                    GAME.unlocked_menus.append(mode_id)

        elif key_effect == "unlocked_activities":
            for activity_id in value_effect:
                if activity_id not in GAME.unlocked_activities:
                    GAME.unlocked_activities.append(activity_id)

    # Remove the dialog from the notifications list
    if dialog_code in GAME.notifications_list:
        GAME.notifications_list.remove(dialog_code)

    # Special case for the introduction
    if dialog_code == "introduction":
        launch_new_phase(GAME=GAME)

    USER_DATA.save_changes()

def launch_new_phase(GAME: Game, mode_new_phase: str | None = None) -> str:

    # Go to next trimester
    main_action = GAME.go_to_next_trimester()

    # Handle recrutements
    if "recruit" in GAME.unlocked_menus:
        new_athletes_list = []
        # Classic generation at random when no particular event
        if mode_new_phase is None:
            number_sports_unlocked = len(GAME.unlocked_sports)
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
                new_athletes_list.append(generate_athlete(GAME=GAME))

        # When we unlock recruit mode, three new athletes of the starting sport with basic level are added
        elif mode_new_phase == "unlock_recruit_mode":
            for counter in range(3):
                new_athletes_list.append(generate_athlete(GAME=GAME, max_level=1))

        # When we just unlock a sport, three new athletes of this sport are added
        elif "sport_" in mode_new_phase:
            for counter in range(3):
                new_athletes_list.append(generate_athlete(
                    GAME=GAME,
                    main_sport=mode_new_phase.replace("sport_", "")
                ))

        GAME.update_recrutable_athletes(
            new_athletes_list=new_athletes_list)
    
    # Update the salaries at the beginning of the year
    if "salary_augmentation" in GAME.unlocked_modes and GAME.trimester == 1:
        for athlete in GAME.team:
            new_salary = compute_salary(athlete=athlete, game_difficulty=GAME.difficulty)
            athlete.set_salary(salary=new_salary)

    # Update the list of notifications
    update_notifications(GAME=GAME)

    USER_DATA.save_changes()

    return main_action
