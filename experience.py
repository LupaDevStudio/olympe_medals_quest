import matplotlib.pyplot as plt
import numpy as np

MAX_XP: int = 70

def f(x: float, pow: float, y0: float) -> float:
    return y0 * (1 - (x / MAX_XP)**pow)

EXHAUSTION_FACTOR: float = 0.5
Y0: float = 1.5
FATIGUE_CURRENT_LEVEL: float = 0

# Voici la fonction qui renvoie la quantité d'xp gagnée par un athlète dans une statistique ou un sport
# en fonction de son expérience actuelle dans ce(tte) dernier(ère), du niveau de l'entrainement qu'il a
# réalisé, et de sa fatigue actuelle.
def xp_gain(current_xp: float, activity_level: int, exhaustion_percent: float):
    # Set the quality of the training depending of the level of the activity
    if activity_level == 1:
        n = 0.5
        y0 = 2.5
        # The first level activity is not useful to train a skill that is above 40.
        if current_xp > 40:
            return 0
    elif activity_level == 2:
        n = 1
        y0 = 2
        if current_xp < 10 or current_xp > 50:
            return 0
    elif activity_level == 3:
        n = 1.5
        y0 = 1.75
        if current_xp < 20 or current_xp > 60:
            return 0
    else:
        n = 2
        y0 = 1.5
        if current_xp < 30:
            return 0
    # n: float = training_lvl - 1
    # if n == 0:
    #     n = 0.5
    gross_xp: float = f(current_xp, n, activity_level*y0)
    return gross_xp * (1 - EXHAUSTION_FACTOR * exhaustion_percent)

T = np.arange(0, MAX_XP, 0.1)
COLORS = ['r', 'g', 'b', 'm']
S = []
for i in range(0, 4):
    S.append([xp_gain(t, i+1, FATIGUE_CURRENT_LEVEL) for t in T])
    plt.plot(T, S[i], COLORS[i], label='training lvl '+str(i+1))

DO_NOT_EXCEED = [(MAX_XP - t) for t in T]
plt.plot(T, DO_NOT_EXCEED, 'k--', label='xp until max')

plt.legend()
plt.grid()
plt.xlim(0, MAX_XP)
plt.ylim(0, 4*Y0)
plt.xlabel("current XP")
plt.ylabel("XP gain")
plt.show()
plt.clf()

# Petit test: vérifier qu'un athlète passe de 0 à 10 d'XP (du rang F au rang E)
# en suivant 6 entraînements de niveau 1, sans fatigue
xp = 0
for i in range(0, 6):
    xp += xp_gain(xp, 1, 0)
print()
print(xp)
