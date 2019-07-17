# coding: UTF-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
import pdb
# pdb.set_trace()

# Chargement du module tkinter
from tkinter import Tk, Frame, Button, Label
from random import shuffle, choice
from tkinter import ttk
from tkinter.constants import *

# import sys
# sys.setrecursionlimit(6000)


# CLASSES

class Case(Button):
    """
    Classe représentant une case de la grille de Sudoku.

    Héritage : Une case se configure comme une bouton.
    mais possède des attributs et des méthodes supplémentaires.

    attributs:
    ---------
    index : Chaque case a un index compris entre 0 et 80 qui indique
    sa position dans la grille.

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
    >>> ma_case = Case(root, 0, index_cousines, text="une case")
    >>> ma_case.pack()
    >>> ma_case.pretendants
    ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> ma_case
    0
    """

    def __init__(self, cadre, index, index_cousines, *args, **kwargs):
        """
        Construit un widget 'case'

        avec comme paramètres:
        CADRE : le cadre de destination (transmis à la classe Button
        grâce à *args)
        INDEX : la position dans la grille  (un nombre entier compris
        entre 0 et 80)
        INDEX_COUSINES : la liste des index des cases cousines (cases de même
        ligne, colonne ou carré 3x3)
         *ARGS : arguments simples destinés à la classe Button
        **KWARGS : arguments de type clé='valeur' transmis à la classe Button
        """
        super().__init__(cadre, *args, **kwargs)  # ce qui relève de la classe Button
        self.index = index
        self.contenu = None
        self.pretendants = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.index_cousines = index_cousines

    def __repr__(self):
        """
        Permet l'affichage fainéant d'une case dans l'interpréteur.

        Lorsque l'on tape le nom d'une case dans l'interpréteur python
        son `contenu` est affiché. À ceci près, que si son contenu est vide,
        un zéro est affiché.

        Remarque : la classe Grille a recours à l'affichage fainéant des cases
        pour afficher joliment (sous forme de grille 9x9) une grille dans
        l'interpréteur python.
        """
        if self.contenu is None:
            return "0"    # signifie que la case est vide "⛶"
        else:
            return self.contenu


