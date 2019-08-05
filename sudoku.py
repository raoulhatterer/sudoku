# coding: UTF-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
# import pdb
# pdb.set_trace()
import pdb, traceback, sys




# Chargement des modules
from tkinter import Tk, Frame, Button, Label, Message
from tkinter import ttk
from tkinter.constants import TOP, X, BOTTOM, LEFT, BOTH, RIGHT
from random import choice
from datetime import datetime
from itertools import combinations

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

    pretendants : Une case vide à des prétendants (symboles qu'il est  possible
    de mettre cette case).

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
        super().__init__(cadre, *args, **kwargs)  # relève de la classe Button
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

    attributs:
    ----------
    - compteur : nombre de symboles posés sur la grille (en lien avec la jauge
    de remplissage)
    - destinations_en_place : dictionnaire avec l'emplacement des symboles
    placés sur la grille
    - symboles_a_placer : liste ordonnée des symboles restant à placer sur la
    grille

    méthodes:
    ---------
    - get_couleur_case
    - get_case
    - get_index_cousines
    - get_index_cousines_en_bloc
    - get_index_cousines_en_colonne
    - get_index_cousines_en_ligne
    - __getitem__
    - __setitem__
    - __len__
    - __repr__
    - basculer_le_bouton_effacer
    - activer_le_symbole
    - rafraichir_affichage
    - afficher_les_index
    - effacer_grille
    - effacer_case
    - diminuer_jauge
    - restaurer_pretendants
    - remplir_case
    - augmenter_jauge
    - reduire_pretendants_des_cousines_de_la_case
    - get_colonne
    - get_ligne
    - get_bloc
    - solveur
    - tirage
    - placer_pioche_sur_grille
    - placement_est_possible
    - grille_export
    - grille_import
    - recalculer_les_destinations_envisageables

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_pioche = Pioche(mon_cadre)
    >>> ma_grille = Grille(mon_cadre, ma_pioche)  # affichage dans tkinter
    """
    # Dimensions
    LARGEUR_BLOC = 3
    LARGEUR_GRILLE = LARGEUR_BLOC * LARGEUR_BLOC
    NBR_CASES = LARGEUR_GRILLE * LARGEUR_GRILLE
    SYMBOLES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Couleurs des cases de la grille
    COULEUR_BLOCS_PAIRS = 'LightSteelBlue1'
    COULEUR_BLOCS_IMPAIRS = 'LightSteelBlue2'
    COULEUR_SELECTION_CASE = 'LightSteelBlue3'

    def __init__(self, cadre, pioche):
        """
        Préciser le cadre de destination de la grille et la pioche à utiliser.
        exemple:
        -------
        >>> root = Tk()
        >>> mon_cadre = Frame(root)
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> ma_grille = Grille(mon_cadre, ma_pioche) # la grille apparaît
        """
        self.cadre = cadre
        self.pioche = pioche
        self.destinations_en_place = {'1': list(), '2': list(), '3': list(),
                                      '4': list(), '5': list(), '6': list(),
                                      '7': list(), '8': list(), '9': list()}
        self.symboles_a_placer = self.pioche.get_symboles_a_placer()
        self.compteur = 0

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
                         index, ' ')).grid(row=j,
                                           column=i,
                                           sticky="nsew")
                index += 1

    def get_couleur_case(self, index, symbole):
        """
        Retourne la couleur à donner à la case de la grille.

        Il y a trois possibilités suivant que la case appartient à un bloc 3x3
        pair ou impair ou alors qu'elle comporte le symbole actif.
        """
        if symbole == self.pioche.get_symbole_actif():
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
        >>> mon_cadre.pack()
        >>> ma_pioche = Pioche(mon_cadre)
        >>> ma_grille = Grille(mon_cadre, ma_pioche) # la grille apparaît
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
        Permet d'obtenir une case de la grille avec ma_grille[index]

        où index est compris entre 0 et NBR_CASES-1.
        Équivalent à : ma_grille.get_case(index)

        exemple:
        -------
        print(ma_grille[7].contenu)
        """
        return self.get_case(index)

    def __setitem__(self, index, symbole):
        """
        Permet d'écrire facilement un symbole dans une case de la grille.

        Le symbole doit être de type str.
        Équivalent à : ma_grille.get_case(index).contenu = symbole

        exemple:
        -------
        ma_grille[0] = '5'
        """
        if not(isinstance(index, int)):
            raise TypeError
        if symbole is not None:
            if not(isinstance(symbole, str)):
                raise TypeError

        if index < self.NBR_CASES:
            self.get_case(index).contenu = symbole
        else:
            raise IndexError

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
            une_case = self[index]
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

    def basculer_le_bouton_effacer(self):
        """
        Bascule le bouton effacer et désactive les autres sélections
        """
        self.pioche.basculer_le_bouton_effacer()
        self.rafraichir_affichage()

    def activer_le_symbole(self, symbole):
        """
        Sélectionne le bon symbole (sur la grille et dans la pioche)
        """
        self.pioche.focus_sur_sac(symbole)
        self.symbole_actif = symbole
        self.rafraichir_affichage()

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
            ma_case = self[index]
            if ma_case.contenu is None:
                ma_case['text'] = ' '
            else:
                ma_case['text'] = ma_case.contenu
            ma_case['background'] = self.get_couleur_case(
                index,
                ma_case['text'])

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
            ma_case = self[index]
            ma_case['text'] = str(index)

    def effacer_grille(self):
        """
        Efface le contenu de toutes les cases de la grille.

        C'est à dire:
        - le contenu de chacune des cases est None (valeur non visible)
        - visuellement les cases sont vierges

        S'occupe également de la mise à jour:
        - des prétendants
        - des destinations_en_place
        - du symbole_actif
        - de l'affichage qui est à rafraîchir
        - de la pioche qui est à réinitialiser
        - du compteur
        - de la jauge_de_remplissage
        - des symboles_a_placer

        Les cases sont prêtes à accepter n'importe lequel des 9 symboles
        """
        for index in range(self.NBR_CASES):
            self[index].contenu = None
            self[index]['text'] = ' '
            self[index].pretendants = ['1', '2', '3', '4',
                                       '5', '6', '7', '8', '9']
        self.destinations_en_place = {'1': list(), '2': list(), '3': list(),
                                      '4': list(), '5': list(), '6': list(),
                                      '7': list(), '8': list(), '9': list()}
        self.symbole_actif = None
        self.rafraichir_affichage()
        self.pioche.reinitialiser()
        self.compteur = 0
        jauge_de_remplissage["value"] = self.compteur
        self.symboles_a_placer = self.pioche.get_symboles_a_placer()

    def effacer_case(self, case_a_effacer):
        """
        Efface le contenu de la case s'il y en a un

        Puis demande la mise à jour:
        - de la jauge_de_remplissage
        - des prétendants
        - des destinations envisageables
        - des destinations en place
        - de la pioche
        - de l'affichage
        - des symboles_a_placer
        """
        if case_a_effacer.contenu:
            case_a_effacer['text'] = ' '
            symbole = case_a_effacer.contenu
            case_a_effacer.contenu = None
            self.diminuer_jauge()
            self.restaurer_pretendants()
            self.recalculer_les_destinations_envisageables()
            self.destinations_en_place[symbole].remove(case_a_effacer.index)
            self.pioche.remettre_dans_son_sac(symbole)
            self.rafraichir_affichage()
            self.symboles_a_placer.insert(0, symbole)

    def diminuer_jauge(self):
        """
        Diminution de la jauge car un symbole à été retiré de la grille pour
        être replacé dans la pioche.
        """
        self.compteur -= 1
        #print("Compteur:", self.compteur)
        jauge_de_remplissage["value"] = self.compteur
        jauge_de_remplissage.update()        

    def restaurer_pretendants(self):
        """
        Détermine les prétendants de chacune des cases de la grille
        en tenant compte du remplissage actuel de la grille.
        """
        for index in range(self.NBR_CASES):
            ma_case = self[index]
            if ma_case.contenu is None:
                ma_case.pretendants = ['1', '2', '3', '4',
                                       '5', '6', '7', '8', '9']
            else:
                ma_case.pretendants = []
        for index in range(self.NBR_CASES):
            ma_case = self[index]
            if not(ma_case.contenu is None):
                self.reduire_pretendants_des_cousines_de_la_case(index)

    def remplir_case(self, index, symbole_a_placer):
        """
        Rempli la case d'index compris entre 0 et 80 avec `symbole_a_placer`.

        Puis demande la mise à jour:
        - de la jauge_de_remplissage
        - des prétendants
        - des destinations_envisageables
        - des destinations_en_place
        - de la pioche
        - de l'affichage
        - des symboles_a_placer
        """
        case_a_remplir = self[index]
        if symbole_a_placer in case_a_remplir.pretendants:
            self.__setitem__(index, symbole_a_placer)
            self.augmenter_jauge()
            case_a_remplir.pretendants = []
            reduction_OK = self.reduire_pretendants_des_cousines_de_la_case(index) # peut conduire à une case sans contenu ni prétendants
            self.recalculer_les_destinations_envisageables()
            self.destinations_en_place[symbole_a_placer].append(index)
            self.pioche.reduire_sac(symbole_a_placer)
            self.rafraichir_affichage()
            self.symboles_a_placer.remove(symbole_a_placer)
            return reduction_OK
        else:
            # print("Ce symbole ne figure pas parmi les prétendants de la case\
            #  d'index", index) ##
            return False

    def augmenter_jauge(self):
        """
        Augmentation de la jauge car un symbole à été retiré de la pioche pour
        être replacé sur la grille.
        """
        self.compteur += 1
        #print("Compteur:", self.compteur)
        jauge_de_remplissage["value"] = self.compteur
        jauge_de_remplissage.update()

    def reduire_pretendants_des_cousines_de_la_case(self, index):
        """
        Réduit le nombre de prétendants des cousines d'une case d'index donné

        Les cases cousines vierges ont des prétendants.
        Cette fonction retire le SYMBOLE contenu dans la case de la liste de
        leurs prétendants.
        Retourne False si une case vide se retrouve sans prétendants.
        """
        ma_case = self[index]
        symbole = ma_case.contenu
        for index_cousine in ma_case.index_cousines:
            case_cousine = self.get_case(index_cousine)
            if case_cousine.contenu is None:
                pretendants = case_cousine.pretendants
                if symbole in pretendants:
                    pretendants.remove(symbole)
                if not pretendants:
                    #print('Case', index_cousine, 'sans contenu ni prétendants') ##
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

    def tirage(self, pioche):
        """
        Génération d'une grille pleine en partant d'une grille vierge
        """
        self.effacer_grille()
        datetime_depart = datetime.now()
        mon_watchdog = Watchdog()
        pile = list()
        dernier_placement_OK = True
        while self.symboles_a_placer:
            symbole_a_placer = self.symboles_a_placer[0]
            self.pioche.focus_sur_sac(symbole_a_placer)
            if self.pioche.get_destinations_envisageables(
                    symbole_a_placer) and self.placement_est_possible(
                        self.destinations_en_place[symbole_a_placer],
                        self.pioche.get_destinations_envisageables(
                            symbole_a_placer)) and dernier_placement_OK:
                destinations = self.pioche.get_destinations_envisageables(
                    symbole_a_placer).copy()
                index_case = choice(list(
                    self.pioche.get_destinations_envisageables(
                        symbole_a_placer)))  # valeur au hasard
                pile.append((symbole_a_placer,
                            index_case,
                             destinations))
                dernier_placement_OK = self.remplir_case(index_case, symbole_a_placer)
                mon_watchdog.reset()
            elif mon_watchdog.alarm():
                # Retirer les plus anciens symboles identiques posés sur la grille
                # et les renvoyer en fin de liste pour être placés en dernier
                mon_watchdog.reset()
                symbole_recherche = pile[0][0]
                while pile and symbole_recherche == pile[0][0]:
                    symbole_a_retirer, destination_liberee, sans_interet = pile.pop(0)
                    case_a_effacer = self[destination_liberee]
                    self.effacer_case(case_a_effacer)
                    self.symboles_a_placer.pop(0)  # retiré à l'avant
                    self.symboles_a_placer.append(symbole_a_retirer)  # placé à la fin
            else:
                # impasse détectée
                dernier_placement_OK = True  # réinitialisation
                # effacer la dernière case et restaurer les prétendants
                mon_watchdog.update()
                symbole_a_retirer, destination_problematique, destinations = pile.pop()
                case_a_effacer = self[destination_problematique]
                self.effacer_case(case_a_effacer)
                destinations.remove(destination_problematique)
                self.pioche[symbole_a_retirer].destinations_envisageables = destinations
        datetime_fin = datetime.now()
        duree = datetime_fin - datetime_depart
        print('Tous les symboles on été placés en', duree)
        return True

    def solveur(self, pioche):
        """
        Génération d'une grille pleine à partir de l'état actuel de la grille
        et de la pioche.
        Chaque sac de la pioche est traité en tant qu'ensemble. 
        """
        # pdb.set_trace()
        self.symboles_a_placer = self.pioche.get_symboles_a_placer()
        datetime_depart = datetime.now()
        cases_bloquees = self.destinations_en_place
        print("cases à bloquer", cases_bloquees)
        pile = list()
        dernier_placement_OK = True
        determiner_combinaisons = True
        while self.symboles_a_placer:
            symbole_a_placer = self.symboles_a_placer[0]
            self.activer_le_symbole(symbole_a_placer)
            if determiner_combinaisons:
                self.combinaisons = self.determine_combinaisons(symbole_a_placer)
            if self.combinaison_existe() and dernier_placement_OK:
                self.combinaison_au_hasard = choice(list(self.combinaisons))
                sauvegarde_combinaisons = self.combinaisons.copy()
                pile.append((symbole_a_placer, self.combinaison_au_hasard, sauvegarde_combinaisons))
                for emplacement in self.combinaison_au_hasard:
                    dernier_placement_OK = dernier_placement_OK and self.remplir_case(emplacement, symbole_a_placer)
                if not(dernier_placement_OK):
                    for emplacement in self.combinaison_au_hasard:
                        case_a_effacer = self.get_case(emplacement)
                        self.effacer_case(case_a_effacer)
                determiner_combinaisons = True
            elif not(pile):
                print("Cette grille n'admet pas de solution!")
                return False
            else:
                # impasse détectée
                dernier_placement_OK = True  # réinitialisation
                # effacer la dernière combinaison et restaurer les prétendants
                symbole_a_retirer, combinaison_problematique, combinaisons = pile.pop()
                self.activer_le_symbole(symbole_a_retirer)
                for emplacement in combinaison_problematique:
                    case_a_effacer = self[emplacement]
                    self.effacer_case(case_a_effacer)
                combinaisons.remove(combinaison_problematique)
                self.combinaisons = combinaisons
                determiner_combinaisons = False
        datetime_fin = datetime.now()
        duree = datetime_fin - datetime_depart
        print('Tous les symboles on été placés en', duree)
        return True

    def determine_combinaisons(self, symbole):
        """
        Génère l'ensemble des combinaisons de destinations envisageables.


        Interroge la pioche puis purge la liste des combinaisons
        dont le placement est impossible.
        """
        combinaisons = self.pioche[symbole].get_combinaisons()
        combinaisons_valables = set()
        for combinaison in combinaisons:
            if self.placement_est_possible(
                    self.destinations_en_place[symbole],
                    list(combinaison)):
                combinaisons_valables.add(combinaison)
        return combinaisons_valables

    def placement_est_possible(self, en_place, autres):
        """
        Retourne True si les 9 lignes, les 9 colonnes et les 9 blocs 3x3
        sont présents parmi les candidats.
        Retourne False dans le cas contraire.
        """
        lignes_requises = set()
        colonnes_requises = set()
        blocs_requis = set()
        destinations = en_place.copy()
        destinations.extend(autres.copy())
        for destination in destinations:
            lignes_requises.add(self.get_ligne(destination))
            colonnes_requises.add(self.get_colonne(destination))
            blocs_requis.add(self.get_bloc(destination))
        return (len(lignes_requises) == 9) and (
            len(colonnes_requises) == 9) and (len(blocs_requis) == 9)

    def combinaison_existe(self):
        """
        Retourne True s'il existe au moins une combinaison envisageable, False s'il n'y en a plus.
        """
        if len(self.combinaisons):
            return True
        else:
            return False

    def grille_export(self):
        """
        Exporte la grille sudoku sous forme de liste.
        """
        grille_en_liste = list()
        for index in range(self.NBR_CASES):
            grille_en_liste.append(self[index].contenu)
        return grille_en_liste

    def grille_import(self, grille_en_liste, pioche):
        """
        Importe puis affiche une grille transmise sous forme de liste.

        """
        self.effacer_grille()
        for index in range(self.NBR_CASES):
            symbole = grille_en_liste[index]
            if symbole != '0':
                self.remplir_case(index, symbole)


    def recalculer_les_destinations_envisageables(self):
        """
        Détermine toutes les destinations possibles pour les symboles

        à partir des prétendants de chacune des cases de la grille.
        """
        for symbole in self.SYMBOLES:
            self.pioche[symbole].destinations_envisageables = set()
        for index in range(self.NBR_CASES):
            une_case = self[index]
            for symbole in self.SYMBOLES:
                if symbole in une_case.pretendants:
                    self.pioche[symbole].destinations_envisageables.add(index)


