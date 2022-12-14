from Robot import Robot
from directeur_rotation import Directeur_Rotation
from JetonAnnulation import JetonAnnulation
from Point import Point
from GPS import GPS
from time import sleep
class DirecteurIA:
    def __init__(self, jeton: JetonAnnulation, robot:Robot, directeur_rotation: Directeur_Rotation, gps:GPS):
        self.__jeton = jeton
        self.__directeur_rotation = directeur_rotation
        self.__robot = robot
        self.__gps = gps

    def demarrer(self):
        self.__gps.start()
        self.__directeur_rotation.démarrer()

    def assigner_destination(self, destination:Point):
        """Donne le point et tourne est déplace le robot"""
        position_actuelle = self.__gps.obtenir_position()#chequer sa
        angle_deplacement = Point.angle(position_actuelle, destination)
        deplacement = Point.soustraire(destination, position_actuelle)
        if deplacement.calculer_norme < 0.3: return
        while self.__jeton.continuer() and deplacement.calculer_norme > 0.3:
            if not self.__directeur_rotation.assigner_destination(angle_deplacement):
                self.__robot.avancer()
                sleep(0.1)
            position_actuelle = self.__gps.obtenir_position()
            angle_deplacement = Point.angle(position_actuelle, destination)
            deplacement = Point.soustraire(destination, position_actuelle)
        self.__robot.freiner()


    def terminer(self):
        self.__gps.stop()
        self.__directeur_rotation.terminer()


    
def main():
    jeton = JetonAnnulation()
    robot = Robot.construire()
    gps = GPS(jeton)
    directeur_rotation = Directeur_Rotation.construire(jeton, robot)
    directeur = DirecteurIA(jeton, robot, directeur_rotation, gps)
    directeur.demarrer()

    # se deplace de 2m vers la gauche
    destination = Point.additionner(gps.obtenir_position(), Point(2, 0))
    directeur.assigner_destination(destination)
    directeur.terminer()
    robot.détruire()

if __name__ == "__main__":
    main()