class Grille:
    """
    Classe représentant une grille de 9 x 9 cases.

    Chacune des 81 cases est accessible via un index allant de 0 à 80.

    Les cases sont des widgets tkinter. Il faut donc donner un cadre à la
    grille.

    L'affichage de la grille sera différent suivant qu'une case de la pioche
    est sélectionnée ou non.

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_pioche = Pioche(mon_cadre)
    >>> ma_grille = Grille(mon_cadre, ma_pioche)  # affichage de la grille dans tkinter
    >>> ma_grille[0] # affichage fainéant d'une case dans l'interpréteur
    '0'              # retourne une chaîne de caractères
    >>> print(ma_grille[0]) # affiche fainéant la première case (d'index 0)
    0
    >>> ma_case = ma_grille.get_case(0)
    >>> type(ma_case)
    <class '__main__.Case'>
    >>> ma_case.contenu # n'affiche rien si le contenu est None
    >>> ma_case.pretendants
    ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> ma_grille
    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0

    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0

    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0
    0 0 0  0 0 0  0 0 0

    print(ma_grille)   # affiche de même la grille 9 x 9 cases
    """

    LARGEUR_BLOC = 3
    LARGEUR_GRILLE = LARGEUR_BLOC * LARGEUR_BLOC
    NBR_CASES = LARGEUR_GRILLE * LARGEUR_GRILLE
    WATCHDOG_LIMITE = 7
    SYMBOLES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    # destinations_des_symboles = dict()
    compteur = 0
    pile = list()

    # Couleurs des cases de la grille
    COULEUR_BLOCS_PAIRS = 'LightSteelBlue1'
    COULEUR_BLOCS_IMPAIRS = 'LightSteelBlue2'
    COULEUR_SELECTION_CASE = 'LightSteelBlue3'

    symbole_actif = None

    def __init__(self, cadre, grille):
        """
        À l'initialisation préciser le cadre de destination de la grille et la pioche à utiliser.
        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> ma_grille = Grille(mon_cadre, ma_pioche) # fait apparaître la grille
        """
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
                     index,
                     self.get_index_cousines(index),
                     name='{}'.format(index),
                     text=' ',  # cases vides à l'initialisation
                     background=self.get_couleur_case(
                         index, ' ', None)).grid(row=j,
                                                 column=i,
                                                 sticky="nsew")
                index += 1
        self.restaurer_pretendants()
        self.restaurer_destinations()
    

    def get_couleur_case(self, index, symbole, symbole_actif):
        """
        Retourne la couleur à donner à la case de la grille.

        Il y a trois possibilités suivant que la case appartient à un bloc 3x3
        pair ou impair ou alors qu'elle comporte le symbole actif.
        """
        if symbole == symbole_actif:
            return self.COULEUR_SELECTION_CASE
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
        Retourne une liste avec les index des 20 autres cases qui sont soit
        dans la même ligne, soit dans la même colonne, soit dans le même bloc
        carré 3x3 que la case d'index donné.
        """
        cousines = list()
        cousines.extend(self.get_index_cousines_en_ligne(index))
        cousines.extend(self.get_index_cousines_en_colonne(index))
        cousines.extend(self.get_index_cousines_en_bloc(index))
        cousines = list(dict.fromkeys(cousines))  # retire les doublons
        cousines.remove(index)
        return cousines


    def get_index_cousines_en_bloc(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans le même
        bloc carré 3x3 que la case d'index donné.
        """
        cousines_en_bloc = list()
        if self.get_bloc(index) < 3:                   # 3 premiers blocs
            premiere_triplette = [i for i in range(
                self.get_bloc(index)*3, self.get_bloc(index)*3+3)]
        elif self.get_bloc(index) < 6:                 # 3 blocs suivants
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
        cousines_en_colonne = [i for i in range(
            self.get_colonne(index),
            self.NBR_CASES, self.LARGEUR_GRILLE)]
        return cousines_en_colonne

    def get_index_cousines_en_ligne(self, index):
        """
        Retourne une liste avec les index des 9 cases qui sont dans la même
        ligne que la case d'index donné.
        """
        cousines_en_ligne = [i for i in range(
            self.LARGEUR_GRILLE * self.get_ligne(index),
            self.LARGEUR_GRILLE * self.get_ligne(index) + self.LARGEUR_GRILLE)]
        return cousines_en_ligne

    def __getitem__(self, index):
        """
        Permet d'obtenir le symbole d'une case de la grille
        avec ma_grille[index] où index est compris entre 0 et NBR_CASES-1.
        """
        return self.get_case(index).__repr__()

    def __setitem__(self, index, symbole):
        """
        Permet d'écrire facilement un symbole dans une case de la grille.

        Le symbole doit être de type str.
        exemple:
        -------
        ma_grille[0] = '5'
        """
        if not(isinstance(index, int)):
            raise TypeError()
        if symbole is not None:
            if not(isinstance(symbole, str)):
                raise TypeError()

        if index < self.NBR_CASES:
            self.get_case(index).contenu = symbole
        else:
            raise IndexError()

    def __len__(self):
        return self.NBR_CASES

    def __repr__(self):
        """
        Affichage d'une grille dans l'interpréteur Python.

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
                affichage += une_case.contenu  # ajout affichage d'une case
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

    def rafraichir_affichage(self):
        """
        Affiche le contenu des cases dans tkinter.

        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_grille = Grille(mon_cadre)
        >>> ma_grille[0] = '5'
        >>> ma_grille.rafraichir_affichage()
        """
        for index in range(self.NBR_CASES):
            ma_case = self.get_case(index)
            if ma_case.contenu is None:
                ma_case['text'] = ' '
            else:
                ma_case['text'] = ma_case.contenu
            ma_case['background'] = self.get_couleur_case(
                index,
                ma_case['text'],
                self.symbole_actif)

    def afficher_les_index(self):
        """
        Révèle dans tkinter les index des 81 cases à la place du contenu.

        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_grille = Grille(mon_cadre)
        >>> ma_grille.afficher_les_index()
        """
        for index in range(self.NBR_CASES):
            ma_case = self.get_case(index)
            ma_case['text'] = str(index)

    def efface_grille(self):
        """
        Efface le contenu de toutes les cases de la grille.
        """
        for index in range(self.NBR_CASES):
            case_a_effacer = self.get_case(index)
            case_a_effacer['text'] = ' '
            case_a_effacer.contenu = None
            case_a_effacer.pretendants = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def efface_case(self, case_a_effacer):
        """
        Efface le contenu de la case cliquée
        """
        case_a_effacer['text'] = ' '
        case_a_effacer.contenu = None
        self.restaurer_pretendants()
        self.rafraichir_affichage()

    def restaurer_pretendants(self):
        """
        Détermine les prétendants de chacune des cases de la grille.
        """
        for index in range(self.NBR_CASES):
            ma_case = self.get_case(index)
            ma_case.pretendants = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for index in range(self.NBR_CASES):
            symbole = self.get_case(index).contenu
            if not(symbole is None):
                self.reduire_pretendants_des_cousines(index, symbole)

    def remplir_case(self, index, symbole_a_placer):
        """
        Rempli la case d'index compris entre 0 et 80 avec `symbole_a_placer`.
        """
        case_a_remplir = self.get_case(index)
        if symbole_a_placer in case_a_remplir.pretendants:
            self.__setitem__(index, symbole_a_placer)
            self.rafraichir_affichage()
            return self.reduire_pretendants_des_cousines(index,
                                                         symbole_a_placer)
        else:
            print("Ce symbole ne figure pas parmi les prétendants de la case d'index", index)
            return False

    def reduire_pretendants_des_cousines(self, index, symbole):
        """
        Réduit le nombre de prétendants des cousines d'une case d'index donné

        Les cases cousines vierges ont des prétendants.
        Cette fonction retire SYMBOLE de la liste de leurs prétendants.
        """
        ma_case = self.get_case(index)
        ma_case.pretendants = list()
        for index_cousine in ma_case.index_cousines:
            case_cousine = self.get_case(index_cousine)
            if case_cousine.contenu is None:
                pretendants = case_cousine.pretendants
                if symbole in pretendants:
                    pretendants.remove(symbole)
                if not pretendants:
                    print('Case sans contenu ni prétendants')
                    return False
        return True

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

    # def tirage_debutant(self):
    #     """
    #     |----------+---------+-------------+-----------|------------------+
    #     | niveau   | restant | pourcentage |   détail  | restant à placer |
    #     |----------+---------+-------------+-----------|------------------+
    #     | Débutant |      24 |          30 | 112233444 |    887766555     |
    #     |----------+---------+-------------+-----------|------------------+

    #     Si le tirage réussi, la fonction retourne True. S'il échoue, la
    #     fonction retourne False.
    #     """

    #     # Construction d'un dictionnaire 'nombre_symboles_a_placer'
    #     # associant à chaque symbole ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    #     # le nombre aléatoire de fois qu'il sera prélevé dans la pioche.
    #     init_nombre_symboles_a_placer = [8, 8, 7, 7, 6, 6, 5, 5, 5]
    #     shuffle(init_nombre_symboles_a_placer)
    #     nombre_symboles_a_placer = dict(zip(self.SYMBOLES,
    #                                         init_nombre_symboles_a_placer))

    #     # Construction d'une liste comportant tous les symboles à placer
    #     symboles_a_placer = list()
    #     for symbole in self.SYMBOLES:
    #         symboles = symbole*nombre_symboles_a_placer[symbole]
    #         for element in symboles:
    #             symboles_a_placer.append(element)

    #     # Construction d'un dictionnaire destinations_des_symboles
    #     # associant à chaque symbole ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    #     # les destinations possibles (au départ toutes les cases)
    #     toutes_les_cases = [index for index in range(81)]
    #     destinations_des_symboles = dict()
    #     for symbole in self.SYMBOLES:
    #         toutes_les_cases = toutes_les_cases.copy()
    #         destinations_des_symboles.update({symbole: toutes_les_cases})


    #     # print('symboles à placer', symboles_a_placer)
    #     # print('nombre de symb à placer', nombre_symboles_a_placer)

    #     while symboles_a_placer:
    #         symbole_a_placer = symboles_a_placer.pop(0)
    #         # print("Placement d'un", symbole_a_placer)
    #         index_case = choice(destinations_des_symboles[symbole_a_placer])
    #         # print('index_case', index_case)
    #         if self.remplir_case(index_case, symbole_a_placer):
    #             pioche_sudoku.reduire_sac(symbole_a_placer)
    #             case_a_remplir = grille_sudoku.get_case(index_case)
    #             for index in case_a_remplir.index_cousines:
    #                 if index in destinations_des_symboles[symbole_a_placer]:
    #                     destinations_des_symboles[symbole_a_placer].remove(index)
    #             for symbole in self.SYMBOLES:
    #                 if index_case in destinations_des_symboles[symbole]:
    #                     destinations_des_symboles[symbole].remove(index_case)
    #                     if len(destinations_des_symboles[symbole]) + nombre_symboles_a_placer[symbole] == 9:
    #                         a_proteger = destinations_des_symboles[symbole]
    #                         # print('Alerte ! À protéger:', a_proteger)
    #                         for case_protegee in a_proteger:
    #                             for autres_symboles in self.SYMBOLES:
    #                                 if autres_symboles != symbole and case_protegee in destinations_des_symboles[autres_symboles]:
    #                                     destinations_des_symboles[autres_symboles].remove(case_protegee)
    #             for symbole in self.SYMBOLES:
    #                 if len(destinations_des_symboles[symbole]) + nombre_symboles_a_placer[symbole] < 9:
    #                     return  False
    #         else:
    #             return False
    #     return True


    def tirageR(self, pioche):
        """
        Génération d'une grille pleine
        """
        self.pioche = pioche
        i = 0
        trouvé = False
        while trouvé == False:
            i += 1
            print('Tentative',i)
            try:
                self.pioche.reinitialiser() 
                self.efface_grille() 
                self.restaurer_pretendants() 
                self.restaurer_destinations()
                self.compteur = 0
                trouvé = self.placementR(self.pioche)
            except:
                trouvé = False

    def solveur(self, pioche):
        """
        """
        self.pioche = pioche
        trouvé = self.placementR(self.pioche)


                
    def placementR(self, pioche):  
        #input('pause')
        symboles_a_placer = pioche.get_symboles_a_placer()
        # print (symboles_a_placer)
        if symboles_a_placer:
            symbole_a_placer = symboles_a_placer.pop(0)
            while self.destinations_des_symboles[symbole_a_placer]:
                self.compteur += 1
                progressbar["value"] = self.compteur
                progressbar.update()
                index_case = choice(self.destinations_des_symboles[symbole_a_placer])
                self.pile.append((symbole_a_placer, index_case,self.destinations_des_symboles[symbole_a_placer].copy()))
                print('compteur:',self.compteur, 'pile', self.pile[-1])
                self.remplir_case(index_case, symbole_a_placer)
                # Réduire la pioche
                self.pioche.reduire_sac(symbole_a_placer)
                # Retirer les cousines des destinations possibles
                case_a_remplir = self.get_case(index_case)
                for index in case_a_remplir.index_cousines:
                    if index in self.destinations_des_symboles[symbole_a_placer]:
                        self.destinations_des_symboles[symbole_a_placer].remove(index)
                # Retirer la case des destinations possibles
                for symbole in self.SYMBOLES:
                    destinations = self.destinations_des_symboles[symbole]
                    if index_case in destinations:
                        destinations.remove(index_case)
                if self.placementR(pioche):
                    return True
                else:
                    print('Placement a retourné False')
                    # pdb.set_trace()
                    symbole_a_retirer, destination_problematique, destinations = self.pile.pop()
                    print('pile après pop',self.pile[-1])
                    # effacer la dernière case et restaurer les prétendants
                    case_a_effacer = self.get_case(destination_problematique)
                    self.efface_case(case_a_effacer)
                    # décrémenter compteur
                    self.compteur -=1
                    progressbar["value"] = self.compteur
                    #
                    # le symbole que l'on vient de retirer est à replacer dans la pioche
                    self.pioche.remettre_dans_son_sac(symbole_a_retirer)
                    if len(destinations) == 1:
                        symbole_a_retirer, destination_problematique, destinations = self.pile.pop()
                        print('last in pile après deuxième pop',self.pile[-1])
                        # effacer la dernière case et restaurer les prétendants
                        case_a_effacer = self.get_case(destination_problematique)
                        self.efface_case(case_a_effacer)
                        # décrémenter compteur
                        self.compteur -=1
                        progressbar["value"] = self.compteur
                        # le symbole que l'on vient de retirer est à replacer dans la  pioche
                        self.pioche.remettre_dans_son_sac(symbole_a_retirer)
                        # amorcer la nouvelle tentative en ayant retiré
                        # index_case_bloquante  de destinations_des_symboles
                    self.restaurer_pretendants()
                    self.restaurer_destinations()
                    destinations.remove(destination_problematique)
                    self.destinations_des_symboles[symbole_a_retirer] = destinations
            #pdb.set_trace()
            print("While terminé car il n'y a plus de destinations") 
            return False
        else:
            print('Tous les symboles on été placés')
            return True


    def tirage(self, pioche):
        """
        Génération d'une grille pleine en partant d'une grille vierge
        """
        self.pioche = pioche
        self.pioche.reinitialiser() 
        self.efface_grille() 
        self.restaurer_pretendants() 
        self.restaurer_destinations()
        destinations_en_place = {'1':list(), '2':list(), '3':list(), '4':list(), '5':list(), '6':list(), '7':list(), '8':list(), '9':list()}
        self.compteur = 0
        watchdog = True
        self.placement_de_la_pioche_sur_la_grille(destinations_en_place, pioche, watchdog)
           


    def placement_de_la_pioche_sur_la_grille(self, destinations_en_place, pioche, watchdog):
        """
        Génération d'une grille pleine à partir de l'état actuel de la grille et de la pioche
        """
        symboles_a_placer = pioche.get_symboles_a_placer()
        
        # pdb.set_trace()
        while symboles_a_placer:
            symbole_a_placer = symboles_a_placer.pop(0)
            if self.destinations_des_symboles[symbole_a_placer]\
               and self.placement_possible(
                   destinations_en_place[symbole_a_placer],
                   self.destinations_des_symboles[symbole_a_placer]):
                self.compteur += 1
                progressbar["value"] = self.compteur
                progressbar.update()
                index_case = choice(self.destinations_des_symboles[symbole_a_placer])
                self.pile.append((symbole_a_placer,
                                  index_case,
                                  self.destinations_des_symboles[symbole_a_placer].copy()))
                print('compteur:',self.compteur, 'pile', self.pile[-1])
                self.remplir_case(index_case, symbole_a_placer)
                destinations_en_place[symbole_a_placer].append(index_case)
                # Réduire la pioche
                self.pioche.reduire_sac(symbole_a_placer)
                self.restaurer_destinations()
                watchdog_compteur = self.WATCHDOG_LIMITE
            elif self.pioche.get_widget_sac(symbole_a_placer).cardinal == 0:
                # un sac est vide ; on passe au sac suivant
                symboles_a_placer = pioche.get_symboles_a_placer()
            elif watchdog_compteur == 0:
                watchdog_compteur = self.WATCHDOG_LIMITE
                self.pioche.reinitialiser() 
                self.efface_grille() 
                self.restaurer_pretendants() 
                self.restaurer_destinations()
                destinations_en_place = {'1':list(), '2':list(), '3':list(), '4':list(), '5':list(), '6':list(), '7':list(), '8':list(), '9':list()}
                self.compteur = 0
                symboles_a_placer = pioche.get_symboles_a_placer()
            else:
                # impasse détectée
                # effacer la dernière case et restaurer les prétendants
                watchdog_compteur -= 1
                symbole_a_retirer, destination_problematique, destinations = self.pile.pop()
                case_a_effacer = self.get_case(destination_problematique)
                self.efface_case(case_a_effacer)
                destinations_en_place[symbole_a_retirer].pop()
                # décrémenter compteur
                self.compteur -=1
                progressbar["value"] = self.compteur
                # le symbole que l'on vient de retirer est à replacer dans la pioche
                self.pioche.remettre_dans_son_sac(symbole_a_retirer)
                destinations.remove(destination_problematique)
                print('-------------retire', destination_problematique)
                self.destinations_des_symboles[symbole_a_retirer] = destinations
                symboles_a_placer = pioche.get_symboles_a_placer()
        print('Tous les symboles on été placés')
        return True
        
    def placement_possible(self, destinations_en_place, autres_destinations):
        """
        Retourne True si les 9 lignes, les 9 colonnes et les 9 blocs 3x3
        sont présents parmi les candidats.
        Retourne False dans le cas contraire.
        """
        lignes_requises = set()
        colonnes_requises = set()
        blocs_requis = set()
        destinations = destinations_en_place.copy()
        destinations.extend(autres_destinations.copy())
        for destination in destinations:
            lignes_requises.add(self.get_ligne(destination))
            colonnes_requises.add(self.get_colonne(destination))
            blocs_requis.add(self.get_bloc(destination))
        return (len(lignes_requises) == 9) and (len(colonnes_requises) == 9) and (len(blocs_requis) == 9)

    def grille_export(self):
        """
        Exporte la grille sudoku sous forme de liste.
        """
        grille_en_liste = list()
        for index in range(self.NBR_CASES):
            grille_en_liste.append(self[index])
        return grille_en_liste

    def grille_import(self, grille_en_liste):
        """
        Importe puis affiche une grille transmise sous forme de liste.
        """
        for index in range(self.NBR_CASES):
            if grille_en_liste[index] == '0':
                self[index] = None
            else:
                self[index] = grille_en_liste[index]
        self.rafraichir_affichage()
        self.restaurer_pretendants()
        self.restaurer_destinations()

    def restaurer_destinations(self):
        """
        Restaure les destinations possibles pour les symboles

        à partir des prétendants de chacune des cases de la grille.
        """
        self.destinations_des_symboles = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}
        for index in range(self.NBR_CASES):
            une_case = self.get_case(index)
            for symbole in self.SYMBOLES:
                if symbole in une_case.pretendants:
                    self.destinations_des_symboles[symbole].append(index)



                    
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
    contient 9 symboles 5
    """
    def __init__(self, master, symbole, *args, **kwargs):
        """
        Construit un widget 'sac' avec comme cadre MASTER

        contenant 9 symboles identiques
        """
        super().__init__(master, *args, **kwargs) # ce qui relève de la classe Button
        self.symbole = str(symbole)
        self.cardinal = 9  # nombre d'éléments dans le sac

    def __repr__(self):
        """
        Représentation officielle d'un sac lorsque l'on tape son nom dans
        l'interpréteur.

        Le contenu du sac est renvoyé.

        exemple:
        -------
        contient 9 symboles 5

        """
        if self.cardinal == 0:
            return "sac vide"
        elif self.cardinal == 1:
            return "contient 1 symbole {}".format(self.symbole)
        else:
            return "contient {} symboles {}".format(self.cardinal,
                                                    self.symbole)

    def get_symboles_a_placer(self):
        """
        Retourne une liste avec les symboles à placer sur la grille
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> mon_sac = Sac(mon_cadre,'5')
        >>> mon_sac.get_symboles_a_placer()
        ['5', '5', '5', '5', '5', '5', '5', '5', '5']
        >>> mon_sac.cardinal = 3
        >>> mon_sac.get_symboles_a_placer()
        ['5', '5', '5']
        """
        return list(self.symbole)*self.cardinal

class Pioche:
    """
    Classe représentant 9 sacs contenant chacun des symboles identiques tous
    différents (1 sac avec que des "1", un autre avec que des "2", etc.)

    À l'initialisation de la grille, un certain nombre de ces symboles est
    prélevé pour les placer sur la grille.
    Au cours du jeu, tant qu'il reste des symboles dans un sac, le joueur peut
    en piocher pour les placer sur la grille.

    Les sacs sont des widgets tkinter. Il faut donc donner un cadre à la
    pioche.

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_pioche = Pioche(mon_cadre) # affiche les neuf boutons tkinter de la pioche
    >>> ma_pioche.NBR_SACS
    9
    >>> ma_pioche.get_sac(3)
    contient 9 symboles 3
    >>> ma_pioche[3]
    contient 9 symboles 3
    >>> print(ma_pioche[1])      # affiche le contenu du premier sac de pioche
    """

    NBR_SACS = 9
    SYMBOLES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    COULEUR_INITIALE_SAC = '#d9d9d9'
    COULEUR_SELECTION_SAC = 'LightSteelBlue3'

    def __init__(self, cadre):
        """
        Initialisation d'une liste contenant 9 sacs
        chaque sac contenant chacun 9 symboles identiques
        """
        self.cadre = cadre
    
        # Disposition du conteneur cadre qui contient la pioche
        for column in range(1, self.NBR_SACS+2):
            cadre.columnconfigure(column, weight=1)
        for index in range(1, self.NBR_SACS+1):
            Sac(cadre,
                index,
                name='{}'.format(index),
                text='{}'.format(index)).grid(row=0,
                                              column=index,
                                              sticky="nsew")
            Label(cadre,
                  name='cardinal{}'.format(index),
                  text='{}'.format(self[index].cardinal)).grid(row=1,
                                                               column=index,
                                                               sticky="nsew")
        Button(cadre, name='x', text='X').grid(row=0,
                                               column=10,
                                               sticky="nsew")

    def __iter__(self):
        """
        Rends la pioche itérable.
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> i = iter(ma_pioche)
        >>> next(i)
        contient 9 symboles 1
        >>> next(i)
        contient 9 symboles 2
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

    def get_widget_sac(self, index):
        """
        Retourne le widget sac d'index donné

        à partir de son nom (le nom du Widget étant reconstruit à partir de
        son index).

        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> print(ma_pioche.get_widget_sac(1))
        .!frame.1
        >>> ma_pioche.get_widget_sac(1)
        contient 9 symboles 1
        >>> print(ma_pioche[1])           # accès fainéant
        .!frame.1
        >>> ma_pioche[1]                  # affichage fainéant
        contient 9 symboles 1
        >>> ma_pioche.get_widget_sac(1).symbole
        '1'
        >>> ma_pioche.get_widget_sac(1).cardinal
        9
        """
        return root.nametowidget(str(self.cadre)+"."+str(index))

    def get_widget_cardinal_sac(self, index):
        """
        Accès à l'étiquette tkinter

        qui affiche le cardinal d'un sac d'index donné.
        """
        return root.nametowidget(str(self.cadre)+".cardinal"+str(index))

    def __getitem__(self, index):
        """
        Permet d'obtenir le contenu d'un sac dans la pioche avec:
        ma_pioche[index] # où index est compris entre 1 et NBR_SACS.

        exemple:
        -------
        >>> for i in range(1,10):
        ...     ma_pioche[i]
        ...
        contient 9 symboles 1
        contient 9 symboles 2
        contient 9 symboles 3
        contient 9 symboles 4
        contient 9 symboles 5
        contient 9 symboles 6
        contient 9 symboles 7
        contient 9 symboles 8
        contient 9 symboles 9

        """
        return self.get_widget_sac(index)

    def __repr__(self):
        """
        Représentation de la pioche

        quand on tape son nom dans l'interpréteur.
        """
        for index in range(1, self.NBR_SACS):
            print(self.__getitem__(index))

    def affiche_pioche(self, index_selection):
        """
        Rafraîchi la couleur de la pioche dans tkinter

        Si un sac est sélectionné, il est affiché avec une couleur distinctive.
        """
        for index in range(1, self.NBR_SACS+1):
            self.get_widget_sac(index)['background'] = self.COULEUR_INITIALE_SAC
        if index_selection == 0:  # code pour juste effacer la sélection
            pass
        elif index_selection <= 9:
            self.get_widget_sac(index_selection)['background'] = self.COULEUR_SELECTION_SAC
        else:
            raise IndexError

    def get_symboles_a_placer(self):
        """
        Retourne une liste avec les symboles à placer sur la grille
        ['1','1','1','1','1','1','1','1','1','2','2','2',...,'9','9']
        """
        symboles_a_placer = list()
        for symbole in self.SYMBOLES:
            un_sac = self.get_widget_sac(symbole)
            symboles_a_placer.extend(un_sac.get_symboles_a_placer())
        return symboles_a_placer
        
    def reduire_sac(self, symbole):
        """
        Il faut réduire le nombre de symbole d'un sac de la pioche

         à chaque fois qu'un symbole est placé sur la grille.
        """
        mon_sac = self.get_widget_sac(symbole)
        mon_sac.cardinal -= 1
        self.get_widget_cardinal_sac(symbole)['text'] = mon_sac.cardinal

    def remettre_dans_son_sac(self, symbole):
        """
        À chaque fois qu'un symbole est effacé de la grille

        il faut le remettre dans le sac de la pioche approprié.
        """
        mon_sac = self.get_widget_sac(symbole)
        mon_sac.cardinal += 1
        self.get_widget_cardinal_sac(symbole)['text'] = mon_sac.cardinal

    def reinitialiser(self):
        """
        Réinitialise la pioche

        en mettant 9 symboles identiques dans chaque sac.
        """
        for symbole in self.SYMBOLES:
            sac_a_remplir = self.get_widget_sac(symbole)
            sac_a_remplir.cardinal = 9
            self.get_widget_cardinal_sac(symbole)['text'] = 9