class Watchdog():
    """
    Signale quand l'exploration de l'arbre va trop profond.
    """

    watchdog_limit = 4

    def __init__(self):
        self.compteur = 0

    def reset(self):
        self.compteur = 0

    def update(self):
        self.compteur += 1

    def alarm(self):
        if self.compteur > self.watchdog_limit:
            self.elargissement()
            return True
        else:
            return False

    def elargissement(self):
        self.watchdog_limit += 0.125


class Sac(Frame):
    """
    Classe représentant un sac. Un sac contient des symboles identiques.

    Attributs:
    ---------
    - symbole: '1' pour indiquer que le sac contient des '1', '2' pour ...
    - cardinal: nombre d'éléments dans le sac
    - destinations_envisageables : ensemble des cases de la grille
    envisageables pour le prochain symbole tiré de ce sac.
    À l'initialisation chacune des 81 cases de la grille constitue une
    destination envisageable.

    Méthodes:
    ---------
    - reinitialiser
    - get_symboles_a_placer
    - get_nombre_combinaisons
    - get_symbole
    - set_symbole
    - get_cardinal
    - set_cardinal
    - ajouter_un_element
    - retirer_un_element
    - get_destinations_envisageables
    - set_destinations_envisageables
    - selectionner
    - deselectionner

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> mon_sac = Sac(mon_cadre,'5')
    >>> mon_sac
    contient 9 symboles 5
    """
    police_symbole = "{dyuthi} 12"
    police_cardinal = "{dyuthi} 8"
    COULEUR_INITIALE_SAC = '#d9d9d9'
    COULEUR_SELECTION_SAC = 'LightSteelBlue3'

    def __init__(self, master, symbole, *args, **kwargs):
        """
        Construit un widget 'sac' avec comme cadre MASTER
        """
        super().__init__(master, *args, **kwargs)
        self.symbole = str(symbole)
        self.cardinal = 9
        self.destinations_envisageables = set(
            [destination for destination in range(81)])
        Button(self,
               name="symbole",
               font=self.police_symbole,
               text=symbole).pack(side=TOP, fill=X)
        Label(self,
              name="cardinal",
              font=self.police_cardinal,
              text='{}'.format(self.cardinal)).pack(side=BOTTOM, fill=X)

    def reinitialiser(self):
        """
        Réinitialisation du sac.
        """
        self.set_cardinal(9)
        self.destinations_envisageables = set(
            [destination for destination in range(81)])

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

    def get_nombre_combinaisons(self):
        """
        Pour ce sac retourne le nombre de combinaisons compte tenu du nombre
        de destinations_envisageables et du nombre de symboles dans le sac.
        """
        return nCr(len(self.destinations_envisageables), self.cardinal)

    def get_symbole(self):
        """
        Retourne le symbole du sac.
        """
        return self.symbole

    def set_symbole(self, symbole):
        """
        Permet d'attribuer un symbole au sac.
        """
        # Sauvegarde
        self.symbole = symbole
        # Affichage
        root.nametowidget(str(self)+".symbole")['text'] = symbole

    def get_cardinal(self):
        """
        Retourne le nombre d'éléments dans le sac.
        """
        return self.cardinal

    def set_cardinal(self, cardinal):
        """
        Permet d'attribuer un cardinal au sac.
        """
        # Sauvegarde
        self.cardinal = cardinal
        # Affichage
        root.nametowidget(str(self)+".cardinal")['text'] = cardinal

    def ajouter_un_element(self):
        """
        Permet d'incrémenter le cardinal du sac.
        """
        # Sauvegarde
        self.cardinal += 1
        if self.cardinal > 9:
            self.cardinal = 9
            raise IndexError()
        # Affichage
        root.nametowidget(str(self)+".cardinal")['text'] = self.cardinal

    def retirer_un_element(self):
        """
        Permet d'incrémenter le cardinal du sac.
        """
        # Sauvegarde
        self.cardinal -= 1
        if self.cardinal < 0:
            self.cardinal = 0
            raise IndexError()
        # Affichage
        root.nametowidget(str(self)+".cardinal")['text'] = self.cardinal

    def get_destinations_envisageables(self):
        """
        Retourne l'ensemble des destinations envisageables où l'on pourrait
        placer les symboles contenus dans le sac.
        """
        return self.destinations_envisageables

    def set_destinations_envisageables(self, destinations):
        """
        Permet d'attribuer des destinations envisageables au sac.
        """
        self.destinations_envisageables = destinations

    def get_combinaisons(self):
        """
        Génère puis retourne l'ensemble des combinaisons de destinations envisageables
        """
        return set(combinations(self.destinations_envisageables,self.cardinal))
    
    def selectionner(self):
        """
        Active la couleur SELECTION du sac
        """
        root.nametowidget(
            str(self)+".symbole")['background'] = self.COULEUR_SELECTION_SAC

    def deselectionner(self):
        """
        Active la couleur SANS-SELECTION du sac
        """
        root.nametowidget(
            str(self)+".symbole")['background'] = self.COULEUR_INITIALE_SAC


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

    attributs:
    ----------
    - symboles_a_placer : liste de tous les symboles à placer
    - symbole_actif : symbole sélectionné

    méthodes:
    ---------
    - montrer_destinations_envisageables
    - cacher_destinations_envisageables
    - get_sac
    - deselectionner_le_bouton_effacer
    - basculer_le_bouton_effacer
    - deselectionner_tout
    - focus_sur_sac
    - get_symbole_actif
    - get_destinations_envisageables
    - get_combinaisons
    - get_symboles_a_placer
    - reduire_sac
    - remettre_dans_son_sac
    - reinitialiser

    exemple:
    -------
    >>> root = Tk()
    >>> mon_cadre = Frame(root)
    >>> mon_cadre.pack()
    >>> ma_pioche = Pioche(mon_cadre) # affiche 9 boutons tkinter de la pioche
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
    police_X = "{dyuthi}"

    def __init__(self, cadre):
        """
        Initialisation d'une pioche contenant 9 sacs
        chaque sac contenant chacun 9 symboles identiques
        """
        self.cadre = cadre
        Message(self.cadre, name='msg_destinations_envisageables',
                text='Destinations envisageables', aspect=200).pack_forget()
        for index in range(1, self.NBR_SACS+1):
            Sac(self.cadre,
                index,
                name='{}'.format(index)).pack(side=LEFT, fill=BOTH, expand=1)
        Button(self.cadre, name='x', text='X', font=self.police_X).pack(
            side=RIGHT, fill=BOTH, expand=True, anchor="se")
        self.symbole_actif = None

    def montrer_destinations_envisageables(self):
        """
        Montre les destinations envisageables.
        """
        if self.symbole_actif and self.symbole_actif != 'X':
            root.nametowidget(
                str(self.cadre)+".msg_destinations_envisageables")['text'] = \
                    self[self.symbole_actif].destinations_envisageables
            root.nametowidget(str(self.cadre)+".x").pack_forget()
            root.nametowidget(
                str(self.cadre)+".msg_destinations_envisageables").pack(
                    side=LEFT)
            root.nametowidget(
                str(self.cadre)+".x").pack(
                    side=RIGHT, fill=BOTH, expand=True, padx=1)

    def cacher_destinations_envisageables(self):
        """
        Cache  les destinations envisageables.
        """
        root.nametowidget(
            str(self.cadre)+".msg_destinations_envisageables").pack_forget()

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

    def get_sac(self, index):
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
        >>> print(ma_pioche.get_sac(1))
        .!frame.1
        >>> ma_pioche.get_sac(1)
        contient 9 symboles 1
        >>> print(ma_pioche[1])           # accès fainéant
        .!frame.1
        >>> ma_pioche[1]                  # affichage fainéant
        contient 9 symboles 1
        >>> ma_pioche.get_sac(1).symbole
        '1'
        >>> ma_pioche.get_sac(1).cardinal
        9
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
        return self.get_sac(index)

    def __repr__(self):
        """
        Représentation de la pioche

        quand on tape son nom dans l'interpréteur.
        """
        la_pioche_contient = ""
        for index in range(1, self.NBR_SACS+1):
            if self.__getitem__(index).cardinal < 2:  # accord sing./pluriel
                la_pioche_contient += "contient {} symbole '{}'\n".format(
                    self.__getitem__(index).cardinal, self.__getitem__(index).symbole)
            else:
                la_pioche_contient += "contient {} symboles '{}'\n".format(
                    self.__getitem__(index).cardinal, self.__getitem__(index).symbole)
        return la_pioche_contient

    def deselectionner_le_bouton_effacer(self):
        self.symbole_actif = None
        root.nametowidget(
            str(self.cadre)+'.x')['background'] = self.COULEUR_INITIALE_SAC

    def basculer_le_bouton_effacer(self):
        """
        Affichage : bascule la sélection du X
        """
        if self.symbole_actif == 'X':
            self.deselectionner_tout()
            self.deselectionner_le_bouton_effacer()
        else:
            self.deselectionner_tout()
            self.symbole_actif = 'X'
            # case X en rouge
            root.nametowidget(str(self.cadre)+'.x')['background'] = 'red'

    def deselectionner_tout(self):
        """
        La pioche est affichée sans sac sélectionné
        """
        self.symbole_actif = None
        self.focus_sur_sac(None)

    def focus_sur_sac(self, symbole):
        """
        Rafraîchi la couleur de la pioche dans tkinter

        Si un sac est sélectionné, il est affiché avec une couleur distinctive.
        """
        # désélection
        self.deselectionner_le_bouton_effacer()
        for index in range(1, self.NBR_SACS+1):
            self[index].deselectionner()
        # sélection
        if symbole:
            self.symbole_actif = symbole
            index_selection = int(self.symbole_actif)
            if index_selection <= 9:
                self[index_selection].selectionner()
            else:
                raise IndexError

    def get_symbole_actif(self):
        """
        Retourne le symbole actuellement sélectionné dans la pioche.
        """
        return self.symbole_actif

    def get_destinations_envisageables(self, symbole):
        """
        Retourne l'ensemble des destinations_envisageables pour ce symbole
        """
        return self[symbole].get_destinations_envisageables()
    
    def get_symboles_a_placer(self):
        """
        Par lecture de la pioche, cette fonction retourne une liste
        avec les symboles à placer sur la grille. Dans l'ordre croissant des combinaisons à calculer.
        ['1','1','1','1','1','1','1','1','1','2','2','2',...,'9','9']
        """
        nombres_de_combinaisons = list()
        for symbole in self.SYMBOLES:
            un_sac = self.get_sac(symbole)
            nombres_de_combinaisons.append((un_sac.get_nombre_combinaisons(), symbole))
        nombres_de_combinaisons_triees = sorted(nombres_de_combinaisons)
        symboles_a_placer = list()
        while nombres_de_combinaisons_triees:
            nombre_de_combinaisons, symbole = nombres_de_combinaisons_triees.pop(0)
            un_sac = self.get_sac(symbole)
            symboles_a_placer.extend(un_sac.get_symboles_a_placer())
        return symboles_a_placer


    def reduire_sac(self, symbole):
        """
        Il faut réduire le nombre de symboles d'un sac de la pioche

        à chaque fois qu'un symbole est placé sur la grille.
        """
        self[symbole].retirer_un_element()

    def remettre_dans_son_sac(self, symbole):
        """
        À chaque fois qu'un symbole est effacé de la grille

        il faut le remettre dans le sac de la pioche approprié.
        """
        self[symbole].ajouter_un_element()

    def reinitialiser(self):
        """
        Réinitialise la pioche

        """
        for symbole in self.SYMBOLES:
            self[symbole].reinitialiser()
        self.deselectionner_tout()


