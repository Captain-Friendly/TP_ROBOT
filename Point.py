# Pascala Arès
# 2022-11-24
# Labo 4
# Classe Point: Classe représentant un Point (2d)

from math import atan2,pi,sqrt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def soustraire(self,point_c):
        return Point(self.x-point_c.x,self.y-point_c.y)
    def angle(point_a,point_o):
        p=point_o.soustraire(point_a)
        return atan2(p.y,p.x)/pi*180
    def distance(point_a,point_b):
        point_x=point_a.x-point_b.x
        point_y=point_a.y-point_b.y
        return sqrt(point_x*point_x+point_y*point_y)

def main():
    point1=Point(0,0)
    point2=Point(0,-1)
    point3=Point(0,1)
    point4=Point(-1,0)
    point6=Point(-1,-1)
    point7=Point(-1,1)
    point5=Point(1,0)
    point8=Point(1,-1)
    point9=Point(1,1)
    
    print(Point.angle(point1,point2)==-90)
    print(Point.angle(point1,point3)==90)
    print(Point.angle(point1,point4)==180)
    print(Point.angle(point1,point5)==0)
    print(Point.angle(point1,point6)==-135)
    print(Point.angle(point1,point7)==135)
    print(Point.angle(point1,point8)==-45)
    print(Point.angle(point1,point9)==45)
    print(Point.angle(point9,point1)==-135)
    print(Point.angle(point9,point3)==180)
    print(Point.angle(point9,point5)==-90)
    print(Point.angle(point9,point6)==-135)
    print(Point.angle(point9,point7)==180)
    print(Point.angle(point9,point8)==-90)
    print(Point.angle(point9,point9)==0)
    
if __name__ == "__main__":
    main()

    