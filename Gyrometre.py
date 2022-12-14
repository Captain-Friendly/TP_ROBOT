# Pascal Arès
# 2022-12-05

# Classe Gyrometre: Classe permettant de suivre la position anglaire du module inertiel autour de l'abscisse
#                   Basée sur la classe Navigation du laboratoire 6

from JetonAnnulation import JetonAnnulation
from ModuleInertiel import ModuleInertiel

class Gyrometre:
    def __init__(self, module_inertiel:ModuleInertiel, obtenir_temps, jeton: JetonAnnulation, attendre):
        self.__module_inertiel = module_inertiel
        self.angle=0
        self.gx = 0
        self.__jeton = jeton
        self.__obtenir_temps = obtenir_temps
        self.__attendre = attendre
        
    def __boucle_obtenir_mesure(self):
        while(self.__jeton.continuer()):
            ax, ay, az, gx, gy, gz=self.__module_inertiel.obtenir_mesure()
            t = self.__obtenir_temps()
            dt = t - self.t 
            self.t = t
            gx = self.corriger_angle(gx)
            self.angle += dt * (self.gx + gx) / 2 
            self.gx = gx
            self.__attendre()

    def demarrer(self):
        self.t = self.__obtenir_temps()
        self.angle = 0
        self.gx = 0
        self.__boucle_obtenir_mesure()

    def obtenir_angle(self):
        return self.angle

    def arreter(self):
        self.__jeton.terminer()

    def abonner(self,callback):
        self.__list_callback.append(callback)

    def assigner_angle(self, angle):
        self.angle = angle
        self.gx = 0

    def corriger_angle(self, gx):
        return gx - self.correction_gx

    def reinitialiser(self, jeton:JetonAnnulation):
        self.__jeton = jeton
        self.demarrer()