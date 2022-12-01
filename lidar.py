import PyLidar3
import time
from Algos import Algos

# angle:distence en mm
# FRONT : 180°
# BACK : 0°
# geogebra: x^(2)+y^(2)=r^(2)

# x = distance * cos(angle)
# y = distance * sin(angle)


# 25cm, 135° == (-17,678, 17.678)
# 25cm, 225° == (-17.678, -17.678)


# AxxxxxxxxxxxxxxxxxxxB
# xxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxx
# CxxxxxxxxxxxxxxxxxxxD

# A = (-50, 17.678)
# B = (-17.678, 17.678)

# C = (-50, -17.678)
# D = (-17.678, -17.678)

MAX_X = -176.78
# MIN_X = -500
MIN_X = -1000
MAX_Y = 176.78
MIN_Y = -176.78

ANGLE_MIN = 135
ANGLE_MAX = 225

class Lidar:
    def __init__(self):
        port = "/dev/ttyUSB0"
        self.__sensor = PyLidar3.YdLidarX4(port) 
        self.__objet_present = False

    def printShit(self):
        """Prints data of lidar"""
        if(self.__sensor.Connect()):
            # print(self.__sensor.GetDeviceInfo())
            gen = self.__sensor.StartScanning()
            data = {}

            end = time.perf_counter() + 1
            while time.perf_counter() < end:
                data = next(gen)
                # print(data)               
                time.sleep(0.5)
                self.__sensor.StopScanning()
                self.__sensor.Disconnect()
            
            angle = ANGLE_MIN
            compteur = 0
            # print(data)
            while angle <= ANGLE_MAX and compteur < 3:
                if(data[angle] != 0):
                    point = Algos.TrouverPosition(angle, data[angle])
                    print(point)
                    if(Algos.EstDansAire(MIN_X,MAX_X,MIN_Y, MAX_Y,point[0], point[1])):
                        compteur +=1
                        print("angle suspicieux")

                angle+=1

            if(compteur >= 2):
                self.__objet_present = True
                print(f"objet dans la zone")
            else:
                self.__objet_present = False
                print(f"zone vide")

        else:
            print("Erreur")
            self.__sensor.Reset()   


    def scanner_thread(self):
        """Prints data of lidar"""
        if(self.__sensor.Connect()):
            # print(self.__sensor.GetDeviceInfo())
            gen = self.__sensor.StartScanning()
            data = {}

            end = time.perf_counter() + 1
            while True:
                data = next(gen)
                # print(data)               
                time.sleep(0.5)
                self.__sensor.StopScanning()
                self.__sensor.Disconnect()
            
                angle = ANGLE_MIN
                compteur = 0
                # print(data)
                while angle <= ANGLE_MAX and compteur < 3:
                    # point = Algos.TrouverPosition(angle, data[angle])
                    # print(point)
                    if(data[angle] != 0):
                        point = Algos.TrouverPosition(angle, data[angle])
                        print(point)
                        if(Algos.EstDansAire(MIN_X,MAX_X,MIN_Y, MAX_Y,point[0], point[1])):
                            compteur +=1
                            print("angle suspicieux")

                    angle+=1

                if(compteur >= 2):
                    print(f"objet dans la zone")
                else:
                    print(f"zone vide")
        else:
            print("Erreur")
            self.__sensor.Reset() 



    def Test():
        print(Algos.EstDansAire(MIN_X,MAX_X,MIN_Y, MAX_Y,-306, 43))
        # -250, 0




def main():
    lidar = Lidar()
    lidar.printShit()
    # Lidar.Test()

    # shit = {1:55, 3:45}
    # print(type(shit))
    # print(shit)

if __name__ == "__main__":
    main()