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
        current_angle = self.__gyro.obtenir_angle()
        diff_angle = (desired_angle - current_angle) % 360
        while abs(diff_angle) < 10: 
            current_angle = self.__gyro.obtenir_angle()
            diff_angle = (desired_angle - current_angle) % 360
            if diff_angle < 180: self.__robot.tourner_g()
            else: self.__robot.tourner_d()
        self.__robot.freiner()

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
    while jeton.continuer():
        angle_str = input("Entrez l'angle désiré:")
        if(angle_str == "x"):
            jeton.terminer()
        else:
            Moufasa.set_destination(int(angle_str))
    

    

    

if __name__ == "__main__":
    main()