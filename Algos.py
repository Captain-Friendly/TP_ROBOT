# Pascal Arès & Philippe C. Léger
# 2022-08-25
# Labo 2
# Classe Algos : Classe contenant divers services.

# Modifications:
# Philippe C. Léger 2022-09-19: 
# Ajout de la fonction sommer_resultat_f

import math


class Algos:
    def afficher_test(nom_test, résultat):
        if résultat:
            print(f"{nom_test}: RÉUSSI")
        else:
            print(f"{nom_test}: ÉCHOUÉ")

    def correction_erreur(liste:list):
        somme=sum(liste)
        if(len(liste)>=3):
            minimum=min(liste)
            maximum=max(liste)
            return (somme-minimum-maximum)/(len(liste)-2)
        else:
            return somme/len(liste)

    # Fonction permettant de calculer la somme des extrants de f
    # sur les éléments de lst.
    def sommer_resultat_f(lst, f):
        somme = 0
        for o in lst:
            somme += f(o)
        return somme

    def obtenir_element_max(lst, obtenir_valeur):
        valeur_max = -math.inf
        element_max = None
        for e in lst:
            valeur = obtenir_valeur(e)
            if obtenir_valeur(e) > valeur_max:
                element_max = e
                valeur_max = valeur
        return element_max

    def construire_thread_arret(jeton):
        from threading import Thread
        def action():
            input("Appuyez sur [Entrer] pour terminer...")
            jeton.terminer()
        return Thread(target=action)

    def construire_fil(action):
        return 

    def integrer_trapeze(x0, dx0, dx1, dy):
        return x0 + dy * (dx0 + dx1) / 2

    def approx_egal(a, b, tol=0.00001):
        return abs(a - b) < tol
    
    #               (  x  ,   y  )
    # 25cm, 315° == (17.67, 17.67)
    # 25cm, 45° == (-17.67, 17.67)

    def TrouverPosition(angle, distance):
        """Transforme l'angle et la distance en position x,y\n
         x = distance * cos(angle) \n
         y = distance * sin(angle)"""
        x = ( distance * math.cos(math.radians(angle))) 
        y = distance * math.sin(math.radians(angle))
        return x,y
        
    def EstDansAire(minX, maxX, minY, maxY, x,y):
        """Determine si un point x,y est à l'interieur d'une aire rectangulaire\n
           à l'aide des x,y maximums et minimums"""
        if x < minX or x > maxX:
            return False
        if y < minY or y > maxY:
            return False

        return True

        # -250, 0
    

def main():
    pass

if __name__ == "__main__":
    main()
    
    
