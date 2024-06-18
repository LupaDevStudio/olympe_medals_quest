"""
Module to handle all the backend of the game.
"""

###############
### Imports ###
###############

### Python imports ###


### Local imports ###

from tools.data_structures import (
    Athlete
)

#################
### Functions ###
#################

def create_athlete() -> Athlete:
    # TODO add random everywhere
    dict_to_load = {
        "first_name": "Gatho",
        "name": "Miamour",
        "age": 20,
        "salary": 1200,
        "recruit_price": 0,
        "stats": {
            "strength": 2,
            "speed": 2,
            "technique": 2,
            "precision": 2,
            "charm": 2
        }
    }
    return Athlete(dict_to_load=dict_to_load)
