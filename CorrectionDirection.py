from Point import Point
from Robot import Robot
from ModuleInertiel import ModuleInertiel
from Point import Point
from Math import abs
from time import sleep
from threading import Thread
from JetonAnnulation import JetonAnnulation
class CorrectionDirection:
    def __init__(self,robot:Robot,gyro,gps,precision_angle=3,precision_distance=0.1):
        self.__robot=robot
        self.__precision_angle=precision_angle
        self.__precision_distance=precision_distance
        self.__gyro=gyro
        self.__gps=gps
        self.__destination=None
        self.__thread=Thread(target=self.centrer)
        self.__jeton=JetonAnnulation()
    def __correction_angle(self, angle_i:int, point_i:Point, point_f:Point):
        return (Point.angle(point_i,point_f)-angle_i-180)%360-180
    
    def set_destination(self,point:Point):
        self.__destination=point

    def demarrer(self,f_next):
        self.__thread.start()

    def centrer(self):#,current_angle,point_ini,point_final):
        while self.__jeton.continuer():
            current_angle=self.__gps.current_angle()
            point_ini=self.__gps.position()
            point_final=self.__destination
            dt_angle=self.__correction_angle(current_angle,point_ini,point_final)
            if abs(dt_angle)>self.__precision_angle:
                angle_gyro_ini=self.__gyro.angle()

                def obtenir_angle():
                    return self.__gyro.angle()-angle_gyro_ini

                while obtenir_angle()<dt_angle:
                    D_angle=dt_angle+obtenir_angle()
                    if D_angle<0:
                        self.__robot.tourner_g()
                    else:
                        self.__robot.tourner_d()
            else:
                self.__robot.avancer()
            sleep(0.05)
    def arreter(self):
        self.__jeton.terminer()
        self.__thread.join()
def main():
    robot=Robot.construire()
    gyro=ModuleInertiel()
    correcteur=CorrectionDirection(robot,gyro,None,3,0.05)
if __name__=="__main__":
    main()

            

