# coding: UTF-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
# import pdb
# pdb.set_trace()

# Chargement du module tkinter
from tkinter import Tk, Frame, Button, Label, Event



class Case(Button):
    """
    Classe représentant une case de la grille de Sudoku.

    Héritage : Une case se configure comme une bouton.
    mais possède des attributs et des méthodes supplémentaires.

    attributs:
    ---------
    contenu : Une case non vide a un `contenu`, le symbole qui est affiché
    quand on tape le nom de la case dans l'interpréteur.

    pretendants : Une case vide à des prétendants (valeurs possibles de la
    case).

    index_cousines : Une case a des cases cousines qui sont soit dans la même
    ligne, soit dans la même colonne soit dans le même carré (3 x 3). Une case
    conserve les index de ses cousines.

    exemple :
    -------
    >>> root = Tk()
    >>> index_cousines = list()
    >>> ma_case = Case(root, index_cousines, text="une case")
    >>> ma_case.pack()
    >>> ma_case.pretendants
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> ma_case
    0
    """

    def __init__(self, master, index_cousines, *args, **kwargs):
        """
        Construit un widget case avec comme cadre MASTER.
        """
        super().__init__(master, *args, **kwargs) # ce qui relève de la classe Button
        self.contenu = None
        self.pretendants = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.index_cousines = index_cousines

    def __repr__(self):
        """
        Affichage d'une case dans l'interpréteur.

        Lorsque l'on tape son nom dans l'interpréteur
        son `contenu` est affiché.
        """
        if self.contenu is None:
            return "0"    # la case est vide "⛶"
        else:
            return self.contenu