# FONCTIONS

def gestion_des_evenements_on_press(event):
    """
    Identifie l'élément cliqué par le joueur.

    Réagit en conséquence:
    - Si le bouton_index_cases est cliqué
    - Si le bouton effacer (X) est cliqué
    - Si une case de la grille est cliqué
    - Si un sac de la pioche est cliqué
    - Si le bouton_ajout_aleatoire est cliqué
    """
    #  Si le bouton_index_cases est cliqué
    if event.widget['text'] == 'Index des cases':
        grille_sudoku.afficher_les_index()
    # Si le bouton effacer (X) est cliqué
    if event.widget['text'] == 'X':
        deselectionner_les_cases_de_la_pioche()
        event.widget['background'] = 'red'  # case X en rouge
        grille_sudoku.symbole_actif = 'X'
        label_symbole_actif['text'] = 'Sélection: X'
        grille_sudoku.rafraichir_affichage()
    # Si une case de la grille est cliqué
    if type(event.widget) == Case:
        if grille_sudoku.symbole_actif == 'X' and not(event.widget.contenu is None):
            symbole = event.widget.contenu  # sauvegarde avant effacement
            grille_sudoku.efface_case(event.widget)
            # grille_sudoku.restaurer_pretendants()
            grille_sudoku.restaurer_destinations()
            pioche_sudoku.remettre_dans_son_sac(symbole)
        else:
            if grille_sudoku.remplir_case(event.widget.index,
                                                grille_sudoku.symbole_actif):
                pioche_sudoku.reduire_sac(grille_sudoku.symbole_actif)
    # Si un sac de la pioche est cliqué
    if type(event.widget) == Sac:
        deselectionner_le_bouton_effacer()
        pioche_sudoku.affiche_pioche(int(event.widget.symbole))
        grille_sudoku.symbole_actif = event.widget.symbole
        label_symbole_actif['text'] = 'Sélection: '+event.widget.symbole
        grille_sudoku.rafraichir_affichage()  # rafraîchissement sélection
    # Si le bouton_ajout_aleatoire est cliqué
    if event.widget['text'] == 'Tirage aléatoire':
        grille_valide = False
        tentatives_de_remplissage = 0
        afficher_tentatives = (input('Afficher chaque tentatives ?') in ['oui', 'o', 'O', 'y', 'yes'])
        while not(grille_valide) and (tentatives_de_remplissage < 5000):
            if afficher_tentatives:
                input('ENTER pour faire une tentative')
            grille_sudoku.efface_grille()
            pioche_sudoku.reinitialiser()
            tentatives_de_remplissage +=1
            print('Tentative de remplissage n°{}'.format(tentatives_de_remplissage))
            tirage = grille_sudoku.tirage_debutant()
            print(grille_sudoku)
            if tirage:
                print('Tirage réussi')
                grille_valide = True
            else:
                print('Tirage non valide !')
    if event.widget['text'] == 'TirageR':
        #grille_sudoku.efface_grille()
        #pioche_sudoku.reinitialiser()
        grille_sudoku.tirageR(pioche_sudoku)
    if event.widget['text'] == 'Solveur':
        grille_sudoku.solveur(pioche_sudoku)
    if event.widget['text'] == 'Tirage':
        #grille_sudoku.efface_grille()
        #pioche_sudoku.reinitialiser()
        grille_sudoku.tirage(pioche_sudoku)
        

