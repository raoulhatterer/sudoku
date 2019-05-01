# coding: utf-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
# import pdb
# pdb.set_trace()


class sac:
    """
    Classe représentant un sac. Un sac contient des symboles identiques.

    Attributs:
    ---------
    symbole : symbole placé dans le sacs
    cardinal : nombre de symboles que le sac contient
    """
    def __init__(self, symbole):
        """
        Constructeur de sac contenant 9 symboles identiques
        """
        self.symbole = symbole
        self.cardinal = 9  # nombre d'éléments dans le sac

    def __repr__(self):
        """
        Représentation officielle d'un sac lorsque l'on tape son nom dans
        l'interpréteur.

        Le contenu du sac est renvoyé.
        """
        if self.cardinal == 0:
            return "sac vide"
        elif self.cardinal == 1:
            return "contient 1 chiffre {}".format(self.symbole)
        else:
            return "contient {} chiffres {}".format(self.cardinal,
                                                    self.symbole)


class pioche():
    """
    Classe représentant 9 sacs contenant chacun des symboles identiques
    tous différents (1 sac avec que des "1", un autre avec que des "2", etc.)

    À l'initialisation de la grille, un certain nombre de ces symboles est
    prélevé pour les placer sur la grille.
    Au cours du jeu, tant qu'il reste des symboles dans un sac, le joueur peut
    en piocher pour les placer sur la grille.

    exemple:
    -------
    ma_pioche = pioche()
    print(ma_pioche)         # affiche la pioche (contenu des 9 sacs de pioche)
    print(ma_pioche.contenu) # affiche la pioche sous forme de liste
    print(ma_pioche[1])      # affiche le contenu du premier sac de pioche


    """
    NBR_SACS = 9

    def __init__(self):
        """
        Initialisation d'une liste contenant 9 sacs

        chaque sac contenant chacun 9 symboles identiques
        """
        self.contenu = [sac(numéro) for numéro in range(1, self.NBR_SACS+1)]

    def __getitem__(self, index):
        """
        Permet d'obtenir le contenu d'un sac dans la pioche avec:
        ma_pioche[index] # où index est compris entre 1 et NBR_SACS.
        """
        return self.contenu[index-1]

    def __setitem__(self, index, sac):
        """
        Permet d'écrire un sac dans la pioche.

        exemple:
        -------
        ma_pioche[9] = sac(9)
        """
        if index < self.NBR_SACS+1:
            self.contenu[index-1] = sac
        else:
            raise IndexError()

    def __len__(self):
        return self.NBR_SACS

    def __repr__(self):
        """
        Représentation de la pioche.

        Le contenu des 9 sacs est renvoyé.
        """
        affichage = ""
        for sac in self.contenu:
            affichage += sac.__repr__() + "\n"
        return affichage


class case:
    """
    Classe représentant une case.

    Une case non vide a un `contenu`, le symbole qui est affiché quand on tape
    le nom de la case dans l'interpréteur.
    Une case vide à des prétendants (valeurs possibles de la case).
    Une case a des cases cousines qui sont soit dans la même ligne, soit dans
    la même colonne soit dans le même carré (3 x 3).

    exemple:
    -------
    ma_case = case()
    print(ma_case)
    """
    def __init__(self):
        self.contenu = None
        self.pretendants = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.cousines = None

    def __repr__(self):
        """
        Affichage d'une case.

        Lorsque l'on tape son nom dans l'interpréteur
        son `contenu` est affiché.
        """
        if self.contenu is None:
            return "0"    # "⛶"
        else:
            return "{}".format(self.contenu)

