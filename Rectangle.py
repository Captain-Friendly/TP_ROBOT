# Philippe C. Léger
# 2022-09-26
# Labo 4
# Classe Rectangle: Classe représentant un rectangle


from Point import Point

class Rectangle:
    def __init__(self, x, y, l, h):
        self.x = x
        self.y = y
        self.l = l
        self.h = h

    def aire(self):
        return self.l * self.h

    def centre(self):
        return Point(self.x + self.l/2, self.y + self.h/2)