def deselectionner_le_bouton_effacer():
    root.nametowidget('.pioche.x')['background'] = COULEUR_PIOCHE


def deselectionner_les_cases_de_la_pioche():
    pioche_sudoku.affiche_pioche(0)  # pioche affichée sans sélection


def gestion_des_evenements_on_release(event):
    """
    Identifie l'élément cliqué préalablement par le joueur.

    Réagit en conséquence:
    - Si le bouton_index_cases est relâché le contenu des cases est rétabli:
    permet de révéler l'index des cases de façon temporaire.
    - Si une le contenu d'une case vient d'être supprimé il est nécessaire
    de rafraîchir l'affichage des prétendants.
    """
    if event.widget['text'] == 'Index des cases':
        grille_sudoku.rafraichir_affichage()

    if type(event.widget) == Case:
        label_pretendants['text'] = event.widget.pretendants


def gestion_des_evenements_on_mouse_over(event):
    """
    Identifie l'élément survolé par la souris.

    Réagit en conséquence:
    - Si la souris survole une case de la grille les prétendants sont affichés.
    """
    if type(event.widget) == Case:
        label_pretendants['text'] = event.widget.pretendants


def gestion_des_evenements_on_mouse_leave(event):
    pass


# CONSTANTES

COULEUR_CADRE_HAUT = 'lavender'
COULEUR_CADRE_GAUCHE = 'lavender'
COULEUR_CADRE_DROIT = 'lavender'
COULEUR_PIOCHE = '#d9d9d9'
COULEUR_CADRE_BAS = 'lavender'

