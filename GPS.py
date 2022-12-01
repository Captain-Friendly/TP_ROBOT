#sudo pip3 install pyserial 
import serial
from time import sleep
from Point import Point
from CollectionCirculaire import CollectionCirculaire
from JetonAnnulation import JetonAnnulation
from threading import Thread
class GPS:
    def __init__(self) -> None:
        self.serial = serial.Serial() 
        self.serial.port = '/dev/ttyACM0'
        self.serial.baudrate = 115200
        self.serial.open()
        self.__jeton=JetonAnnulation()
        self.liste=CollectionCirculaire(2)
    
    def __string_to_data(string:str):
        data=string.split(",")
        if data[0]=="POS":
            return Point(float(data[1]),float(data[2]))
        else: return None

    def __get_position(self):
        self.serial.write(b'lep\n')
        data = str(self.serial.readline())
        return GPS.__string_to_data(data)

    def __t_start(self):
        while self.__jeton.continuer():
            self.liste.ajouter(self.__get_position())
            sleep(1)

    def get_position(self):
        return self.liste.dernier_ajouté()


    def get_angle(self):
        return self.liste.dernier_ajouté()

    def start(self):
        self.serial.write(b'\r\r')
        sleep(1)
        self.t_start=Thread(target=self.__t_start)
        self.t_start.start()

    def stop(self):
        self.__jeton.terminer()
        self.t_start.join()
        self.serial.close()

def main():
    gps= GPS()
    gps.start()
    gps.stop()

if __name__=="__main__":
    main()

