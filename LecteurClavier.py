# Pascal Arès
# 2022-08-25
# Labo 1
# Classe LecteurClavier: Classe wrapper de CV2 pour gérer les 
# évènements du clavier.

import numpy as np
import cv2
from JetonAnnulation import JetonAnnulation

class LecteurClavier:
    def __init__(self):
        self.__appels = {}

    def assigner_appel(self, caractère, fonction):
        self.__appels[caractère] = fonction
    
    def activer(self,jeton_annulation:JetonAnnulation):
        img = np.zeros((100,100,3),np.uint8)
        cv2.imshow('Labo 1',img)
        # dans un thread
        while(jeton_annulation.continuer()):
            key=cv2.waitKey(0)
            for touche in self.__appels:
                if(key!=-1):
                    if(chr(key)==touche):
                        self.__appels[touche]()
def main():
    def hi():
        print('hi')
    def hi2():
        print('hi2')
    def hi3():
        print('hi3')
    lecteur=LecteurClavier()
    jeton=JetonAnnulation()
    lecteur.assigner_appel('s',hi)
    lecteur.assigner_appel('a',hi2)
    lecteur.assigner_appel('d',hi3)
    lecteur.assigner_appel('x',jeton.terminer)
    lecteur.activer(jeton)

if __name__ == "__main__":
    main()
