# Julian Angel Murillo
# 2022-12-19
# PFI - Le robot autonome
# classe DetecteurMouvement: Utilise la camera pour detecter des mouvements 

from Camera import Camera 
import cv2
import numpy as np
import threading
from JetonAnnulation import JetonAnnulation


SEUIL_MAX = 255
SEUIL_MIN = 70
AIRE_MIN = 500

class DetecteurMouvement:
    def __init__(self) :
        self.__cam = Camera()
        # self.__thread = threading.Thread(target=self.detecter_mouvement)
        self.__thread = threading.Thread(target=self.__detecter_mouvement)
        
        

    def commencer(self,jeton:JetonAnnulation):
        self.jeton = jeton
        self.__thread.start()

    def finir(self):
        self.jeton.terminer()
        self.__thread.join()


    def __detecter_mouvement(self):
        compteur_frame = 0
        frame_precendente = None
        while self.jeton.continuer():
            compteur_frame +=1
            succes, img = self.__cam.obtenir_image()
            frame_actuelle = Camera.convert_to_grayscale(img)
            if((compteur_frame % 2) == 0):
                frame_actuelle = cv2.GaussianBlur(src=frame_actuelle, ksize=(5,5), sigmaX=0)
                
                
                if(frame_precendente is None):
                    frame_precendente = frame_actuelle
                    continue
                
                differences = cv2.absdiff(src1=frame_precendente, src2=frame_actuelle)
                frame_precendente = frame_actuelle

                # I dont even know what this does
                kernel = np.ones((5, 5))
                differences = cv2.dilate(differences, kernel, 1)

                # prend les differences d'une taille minimum
                # differences_min =  cv2.threshold(src=differences, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
                differences_min =  cv2.threshold(src=differences, thresh=SEUIL_MIN, maxval=SEUIL_MAX, type=cv2.THRESH_BINARY)[1]


                contours, _ = cv2.findContours(image=differences_min, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    if cv2.contourArea(contour) < AIRE_MIN:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)

                cv2.imshow('Motion detector', img)

                if cv2.waitKey(1) == ord('x'):
                    self.jeton.terminer()

def test():
    cam = Camera()
    compteur_frame = 0
    frame_precendente = None
    jeton = JetonAnnulation()

    while jeton.continuer():
        compteur_frame +=1
        succes, img = cam.obtenir_image()
        frame_actuelle = Camera.convert_to_grayscale(img)
        #cheque si le compyeur est pair
        if((compteur_frame % 2) == 0):
            frame_actuelle = cv2.GaussianBlur(src=frame_actuelle, ksize=(5,5), sigmaX=0)
            
            
            if(frame_precendente is None):
                #si on a pas de frame precendete, on skip le reste du while
                frame_precendente = frame_actuelle
                continue
            
            differences = cv2.absdiff(src1=frame_precendente, src2=frame_actuelle)
            frame_precendente = frame_actuelle

            # I dont even know what this does
            kernel = np.ones((5, 5))
            differences = cv2.dilate(differences, kernel, 1)

            # prend les differences d'une taille minimumx
            # differences_min =  cv2.threshold(src=differences, thresh=SEUIL_MIN, maxval=255, type=cv2.THRESH_BINARY)[1]
            differences_min =  cv2.threshold(src=differences, thresh=70, maxval=SEUIL_MAX, type=cv2.THRESH_BINARY)[1]


            contours, _ = cv2.findContours(image=differences_min, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

            for contour in contours:
                if cv2.contourArea(contour) > AIRE_MIN:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
                

            cv2.imshow('Motion detector', img)

            if cv2.waitKey(1) == ord('x'):
                jeton.terminer()

def main():
    # test()
    
    bigD = DetecteurMouvement()
    bigD.detecter_mouvement()
    



if __name__ == "__main__":
    main()