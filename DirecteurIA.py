from Robot import Robot
from Point import Point
from icm20948 import ICM20948
from JetonAnnulation import JetonAnnulation
from ModuleInertiel import ModuleInertiel
from time import sleep,perf_counter
from GPS import GPS
from Gyrometre import Gyrometre
from CorrectionDirection import CorrectionDirection
class DirecteurIA:

    def __init__(self, robot:Robot, correcteur_direction:CorrectionDirection, detecteur_obstacle, jeton:JetonAnnulation):
        self.__correcteur_direction = correcteur_direction
        self.__robot=robot
        self.__jeton=jeton
    def start(self):
        POINT=[Point(3,3),Point(3,5),Point(5,5),Point(5,3),Point(3,3)]
        imu = ICM20948()
        correcteur=self.__correcteur_direction
        correcteur.demarrer()
        self.__robot.avancer()
        while len(POINT>=1):
            point=POINT.pop(0)
            correcteur.set_destination(point)
            while correcteur.est_destination_atteinte():
                # détecter obstacle
                sleep(0.02)

    def __avancer_robot(self):
        self.__robot.avancer()

    def __tourner_robot(self, angle_voulu):
        from icm20948 import ICM20948
        from ModuleInertiel import ModuleInertiel

        module_inertiel = ModuleInertiel(ICM20948)
        while True:
            if angle_voulu > 0:
                self.__robot.tourner_g()
            else:
                self.__robot.tourner_d()