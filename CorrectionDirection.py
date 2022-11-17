from Point import Point
class CorrectionDirection:
    def __init__(self) -> None:
        pass
    def a(self,angle_i:int,point_i:Point,point_f:Point):
        point_i.soustraire(point_f)
        pass