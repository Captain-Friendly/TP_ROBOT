from Robot import Robot
from JetonAnnulation import JetonAnnulation
from Gyrometre import Gyrometre
from GPS import GPS
from Point import Point

class DirecteurIA:

    def __init__(self, gps: GPS, gyrometre: Gyrometre, robot: Robot, jeton: JetonAnnulation):
        self.__jeton = jeton
        self.__gps = gps
        self.gyrometre = gyrometre
        self.robot = robot
        self.destinations = []


    def démarrer(self):
        pass

    def avancer(self):
        pass

    def 
    
    def decider(self, orientation, position, destination):
        angle_deplacement = Point.angle(position, destination)
        if abs(orientation - angle_deplacement) > 10:
            # On tourne le robot
            pass
        elif Point.distance(position, destination) > 10:
            # On avance
            pass
        else:
            # Changer de destination, s'il en reste une
            self.destinations.pop(0)
            if(len(self.destinations)> 0):
                destination = self.destinations[0]
                self.decider(orientation, position, destination)


    def main(self):
        while self.__jeton.continuer():
            if len(self.destinations>=1):
                orientation = self.gyrometre.obtenir_angle()
                position = self.__gps.get_position()
                destination = self.destinations[0]
                self.decider(orientation, position, destination)


    
