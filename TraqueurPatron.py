# Pascal Arès & Philippe C. Léger
# 2022-10-17
# Labo 5
# Classe TraqueurPatron: Classe utilisée pour trouver un patron
# dans une image.

from Camera import Camera
from Point import Point
from Rectangle import Rectangle
import cv2

class TraqueurPatron:
    def __init__(self, patron, masque, seuil, coeff_roi):
        self.__patron = cv2.cvtColor(patron, cv2.COLOR_BGR2GRAY)
        self.__masque = cv2.cvtColor(masque, cv2.COLOR_BGR2GRAY)
        self.__seuil = seuil
        self.__largeur_roi = coeff_roi * self.__patron.shape[1]
        self.__hauteur_roi = coeff_roi * self.__patron.shape[0]


    def obtenir_objet(self, img, roi:Rectangle=None) -> Rectangle:
        img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coin_haut_gauche = Point(0, 0)
        if roi != None and roi.l >= self.__patron.shape[1] and roi.h >= self.__patron.shape[0]:
            coin_haut_gauche = Point(roi.x, roi.y)
            img_gris = img_gris[int(roi.y):int(roi.y+roi.h), int(roi.x):int(roi.x+roi.l)]
        res = cv2.matchTemplate(img_gris, self.__patron, cv2.TM_CCOEFF_NORMED, None, self.__masque)
        val_min, val_max, pos_min, pos_max = cv2.minMaxLoc(res)
        if val_max < self.__seuil: 
            if roi == None: return None
            else: return self.obtenir_objet(img)
        else:
            h, l = self.__patron.shape
            x, y = pos_max
            return Rectangle(x + coin_haut_gauche.x, y + coin_haut_gauche.y, l, h)


    def obtenir_region_interet(self, img, obj:Rectangle) -> Rectangle:
        if obj is not None:
            centre=obj.centre()
            x = int(max(0, centre.x-self.__largeur_roi/2))
            y = int(max(0, centre.y-self.__hauteur_roi/2))
            l = int(min(img.shape[1], centre.x+self.__largeur_roi/2)) - x
            h = int(min(img.shape[0], centre.y+self.__hauteur_roi/2)) - y
            return Rectangle(x, y, l, h)


def main():
    testUnitaire()

def testUnitaire():
    img = cv2.imread("images/test.bmp")
    patron = cv2.imread("images/patron.bmp")
    masque = cv2.imread("images/masque.bmp")
    SEUIL = 0.5
    COEFF_ROI = 3
    traqueur = TraqueurPatron(patron, masque, SEUIL,COEFF_ROI)
    obj=traqueur.obtenir_objet(img,None)
    roi=traqueur.obtenir_region_interet(img, obj)
    cv2.rectangle(img, (obj.x, obj.y), (obj.x + obj.l, obj.y + obj.h), (255, 0, 0), 3)
    cv2.rectangle(img, (int(roi.x), int(roi.y)), (int(roi.x + roi.l), int(roi.y + roi.h)), (0, 255, 0), 3)
    cv2.imshow("TestUnitaire", img)
    cv2.waitKey()

if __name__ == "__main__":
    main()