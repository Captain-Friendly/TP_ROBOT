from Gyrometre import Gyrometre
from Robot import Robot
from time import perf_counter, sleep
from icm20948 import ICM20948
import threading
from ModuleInertiel import ModuleInertiel
from JetonAnnulation import JetonAnnulation


class Directeur_Rotation:
    def __init__(self, jeton: JetonAnnulation, gyro: Gyrometre, robot: Robot):
        self.__gyro = gyro
        self.__ma_thread = threading.Thread(target=lambda: self.__gyro.demarrer())
        self.__robot = robot
        
        
    def set_destination(self, desired_angle):
        # étalonner gyro avant, pendant qu'on sait que le robot est immobile
        current_angle = self.__gyro.obtenir_angle()
        diff_angle = (desired_angle - current_angle) % 360
        print(f"abs(diff): {abs(diff_angle)}")
        while abs(diff_angle) > 5: 
            print(f"current: {current_angle}\tdesired: {desired_angle}\tdiff: {diff_angle}\n")
            if abs(diff_angle) < 30: self.__robot.modifier_vitesse(0.5)
            if diff_angle < 180: self.__robot.tourner_d()
            else: self.__robot.tourner_g()
            current_angle = self.__gyro.obtenir_angle()
            diff_angle = (desired_angle - current_angle) % 360
            sleep(0.05)

        print(f"current: {current_angle}\tdesired: {desired_angle}\tdiff: {diff_angle}\n")
        self.__robot.freiner()
        self.__robot.modifier_vitesse(0.8)

    def démarrer(self):
        self.__ma_thread.start()
        

    def terminer(self):
        self.__gyro.arreter()
        self.__ma_thread.join()



def main():
    def construire_gyrometre(jeton):
        imu = ICM20948()
        mod = ModuleInertiel(imu)
        return Gyrometre(mod, perf_counter, jeton, lambda: sleep(0.05))

    jeton = JetonAnnulation()
    gyro = construire_gyrometre(jeton)
    robot = Robot.construire()
    
    Moufasa = Directeur_Rotation(jeton, gyro, robot)
    Moufasa.démarrer()
    while jeton.continuer():
        angle_str = input("Entrez l'angle désiré:")
        if angle_str == "x":
            jeton.terminer()
        elif angle_str == "a": print(f"Angle actuel: {gyro.obtenir_angle()}")
        else:
            Moufasa.set_destination(int(angle_str))
    

    

    

if __name__ == "__main__":
    main()