# Pascal Arès
# 2022-12-05

# Classe Gyrometre: Classe permettant de suivre la position anglaire du module inertiel autour de l'abscisse
#                   Basée sur la classe Navigation du laboratoire 6

from time import perf_counter, sleep
from JetonAnnulation import JetonAnnulation
from ModuleInertiel import ModuleInertiel
from statistics import mean
from CollectionCirculaire import CollectionCirculaire
from Robot import EtatRobot, Robot

class Gyrometre:
    CORRECTION_ANGLE=360.0/345
    def __init__(self, module_inertiel:ModuleInertiel, obtenir_temps, jeton: JetonAnnulation, attendre, obtenir_etat):
        self.__module_inertiel = module_inertiel
        self.angle=0
        self.gx = 0
        self.correction_gx=0
        self.__jeton = jeton
        self.__obtenir_temps = obtenir_temps
        self.__attendre = attendre
        self.collection_gx = CollectionCirculaire(5)
        self.__obtenir_etat = obtenir_etat

        
    # def __boucle_obtenir_mesure(self):
    #     while(self.__jeton.continuer()):
    #         ax, ay, az, gx, gy, gz=self.__module_inertiel.obtenir_mesure()
    #         t = self.__obtenir_temps()
    #         dt = t - self.t 
    #         self.t = t
    #         gx = self.corriger_gx(gx)
    #         self.angle += dt * (self.gx + gx) / 2 
    #         self.gx = gx
    #         self.__attendre()

    # def corriger_gx(self,gx):
    #     return gx - self.correction_gx

    # def calibrer_gx(self,gx=0):
    #     self.collection_gx.ajouter(gx)
    #     self.correction_gx = mean(self.collection_gx.obtenir_valeurs())

    # def demarrer(self):
    #     self.t = self.__obtenir_temps()
    #     self.angle = 0
    #     self.gx = 0
    #     self.__boucle_obtenir_mesure()

    # def obtenir_angle(self):
    #     return self.corriger_gx(self.angle)

    # def arreter(self):
    #     self.__jeton.terminer()

    # def abonner(self,callback):
    #     self.__list_callback.append(callback)

    # def assigner_angle(self, angle, gx=0):
    #     self.angle = angle
    #     self.gx = gx

    # # def corriger_gx(self, gx):
    # #     return gx - self.correction_gx

    # def reinitialiser(self, jeton:JetonAnnulation):
    #     self.__jeton = jeton
    #     self.demarrer()

##########################################
    def __boucle_obtenir_mesure(self):
        while(self.__jeton.continuer()):
            ax, ay, az, gx, gy, gz=self.__module_inertiel.obtenir_mesure()
            t = self.__obtenir_temps()
            dt = t - self.t 
            self.t = t
            etat = self.__obtenir_etat()
            if etat == EtatRobot.TOURNER:
                gx = self.corriger_gx(gx)
                self.angle += dt * (self.gx + gx) / 2 
                self.gx = gx
            else :
                self.etalonner(gx)
                #self.gx = 0
            self.__attendre()

    def demarrer(self):
        self.t = self.__obtenir_temps()
        self.__boucle_obtenir_mesure()

    def arreter(self):
        self.__jeton.terminer()

    def assigner_etat(self,etat):
        self.__etat=etat

    # def obtenir_etat(self):
    #     return self.__etat

    def corriger_gx(self, gx):
        return gx - self.correction_gx


    def etalonner(self, gx=0):
        self.collection_gx.ajouter(gx)
        self.correction_gx = mean(self.collection_gx.obtenir_valeurs())

    def obtenir_angle(self):
        return self.angle *Gyrometre.CORRECTION_ANGLE

    def construire(jeton:JetonAnnulation, robot:Robot):
        mod = ModuleInertiel.construire()
        return Gyrometre(mod, perf_counter, jeton, lambda: sleep(0.05), lambda: robot.obtenir_etat())



def main():
    from time import perf_counter, sleep
    from icm20948 import ICM20948
    from threading import Thread
    from Robot import Robot

    imu = ICM20948()
    mod = ModuleInertiel(imu)
    jeton = JetonAnnulation()
    etat = [EtatRobot.IMMOBILE]
    gyro = Gyrometre(mod,perf_counter, jeton, lambda: sleep(0.05), lambda: etat[0])
    t_gyro= Thread(target=gyro.demarrer)
    t_gyro.start()
    robot=Robot.construire()

    def printAngle():
        # print("étalonage")
        # now=perf_counter()
        # while perf_counter()-now<2:
        #     gyro.etalonner()
        #     sleep(0.1)
        etat[0] = EtatRobot.IMMOBILE
        # gyro.assigner_etat(EtatRobot.TOURNER)
        print("mesures")
        while jeton.continuer():
            print(gyro.obtenir_angle())
            sleep(0.5)
        

    t_print = Thread(target= printAngle)
    t_print.start()
    # robot.avancer()
    # sleep(5)
    # robot.freiner()
    
    etat[0] = EtatRobot.IMMOBILE
    sleep(3)
    etat[0] = EtatRobot.TOURNER
    sleep(5)
    etat[0] = EtatRobot.IMMOBILE
    sleep(3)
    etat[0] = EtatRobot.TOURNER
    sleep(5)
    etat[0] = EtatRobot.IMMOBILE

    input("Appuyez sur [Entrer] pour quitter...")
    jeton.terminer()
    t_gyro.join()
    t_print.join()
    
if __name__=="__main__":
    main()