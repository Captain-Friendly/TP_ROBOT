# Philippe C. Léger
# 2022-08-27
# Labo 1
# Classe Mode: Énumération des modes possibles
# pour les moteurs.


from enum import IntEnum


class Mode(IntEnum):
    NEUTRE = 0
    AVANCER = 1
    RECULER = 2
    FREINER = 3
