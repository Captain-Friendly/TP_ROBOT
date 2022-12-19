# Pascal Arès, Philippe C. Léger & Julian Angel Murillo
# 2022-12-19
# PFI - Le robot autonome
# classe DirecteurIA: Classe permettant de déplacer le robot à une liste
# de positions dans la classe.

from Robot import Robot
from DirecteurRotation import DirecteurRotation
from JetonAnnulation import JetonAnnulation
from Point import Point
from GPS import GPS
from time import sleep
from Algos import Algos
from Lidar import Lidar

class DirecteurIA:
    TOLERANCE_DISTANCE = 0.2
    VITESSE_TRANSLATION = 0.4
    PERIODE = 0.1

    def __init__(self, jeton: JetonAnnulation, robot:Robot, directeur_rotation: DirecteurRotation, gps:GPS):
        self.__jeton = jeton
        self.__directeur_rotation = directeur_rotation
        self.__robot = robot
        self.__gps = gps
        self.__lidar = Lidar(jeton)

    def demarrer(self):
        self.__gps.demarrer()
        print("gps démarrer")
        self.__directeur_rotation.démarrer()
        print("directeur rotation démarrer")
        self.__lidar.demarrer()
        print("démarrage du linar")


    def assigner_destination(self, destination:Point):
        """Donne le point et tourne est déplace le robot"""
        
        position_actuelle = self.__gps.obtenir_position()
        while position_actuelle == None:
            position_actuelle = self.__gps.obtenir_position()
        
        print(f"Info\nPosition début {position_actuelle.to_string()}")
        angle_deplacement = Point.angle(position_actuelle, destination)
        position_initiale = position_actuelle
        deplacement = Point.soustraire(destination, position_actuelle)
        distance_a_parcourir = deplacement.calculer_norme()
        if distance_a_parcourir > 0.25: distance_a_parcourir -= 0.25
        distance_parcourue = Point.soustraire(position_actuelle, position_initiale).calculer_norme()
        if deplacement.calculer_norme() < DirecteurIA.TOLERANCE_DISTANCE: return
        self.__directeur_rotation.assigner_destination(angle_deplacement, 5)
        sleep(0.5)
        print(f"à parcourir: {distance_a_parcourir}\tparcourue: {distance_parcourue}")
        self.__robot.modifier_vitesse(DirecteurIA.VITESSE_TRANSLATION)

        nb_identique = 0
        while self.__jeton.continuer() and distance_a_parcourir > distance_parcourue:
            nouvelle_position = self.__gps.obtenir_position()
            if self.__lidar.objet_present:
                self.__robot.freiner()
                print("objet trouvé")
            elif nouvelle_position is None: 
                self.__robot.freiner()
            elif  nb_identique > 5:
                self.__robot.freiner()
                print("GPS a planté")
                self.__jeton.terminer()
                return
            elif Algos.approx_egal_point(position_actuelle, nouvelle_position):
                nb_identique += 1
            else:
                nb_identique = 0
                position_actuelle = nouvelle_position
                self.__robot.avancer()
            sleep(DirecteurIA.PERIODE)
            deplacement = Point.soustraire(destination, position_actuelle)
            distance_parcourue = Point.soustraire(position_actuelle, position_initiale).calculer_norme()
        self.__robot.freiner()
        print(f"à parcourir: {distance_a_parcourir}\tparcourue: {distance_parcourue}")
        print(f"Info\nPosition finale {position_actuelle.to_string()}\tDestination prévue {position_initiale.to_string()}")
        sleep(1)


    def terminer(self):
        self.__gps.terminer()
        self.__directeur_rotation.terminer()
        self.__lidar.terminer()

def se_rendre(directeur:DirecteurIA, jeton:JetonAnnulation, destination:Point):
    if jeton.continuer(): 
        print(f"destination:{destination.to_string()}")
        directeur.assigner_destination(destination)

def main():
    jeton = JetonAnnulation()
    robot = Robot.construire()
    gps = GPS(jeton)
    directeur_rotation = DirecteurRotation.construire(jeton, robot)
    directeur = DirecteurIA(jeton, robot, directeur_rotation, gps)
    directeur.demarrer()

    # se deplace de m vers la gauche
    depart = gps.obtenir_position()
    while depart is None:
        depart = gps.obtenir_position()
        print(depart)
    destination1 = Point.additionner(depart, Point(0, -3))
    destination2 = Point.additionner(depart, Point(0, 0))
    while input("x pour quitter...") != "x" and jeton.continuer():
        if jeton.continuer(): 
            print(f"destination1:{destination1.to_string()}")
            directeur.assigner_destination(destination1)
        if jeton.continuer(): 
            print(f"destination2:{destination2.to_string()}")
            directeur.assigner_destination(destination2)
    directeur.terminer()
    robot.détruire()

if __name__ == "__main__":
    main()