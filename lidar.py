# Julian Angel Murillo
# 2022-12-19
# PFI - Le robot autonome
# Classe Lidar: Classe permettant d'utiliser le Lidar PyLidar3
# pour déterminer si on objet se trouve dans la zone de détection.

import PyLidar3
import time
from Algos import Algos
from JetonAnnulation import JetonAnnulation

import threading

# angle en degrés
# distance en mm
# AVANT : 180°
# ARRIÈRE : 0°

# x = distance * cos(angle)
# y = distance * sin(angle)

# angle et distance déterminés expérimentalement.
# 250mm, 135° == (-176.78, 176.78)
# 250mm, 225° == (-176.78, -176.78)


# Zone de détection
# AxxxxxxB
# xxxxxxxx  <-Robot
# CxxxxxxD

# A = (-1000, 176.78)
# B = (-176.78, 176.78)
# C = (-1000, -176.78)
# D = (-176.78, -176.78)
# Note: coordonnées en mm

MAX_X = -176.78
MIN_X = -500

MAX_Y = 176.78
MIN_Y = -176.78

ANGLE_MIN = 135
ANGLE_MAX = 225

class Lidar:
    def __init__(self, jeton:JetonAnnulation):
        port = "/dev/ttyUSB0"
        self.__sensor = PyLidar3.YdLidarX4(port) 
        self.objet_present = False
        self.__jeton = jeton
        self.__thread = threading.Thread(target=self.détecter_objet)


    def demarrer(self):
        self.__thread.start()
    
    def terminer(self):
        self.__jeton.terminer()
        self.__thread.join()


    def détecter_objet(self):
        """Tant que le thread, continue, check si un objet est present"""
        if(self.__sensor.Connect()):
            gen = self.__sensor.startScanning()
            while self.__jeton.continuer():
                data = next(gen)
                self.objet_present = self.__détecter_obstacle(data)
                time.sleep(0.5)
            self.__sensor.StopScanning()
            self.__sensor.Disconnect()

        else:
            print("Lidar ne se connecte pas, reboot le robot")
            self.__sensor.Reset()   

        
    def __détecter_obstacle(self,data):
        """Detecte objet dans le rectangle"""
        
        angle = ANGLE_MIN
        compteur = 0
        obstacle_trouvé = False
        while not obstacle_trouvé and angle <= ANGLE_MAX and compteur < 3:
            if(data[angle] != 0):
                point = Algos.trouver_position(angle, data[angle])
                if(Algos.est_dans_aire(MIN_X,MAX_X,MIN_Y, MAX_Y,point[0], point[1])):
                    compteur +=1
                    if compteur >= 3:
                        obstacle_trouvé = True
                else:
                    compteur = 0
            angle+=1


        return obstacle_trouvé

    

def test(p1 = (-306,43), p2 = (20,43)):
    """Test si les point x et y sont dans le carré devant le robot"""
    print(Algos.est_dans_aire(MIN_X,MAX_X,MIN_Y, MAX_Y,p1[0], p1[1]))
    print(Algos.est_dans_aire(MIN_X,MAX_X,MIN_Y, MAX_Y,p2[0], p2[1]))

def main():
    
    jeton = JetonAnnulation()
    lidar = Lidar(jeton)
    lidar.demarrer()
    time.sleep(10)
    lidar.terminer()

if __name__ == "__main__":
    main()