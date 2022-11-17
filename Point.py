# Philippe C. Léger
# 2022-09-26
# Labo 4
# Classe Point: Classe représentant un Point (2d)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def soustraire(self,point_c:Point):
        return Point(self.x-point_c.x,self.y-point_c.y)
    def angle(point_a:Point,point_o:Point=Point(0,0)):
        p=point_a.soustraire(point_o)
    