# APPLICATION Tkinter

root = Tk()
root.title('Sudoku')
# Contrôleur : Souris (Types d'évènements gérés)
root.bind("<ButtonPress>", gestion_des_evenements_on_press)
root.bind("<ButtonRelease>", gestion_des_evenements_on_release)
root.bind("<Enter>", gestion_des_evenements_on_mouse_over)
root.bind("<Leave>", gestion_des_evenements_on_mouse_leave)

# Création des conteneurs principaux
cadre_haut = Frame(root, name='en_tete', background=COULEUR_CADRE_HAUT, width=640, height=50)
cadre_gauche = Frame(root, name='gauche', background=COULEUR_CADRE_GAUCHE, height=400)
cadre_central = Frame(root, name='grille_sudoku', background='white')
cadre_droite = Frame(root, name='droite', background='lavender')
cadre_separation_verticale = Frame(root, name='separation', background='lavender', height=20)
cadre_pioche = Frame(root, name='pioche', background=COULEUR_PIOCHE, height=120)
cadre_bas = Frame(root, name='pied_de_page', background=COULEUR_CADRE_BAS, height=60)

# Disposition des conteneurs principaux
cadre_haut.grid(row=0, columnspan=3,  sticky="nsew")
cadre_gauche.grid(row=1, column=0, sticky="nsew")
cadre_central.grid(row=1, column=1,  sticky="nsew")
cadre_droite.grid(row=1, column=2,  sticky="nsew")
cadre_separation_verticale.grid(row=2, columnspan=3,  sticky="nsew")
cadre_pioche.grid(row=3, columnspan=3, sticky="nsew")
cadre_bas.grid(row=4, columnspan=3, sticky="nsew")

