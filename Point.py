# Pascala Arès
# 2022-11-24
# Labo 4
# Classe Point: Classe représentant un Point (2d)

from math import atan2,pi,sqrt
from Algos import Algos

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def soustraire(p0,p1):
        return Point(p0.x-p1.x,p0.y-p1.y)
    def angle(point_o, point_a):
        p=Point.soustraire(point_a, point_o)
        return atan2(p.y,p.x)/pi*180
    def distance(point_a,point_b):
        point_x=point_a.x-point_b.x
        point_y=point_a.y-point_b.y
        return sqrt(point_x*point_x+point_y*point_y)
        
    def egal(self, p):
        return self.x == p.x and self.y == p.y

    def to_string(self):
        return f"({self.x}, {self.y})"

def main():

    def test_soustraire(p0:Point, p1:Point):
        p_diff = p0.soustraire(p1)
        p_attendu = Point(p0.x - p1.x, p0.y - p1.y)
        print(p_diff.egal(p_attendu))

    def test_angle(p0:Point, p1:Point, angle_attendu):
        print(Algos.approx_egal(Point.angle(p0, p1), angle_attendu))
        # print(Point.angle(p0, p1) == angle_attendu)

    point1=Point(0,0)
    point2=Point(0,-1)
    point3=Point(0,1)
    point4=Point(-1,0)
    point6=Point(-1,-1)
    point7=Point(-1,1)
    point5=Point(1,0)
    point8=Point(1,-1)
    point9=Point(1,1)

    test_soustraire(point1, point2)
    test_soustraire(point1, point3)

    test_angle(point1, point2,-90.0)
    test_angle(point1,point3,90)
    test_angle(point1,point4,180)
    test_angle(point1,point5,0)
    test_angle(point1,point6,-135)
    test_angle(point1,point7,135)
    test_angle(point1,point8,-45)
    test_angle(point1,point9,45)
    test_angle(point9,point1,-135)
    test_angle(point9,point3,180)
    test_angle(point9,point5,-90)
    test_angle(point9,point6,-135)
    test_angle(point9,point7,180)
    test_angle(point9,point8,-90)
    test_angle(point9,point9,0)
    
if __name__ == "__main__":
    main()

    