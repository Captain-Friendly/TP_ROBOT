#sudo pip3 install pyserial 
import serial
from time import sleep
from Point import Point
from CollectionCirculaire import CollectionCirculaire
from JetonAnnulation import JetonAnnulation
from threading import Thread
class GPS:
    def __init__(self, jeton:JetonAnnulation, période=1/10) -> None:
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

        #print("hors:",data[0])
        if data[0]=="POS":
            # print(f"good: {string}")
            return Point(float(data[1]),float(data[2]))
        else: 
            # print(f"bad: {string}")
            #print("bad:",data)
            return None

    def __get_position(self):
        # self.serial.write(b'lep\n')
        #data = str(self.serial.readline())
        data = self.serial.readline().decode("utf-8")
        # if data[0]=="P":
        #     print(f"New data:{data}")
        return GPS.__string_to_data(data)



    def __t_start(self):
        while self.__jeton.continuer():
            pos=self.__get_position()
            if pos is not None:
                difference=0.15
                if self.liste.dernier_ajouté() is None or Point.distance(pos,self.liste.dernier_ajouté())>difference:
                # if self.__position is None or Point.distance(pos,self.__position)>difference:
                    print(f"Ajouté: {pos.to_string()}")
                    self.liste.ajouter(pos)
                    # self.__position = pos
                # else: print(f"Pas ajouté: {pos.to_string()}")
            # else: print("Rien")
            sleep(self.__période)

    def get_position(self):
        # return self.__position
        return self.liste.dernier_ajouté()


    def get_angle(self):
        valeurs=self.liste.obtenir_valeurs()
        
        if len(valeurs)==2 and valeurs[0] is not None and valeurs[1] is not None:
            return Point.angle(valeurs[0],valeurs[1])
        return None #Point.angle()

    def start(self):
        self.serial.write(b'\r\r')
        sleep(1)
        self.serial.write(b'lep\n')
        sleep(1)
        self.t_start=Thread(target=self.__t_start)
        self.t_start.start()

    def stop(self):
        self.__jeton.terminer()
        self.t_start.join()
        self.serial.close()

def main():
    
    jeton=JetonAnnulation()
    gps= GPS(jeton)
    # def wait(j:JetonAnnulation):
    #     input()
    #     j.terminer()
    # t=Thread(lambda:wait(jeton))
    # t.start()
    def get_ma_position(jeton):
        gps.start()
        while jeton.continuer():
            p=gps.get_position()
            a=gps.get_angle()
            if p is not None:
                print(f"({p.x}, {p.y}) @ {a}°")
                pass
            else:
                pass#print("is bullshit")
            sleep(0.5)
        gps.stop()

    t = Thread(target=lambda: get_ma_position(jeton))
    t.start()
    input("Appuyez sur [enter pour terminer...]\n")
    jeton.terminer()
    t.join()

if __name__=="__main__":
    main()