# Répartition de l'espace élastique vertical
# la ligne qui contient la grille sudoku est prioritaire
root.grid_rowconfigure(1, weight=1)
# Répartition de l'espace élastique horizontal
root.grid_columnconfigure(0, weight=1)  # cadre_gauche cadre_central
root.grid_columnconfigure(1, weight=1)  # et cadre_droite se partagent
root.grid_columnconfigure(2, weight=1)  # l'espace horizontal à égalité

progressbar = ttk.Progressbar(cadre_gauche,
                              orient="vertical",
                              length=300,
                              maximum = 81,
                              mode="determinate")
progressbar.pack(side = BOTTOM)
pioche_sudoku = Pioche(cadre_pioche)
grille_sudoku = Grille(cadre_central, pioche_sudoku)

bouton_index_cases = Button(cadre_gauche,
                            name='index_cases',
                            text='Index des cases')
label_symbole_actif = Label(cadre_gauche,
                            name='lbl_symbole_actif',
                            text='Sélection: '+str(grille_sudoku.symbole_actif),
                            background=COULEUR_CADRE_GAUCHE)
label_pretendants = Label(cadre_gauche,
                          name='lbl_pretendants',
                          text='Prétendants: ',
                          background=COULEUR_CADRE_GAUCHE)
bouton_tirage_aleatoire = Button(cadre_gauche,
                            name='tirage_aleatoire',
                            text='Tirage aléatoire')
bouton_tirageR = Button(cadre_gauche,
                            name='tirageR',
                            text='TirageR')
bouton_solveur = Button(cadre_gauche,
                            name='solveur',
                            text='Solveur')
bouton_tirage = Button(cadre_gauche,
                            name='tirage',
                            text='Tirage')


bouton_index_cases.pack()
label_symbole_actif.pack()
label_pretendants.pack()
bouton_tirage_aleatoire.pack()
bouton_tirageR.pack()
bouton_solveur.pack()
bouton_tirage.pack()
# Disposition du conteneur cadre_bas
cadre_bas.columnconfigure(0, weight=1)

# Création du bouton quitter dans cadre_bas
bouton_quitter = Button(cadre_bas, text='Quitter', command=root.quit)

# Disposition du bouton quitter
bouton_quitter.grid(sticky="nsew")

# Boucle du programme
root.mainloop()
root.destroy()
