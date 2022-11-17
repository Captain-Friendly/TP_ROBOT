# Philippe C. Léger
# 2022-02-21
# Laboratoire 3 - Le GrovePi+
# Classe JetonAnnulation: Classe utilisée pour interrompre des fils
# d'exécition en boucle à partir de l'extérieur du fil.

class JetonAnnulation:

    def __init__(self):
        self.__continuer = True

    def continuer(self):
        return self.__continuer
    
    def terminer(self):
        self.__continuer = False