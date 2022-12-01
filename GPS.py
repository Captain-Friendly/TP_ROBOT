#sudo pip3 install pyserial 
import serial
from time import sleep
from Point import Point
from CollectionCirculaire import CollectionCirculaire
from JetonAnnulation import JetonAnnulation
from threading import Thread
class GPS:
    def __init__(self,période=1/4) -> None:
        self.__période=période
        self.serial = serial.Serial() 
        self.serial.port = '/dev/ttyACM0'
        self.serial.baudrate = 115200
        self.serial.open()
        self.__jeton=JetonAnnulation()
        self.liste=CollectionCirculaire(2)
    
    def __string_to_data(string):
        data=string.split(",")

        print("hors:",data[0])
        if data[0]=="POS":
            print("good",data[0])
            return Point(float(data[1]),float(data[2]))
        else: 
            print("bad:",data)
            return None

    def __get_position(self):
        self.serial.write(b'lep\n')
        #data = str(self.serial.readline())
        data = self.serial.readline().decode("utf-8")
        return GPS.__string_to_data(data)

    def __t_start(self):
        while self.__jeton.continuer():
            self.liste.ajouter(self.__get_position())
            sleep(self.__période)

    def get_position(self):
        return self.liste.dernier_ajouté()


    def get_angle(self):

        return None #Point.angle()

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
    
    jeton=JetonAnnulation()
    # def wait(j:JetonAnnulation):
    #     input()
    #     j.terminer()
    # t=Thread(lambda:wait(jeton))
    # t.start()
    def get_ma_position(jeton):
        gps.start()
        while jeton.continuer():
            p=gps.get_position()
            if p is not None:
                print(p.x,p.y)
            else:
                print("is bullshit")
            sleep(1)
        gps.stop()

    t = Thread(target=lambda: get_ma_position(jeton))
    t.start()
    input("Appuyez sur [enter pour terminer...]\n")
    jeton.terminer()
    t.join()

if __name__=="__main__":
    main()