# FONCTIONS

def nCr(n, r):
    """
    Retourne le nombre de combinaisons de n objets pris r à r
    """
    if r > n//2:
        r = n-r
    x = 1
    y = 1
    i = n-r+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x


def tirage():
    """
    Remplissage d'une grille complète
    """
    grille_sudoku.tirage(pioche_sudoku)


def vierge():
    """
    Efface la grille
    """
    grille_sudoku.effacer_grille()
    label_pretendants['text'] = "Prétendants"


def exemple():
    """
    Charge un exemple
    """
    grille_sudoku.grille_import(['0', '6', '0', '0', '0', '0', '0', '0', '8',
                                 '0', '0', '7', '6', '9', '3', '0', '0', '0',
                                 '3', '0', '0', '0', '1', '0', '0', '2', '0',
                                 '0', '0', '2', '0', '7', '0', '4', '0', '0',
                                 '0', '1', '0', '0', '0', '0', '9', '6', '7',
                                 '0', '0', '0', '1', '0', '0', '0', '8', '2',
                                 '5', '9', '0', '7', '0', '1', '0', '4', '0',
                                 '0', '0', '0', '0', '0', '6', '2', '0', '0',
                                 '0', '0', '0', '9', '0', '0', '8', '0', '0'],
                                pioche_sudoku)


