from Robot import Robot
from directeur_rotation import Directeur_Rotation
from JetonAnnulation import JetonAnnulation
from Point import Point
from GPS import GPS
from time import sleep
from Algos import Algos
from lidar import Lidar
class DirecteurIA:
    TOLERANCE_DISTANCE = 0.2
    VITESSE_TRANSLATION = 0.5
    PERIODE = 0.1

    def __init__(self, jeton: JetonAnnulation, robot:Robot, directeur_rotation: Directeur_Rotation, gps:GPS):
        self.__jeton = jeton
        self.__directeur_rotation = directeur_rotation
        self.__robot = robot
        self.__gps = gps
        self.__lidar = Lidar(jeton)

    def demarrer(self):
        self.__gps.start()
        print("gps démarrer")
        self.__directeur_rotation.démarrer()
        print("directeur rotation démarrer")
        self.__lidar.demarrer()
        print("lidar demarer")


    def assigner_destination(self, destination:Point):
        """Donne le point et tourne est déplace le robot"""
        
        position_actuelle = self.__gps.obtenir_position()#chequer sa
        while position_actuelle == None:
            position_actuelle = self.__gps.obtenir_position()#chequer sa
        
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
        # while self.__jeton.continuer() and (deplacement.calculer_norme() > DirecteurIA.TOLERANCE_DISTANCE or distance < distance_parcourue):
            # if not self.__directeur_rotation.assigner_destination(angle_deplacement, 20):
            # self.__robot.modifier_vitesse(DirecteurIA.VITESSE_TRANSLATION)
            # self.__robot.avancer()
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
            # angle_deplacement = Point.angle(position_actuelle, destination)
            deplacement = Point.soustraire(destination, position_actuelle)
            distance_parcourue = Point.soustraire(position_actuelle, position_initiale).calculer_norme()
        self.__robot.freiner()
        print(f"à parcourir: {distance_a_parcourir}\tparcourue: {distance_parcourue}")
        print(f"Info\nPosition finale {position_actuelle.to_string()}\tDestination prévue {position_initiale.to_string()}")
        sleep(1)


    def terminer(self):
        self.__gps.stop()
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
    directeur_rotation = Directeur_Rotation.construire(jeton, robot)
    directeur = DirecteurIA(jeton, robot, directeur_rotation, gps)
    directeur.demarrer()

    # se deplace de m vers la gauche
    depart = gps.obtenir_position()
    while depart is None:
        depart = gps.obtenir_position()
        print(depart)
    # destination1 = Point.additionner(depart, Point(0, 2))
    # destination2 = Point.additionner(destination1, Point(2, 0))
    # destination3 = Point.additionner(destination2, Point(0, -2))
    # destination4 = Point.additionner(destination3, Point(-2, 0))

    # print(f"depart:{depart.to_string()}")
    # print(f"destination:{destination1.to_string()}")
    # print(f"destination2:{destination2.to_string()}")
    # print(f"destination3:{destination3.to_string()}")
    # print(f"destination4:{destination4.to_string()}")

    # se_rendre(directeur, jeton, destination3)
    # se_rendre(directeur, jeton, destination2)
    # se_rendre(directeur, jeton, destination3)
    # se_rendre(directeur, jeton, destination4)
    # directeur.assigner_destination(destination1)
    # if jeton.continuer(): 
    #     print(f"destination3:{destination3.to_string()}")
    #     directeur.assigner_destination(destination3)
    # if jeton.continuer(): 
    #     print(f"destination2:{destination2.to_string()}")
    #     directeur.assigner_destination(destination2)
    # if jeton.continuer(): 
    #     print(f"destination4:{destination4.to_string()}")
    #     directeur.assigner_destination(destination4)


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