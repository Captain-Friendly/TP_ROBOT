# Philippe C. Léger
# 2022-09-26
# Labo 4
# Classe Camera: classe facilitant l'utilisation d'une
# VideoCapture d'OpenCV

import cv2

class Camera:
    LARGEUR_DEFAUT = 320
    HAUTEUR_DEFAUT = 240
    def __init__(self, largeur=LARGEUR_DEFAUT, hauteur=HAUTEUR_DEFAUT, indice=0):
        self.__largeur = largeur
        self.__hauteur = hauteur
        self.__actif = False
        self.__indice = indice
        pass

    def obtenir_hauteur(self):
        return self.__hauteur
        
    def obtenir_largeur(self):
        return self.__largeur

    def demarrer(self):
        if not self.__actif: 
            self.__camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
            self.__actif = self.__camera.isOpened()
            if self.__actif:
                self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.obtenir_largeur())
                self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.obtenir_hauteur())
            return self.__actif
        return False

    def terminer(self):
        if self.__actif: 
            self.__camera.release()
            self.__actif = False
            return True
        return False

    def obtenir_image(self):
        if self.__actif:
            return self.__camera.read()
        elif self.demarrer():
            return self.obtenir_image()
        return (False, None)

    def convert_to_grayscale(img):
        """Convertir image en grayscale"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def main():
    ma_camera = Camera(320, 240)
    ok, img = ma_camera.obtenir_image()
    ma_camera.terminer()
    if ok:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()