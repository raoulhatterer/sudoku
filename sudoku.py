# coding: utf-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
# import pdb
# pdb.set_trace()

# Chargement du module tkinter
from tkinter import Tk, Frame, Button


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
        self.contenu = [sac(numero) for numero in range(1, self.NBR_SACS+1)]

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
    """
    LARGEUR_BLOC = 3
    LARGEUR_GRILLE = LARGEUR_BLOC * LARGEUR_BLOC
    NBR_CASES = LARGEUR_GRILLE * LARGEUR_GRILLE

    def __init__(self):
        liste_cases = list()
        for index in range(self.NBR_CASES):
            une_case = case()
            une_case.cousines = self.get_cousines(index)
            liste_cases.append(une_case)
        self.contenu = liste_cases

    def get_cousines(self, index):
        """
        Retourne une liste avec les index des 27 cases qui sont soit dans la
        même ligne, soit dans la même colonne, soit dans le même bloc
        carré 3x3 que la case d'index donné.
        """
        cousines = list()
        cousines.extend(self.get_cousines_en_ligne(index))
        cousines.extend(self.get_cousines_en_colonne(index))
        cousines.extend(self.get_cousines_en_bloc(index))
        return cousines

    def get_cousines_en_bloc(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans le même
        bloc carré 3x3 que la case d'index donné.
        """
        cousines_en_bloc = list()
        if self.get_bloc(index) < 3:                    # 3 premiers blocs
            premiere_triplette = [i for i in range(
                self.get_bloc(index)*3, self.get_bloc(index)*3+3)]
        elif self.get_bloc(index) < 6:                  # 3 blocs suivants
            premiere_triplette = [i for i in range(
                18+self.get_bloc(index)*3, 21+self.get_bloc(index)*3)]
        else:                                          # 3 derniers blocs
            premiere_triplette = [i for i in range(
                36+self.get_bloc(index)*3, 39+self.get_bloc(index)*3)]
        for i in range(3):
            cousines_en_bloc.extend(list(map(lambda x: x+9*i,
                                             premiere_triplette)))
        return cousines_en_bloc

    def get_cousines_en_colonne(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans la même
        colonne que la case d'index donné.
        """
        return [i for i in range(self.get_colonne(index),
                                 self.NBR_CASES, self.LARGEUR_GRILLE)]

    def get_cousines_en_ligne(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans la même
        ligne que la case d'index donné.
        """
        return [i for i in range(
            self.LARGEUR_GRILLE * self.get_ligne(index),
            self.LARGEUR_GRILLE * self.get_ligne(index) + self.LARGEUR_GRILLE)]

    def __getitem__(self, index):
        """
        Permet d'obtenir le symbole d'une case de la grille avec:
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
        if (self.get_autorisation_ecriture(index)):
            self.__setitem__(index, valeur)
            self.reduire_pretendants
            self.reduire_sac

    def get_autorisation_ecriture(self, index):
        return self.get_autorisation_colonne(index)\
            and self.get_autorisation_ligne(index)\
            and self.get_autorisation_bloc(index)

    def get_autorisation_colonne(self, index):
        return True

    def get_autorisation_ligne(self, index):
        return True

    def get_autorisation_bloc(self, index):
        return True

    def reduire_pretendants(self, index):
        pass

    def reduire_sac(self, index):
        pass

    def get_colonne(self, index):
        """
        Retourne le numéro de colonne de la case d'index compris entre 0 et 80.

        Les 9 colonnes sont numérotées de 0 à 8.
        """
        return index % 9

    def get_ligne(self, index):
        """
        Retourne le numéro de ligne de la case d'index compris entre 0 et 80.

        Les 9 lignes sont numérotées de 0 à 8.
        """
        return index//9

    def get_bloc(self, index):
        """
        Retourne le numéro du bloc 3 x 3 auquel appartient la case d'index
        compris entre 0 et 80.

        Il y a 9 blocs 3 x 3 d'index compris entre 0 et 8.
        """
        return self.get_colonne(index)//3 + (self.get_ligne(index)//3)*3

    def marquer_cousines(self, index):
        """
        Montre les cases cousines de la case d'index donné.
        Attention cette méthode est destructive.

        exemple:
        -------
        grille_test = grille()
        grille_test.marquer_cousines(50)
        print(grille_test)
        """
        for cousine in self.contenu[index].cousines:
            self.remplir_case_avec(cousine, "*")


root = Tk()
root.title('grid test')

# création des conteneurs principaux
haut_frame = Frame(root, name='en_tete', bg='cyan', width=640, height=50)
gauche_frame = Frame(root, name='gauche', bg='blue', height=400)
centre_frame = Frame(root, name='grille_sudoku', bg='white')
droite_frame = Frame(root, name='droite', bg='red')
bas_frame = Frame(root, name='pied_de_page', bg='lavender', height=60)


# Disposition des conteneurs principaux

haut_frame.grid(row=0, columnspan=3,  sticky="nsew")
gauche_frame.grid(row=1, column=0, sticky="nsew")
centre_frame.grid(row=1, column=1,  sticky="nsew")
droite_frame.grid(row=1, column=2,  sticky="nsew")
bas_frame.grid(row=2, columnspan=3, sticky="nsew")

root.grid_rowconfigure(1, weight=1)     # la ligne centrale est prioritaire.
root.grid_columnconfigure(0, weight=1)  # gauche_frame centre_frame
root.grid_columnconfigure(1, weight=1)  # et droite_frame se partagent
root.grid_columnconfigure(2, weight=1)  # l'espace horizontal à égalité

# Disposition du conteneur centre_frame qui contient la grille de sudoku
for row in range(9):
    centre_frame.rowconfigure(row, weight=1)

for column in range(9):
    centre_frame.columnconfigure(column, weight=1)


# Création et disposition des 81 boutons faisant office de case de la grille
# de Sudoku dans centre_frame.
index = 0
for j in range(9):
    for i in range(9):
        Button(centre_frame,
               name='{}'.format(index),
               text='{}'.format(index)).grid(row=j, column=i, sticky="nsew")
        index += 1


# Disposition du conteneur bas_frame
bas_frame.columnconfigure(0, weight=1)

# Création du bouton quitter dans bas_frame
bouton_quitter = Button(bas_frame, text='Quitter', command=root.quit)

# Disposition du bouton quitter
bouton_quitter.grid(sticky="nsew")

root.mainloop()
root.destroy()
