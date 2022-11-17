# Philippe C. Léger
# 2022-11-03
# Labo 6
# Classe EtatRobot: Énumération des états possibles du Robot

from enum import IntEnum
class EtatRobot(IntEnum):
    IMMOBILE = 0
    TRANSLATION = 1
    TOURNER = 2
