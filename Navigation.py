# Pascal Arès
# 2022-27-10

# Classe Navigation: Classe Navigation qui permet de recevoir les données du module inertiel...

from statistics import mean
from EtatRobot import EtatRobot
from ModuleInertiel import ModuleInertiel
from CollectionCirculaire import CollectionCirculaire
from JetonAnnulation import JetonAnnulation
from Algos import Algos

class Navigation:
    SCRUTATION=0.05
    CAPACITE_MAX=5
    g = 9.80665
    def __init__(self,module_inertiel:ModuleInertiel, obtenir_temps, jeton: JetonAnnulation, attendre):
        self.__jeton= jeton
        self.__list_callback=[]
        self.__moduleInertiel = module_inertiel
        self.__etat=0
        self.__obtenir_temps = obtenir_temps
        self.ay = 0
        self.vy = 0
        self.y = 0

        self.angle=0
        self.gx = 0
        self.correction_ay = 0
        self.correction_gx = 0
        self.collection_ay = CollectionCirculaire(Navigation.CAPACITE_MAX)
        self.collection_gx = CollectionCirculaire(Navigation.CAPACITE_MAX)
        self.attendre = attendre

    def __boucle_obtenir_mesure(self):
        while(self.__jeton.continuer()):
            ax, ay, az, gx, gy, gz=self.__moduleInertiel.obtenir_mesure()
            t = self.__obtenir_temps()
            dt = t - self.t 
            self.t = t
            etat = self.obtenir_etat()
            if etat == EtatRobot.IMMOBILE:
                self.etalonner(ay,gx)
                self.ay = 0
                self.vy = 0
                self.gx = 0
            elif etat == EtatRobot.TRANSLATION :
                ay = self.corriger_ay(ay)
                vy = self.vy + dt * (self.ay + ay) * Navigation.g / 2
                self.y += dt*(self.vy + vy) / 2
                self.vy = vy
                self.ay = ay
            elif etat == EtatRobot.TOURNER :
                gx = self.corriger_gx(gx)
                self.angle += dt * (self.gx + gx) / 2 
                self.gx = gx
            for callback in self.__list_callback:
                callback()
            self.attendre()

    def demarrer(self):
        self.t = self.__obtenir_temps()
        self.ay = 0
        self.vy = 0
        self.y = 0
        self.__boucle_obtenir_mesure()

    def arreter(self):
        self.__jeton.terminer()

    def abonner(self,callback):
        self.__list_callback.append(callback)

    def assigner_etat(self,etat):
        self.__etat=etat

    def obtenir_etat(self):
        return self.__etat

    def corriger_ay(self, ay):
        return ay - self.correction_ay
    def corriger_gx(self, gx):
        return gx - self.correction_gx


    def etalonner(self, ay,gx):
        self.collection_ay.ajouter(ay)
        self.correction_ay = mean(self.collection_ay.obtenir_valeurs())
        self.collection_gx.ajouter(gx)
        self.correction_gx = mean(self.collection_gx.obtenir_valeurs())

def main():
    def test():
        from ModuleInertiel import FauxModuleInertiel
        jeton = JetonAnnulation()
        imu = FauxModuleInertiel()
        temps = [0]
        nav = Navigation(imu, lambda: temps[0], jeton, None)
        lst_tests = []
        # Liste de tuples: EtatRobot, gx, ay, angle attendu, y attendu
        lst_tests.append((EtatRobot.IMMOBILE, 0.1, 0.1, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.1, 0.1, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.3, 0.3, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.3, 0.3, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.IMMOBILE, 0.2, 0.2, 0, 0))

        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 0))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.3, 0, 0.24516625))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.3, 0, 1.22583125))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.3, 0, 3.18716125))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.3, 0, 6.12915625))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 9.80665))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 13.72931))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 17.65197))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 21.57463))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.1, 0, 25.25212375))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.1, 0, 28.19411875))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.1, 0, 30.15544875))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.1, 0, 31.13611375))
        lst_tests.append((EtatRobot.TRANSLATION, 0.2, 0.2, 0, 31.38128))

        lst_tests.append((EtatRobot.TOURNER, 0.3, 0.2, 0.05, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.3, 0.2, 0.15, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.3, 0.2, 0.25, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.2, 0.2, 0.3,  31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.2, 0.2, 0.3,  31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.1, 0.2, 0.25, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.1, 0.2, 0.15, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.1, 0.2, 0.05, 31.38128))
        lst_tests.append((EtatRobot.TOURNER, 0.2, 0.2, 0,    31.38128))

        reussi = [True]

        def attendre():
            reussi[0] = reussi[0] and Algos.approx_egal(nav.angle, lst_tests[temps[0]][3]) and Algos.approx_egal(nav.y, lst_tests[temps[0]][4])
            temps[0] += 1
            if temps[0] < len(lst_tests):
                nav.assigner_etat(lst_tests[temps[0]][0])
                imu.ay = lst_tests[temps[0]][2]
                imu.gx = lst_tests[temps[0]][1]
            else: jeton.terminer()

        nav.attendre = attendre
        nav.demarrer()

        if reussi[0]:
            print("Test réussi")
        else:
            print("Test échoué")

    test()



if __name__ == "__main__":
    main()