def solveur():
    """
    Remplissage d'une grille complète
    """
    grille_sudoku.solveur(pioche_sudoku)


def afficher_les_index(event):
    """
    Les index des cases sont montrés, si le bouton_index_cases est enfoncé.

    Permet de révéler l'index des cases de façon temporaire.
    """
    grille_sudoku.afficher_les_index()


def cacher_les_index(event):
    """
    Si le bouton_index_cases est relâché le contenu des cases est rétabli.

    Permet de révéler l'index des cases de façon temporaire.
    """
    grille_sudoku.rafraichir_affichage()


def gestion_des_evenements_on_press(event):
    """
    Identifie l'élément cliqué par le joueur.

    Réagit en conséquence:
    - si le bouton effacer (X) est cliqué
    - si un sac de la pioche est cliqué
    - si une case de la grille est cliqué
    """

    # Cacher les destinations envisageables
    pioche_sudoku.cacher_destinations_envisageables()

    # Si le bouton effacer (X) est cliqué
    if type(event.widget) == Button and event.widget['text'] == 'X':
        grille_sudoku.basculer_le_bouton_effacer()

    # Si un sac de la pioche est cliqué
    if type(event.widget.master) == Sac:
        symbole_a_activer = event.widget.master.symbole
        grille_sudoku.activer_le_symbole(symbole_a_activer)

    # Si une case de la grille est cliqué
    if type(event.widget) == Case:
        # print(pioche_sudoku.get_symbole_actif()) ##
        if pioche_sudoku.get_symbole_actif() == 'X':
            if event.widget.contenu is None:
                pass  # ne rien faire la case est déjà vide
            else:
                grille_sudoku.effacer_case(event.widget)
        else:
            grille_sudoku.remplir_case(event.widget.index,
                                       pioche_sudoku.get_symbole_actif())


