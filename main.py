# Pascal Arès, Philippe C. Léger & Julian Angel Murillo
# 2022-12-19
# PFI - Le robot autonome
# Fichier main: Fichier d'exécution principal du programme.


from Robot import Robot
from DirecteurRotation import DirecteurRotation
from JetonAnnulation import JetonAnnulation
from Point import Point
from GPS import GPS
from time import sleep
from Algos import Algos
from Lidar import Lidar
from DirecteurIA import DirecteurIA
from DetecteurMouvement import DetecteurMouvement
import cv2


def obtenir_position_depart(gps:GPS):
    depart = gps.obtenir_position()
    while depart is None:
        depart = gps.obtenir_position()
        print(depart)
    return depart

def obtenir_points_carre(gps:GPS):
    depart = obtenir_position_depart(gps)
    print(f"position de départ: {depart.to_string()}")
    points = []
    points.append(Point.additionner(depart, Point(0, 2)))
    points.append(Point.additionner(depart, Point(2, 2)))
    points.append(Point.additionner(depart, Point(2, 0)))
    points.append(Point.additionner(depart, Point(0, 0)))
    return points

def obtenir_points_X(gps:GPS):
    points_carre = obtenir_points_carre(gps)
    points_x = []
    points_x.append(points_carre[0])
    points_x.append(points_carre[2])
    points_x.append(points_carre[1])
    points_x.append(points_carre[3])
    return points_x

def obtenir_points_L(gps:GPS):
    points_carre = obtenir_points_carre(gps)
    points_L = []
    points_L.append(points_carre[0])
    points_L.append(points_carre[1])
    points_L.append(points_carre[0])
    points_L.append(points_carre[3])
    return points_L

def detecter_mouvement():
    jeton =  JetonAnnulation()
    detecteur_mouvement = DetecteurMouvement(jeton)
    detecteur_mouvement.lancer_detection_mouvement(jeton)
    # detecteur_mouvement.commencer(jeton)
    # cv2.waitKey()
    # detecteur_mouvement.finir()


def main():
    jeton = JetonAnnulation()
    robot = Robot.construire()
    gps = GPS(jeton)
    # gps.demarrer()
    directeur_rotation = DirecteurRotation.construire(jeton, robot)
    detecteur_mouvement = DetecteurMouvement(JetonAnnulation())
    
    directeur = DirecteurIA(jeton, robot, directeur_rotation, gps)
    directeur.demarrer()

    # se deplace de m vers la gauche

    destinations = obtenir_points_L(gps)
    # gps.terminer()
    # print("succes")
    # return
    for destination in destinations:
        if jeton.continuer(): 
            print(f"destination:{destination.to_string()}")
            directeur.assigner_destination(destination)
            detecter_mouvement()
    directeur.terminer()
    robot.détruire()

if __name__ == "__main__":
    main()