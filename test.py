from Robot import Robot
from time import sleep

def main():
    myRobot = Robot.construire()
    myRobot.avancer()
    sleep(1)
    myRobot.reculer()
    sleep(1)
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.augmenter_vitesse()
    myRobot.tourner_d()
    sleep(1)
    myRobot.tourner_g()
    sleep(1)
    myRobot.détruire()

        

if __name__ == "__main__":
    main()