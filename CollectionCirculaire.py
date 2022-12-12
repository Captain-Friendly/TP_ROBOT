# Philippe C. Léger
# 2022-09-01
# Labo 1
# Classe CollectionCirculaire: Classe permettant d'accumuler un nombre x
# d'éléments. Lorsque la capacité est atteinte, le nouvel éléments écrase
# l'éléments le plus ancien.


class CollectionCirculaire:
    def __init__(self, capacité):
        self.__capacité = capacité
        self.__nombre_éléments = 0
        self.__éléments = []
        self.__index_prochain = 0
        self.__dernier_ajoute=None

    def ajouter(self, élément):
        self.__dernier_ajoute=élément
        if self.__nombre_éléments < self.__capacité:
            self.__éléments.append(élément)
            self.__nombre_éléments += 1
        else:
            self.__éléments[self.__index_prochain] = élément
        self.__index_prochain = (self.__index_prochain + 1) % self.__capacité

    def dernier_ajouté(self):
        return self.__dernier_ajoute

    def obtenir_valeurs(self):
        return self.__éléments

    def obtenir_valeurs_ordonnees(self):
        valeurs = []
        éléments = self.__éléments
        nb_elements = len(éléments)
        capacité = self.__capacité
        prochain = self.__index_prochain
        for i in range(nb_elements):
            valeurs.append(éléments[(i + prochain) % capacité])
        return valeurs

def main():
    from statistics import mean

    def test():
        CAPACITÉ = 5
        MAX = 16
        sommes = [1,3,6,10,15,20,25,30,35,40,45,50,55,60,65,70]
        moyennes = [1,1.5,2,2.5,3,4,5,6,7,8,9,10,11,12,13,14]
        minimums = [1,1,1,1,1,2,3,4,5,6,7,8,9,10,11,12]
        maximums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

        def sont_valeurs_valides(valeurs, indice):
            return sum(valeurs) == sommes[indice] and mean(valeurs) == moyennes[indice] and\
                 min(valeurs) == minimums[indice] and max(valeurs) == maximums[indice]

        valide = True
        col = CollectionCirculaire(CAPACITÉ)
        for i in range(MAX):
            col.ajouter(i + 1)
            valeurs = col.obtenir_valeurs()
            valide = valide and sont_valeurs_valides(valeurs, i)

        if valide:
            print("Test CollectionCirculaire: RÉUSSI")
        else:
            print("Test CollectionCirculaire: ÉCHOUÉ")
    def test_dernier():
        nombres=[1,2,3,4,5,6,7,8,9,0]
        col = CollectionCirculaire(4)
        for n in nombres:
            col.ajouter(n)
            print(n,n==col.dernier_ajouté())

    def test_obtenir_valeurs_ordonnees():
        col = CollectionCirculaire(5)
        for i in range(24):
            col.ajouter(i)

        for i in col.obtenir_valeurs_ordonnees():
            print(i)
    test()
    print("---------------------")
    test_dernier()
    print("---------------------")
    test_obtenir_valeurs_ordonnees()



if __name__ == "__main__":
    main()