def gestion_des_evenements_on_release(event):
    """
    Il est nécessaire de rafraîchir l'affichage des prétendants.
    au cas où le contenu d'une case vient d'être supprimé.
    """
    if type(event.widget) == Case:
        label_pretendants['text'] = event.widget.pretendants


def gestion_des_evenements_on_mouse_over(event):
    """
    Si la souris survole une case de la grille les prétendants sont affichés.
    Si la souris survole le nombre de symbole restants les destinations
    envisageables s'affichent.
    """
    if type(event.widget) == Case:
        label_pretendants['text'] = event.widget.pretendants
    if type(event.widget) == Label and type(event.widget.master) == Sac:
        pioche_sudoku.montrer_destinations_envisageables()


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

# Création des conteneurs principaux
cadre_haut = Frame(root, name='en_tete',
                   background=COULEUR_CADRE_HAUT,
                   width=640, height=50)
cadre_gauche = Frame(root, name='gauche',
                     background=COULEUR_CADRE_GAUCHE,
                     height=400)
cadre_central = Frame(root, name='grille_sudoku',
                      background='white')
cadre_droite = Frame(root, name='droite',
                     background='lavender')
cadre_separation_verticale = Frame(root, name='separation',
                                   background='lavender',
                                   height=20)
cadre_pioche = Frame(root, name='pioche',
                     background=COULEUR_PIOCHE,
                     height=120)
