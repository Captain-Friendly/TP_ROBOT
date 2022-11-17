# Pascal Arès & Philippe C. Léger
# 2022-10-20
# Labo 5
# Point d'entrée de l'application pour le labo 5

import cv2
from Rectangle import Rectangle
from Camera import Camera
from TraqueurPatron import TraqueurPatron

def main():

    def analyser_image(traqueur:TraqueurPatron, img, roi:Rectangle):
        obj = traqueur.obtenir_objet(img, roi)
        if obj != None:
            cv2.rectangle(img, (obj.x, obj.y), (obj.x + obj.l, obj.y + obj.h), (255, 0, 0), 3)
            cv2.drawMarker(img, (int(obj.centre().x), int(obj.centre().y)), (255, 255, 255), markerType= cv2.MARKER_CROSS, thickness=2)
        if roi != None:
            cv2.rectangle(img, (int(roi.x), int(roi.y)), (int(roi.x + roi.l), int(roi.y + roi.h)), (0, 255, 0), 3)
        cv2.imshow("Image", img)
        return traqueur.obtenir_region_interet(img, obj)

    patron = cv2.imread("images/patron.bmp")
    masque = cv2.imread("images/masque.bmp")
    SEUIL = 0.5
    COEFF_ROI = 3
    roi = None
    traqueur = TraqueurPatron(patron, masque, SEUIL, COEFF_ROI)
    camera = Camera()
    camera.demarrer()
    while cv2.waitKey(1) != ord('x'):
        ok, img = camera.obtenir_image()
        if ok:
            roi = analyser_image(traqueur, img, roi)
    cv2.destroyAllWindows()
    camera.terminer()

if __name__ == "__main__":
    main()