class Grille:
    """
    Classe représentant une grille de 9 x 9 cases.

    Chacune des 81 cases est accessible via un index allant de 0 à 80.

    Les cases sont des widgets tkinter. Il faut donc donner un cadre à la grille.


    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_grille = Grille(mon_cadre)
    >>> ma_case = ma_grille.get_case(0) # ou ma_case = ma_grille[0]
    >>> ma_case.pretendants
    [1, 2, 3, 4, 5, 6, 7, 8, 9]


    print(ma_grille)            # affiche la grille 9 x 9 cases
    print(ma_grille[0]) # affiche la première case (son index est 0)
    """

    LARGEUR_BLOC = 3
    LARGEUR_GRILLE = LARGEUR_BLOC * LARGEUR_BLOC
    NBR_CASES = LARGEUR_GRILLE * LARGEUR_GRILLE
    COULEUR_BLOCS_PAIRS = 'LightSteelBlue1'
    COULEUR_BLOCS_IMPAIRS = 'LightSteelBlue2'

    def __init__(self, cadre):
        self.cadre = cadre

        # Disposition du conteneur cadre qui contient la grille de sudoku
        for row in range(self.LARGEUR_GRILLE):
            cadre.rowconfigure(row, weight=1)
        for column in range(self.LARGEUR_GRILLE):
            cadre.columnconfigure(column, weight=1)
        # Affichage de la grille de sudoku
        index = 0
        for j in range(self.LARGEUR_GRILLE):
            for i in range(self.LARGEUR_GRILLE):
                Case(cadre,
                     self.get_index_cousines(index),
                     name='{}'.format(index),
                     text='{}'.format(index),
                     background= self.couleur_bloc(index)).grid(row=j, column=i, sticky="nsew")
                index += 1
    
    def couleur_bloc(self, index):
        """
        Retourne la couleur à donner à la case de la grille.
        """
        if self.get_bloc(index) % 2:
            return self.COULEUR_BLOCS_PAIRS
        else:
            return self.COULEUR_BLOCS_IMPAIRS
               
    def get_case(self, index):
        """
        Retourne la case d'index donné.

        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> grille_sudoku = Grille(mon_cadre)
        >>> print(grille_sudoku.get_case(15).index_cousines)
        >>> print(grille_sudoku.get_case(15).contenu)
        >>> print(grille_sudoku.get_case(15).pretendants)
        """
        return root.nametowidget(str(self.cadre)+"."+str(index))

    def get_index_cousines(self, index):
        """
        Retourne une liste avec les index des 27 cases qui sont soit dans la
        même ligne, soit dans la même colonne, soit dans le même bloc
        carré 3x3 que la case d'index donné.
        """
        cousines = list()
        cousines.extend(self.get_index_cousines_en_ligne(index))
        cousines.extend(self.get_index_cousines_en_colonne(index))
        cousines.extend(self.get_index_cousines_en_bloc(index))
        return cousines

    def get_index_cousines_en_bloc(self, index):
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

    def get_index_cousines_en_colonne(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans la même
        colonne que la case d'index donné.
        """
        return [i for i in range(self.get_colonne(index),
                                 self.NBR_CASES, self.LARGEUR_GRILLE)]

    def get_index_cousines_en_ligne(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans la même
        ligne que la case d'index donné.
        """
        return [i for i in range(
            self.LARGEUR_GRILLE * self.get_ligne(index),
            self.LARGEUR_GRILLE * self.get_ligne(index) + self.LARGEUR_GRILLE)]

    def __getitem__(self, index):
        """
        Permet d'obtenir le symbole d'une case de la grille  avec ma_grille[index] 
        où index est compris entre 0 et NBR_CASES-1.
        """
        return self.get_case(index).__repr__()

    def __setitem__(self, index, symbole):
        """
        Permet d'écrire un symbole dans le contenu d'une case de la grille.

        Le symbole doit être de type str.
        exemple:
        -------
        ma_grille[0] = '5'
        """
        if not(isinstance(symbole,str)):
            raise TypeError()
        if index < self.NBR_CASES:
            self.get_case(index).contenu = symbole
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
        for index in range(self.NBR_CASES): 
            une_case = self.get_case(index)
            if une_case.contenu is None:
                affichage += '0'
            else:
                affichage += une_case.contenu  # ajout de l'affichage d'une case
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

    def essaye_remplir_case_avec(self, index, valeur):
        """
        Rempli la case d'index compris entre 0 et 80 avec `valeur`.
        """
        if (self.get_autorisation_ecriture(index)):
            self.__setitem__(index, valeur)
            self.reduire_pretendants
            self.reduire_sac
            return True
        else:
            return False

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
            self.essaye_remplir_case_avec(cousine, "*")

            
class Sac(Button):
    """
    Classe représentant un sac. Un sac contient des symboles identiques.

    Attributs:
    ---------
    symbole : symbole placé dans le sacs
    cardinal : nombre de symboles que le sac contient

    Une case se configure comme une bouton.

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> mon_sac = Sac(mon_cadre,'5')
    >>> mon_sac
    contient 9 chiffres 5
    """
    def __init__(self, master, symbole, *args, **kwargs):
        """
        Construit un widget 'sac' avec comme cadre MASTER

        contenant 9 symboles identiques
        """
        super().__init__(master, *args, **kwargs) # ce qui relève de la classe Button
        self.symbole = symbole
        self.cardinal = 9  # nombre d'éléments dans le sac

    def __repr__(self):
        """
        Représentation officielle d'un sac lorsque l'on tape son nom dans
        l'interpréteur.

        Le contenu du sac est renvoyé.

        exemple:
        -------
        contient 9 chiffres 5

        """
        if self.cardinal == 0:
            return "sac vide"
        elif self.cardinal == 1:
            return "contient 1 chiffre {}".format(self.symbole)
        else:
            return "contient {} chiffres {}".format(self.cardinal,
                                                    self.symbole)


class Pioche:
    """
    Classe représentant 9 sacs contenant chacun des symboles identiques tous 
    différents (1 sac avec que des "1", un autre avec que des "2", etc.)

    À l'initialisation de la grille, un certain nombre de ces symboles est
    prélevé pour les placer sur la grille.
    Au cours du jeu, tant qu'il reste des symboles dans un sac, le joueur peut
    en piocher pour les placer sur la grille.

    Les sacs sont des widgets tkinter. Il faut donc donner un cadre à la pioche.

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_pioche = Pioche(mon_cadre) # affiche les neuf boutons tkinter de la pioche
    >>> ma_pioche.NBR_SACS
    9
    >>> ma_pioche.get_sac(3)
    contient 9 chiffres 3
    >>> ma_pioche[3]
    contient 9 chiffres 3
    >>> print(ma_pioche[1])      # affiche le contenu du premier sac de pioche
    """

    NBR_SACS = 9

    def __init__(self, cadre):
        """
        Initialisation d'une liste contenant 9 sacs
        chaque sac contenant chacun 9 symboles identiques
        """
        self.cadre = cadre
    
        # Disposition du conteneur cadre qui contient la pioche
        for column in range(1, self.NBR_SACS+1):
            cadre.columnconfigure(column, weight=1)
        for index in range(1, self.NBR_SACS+1):
            Sac(cadre,
                index,
                name='{}'.format(index),
                text='{}'.format(index)).grid(row=0, column=index, sticky="nsew")
            Label(cadre,
                  name='lbl{}'.format(index),
                  text='{}'.format(self[index].cardinal)).grid(row=1, column=index, sticky="nsew")

    def __iter__(self):
        """
        Rends la pioche itérable.
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> i = iter(ma_pioche)
        >>> next(i)
        contient 9 chiffres 1
        >>> next(i)
        contient 9 chiffres 2
        """
        self.n = 1
        return self

    def __next__(self):
        """
        Fonction d'itération
        """
        if self.n <= self.NBR_SACS:
            self.n += 1
            return self.get_sac(self.n-1)
        else:
            raise StopIteration

    def get_sac(self, index):
        """
        Retourne le sac d'index donné.

        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> ma_pioche = Pioche(mon_cadre)
        >>> ma_pioche.get_sac(1)
        contient 9 chiffres 1
        >>> print(pioche_sudoku.get_sac(5))

        """
        return root.nametowidget(str(self.cadre)+"."+str(index))

        
    def __getitem__(self, index):
        """
        Permet d'obtenir le contenu d'un sac dans la pioche avec:
        ma_pioche[index] # où index est compris entre 1 et NBR_SACS.


        exemple:
        -------
        >>> for i in range(1,10):
        ...     ma_pioche[i]
        ... 
        contient 9 chiffres 1
        contient 9 chiffres 2
        contient 9 chiffres 3
        contient 9 chiffres 4
        contient 9 chiffres 5
        contient 9 chiffres 6
        contient 9 chiffres 7
        contient 9 chiffres 8
        contient 9 chiffres 9

        """
        return self.get_sac(index)        

    def __repr__(self):
        """
        Représentation de la pioche
        
        quand on tape son nom dans l'interpréteur.
        """
        for index in range(1,self.NBR_SACS):
            print(self.__getitem__(index))


def gestion_des_evenements(event):
    """
    Identifie l'élément cliqué par le joueur.
    """
    print(event.widget)
    if type(event.widget) == Case:
        print(event.widget.index_cousines)

            
root = Tk()
root.title('Sudoku')
root.bind("<Button-1>", gestion_des_evenements)

# création des conteneurs principaux
cadre_haut = Frame(root, name='en_tete', bg='lavender', width=640, height=50)
cadre_gauche = Frame(root, name='gauche', bg='lavender', height=400)
cadre_central = Frame(root, name='grille_sudoku', bg='white')
cadre_droite = Frame(root, name='droite', bg='lavender')
cadre_separation_verticale = Frame(root, name='separation', bg='lavender', height=20)
cadre_pioche = Frame(root, name='pioche', bg='white', height=120)
cadre_bas = Frame(root, name='pied_de_page', bg='lavender', height=60)

# Disposition des conteneurs principaux
cadre_haut.grid(row=0, columnspan=3,  sticky="nsew")
cadre_gauche.grid(row=1, column=0, sticky="nsew")
cadre_central.grid(row=1, column=1,  sticky="nsew")
cadre_droite.grid(row=1, column=2,  sticky="nsew")
cadre_separation_verticale.grid(row=2, columnspan=3,  sticky="nsew")
cadre_pioche.grid(row=3, columnspan=3, sticky="nsew")
cadre_bas.grid(row=4, columnspan=3, sticky="nsew")

root.grid_rowconfigure(1, weight=1)     # la ligne qui contient la grille sudoku est prioritaire.
root.grid_columnconfigure(0, weight=1)  # cadre_gauche cadre_central
root.grid_columnconfigure(1, weight=1)  # et cadre_droite se partagent
root.grid_columnconfigure(2, weight=1)  # l'espace horizontal à égalité

grille_sudoku = Grille(cadre_central)
pioche_sudoku = Pioche(cadre_pioche)

# Disposition du conteneur cadre_bas
cadre_bas.columnconfigure(0, weight=1)

# Création du bouton quitter dans cadre_bas
bouton_quitter = Button(cadre_bas, text='Quitter', command=root.quit)

# Disposition du bouton quitter
bouton_quitter.grid(sticky="nsew")

root.mainloop()
root.destroy()
