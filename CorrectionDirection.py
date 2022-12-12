from Point import Point
from Robot import Robot
from ModuleInertiel import ModuleInertiel
from Point import Point
from Math import abs
from time import sleep,perf_counter
from threading import Thread
from JetonAnnulation import JetonAnnulation
from GPS import GPS
from Gyrometre import Gyrometre
class CorrectionDirection:
    def __init__(self,robot:Robot,gyro:Gyrometre,gps:GPS,precision_angle=3,precision_distance=0.5):
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

    def est_destination_atteinte(self):
        if self.__destination is not None:
            return self.__precision_distance <= Point.distance(self.__gps.get_position(),self.__destination)
        return False

    def demarrer(self,f_next):
        self.__thread.start()

    def centrer(self):#,current_angle,point_ini,point_final):
        while self.__jeton.continuer():
            current_angle=self.__gps.get_angle()
            point_ini=self.__gps.get_position()
            point_final=self.__destination
            dt_angle=self.__correction_angle(current_angle,point_ini,point_final)
            if abs(dt_angle)>self.__precision_angle:
                angle_gyro_ini=self.__gyro.angle

                def obtenir_angle():
                    return self.__gyro.angle-angle_gyro_ini

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
    from icm20948 import ICM20948
    POINT=[Point(3,3),Point(3,5),Point(5,5),Point(5,3),Point(3,3)]
    imu = ICM20948()
    robot=Robot.construire()

    jeton=JetonAnnulation()
    gyro=Gyrometre(ModuleInertiel(imu),perf_counter,jeton)
    gps=GPS(jeton)
    correcteur=CorrectionDirection(robot,gyro,gps,3,0.5)
    correcteur.demarrer()
    robot.avancer()
    while len(POINT>=1):
        point=POINT.pop(0)
        correcteur.set_destination(point)
        while correcteur.est_destination_atteinte():
            # détecter obstacle
            sleep(0.02)
    
if __name__=="__main__":
    main()

            

