# Pascal Arès, Philippe C. Léger
# 2022-12-19
# PFI - Le robot autonome
# class GPS: Classe permettant de déterminer la position du robot
# dans la classe à l'aide des balises de positionnement radio.


import serial
from time import sleep
from Point import Point
from CollectionCirculaire import CollectionCirculaire
from JetonAnnulation import JetonAnnulation
from threading import Thread
from statistics import mean
class GPS:
    def __init__(self, jeton:JetonAnnulation, période=1/20) -> None:
        self.__période=période
        self.serial = serial.Serial() 
        self.serial.port = '/dev/ttyACM0'
        self.serial.baudrate = 115200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1
        self.serial.open()
        self.__jeton=jeton
        self.liste=CollectionCirculaire(2)
        self.__position = None
    
    def __string_to_data(string):
        data=string.split(",")

        if data[0]=="POS":
            try:

                return Point(float(data[1]),float(data[2]))
            except:
                return None
        else: 
            return None

    def __obtenir_position(self):
        data = self.serial.readline().decode("utf-8")
        return GPS.__string_to_data(data)



    def __t_demarrer(self):
        while self.__jeton.continuer():
            pos=self.__obtenir_position()
            if pos is not None:
                self.__position = pos
            sleep(self.__période)

    def obtenir_position(self):
        return self.__position
        
    def demarrer(self):
        self.serial.write(b'\r\r')
        sleep(1)
        self.serial.write(b'lep\n')
        sleep(1)
        self.t_demarrer=Thread(target=self.__t_demarrer)
        self.t_demarrer.start()

    def terminer(self):
        self.__jeton.terminer()
        self.t_demarrer.join()
        self.serial.close()

def main():
    
    jeton=JetonAnnulation()
    gps= GPS(jeton)
    def obtenir_ma_position(jeton):
        gps.demarrer()
        while jeton.continuer():
            p=gps.obtenir_position()
            a=gps.obtenir_angle()
            if p is not None:
                print(f"({p.x}, {p.y}) @ {a}°")
                pass
            else:
                print("is bullshit")
            sleep(2)
        gps.stop()

    t = Thread(target=lambda: obtenir_ma_position(jeton))
    t.start()
    input("Appuyez sur [enter pour terminer...]\n")
    jeton.terminer()
    t.join()

if __name__=="__main__":
    main()

