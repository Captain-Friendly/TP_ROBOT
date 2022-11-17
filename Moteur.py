# Philippe C. Léger
# 2022-05-20
# PFI
# Classe Moteur: Classe permettant de contrôler un moteur du robot

# Modifications:
# Philippe C. Léger 2022-08-27:
# Ajout de la propriété __mode et de la méthode modifier_vitesse()
# Ajout de la class FauxMoteur



from Mode import Mode

class Moteur:
    def __init__(self, in1, in2, en, inverse = False):
        self.__in1 = in1
        self.__in2 = in2
        self.__en = en
        self.__inverse = inverse
        self.__mode = Mode.NEUTRE

    def avancer(self, valeur):
        self.__mode = Mode.AVANCER
        self.__bouger(not self.__inverse, valeur)


    def reculer(self, valeur):
        self.__mode = Mode.RECULER
        self.__bouger(self.__inverse, valeur)

    def __bouger(self, avancer, valeur):
        if (avancer):
            self.__in1.on()
            self.__in2.off()
        else:
            self.__in1.off()
            self.__in2.on()
        self.__en.value = valeur

    def freiner(self):
        self.__mode = Mode.FREINER
        self.__in1.on()
        self.__in2.on()
        self.__en.value = 1

    def neutre(self):
        self.__mode = Mode.NEUTRE
        self.__in1.off()
        self.__in2.off()
        self.__en.value = 0

    def construire(port_in1, port_in2, port_en, inverse = False):
        from gpiozero import PWMOutputDevice, OutputDevice
        in1 = OutputDevice(port_in1)
        in2 = OutputDevice(port_in2)
        en = PWMOutputDevice(port_en)
        return Moteur(in1, in2, en, inverse)

    def modifier_vitesse(self, nouvelle_vitesse):
        if self.__mode == Mode.AVANCER:
            self.avancer(nouvelle_vitesse)
        elif self.__mode == Mode.RECULER:
            self.reculer(nouvelle_vitesse)
        elif self.__mode == Mode.FREINER:
            self.freiner()
        else:
            self.neutre()


class FauxMoteur:
    def __init__(self, liste_sortie):
        self.__liste_sortie = liste_sortie

    def avancer(self, valeur):
        self.__liste_sortie.append(f'a{valeur}')

    def reculer(self, valeur):
        self.__liste_sortie.append(f'r{valeur}')

    def freiner(self):
        self.__liste_sortie.append('f')

    def neutre(self):
        self.__liste_sortie.append('n')

    def modifier_vitesse(self, nouvelle_vitesse):
        self.__liste_sortie.append(f'm{nouvelle_vitesse}')