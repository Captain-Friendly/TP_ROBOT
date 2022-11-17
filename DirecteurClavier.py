# Pascal Arès
# 2022-08-25
# Labo 1
# Classe DirecteurClavier: Classe fournissant les instructions
# au Robot à partir du LecteurClavier.

from Robot import Robot
from LecteurClavier import LecteurClavier
from JetonAnnulation import JetonAnnulation

class DirecteurClavier:
    def __init__(self, lecteur:LecteurClavier, robot:Robot, jeton_annulation:JetonAnnulation):
        self.__lecteur = lecteur
        self.__robot = robot
        self.__jeton = jeton_annulation
        self.__assigner_fonctions_lecteur()
    
    def __arret(self):
        self.__robot.détruire()
        self.__jeton.terminer()

    def __assigner_fonctions_lecteur(self):
        self.__lecteur.assigner_appel('w', self.__robot.avancer)
        self.__lecteur.assigner_appel('s', self.__robot.reculer)
        self.__lecteur.assigner_appel('a', self.__robot.tourner_g)
        self.__lecteur.assigner_appel('d', self.__robot.tourner_d)
        # self.__lecteur.assigner_appel('q', self.__robot.tourner_avancer_g)
        # self.__lecteur.assigner_appel('e', self.__robot.tourner_avancer_d)
        self.__lecteur.assigner_appel(' ', self.__robot.freiner)
        self.__lecteur.assigner_appel('+', self.__robot.augmenter_vitesse)
        self.__lecteur.assigner_appel('-', self.__robot.réduire_vitesse)
        self.__lecteur.assigner_appel('x', self.__arret)

    def activer(self):
        self.__lecteur.activer(self.__jeton)
