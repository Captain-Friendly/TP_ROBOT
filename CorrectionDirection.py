from Point import Point
from Robot import Robot
from Math import abs
class CorrectionDirection:
    def __init__(self,precision=5):
        self.__precision=precision
    def correction_angle(self, angle_i:int, point_i:Point, point_f:Point):
        return (Point.angle(point_i,point_f)-angle_i-180)%360-180
        
    def centrer(self,current_angle,point_ini,point_final, robot:Robot):
        while abs(dt_angle)>self.__precision:
            dt_angle=self.correction_angle(current_angle,point_ini,point_final)
            if dt_angle<0:
                robot.tourner_g()
            else:
                robot.tourner_d()
            