class grille:
    """
    Classe représentant une grille de 9 x 9 cases.

    Chacune des 81 cases est accessible via un index allant de 0 à 80.

    exemple:
    -------
    ma_grille = grille()
    print(ma_grille)            # affiche la grille 9 x 9 cases
    print(ma_grille.contenu)    # affiche la grille sous forme de liste
    print(ma_grille[0]) # affiche la première case (son index est 0)

    options:
    -------
    Affichage en couleur (fonctionne uniquement dans le Terminal pas dans la
    console Python): ma_grille.affichage_en_couleur = True
    """

    COTÉ = 9
    NBR_CASES = COTÉ * COTÉ

    def __init__(self):
        liste_cases = list()
        for index in range(self.NBR_CASES):
            une_case = case()
            cousines_en_ligne = [i for i in range(
                self.COTÉ*self.getligne(index),
                self.COTÉ*self.getligne(index)+self.COTÉ)]
            une_case.cousines = cousines_en_ligne
            cousines_en_colonne = [i for i in range(self.getcolonne(index),
                                                    self.NBR_CASES, self.COTÉ)]
            une_case.cousines.extend(cousines_en_colonne)
            cousines_en_bloc = list()
            if self.getbloc(index) < 3:
                première_triplette = [i for i in range(
                    self.getbloc(index)*3, self.getbloc(index)*3+3)]
            elif self.getbloc(index) < 6:
                première_triplette = [i for i in range(
                    18+self.getbloc(index)*3, 21+self.getbloc(index)*3)]
            else:
                première_triplette = [i for i in range(
                    36+self.getbloc(index)*3, 39+self.getbloc(index)*3)]
            for i in range(3):
                cousines_en_bloc.extend(list(map(lambda x: x+9*i,
                                                 première_triplette)))
            une_case.cousines.extend(cousines_en_bloc)
            liste_cases.append(une_case)
        self.contenu = liste_cases

    def __getitem__(self, index):
        """
        Permet d'obtenir le contenu d'une case de la grille avec:
        ma_grille[index] # où index est compris entre 0 et NBR_CASES-1.
        """
        return self.contenu[index]

    def __setitem__(self, index, symbole):
        """
        Permet d'écrire dans le contenu d'une case de la grille.

        exemple:
        -------
        ma_grille[0] = 5
        """
        if index < self.NBR_CASES:
            self.contenu[index].contenu = symbole
        else:
            raise IndexError()

    def __len__(self):
        return self.NBR_CASES

    def __repr__(self):
        """
        Affichage d'une grille.

        Lorsque l'on tape son nom dans l'interpréteur
        son `contenu` est affiché sous forme d'une grille 9 x 9.
        """
        affichage = ""
        index = 0
        for une_case in self.contenu:
            affichage += une_case.__repr__()  # ajout de l'affichage d'une case
            if index % 27 == 26 and index < 80:
                affichage += "\n\n"  # à faire toutes les 3 lignes
            elif index % 9 == 8:
                affichage += "\n"  # sinon à faire toutes les lignes
            elif index % 3 == 2:
                affichage += "  "   # sinon à faire toutes les 3 colonnes
            elif index % 9 in [0, 1, 3, 4, 6, 7]:
                affichage += " "

            index += 1
        return affichage

    def remplir_case_avec(self, index, valeur):
        """
        Rempli la case d'index compris entre 0 et 80 avec `valeur`.
        """
        if (self.écriture_autorisée(index)):
            self.__setitem__(index, valeur)
            self.réduire_prétendants
            self.réduire_sac

    def écriture_autorisée(self, index):
        return self.autorisation_colonne(index)\
            and self.autorisation_ligne(index)\
            and self.autorisation_carré(index)

    def autorisation_colonne(self, index):
        return True

    def autorisation_ligne(self, index):
        return True

    def autorisation_carré(self, index):
        return True

    def réduire_prétendants(self, index):
        pass

    def réduire_sac(self, index):
        pass

    def getcolonne(self, index):
        """
        Retourne le numéro de colonne de la case d'index compris entre 0 et 80.

        Les 9 colonnes sont numérotées de 0 à 8.
        """
        return index % 9

    def getligne(self, index):
        """
        Retourne le numéro de ligne de la case d'index compris entre 0 et 80.

        Les 9 lignes sont numérotées de 0 à 8.
        """
        return index//9

    def getbloc(self, index):
        """
        Retourne le numéro du bloc 3 x 3 auquel appartient la case d'index
        compris entre 0 et 80.

        Il y a 9 blocs 3 x 3 d'index compris entre 0 et 8.
        """
        return self.getcolonne(index)//3 + (self.getligne(index)//3)*3

    def marquer_cousines(self, index):
        """
        Montre les cases cousines de la case d'index donné.
        """
        for cousine in self.contenu[index].cousines:
            self.remplir_case_avec(cousine, "*")


if __name__ == '__main__':
    # emacs: you will need to use a prefix argument (i.e. C-u C-c C-c)
    # to run the following:
    print("Jeu en développement (pas encore fonctionnel).")

    for i in range(80):
        grille_sudoku = grille()
        grille_sudoku.marquer_cousines(i)
        print("Cases cousines de", i)
        print(grille_sudoku)
