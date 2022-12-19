# Philippe C. Léger & Julian Angel Murillo
# 2022-12-19
# PFI - Le robot autonome
# class DirecteurRotation: classe utilisée pour modifier l'orientation du
# robot vers l'orientation désirée.

from Gyrometre import Gyrometre
from Robot import Robot
from time import sleep
import threading
from JetonAnnulation import JetonAnnulation


class DirecteurRotation:
    VITESSE_ROTATION = 1
    TOLERANCE_ANGLE = 5
    PERIODE = 0.05

    def __init__(self, gyro: Gyrometre, robot: Robot):
        self.__gyro = gyro
        self.__ma_thread = threading.Thread(target=lambda: self.__gyro.demarrer())
        self.__robot = robot
    
    def assigner_destination(self, desired_angle, seuil=None):
        """Bouge le robot vers l'angle desiré"""
        # étalonner gyro avant, pendant qu'on sait que le robot est immobile
        if seuil is None: seuil = DirecteurRotation.TOLERANCE_ANGLE
        current_angle = self.__gyro.obtenir_angle()
        diff_angle = (desired_angle - current_angle) % 360
        if abs(diff_angle) < seuil: return False
        self.__robot.modifier_vitesse(DirecteurRotation.VITESSE_ROTATION)
        # print(f"abs(diff): {abs(diff_angle)}")
        while abs(diff_angle) > seuil: 
            if diff_angle < 180: self.__robot.tourner_d()
            else: self.__robot.tourner_g()
            current_angle = self.__gyro.obtenir_angle()
            diff_angle = (desired_angle - current_angle) % 360
            sleep(DirecteurRotation.PERIODE)

        print(f"current: {current_angle}\tdesired: {desired_angle}\tdiff: {diff_angle}\n")
        self.__robot.freiner()
        return True

    def démarrer(self):
        self.__ma_thread.start()
        

    def terminer(self):
        self.__gyro.arreter()
        self.__ma_thread.join()

    def construire(jeton:JetonAnnulation, robot:Robot):
        gyro = Gyrometre.construire(jeton, robot)
        return DirecteurRotation(gyro, robot)



def main():
    jeton = JetonAnnulation()
    robot = Robot.construire()
    gyro = Gyrometre.construire(jeton, robot)
    
    directeur_rotation = DirecteurRotation(jeton, gyro, robot)
    directeur_rotation.démarrer()
    while jeton.continuer():
        angle_str = input("Entrez l'angle désiré:")
        if angle_str == "x":
            jeton.terminer()
        elif angle_str == "a": print(f"Angle actuel: {gyro.obtenir_angle()}")
        else:
            directeur_rotation.assigner_destination(int(angle_str))
   
if __name__ == "__main__":
    main()