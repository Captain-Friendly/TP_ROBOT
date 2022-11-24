import PyLidar3
import time

# angle:distence en mm
# FRONT : 180°
# BACK : 0°
# TODO: rectangle au devant du robot, tranformer les coins de angle distance en x,y
# geogebra: x^(2)+y^(2)=r^(2)
# r est la distance 
# https://www.math.net/circle-formula


class Lidar:
    def __init__(self):
        port = "/dev/ttyUSB0"
        self.__sensor = PyLidar3.YdLidarX4(port) 

    def printShit(self):
        """Prints data of lidar"""
        if(self.__sensor.Connect()):
            # print(self.__sensor.GetDeviceInfo())
            gen = self.__sensor.StartScanning()
            data = {}

            end = time.perf_counter() + 3
            while time.perf_counter() < end:
                data = next(gen)
                Dictionnaire: data[0:359] 
                # print(data)               
                time.sleep(0.5)
                self.__sensor.StopScanning()
                self.__sensor.Disconnect()
            
            for angle in data:
                # print(f"{data[angle]}")
                print(f" °:{angle}\t Dist:{data[angle]}mm")

                # if(data[angle] == 0):
                #     print(f" °:{angle}\t Dist:{data[angle]}")
        else:
            print("Erreur")
            self.__sensor.Reset()   


def main():
    lidar = Lidar()
    lidar.printShit()

    # shit = {1:55, 3:45}
    # print(type(shit))
    # print(shit)

if __name__ == "__main__":
    main()