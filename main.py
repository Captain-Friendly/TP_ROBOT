# Pascal Arès & Philippe C. Léger
# 2022-11-03
# Labo 6
# Point d'entrée de l'application pour le labo 6

from threading import Thread
from time import perf_counter, sleep
from ModuleInertiel import ModuleInertiel
from Navigation import Navigation
from icm20948 import ICM20948
from JetonAnnulation import JetonAnnulation
from Robot import Robot

def construire_fil_robot(jeton, robot) -> Thread:
    from LecteurClavier import LecteurClavier
    from DirecteurClavier import DirecteurClavier
    
    lecteur = LecteurClavier()
    directeur = DirecteurClavier(lecteur, robot, jeton)
    return Thread(target=directeur.activer)

def main():
    jeton = JetonAnnulation()   
    robot = Robot.construire()

    t = construire_fil_robot(jeton, robot)
    t.start()
    imu = ICM20948()
    module_inertiel = ModuleInertiel(imu)
    navigation = Navigation(module_inertiel, perf_counter, jeton, lambda: sleep(Navigation.SCRUTATION))
    i = [0]
    def callback():
        ERREUR_MANUELLE=25/24
        i[0] += 1
        if i[0] % 2 == 0:
            print(f"ANGLE: {(navigation.angle* ERREUR_MANUELLE):.2f}, Y: {(navigation.y):.2f}")

    navigation.abonner(callback) 
        

    robot.abonner(lambda etat: navigation.assigner_etat(etat))
    navigation.demarrer()
    t.join()

    

if __name__ == "__main__":
    main()