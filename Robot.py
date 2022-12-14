# Philippe C. Léger
# 2022-08-25
# Labo 1
# Classe Robot: Classe représentant le robot

# 2022-11-14: Ajout de l'état du robot et retrait des rotations en avançant.

from EtatRobot import EtatRobot


class Robot:

    FACTEURTOURNERAVANCER = 0.2
    VITESSEDÉFAUT = 0.8
    VITESSEMAX = 1.0
    VITESSEMIN = 0.0
    INCRÉMENTVITESSE = 0.1

    def __init__(self, moteur_g, moteur_d, vitesse):
        self.__moteur_g = moteur_g
        self.__moteur_d = moteur_d
        self.__vitesse = vitesse
        self.__abonnes = []
        self.__etat = EtatRobot.IMMOBILE

    def obtenir_vitesse(self):
        return self.__vitesse

    def avancer(self):
        self.__etat = EtatRobot.TRANSLATION
        self.__signaler_changement_etat()
        self.__moteur_g.avancer(self.__vitesse)
        self.__moteur_d.avancer(self.__vitesse)

    def reculer(self):
        self.__etat = EtatRobot.TRANSLATION
        self.__signaler_changement_etat()
        self.__moteur_g.reculer(self.__vitesse)
        self.__moteur_d.reculer(self.__vitesse)

    def augmenter_vitesse(self):
        self.modifier_vitesse(min(Robot.VITESSEMAX, self.__vitesse + Robot.INCRÉMENTVITESSE))

    def réduire_vitesse(self):
        self.modifier_vitesse(max(Robot.VITESSEMIN, self.__vitesse - Robot.INCRÉMENTVITESSE))

    def modifier_vitesse(self, nouvelle_vitesse):
        self.__vitesse = nouvelle_vitesse
        self.__moteur_g.modifier_vitesse(nouvelle_vitesse)
        self.__moteur_d.modifier_vitesse(nouvelle_vitesse)

    def obtenir_vitesse(self):
        return self.__vitesse

    def tourner_g(self):
        self.__etat = EtatRobot.TOURNER
        self.__signaler_changement_etat()
        self.__moteur_g.reculer(self.__vitesse)
        self.__moteur_d.avancer(self.__vitesse)

    def tourner_d(self):
        self.__etat = EtatRobot.TOURNER
        self.__signaler_changement_etat()
        self.__moteur_g.avancer(self.__vitesse)
        self.__moteur_d.reculer(self.__vitesse)

    def freiner(self):
        self.__moteur_g.freiner()
        self.__moteur_d.freiner()
        self.__etat = EtatRobot.IMMOBILE
        self.__signaler_changement_etat()

    def détruire(self):
        self.__moteur_g.neutre()
        self.__moteur_d.neutre()
        self.__etat = EtatRobot.IMMOBILE
        self.__signaler_changement_etat()

    def construire():
        from Moteur import Moteur
        moteur_g = Moteur.construire(port_in1=6, port_in2=5, port_en=13)
        moteur_d = Moteur.construire(port_in1=15, port_in2=14, port_en=18)
        return Robot(moteur_g, moteur_d, Robot.VITESSEDÉFAUT)

    def abonner(self, assigner_etat):
        self.__abonnes.append(assigner_etat)
        assigner_etat(self.__etat)

    def __signaler_changement_etat(self):
        for assigner_etat in self.__abonnes:
            assigner_etat(self.__etat)




def test():
    from Moteur import FauxMoteur
    VITESSEDÉPARTDÉFAUT = 0.5
    def construire_robot_test(lst_sortie_g, lst_sortie_d, vitesse_départ = VITESSEDÉPARTDÉFAUT):
        from Moteur import FauxMoteur
        moteur_g = FauxMoteur(lst_sortie_g)
        moteur_d = FauxMoteur(lst_sortie_d)
        return Robot(moteur_g, moteur_d, vitesse_départ)

    def publier_test(nom_test, résultat):
        if résultat:
            print(f'{nom_test}: réussi')
        else:
            print(f'{nom_test}: échec')

    def test_vitesse_max():
        lst_g = []
        lst_d = []
        robot = construire_robot_test(lst_g, lst_d)
        for i in range(0, 10):
            robot.augmenter_vitesse()
        publier_test("Vitesse max", robot.obtenir_vitesse() == Robot.VITESSEMAX)

    def test_vitesse_min():
        lst_g = []
        lst_d = []
        robot = construire_robot_test(lst_g, lst_d)
        for i in range(0, 10):
            robot.réduire_vitesse()
        publier_test("Vitesse min", robot.obtenir_vitesse() == Robot.VITESSEMIN)

    def test_séquence():
        vitesse_plus = VITESSEDÉPARTDÉFAUT + Robot.INCRÉMENTVITESSE
        vitesse_tourner_avancer = VITESSEDÉPARTDÉFAUT * Robot.FACTEURTOURNERAVANCER

        lst_g = []
        lst_d = []
        lst_g_ref = []
        lst_d_ref = []

        robot = construire_robot_test(lst_g, lst_d)
        moteur_g_ref = FauxMoteur(lst_g_ref)
        moteur_d_ref = FauxMoteur(lst_d_ref)

        robot.avancer()
        moteur_g_ref.avancer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.avancer(VITESSEDÉPARTDÉFAUT)

        robot.reculer()
        moteur_g_ref.reculer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.reculer(VITESSEDÉPARTDÉFAUT)

        robot.freiner()
        moteur_g_ref.freiner()
        moteur_d_ref.freiner()

        robot.tourner_g()
        moteur_g_ref.reculer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.avancer(VITESSEDÉPARTDÉFAUT)

        robot.tourner_d()
        moteur_g_ref.avancer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.reculer(VITESSEDÉPARTDÉFAUT)

        robot.tourner_avancer_g()
        moteur_g_ref.avancer(vitesse_tourner_avancer)
        moteur_d_ref.avancer(VITESSEDÉPARTDÉFAUT)

        robot.tourner_avancer_d()
        moteur_g_ref.avancer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.avancer(vitesse_tourner_avancer)

        robot.augmenter_vitesse()
        moteur_g_ref.modifier_vitesse(vitesse_plus)
        moteur_d_ref.modifier_vitesse(vitesse_plus)

        robot.avancer()
        moteur_g_ref.avancer(vitesse_plus)
        moteur_d_ref.avancer(vitesse_plus)

        robot.réduire_vitesse()
        moteur_g_ref.modifier_vitesse(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.modifier_vitesse(VITESSEDÉPARTDÉFAUT)

        robot.avancer()
        moteur_g_ref.avancer(VITESSEDÉPARTDÉFAUT)
        moteur_d_ref.avancer(VITESSEDÉPARTDÉFAUT)

        robot.détruire()
        moteur_g_ref.neutre()
        moteur_d_ref.neutre()

        valide = True
        for i in range(0, len(lst_g_ref)):
            valide_loc = lst_g[i] == lst_g_ref[i] and lst_d[i] == lst_d_ref[i]
            valide = valide and valide_loc
            if not valide_loc:
                print(f'{i} - g:{lst_g[i]} vs {lst_g_ref[i]}; d:{lst_d[i]} vs {lst_d_ref[i]}')
        
        publier_test("Test séquence", valide)
    
    print("Test Robot.py")
    test_vitesse_max()
    test_vitesse_min()
    test_séquence()


    



if __name__ == "__main__":
    test()