cadre_bas = Frame(root, name='pied_de_page',
                  background=COULEUR_CADRE_BAS,
                  height=60)

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

pioche_sudoku = Pioche(cadre_pioche)
grille_sudoku = Grille(cadre_central, pioche_sudoku)

# Création des éléments dans le cadre de gauche
bouton_index_cases = Button(cadre_gauche,
                            name='index_cases',
                            text='Index des cases')
label_pretendants = Label(cadre_gauche,
                          name='lbl_pretendants',
                          text='Prétendants',
                          background=COULEUR_CADRE_GAUCHE)
bouton_vierge = Button(cadre_gauche,
                       name='vierge',
                       text='Vierge',
                       command=vierge)
bouton_exemple = Button(cadre_gauche,
                        name='exemple',
                        text='Exemple',
                        command=exemple)
bouton_solveur = Button(cadre_gauche,
                        name='solveur',
                        text='Solveur',
                        command=solveur)
bouton_tirage = Button(cadre_gauche,
                       name='tirage',
                       text='Tirage',
                       command=tirage)
jauge_de_remplissage = ttk.Progressbar(cadre_gauche,
                                       orient="vertical",
                                       length=200,
                                       maximum=81,
                                       mode="determinate")


bouton_index_cases.pack()
label_pretendants.pack()
bouton_vierge.pack()
bouton_exemple.pack()
bouton_solveur.pack()
bouton_tirage.pack()
jauge_de_remplissage.pack(side=BOTTOM)

# Disposition du conteneur cadre_bas
cadre_bas.columnconfigure(0, weight=1)

# Création du bouton quitter dans cadre_bas
bouton_quitter = Button(cadre_bas, text='Quitter', command=root.quit)

# Disposition du bouton quitter
bouton_quitter.grid(sticky="nsew")

# Contrôleur évolué: Souris (Types d'évènements gérés)
bouton_index_cases.bind("<ButtonPress>", afficher_les_index)
bouton_index_cases.bind("<ButtonRelease>", cacher_les_index)
root.bind("<ButtonPress>", gestion_des_evenements_on_press)
root.bind("<ButtonRelease>", gestion_des_evenements_on_release)
root.bind("<Enter>", gestion_des_evenements_on_mouse_over)
root.bind("<Leave>", gestion_des_evenements_on_mouse_leave)

# Boucle du programme
root.mainloop()
root.destroy()
