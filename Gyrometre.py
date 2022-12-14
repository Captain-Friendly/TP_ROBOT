# Pascal Arès
# 2022-12-05

# Classe Gyrometre: Classe permettant de suivre la position anglaire du module inertiel autour de l'abscisse
#                   Basée sur la classe Navigation du laboratoire 6

from JetonAnnulation import JetonAnnulation
from ModuleInertiel import ModuleInertiel
from statistics import mean
from CollectionCirculaire import CollectionCirculaire

class Gyrometre:
    def __init__(self, module_inertiel:ModuleInertiel, obtenir_temps, jeton: JetonAnnulation, attendre):
        self.__module_inertiel = module_inertiel
        self.angle=0
        self.gx = 0
        self.correction_gx=0
        self.__jeton = jeton
        self.__obtenir_temps = obtenir_temps
        self.__attendre = attendre
        self.collection_gx = CollectionCirculaire(5)
        
    def __boucle_obtenir_mesure(self):
        while(self.__jeton.continuer()):
            ax, ay, az, gx, gy, gz=self.__module_inertiel.obtenir_mesure()
            t = self.__obtenir_temps()
            dt = t - self.t 
            self.t = t
            gx = self.corriger_gx(gx)
            self.angle += dt * (self.gx + gx) / 2 
            self.gx = gx
            self.__attendre()

    def corriger_gx(self,gx):
        return gx - self.correction_gx

    def calibrer_gx(self,gx=0):
        self.collection_gx.ajouter(gx)
        self.correction_gx = mean(self.collection_gx.obtenir_valeurs())

    def demarrer(self):
        self.t = self.__obtenir_temps()
        self.angle = 0
        self.gx = 0
        self.__boucle_obtenir_mesure()

    def obtenir_angle(self):
        return self.corriger_gx(self.angle)

    def arreter(self):
        self.__jeton.terminer()

    def abonner(self,callback):
        self.__list_callback.append(callback)

    def assigner_angle(self, angle, gx=0):
        self.angle = angle
        self.gx = gx

    # def corriger_gx(self, gx):
    #     return gx - self.correction_gx

    def reinitialiser(self, jeton:JetonAnnulation):
        self.__jeton = jeton
        self.demarrer()

def main():
    from time import perf_counter, sleep
    from icm20948 import ICM20948
    from threading import Thread

    imu = ICM20948()
    mod = ModuleInertiel(imu)
    jeton = JetonAnnulation()
    gyro = Gyrometre(mod,perf_counter, jeton, lambda: sleep(0.05))
    t_gyro= Thread(target=gyro.demarrer)
    t_gyro.start()

    def printAngle():
        print("étalonage")
        now=perf_counter()
        while perf_counter()-now<2:
            print(gyro.obtenir_angle())
            gyro.calibrer_gx(gyro.obtenir_angle())
            sleep(0.1)
        print("mesures")
        while jeton.continuer():
            print(gyro.obtenir_angle(), gyro.correction_gx)
            sleep(1)
        

    t_print = Thread(target= printAngle)
    t_print.start()
    input("Appuyez sur [Entrer] pour quitter...")
    jeton.terminer()
    t_gyro.join()
    t_print.join()
    
if __name__=="__main__":
    main()