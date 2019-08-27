# coding: UTF-8
# Jeu de Sudoku
# Auteur : Raoul HATTERER

# Pour debugger:
# import pdb
# pdb.set_trace()
#import pdb, traceback, sys

# Chargement des modules
from tkinter import Tk, ttk, Frame, Button, Label, Message, LabelFrame, Scale,\
    Checkbutton, IntVar, StringVar, Menu, BooleanVar, Toplevel
from tkinter.constants import TOP, X, BOTTOM, LEFT, BOTH, RIGHT,\
    DISABLED, ACTIVE, NORMAL, SUNKEN
from random import choice, randrange
from datetime import datetime
from itertools import combinations
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showerror
from csv import reader
from webbrowser import open_new
from platform import system

#  localisation
langue = 'fr'

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
    - cacher_jauge_parcourt_combinaisons
    - monter_jauge_parcourt_combinaisons
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
    - basculer_le_bouton_effacerX
    - activer_le_symbole
    - rafraichir_affichage
    - afficher_les_index
    - effacer_grille
    - effacer_case
    - diminuer_jauge_de_remplissage
    - restaurer_pretendants
    - remplir_case
    - augmenter_jauge_de_remplissage
    - reduire_pretendants_des_cousines_de_la_case
    - get_colonne
    - get_ligne
    - get_bloc
    - solveur
    - remplissage
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
    COULEUR_VICTOIRE = 'green4'
    # Polices
    police_case = "{helvetica} 20"
    police_index = "{helvetica} 14"

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
        self.symboles_a_placer, self.ordre_de_placement = \
            self.pioche.get_symboles_a_placer_et_ordre()
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
                     font=self.police_case,
                     text=' ',  # cases vides à l'initialisation
                     disabledforeground='saddle brown',
                     # background pour linux et windows
                     background=self.get_couleur_case(
                         index, ' '),
                     # highlightbackground pour osx qui a un bug avec background des boutons 
                     highlightbackground=self.get_couleur_case(
                         index, ' ')).grid(row=j,
                                           column=i,
                                           sticky="nsew")
                index += 1
        ttk.Progressbar(cadre,
                        name="jauge_parcourt_combinaisons",
                        orient="horizontal",
                        maximum=3,
                        mode="determinate").grid_forget()

    def cacher_jauge_parcourt_combinaisons(self):
        """
        Cache  la jauge de parcourt des combinaisons lorsque le solveur est
        inactif.
        """
        root.nametowidget(
            str(self.cadre)+".jauge_parcourt_combinaisons").grid_forget()

    def monter_jauge_parcourt_combinaisons(self):
        """
        Montre la jauge de parcourt des combinaisons lorsque le solveur est
        actif.
        """
        root.nametowidget(
            str(self.cadre)+".jauge_parcourt_combinaisons").grid(
                row=self.LARGEUR_GRILLE+1,
                columnspan=self.LARGEUR_GRILLE+1,
                pady=5,
                sticky="ew")

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

    def basculer_le_bouton_effacerX(self):
        """
        Bascule le bouton effacer et désactive les autres sélections
        """
        self.pioche.basculer_le_bouton_effacerX()
        self.rafraichir_affichage()

    def activer_le_symbole(self, symbole):
        """
        Sélectionne le bon symbole (sur la grille et dans la pioche)
        """
        self.pioche.focus_sur_sac(symbole)
        self.symbole_actif = symbole
        self.rafraichir_affichage()

    def rafraichir_affichage(self, secret=False):
        """
        Affiche le contenu des cases dans tkinter.
        Sauf si SECRET vaut True.
        """
        if not(secret):
            # rétablir le texte au cas où l'on avait demandé l'affichage des index
            for index in range(self.NBR_CASES):
                ma_case = self[index]
                if ma_case.contenu is None:
                    ma_case['text'] = ' '
                else:
                    ma_case['text'] = ma_case.contenu
                ma_case['foreground'] = 'black'
                # background pour linux et windows
                ma_case['background'] = self.get_couleur_case(
                    index,
                    ma_case['text'])
                # highlightbackground pour osx qui a un bug avec background
                ma_case['highlightbackground'] = self.get_couleur_case(
                    index,
                    ma_case['text'])
                ma_case['font'] = self.police_case

    def afficher_les_index(self):
        """
        Révèle dans tkinter les index des 81 cases à la place du contenu.
        """
        for index in range(self.NBR_CASES):
            ma_case = self[index]
            ma_case.configure(text=str(index), font=self.police_index)

    def afficher_la_victoire(self):
        """
        Affiche les symboles en vert.
        """
        for index in range(self.NBR_CASES):
            ma_case = self[index]
            ma_case.configure(foreground=self.COULEUR_VICTOIRE)

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
        timer_on(False)
        duree.set("0:00:00")

        for index in range(self.NBR_CASES):
            self[index].contenu = None
            self[index]['text'] = ' '
            self[index]['state'] = NORMAL
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
        self.symboles_a_placer, self.ordre_de_placement =\
            self.pioche.get_symboles_a_placer_et_ordre()

    def effacer_case(self, case_a_effacer, secret=False):
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
            self.diminuer_jauge_de_remplissage()
            self.restaurer_pretendants()
            self.recalculer_les_destinations_envisageables()
            self.destinations_en_place[symbole].remove(case_a_effacer.index)
            self.pioche.remettre_dans_son_sac(symbole)
            self.rafraichir_affichage(secret)
            self.symboles_a_placer.insert(0, symbole)

    def diminuer_jauge_de_remplissage(self):
        """
        Diminution de la jauge car un symbole a été retiré de la grille pour
        être replacé dans la pioche.
        """
        self.compteur -= 1
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

    def remplir_case(self, index, symbole_a_placer, secret=False):
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
            self.augmenter_jauge_de_remplissage()
            case_a_remplir.pretendants = []
            reduction_OK = self.reduire_pretendants_des_cousines_de_la_case(
                index)  # peut conduire à une case sans contenu ni prétendants
            self.recalculer_les_destinations_envisageables()
            self.destinations_en_place[symbole_a_placer].append(index)
            self.pioche.reduire_sac(symbole_a_placer)
            self.rafraichir_affichage(secret)
            self.symboles_a_placer.remove(symbole_a_placer)
            return reduction_OK
        else:
            # print("Ce symbole ne figure pas parmi les prétendants de la case\
            #  d'index", index) ##
            return False

    def augmenter_jauge_de_remplissage(self):
        """
        Augmentation de la jauge car un symbole a été retiré de la pioche pour
        être replacé sur la grille.
        """
        self.compteur += 1
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
                    # Case index_cousine sans contenu ni prétendants
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

    def remplissage(self, secret=False):
        """
        Génération d'une grille pleine en partant d'une grille vierge.
        À tour de rôle, chaque symbole de la pioche est placé aléatoirement
        sur la grille à une position autorisée.
        Si SECRET vaut True le contenu des cases demeure caché.
        """
        self.effacer_grille()
        mon_watchdog = Watchdog()
        pile = list()
        dernier_placement_OK = True
        while self.symboles_a_placer:
            symbole_a_placer = self.symboles_a_placer[0]
            if not(secret):
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
                pile.append((symbole_a_placer, index_case, destinations))
                dernier_placement_OK =\
                    self.remplir_case(index_case, symbole_a_placer, secret)
                mon_watchdog.reset()
            elif mon_watchdog.alarm():
                # Retirer les plus anciens symboles identiques posés sur la grille
                # et les renvoyer en fin de liste pour être placés en dernier
                mon_watchdog.reset()
                symbole_recherche = pile[0][0]
                while pile and symbole_recherche == pile[0][0]:
                    symbole_a_retirer, destination_liberee, sans_interet = pile.pop(0)
                    case_a_effacer = self[destination_liberee]
                    self.effacer_case(case_a_effacer, secret=True)
                    self.symboles_a_placer.pop(0)  # retiré à l'avant
                    self.symboles_a_placer.append(symbole_a_retirer)  # placé à la fin
            else:
                # impasse détectée
                dernier_placement_OK = True  # réinitialisation
                # effacer la dernière case et restaurer les prétendants
                mon_watchdog.update()
                symbole_a_retirer, destination_problematique, destinations = pile.pop()
                case_a_effacer = self[destination_problematique]
                self.effacer_case(case_a_effacer, secret)
                destinations.remove(destination_problematique)
                self.pioche[symbole_a_retirer].destinations_envisageables = destinations
        self.pioche.deselectionner_tout()
        self.pioche.deselectionner_le_bouton_effacerX()
        self.symbole_actif = None
        self.rafraichir_affichage(secret)
        return True

    def solveur(self):
        """
        Génération d'une grille pleine à partir de l'état actuel de la grille.
        Chaque sac de la pioche est traité en tant qu'ensemble de symboles.
        """
        timer_on(False)
        duree.set("0:00:00")
        self.depart_timer = datetime.now()
        timer_on()
        self.congeler()

        # Élimination des singletons
        singleton_possible = True
        while singleton_possible:
            singleton_possible = False
            for index in range(self.NBR_CASES):
                if len(self[index].pretendants) == 1:
                    symbole = self[index].pretendants[0]
                    self.remplir_case(index, symbole)
                    singleton_possible = True

        # Parcours des combinaisons
        if len(self.symboles_a_placer) > 58:
            timer_on(False)
            return False  # Trop de combinaisons à générer
        self.symboles_a_placer, self.ordre_de_placement =\
            self.pioche.get_symboles_a_placer_et_ordre()
        self.monter_jauge_parcourt_combinaisons()
        pile = list()
        maximum_jauge = [1, 1, 1]
        actuel_jauge = [1, 1, 1]
        dernier_placement_OK = True
        determiner_combinaisons = True
        while self.symboles_a_placer:
            symbole_a_placer = self.symboles_a_placer[0]
            self.activer_le_symbole(symbole_a_placer)
            if determiner_combinaisons:
                self.combinaisons = self.determine_combinaisons(symbole_a_placer)
                self.reglage_maximum_jauge(symbole_a_placer, maximum_jauge, actuel_jauge)
            if self.combinaison_existe() and dernier_placement_OK:
                self.reglage_actuel_jauge(symbole_a_placer, actuel_jauge, maximum_jauge)
                self.combinaison_au_hasard = choice(list(self.combinaisons))
                sauvegarde_combinaisons = self.combinaisons.copy()
                pile.append((symbole_a_placer, self.combinaison_au_hasard, sauvegarde_combinaisons))
                for emplacement in self.combinaison_au_hasard:
                    dernier_placement_OK = dernier_placement_OK and\
                        self.remplir_case(emplacement, symbole_a_placer)
                if not(dernier_placement_OK):
                    for emplacement in self.combinaison_au_hasard:
                        case_a_effacer = self.get_case(emplacement)
                        self.effacer_case(case_a_effacer)
                determiner_combinaisons = True
            elif not(pile):
                print("Cette grille n'admet pas de solution!")
                self.cacher_jauge_parcourt_combinaisons()
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
        self.cacher_jauge_parcourt_combinaisons()
        self.pioche.deselectionner_tout()
        self.pioche.deselectionner_le_bouton_effacerX()
        self.symbole_actif = None
        self.rafraichir_affichage()
        traiter_victoire()
        return True

    def reglage_actuel_jauge(self, symbole_a_placer, actuel_jauge, maximum_jauge):
        """
        On explore d'autres branches en restant à la même profondeur
        """
        if symbole_a_placer == self.ordre_de_placement[0]:
            actuel_jauge[0] = len(self.combinaisons)
            actuel_jauge[1] = maximum_jauge[1]
            actuel_jauge[2] = maximum_jauge[2]
        elif symbole_a_placer == self.ordre_de_placement[1]:
            actuel_jauge[1] = len(self.combinaisons)
            actuel_jauge[2] = maximum_jauge[2]
        elif symbole_a_placer == self.ordre_de_placement[2]:
            actuel_jauge[2] = len(self.combinaisons)
        else:
            return
        self.update_jauge_de_parcourt(maximum_jauge, actuel_jauge)

    def reglage_maximum_jauge(self, symbole_a_placer, maximum_jauge, actuel_jauge):
        """
        On explore une autre branche à une autre profondeur.
        """
        if symbole_a_placer == self.ordre_de_placement[0]:
            maximum_jauge[0] = len(self.combinaisons)
        elif symbole_a_placer == self.ordre_de_placement[1]:
            maximum_jauge[1] = len(self.combinaisons)
        elif symbole_a_placer == self.ordre_de_placement[2]:
            maximum_jauge[2] = len(self.combinaisons)

    def update_jauge_de_parcourt(self, maximum_jauge, actuel_jauge):
        """
        La jauge de parcourt indique la portion parcourue dans l'arbre des
        combinaisons possibles.
        """
        parcourt = 0.1
        if maximum_jauge[0]:
            parcourt += 3*(maximum_jauge[0]-actuel_jauge[0])/maximum_jauge[0]
        if maximum_jauge[1]:
            parcourt += (maximum_jauge[1]-actuel_jauge[1])/maximum_jauge[1]
        if maximum_jauge[2]:
            parcourt += 0.1*(maximum_jauge[2]-actuel_jauge[2])/maximum_jauge[2]
        root.nametowidget(
            str(self.cadre)+".jauge_parcourt_combinaisons")["value"] = parcourt

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
        Retourne True s'il existe au moins une combinaison envisageable,
        False s'il n'y en a plus.
        """
        if len(self.combinaisons):
            return True
        else:
            return False

    def purger(self, niveau):
        """
        Purge la grille jusqu'à avoir un pourcentage de cases non remplies égal à niveau.
        """
        nombre_de_cases_a_placer = int(niveau*self.NBR_CASES/100)
        while len(self.symboles_a_placer) < nombre_de_cases_a_placer:
            index = randrange(81)
            self.effacer_case(self[index], secret=True)
        self.congeler()
        self.rafraichir_affichage()

    def grille_export(self):
        """
        Exporte la grille sudoku sous forme de liste.
        Permet de recommencer une partie.
        """
        grille_en_liste = list()
        for index in range(self.NBR_CASES):
            grille_en_liste.append(self[index].contenu)
        return grille_en_liste

    def grille_export_csv(self):
        """
        Exporte la grille sudoku sous forme de chaîne csv.
        """
        grille_en_chaineCSV = str()
        index = 0
        for ligne in range(self.LARGEUR_GRILLE):
            for colonne in range(self.LARGEUR_GRILLE):
                if self[index].contenu:
                    grille_en_chaineCSV += self[index].contenu
                else:
                    grille_en_chaineCSV += '0'
                if colonne < 8:
                    grille_en_chaineCSV += ';'
                index += 1
            grille_en_chaineCSV += '\n'
        return grille_en_chaineCSV

    def grille_import(self, grille_en_liste, pioche):
        """
        Importe puis affiche une grille transmise sous forme de liste.

        """
        self.effacer_grille()
        for index in range(self.NBR_CASES):
            symbole = grille_en_liste[index]
            if symbole != '0':
                self.remplir_case(index, symbole, secret=True)
        self.congeler()
        self.rafraichir_affichage()

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

    def congeler(self):
        """
        Congélation des cases en place pour obtenir la grille à résoudre.
        """
        cases_congelees = self.destinations_en_place
        for symbole in self.SYMBOLES:
            liste_cases = cases_congelees[symbole]
            for index in liste_cases:
                case_congelee = self.get_case(index)
                case_congelee['state'] = DISABLED

    def file_load(self):
        """
        Charge une grille enregistrée sous forme CSV
        (le format sdk n'est pas encore implémenté)
        """
        fichier = askopenfile(filetypes=(("fichiers Sudoku", "*.sdk"),
                                         ("fichiers CSV", "*.csv"),
                                         ("Tous les fichiers", "*.*")))
        if fichier:
            try:
                extension = fichier.name.rpartition('.')[-1]
                if extension == 'csv':
                    document = reader(fichier, delimiter=";")
                    liste = list()
                    for ligne in document:
                        for symbole in ligne:
                            liste.append(str(symbole))
                self.grille_import(liste, self.pioche)
                self.sauvegarde_partie = self.grille_export()
            except:
                showerror("Problème à l'importation du fichier",
                          "%s\nFormat non compatible" % fichier.name)
            return

    def file_save(self):
        f = asksaveasfile(mode='w',
                          defaultextension=".csv",
                          filetypes=(("fichiers Sudoku", "*.sdk"),
                                     ("fichiers CSV", "*.csv"),
                                     ("Tous les fichiers", "*.*")))
        if f is None:  # if dialog closed with "cancel"
            return
        f.write(self.grille_export_csv())
        f.close()


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
    COULEUR_CARDINAL = 'lavender'

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
               background=self.COULEUR_INITIALE_SAC, # linux et windows
               highlightbackground=self.COULEUR_INITIALE_SAC, # mac osx
               text=symbole).pack(side=TOP, fill=X)
        Label(self,
              name="cardinal",
              font=self.police_cardinal,
              background=self.COULEUR_CARDINAL, 
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
        Cela correspond au nombre de symboles de ce type restant à placer sur la grille.
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
        Génère puis retourne l'ensemble des combinaisons de destinations
        envisageables
        """
        return set(combinations(self.destinations_envisageables,
                                self.cardinal))

    def selectionner(self):
        """
        Change la couleur du fond du bouton sac
        """
        # linux et windows
        root.nametowidget(
            str(self)+".symbole")['background'] = self.COULEUR_SELECTION_SAC
        # mac osx
        root.nametowidget(
            str(self)+".symbole")['highlightbackground'] = self.COULEUR_SELECTION_SAC


    def deselectionner(self):
        """
        Change la couleur du fond du bouton sac
        """
        # linux et windows
        root.nametowidget(
            str(self)+".symbole")['background'] = self.COULEUR_INITIALE_SAC
        # mac osx
        root.nametowidget(
            str(self)+".symbole")['highlightbackground'] = self.COULEUR_INITIALE_SAC


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
    - deselectionner_le_bouton_effacerX
    - basculer_le_bouton_effacerX
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
    COULEUR_DESTINATIONS = 'lavender'
    COULEUR_SELECTION_SAC = 'LightSteelBlue3'
    police_X = "{dyuthi}"

    def __init__(self, cadre):
        """
        Initialisation d'une pioche contenant 9 sacs
        chaque sac contenant chacun 9 symboles identiques
        """
        self.cadre = cadre
        Message(self.cadre,
                name='msg_destinations_envisageables',
                text='Destinations envisageables',
                background=self.COULEUR_DESTINATIONS,
                aspect=200).pack_forget()
        for index in range(1, self.NBR_SACS+1):
            Sac(self.cadre,
                index,
                name='{}'.format(index)).pack(side=LEFT, fill=BOTH, expand=1)
        Button(self.cadre,
               name='x',
               text='X',
               background=self.COULEUR_INITIALE_SAC, # linux et windows
               highlightbackground=self.COULEUR_INITIALE_SAC, # mac osx
               font=self.police_X).pack(
            side=RIGHT, fill=BOTH, expand=True, anchor="se")
        self.symbole_actif = None

    def montrer_destinations_envisageables(self):
        """
        Révèle les destinations envisageables.
        """
        if self.symbole_actif and self.symbole_actif != 'X' and aide_pioche.get():
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

    def deselectionner_le_bouton_effacerX(self):
        """
        Dé-sélectionne le bouton effacer X
        """
        self.symbole_actif = None
        # linux et windows
        root.nametowidget(
            str(self.cadre)+'.x')['background'] = self.COULEUR_INITIALE_SAC
        # mac osx
        root.nametowidget(
            str(self.cadre)+'.x')['highlightbackground'] = self.COULEUR_INITIALE_SAC
        

    def basculer_le_bouton_effacerX(self):
        """
        Affichage : bascule la sélection du X
        """
        if self.symbole_actif == 'X':
            self.deselectionner_tout()
            self.deselectionner_le_bouton_effacerX()
        else:
            self.deselectionner_tout()
            self.symbole_actif = 'X'
            # case X en rouge (linux et windows)
            root.nametowidget(str(self.cadre)+'.x')['background'] = 'red'
            # case X en rouge (osx)
            root.nametowidget(str(self.cadre)+'.x')['highlightbackground'] = 'red'
            

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
        self.deselectionner_le_bouton_effacerX()
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

    def get_symboles_a_placer_et_ordre(self):
        """
        Par lecture de la pioche, cette fonction retourne deux listes:
        - une avec les symboles à placer sur la grille dans l'ordre croissant
        du nombre de combinaisons à calculer
        - une avec l'ordre des symboles_a_placer
        """
        nombres_de_combinaisons = list()
        for symbole in self.SYMBOLES:
            un_sac = self.get_sac(symbole)
            nombres_de_combinaisons.append((un_sac.get_nombre_combinaisons(),
                                            symbole))
        nombres_de_combinaisons_triees = sorted(nombres_de_combinaisons)
        symboles_a_placer = list()
        ordre_de_placement = list()
        while nombres_de_combinaisons_triees:
            nombre_de_combinaisons, symbole = nombres_de_combinaisons_triees.pop(0)
            un_sac = self.get_sac(symbole)
            symboles_a_placer.extend(un_sac.get_symboles_a_placer())
            ordre_de_placement.extend(symbole)
        return (symboles_a_placer, ordre_de_placement)

    def reduire_sac(self, symbole):
        """
        Permet de réduire le nombre de symboles d'un sac de la pioche

        à chaque fois qu'un symbole est placé sur la grille.
        """
        self[symbole].retirer_un_element()

    def remettre_dans_son_sac(self, symbole):
        """
        À chaque fois qu'un symbole est effacé de la grille

        cette fonction permet de le remettre dans le sac de la pioche approprié.
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


def localisation(langue):
    """
    Localisation des inscriptions figurant sur les boutons et les labels.
    """
    bouton_effacer_grille.configure(text={'fr': 'Effacer la grille',
                                          'en': 'Clear grid',
                                          'el': 'Καθαρίστε το πλέγμα'}[langue])
    bouton_remplissage.configure(text={'fr': 'Remplissage complet',
                                       'en': 'Full draw',
                                       'el': 'Αυτόματο γέμισμα'}[langue])
    bouton_congeler.configure(text={'fr': 'Congeler',
                                    'en': 'Freeze',
                                    'el': 'Πάγωμα'}[langue])
    bouton_exemple.configure(text={'fr': 'Exemple difficile',
                                   'en': 'Difficult example',
                                   'el': 'Δύσκολο παράδειγμα'}[langue])
    bouton_solveur.configure(text={'fr': 'Solveur',
                                   'en': 'solver',
                                   'el': 'Λύση'}[langue])
    label_pretendants.configure(text={'fr': 'Prétendants',
                                      'en': 'Suitors',
                                      'el': 'Διαλύτης'}[langue])
    cadre_aides.configure(text={'fr': 'aides',
                                'en': 'Aids',
                                'el': 'Βοηθήματα'}[langue])
    check_grille.configure(text={'fr': "Grille",
                                 'en': "Grid",
                                 'el': "Πλέγμα"}[langue])
    check_pioche.configure(text={'fr': "Pioche",
                                 'en': "Pick",
                                 'el': "Επιλογή"}[langue])
    bouton_index_cases.configure(text={'fr': 'Index des cases',
                                       'en': 'Indexes of Boxes',
                                       'el': 'Δείκτες των τετραγώνων'}[langue])
    bouton_niveaux.configure(text={'fr': "Nouvelle partie",
                                   'en': "New game",
                                   'el': "Νέο παιχνίδι"}[langue])
    echelle_niveaux.configure(label={'fr': 'Niveau (% restant à placer)',
                                     'en': 'Level (remaining percentage)',
                                     'el': "Επίπεδο (% που απομένει)"}[langue])
    bouton_recommencer.configure(text={'fr': "Recommencer",
                                       'en': "Start again",
                                       'el': "Επανεκκίνηση"}[langue])
    label_patientez.configure(text={'fr': "Patientez SVP",
                                    'en': "Please wait",
                                    'el': "Παρακαλώ περιμένετε"}[langue])
    bouton_commencer.configure(text={'fr': "Commencer",
                                     'en': "Start",
                                     'el': "Αρχή"}[langue])
    bouton_quitter.configure(text={'fr': 'Quitter',
                                   'en': 'Quit',
                                   'el': 'Τερματισμός'}[langue])


def file_load():
    """
    Charge un fichier
    """
    grille_sudoku.file_load()
    timer_on(False)
    duree.set("0:00:00")
    # Lancer le chronomètre
    grille_sudoku.depart_timer = datetime.now()
    timer_on()


def file_save():
    """
    Sauvegarde une grille dans un fichier
    """
    grille_sudoku.file_save()


def affichage_pretendants():
    """
    Affiche ou masque les prétendants suivant que la case d'aide est cochée ou non
    """
    if aide_grille.get():
        label_pretendants.pack()
    else:
        label_pretendants.pack_forget()


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


def remplissage():
    """
    Remplissage d'une grille complète
    """
    grille_sudoku.remplissage()


def effacer_grille():
    """
    Efface la grille
    """
    grille_sudoku.effacer_grille()
    label_pretendants.configure(text={'fr': 'Prétendants',
                                      'en': 'Suitors',
                                      'el': 'Διαλύτης'}[langue])


def exemple_diffile():
    """
    Charge un exemple connu (pour analyse ou comparaison)
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
    grille_sudoku.solveur()


def congeler():
    """
    Congèle les symboles en place sur la grille.
    """
    grille_sudoku.congeler()


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


def choix_du_niveau():
    """
    Le joueur vient de lancer une nouvelle partie.
    Cette fonction permet de choisir le niveau de la partie.
    |-----------+---------+-------------+
    | niveau    | restant | pourcentage |
    |-----------+---------+-------------+
    | Débutant  |      24 |          30 |
    |-----------+---------+-------------+
    | Facile    |      37 |          46 |
    |-----------+---------+-------------+
    | Moyen     |      48 |          59 |
    |-----------+---------+-------------+
    | Difficile |      52 |          64 |
    |-----------+---------+-------------+
    | Extrême   |      56 |          69 |
    """
    # Arrêter le chronomètre (au cas où le joueur a lancé la nouvelle partie
    # pour interrompre une partie précédente)
    timer_on(False)
    duree.set("0:00:00")
    # Désactiver les boutons
    for child in les_boutons.winfo_children():
        child.configure(state=DISABLED)
    # Afficher l'interface permettant de choisir le niveau
    echelle_niveaux.pack(padx=5, pady=5)
    echelle_niveaux.set(50)
    bouton_commencer.configure(state=DISABLED)
    bouton_recommencer.configure(state=DISABLED)
    bouton_commencer.pack()
    label_patientez.pack()
    # Procéder au remplissage d'une grille complète
    grille_sudoku.remplissage(secret=True)
    label_patientez.pack_forget()
    bouton_index_cases.configure(state=DISABLED)
    bouton_niveaux.configure(state=DISABLED)
    echelle_niveaux.configure(state=NORMAL)
    bouton_commencer.configure(state=NORMAL)


def timer_on(on=True):
    """
    Permet de chronométrer le temps de résolution
    """
    global after_id
    if on:
        difference = datetime.now()-grille_sudoku.depart_timer
        duree.set(str(difference).split('.', 2)[0])
        after_id = root.after(1000, timer_on)
    elif after_id is not None:
        root.after_cancel(after_id)
        after_id = None


def anglais():
    """
    Passe l'interface en anglais
    """
    global langue
    langue = 'en'
    localisation(langue)


def francais():
    """
    Passe l'interface en français
    """
    global langue
    langue = 'fr'
    localisation(langue)


def grec():
    """
    Passe l'interface en grec
    """
    global langue
    langue = 'el'
    localisation(langue)


def recommencer_la_partie():
    """
    Permet de recommencer la partie précédente.
    """
    grille_sudoku.grille_import(grille_sudoku.sauvegarde_partie, pioche_sudoku)
    # Lancer le chronomètre
    grille_sudoku.depart_timer = datetime.now()
    timer_on()


def commencer_la_partie():
    """
    Commence la partie
    """
    bouton_index_cases.configure(state=NORMAL)
    bouton_commencer.configure(state=DISABLED)
    echelle_niveaux.configure(state=DISABLED)
    bouton_recommencer.configure(state=NORMAL)
    bouton_niveaux.configure(state=NORMAL)
    # Préparer la grille pour le niveau choisi par le joueur
    niveau = echelle_niveaux.get()
    grille_sudoku.purger(niveau)
    grille_sudoku.sauvegarde_partie = grille_sudoku.grille_export()
    # Lancer le chronomètre
    grille_sudoku.depart_timer = datetime.now()
    timer_on()
    # Afficher les boutons de gauche car un abandon est toujours possible
    for child in les_boutons.winfo_children():
        child.configure(state=NORMAL)


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
        grille_sudoku.basculer_le_bouton_effacerX()

    # Sélectionne le symbole actif si un sac de la pioche est cliqué
    if type(event.widget.master) == Sac:
        symbole_a_activer = event.widget.master.symbole
        grille_sudoku.activer_le_symbole(symbole_a_activer)

    # Si une case de la grille est cliquée
    if (type(event.widget) == Case) and (event.widget['state'] == ACTIVE):
        if pioche_sudoku.get_symbole_actif() == 'X':
            if event.widget.contenu is None:
                pass  # ne rien faire (case déjà vide)
            else:
                grille_sudoku.effacer_case(event.widget)
        else:
            grille_sudoku.remplir_case(event.widget.index,
                                       pioche_sudoku.get_symbole_actif())
    # Sélectionne le symbole actif si une case pleine est cliquée
    if (type(event.widget) == Case) and (event.widget.contenu) and bouton_commencer['state'] == DISABLED:
        symbole_a_activer = event.widget.contenu
        grille_sudoku.activer_le_symbole(symbole_a_activer)
    # Victoire détectée
    if not(grille_sudoku.symboles_a_placer):
        traiter_victoire()


def traiter_victoire():
    """
    En cas de résolution réussie:
    - le timer est arrêté et affiché sur fond vert
    - les symboles sont affichés en vert 
    """
    timer_on(False)
    label_timer.configure(background=COULEUR_VICTOIRE)
    grille_sudoku.afficher_la_victoire()


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
    Si la souris survole le nombre de symbole restants dans la pioche les
    destinations envisageables s'affichent.
    """
    global langue
    if type(event.widget) == Case:
        label_pretendants['text'] = event.widget.pretendants
    elif type(event.widget) == Label and type(event.widget.master) == Sac:
        pioche_sudoku.montrer_destinations_envisageables()
    elif type(event.widget) != Label:
        # Mise à jour du menu (utile en cas de changement de langue)
        updatemenu()
    else:
        label_pretendants.configure(text={'fr': 'Prétendants',
                                          'en': 'Suitors',
                                          'el': 'Διαλύτης'}[langue])


def gestion_des_evenements_on_mouse_leave(event):
    """
    Contrôle de passage à autre chose après victoire.
    """
    if grille_sudoku.symboles_a_placer:
        label_timer.configure(background=COULEUR_TIMER)


def updatemenu():
    """
    Permet:
    - la mise à jour du menu en tenant compte de la langue sélectionnée
    - d'afficher ou de cacher outils et chronomètre.
    """
    if system() == 'Darwin': # C'est un mac
        # Sur mac il y a d'office un menu Python en première position
        MENU1, MENU2, MENU3 = (2,3,4)        
    else:
        MENU1, MENU2, MENU3 = (1,2,3)
    global langue, afficher_outils, afficher_chronometre
    menubar.entryconfig(MENU1, label={'fr': 'Fichier',
                                             'en': 'File',
                                             'el': 'Αρχείο'}[langue])
    menubar.entryconfig(MENU2, label={'fr': 'Langue',
                                            'en': 'Language',
                                            'el': 'Γλώσσα'}[langue])
    menubar.entryconfig(MENU3, label={'fr': 'Afficher',
                                              'en': 'Display',
                                              'el': 'Απεικόνιση'}[langue])
    menu_fichiers.entryconfig(0, label={'fr': 'Effacer la grille',
                                        'en': 'Clear grid',
                                        'el': 'Καθαρίστε το πλέγμα'}[langue])
    menu_fichiers.entryconfig(1, label={'fr': 'Ouvrir...',
                                        'en': 'Open...',
                                        'el': 'Άνοιγμα...'}[langue])
    menu_fichiers.entryconfig(2, label={'fr': 'Enregistrer',
                                        'en': 'Save',
                                        'el': 'Αποθήκευση'}[langue])
    menu_fichiers.entryconfig(4, label={'fr': 'Quitter',
                                        'en': 'Quit',
                                        'el': 'Τερματισμός'}[langue])
    menu_afficher.entryconfig(0, label={'fr': "Outils développeur",
                                        'en': 'Developer Tools',
                                        'el': "Εργαλεία προγραμματιστή"}[langue])
    menu_afficher.entryconfig(1, label={'fr': "Chronomètre",
                                        'en': 'Stopwatch',
                                        'el': "Χρονόμετρο"}[langue])
    menu_afficher.entryconfig(2, label={'fr': 'À propos',
                                        'en': 'About',
                                        'el': 'Σχετικά με'}[langue])
    

    # Afficher/cacher les outils
    if afficher_outils.get() and afficher_chronometre.get():
        label_timer.pack_forget()
        les_boutons.pack(padx=5, pady=5, side=TOP)
        label_timer.pack(padx=15, pady=10, ipadx=5)
    elif afficher_outils.get():
        les_boutons.pack(padx=5, pady=5, side=TOP)
        label_timer.pack_forget()
    elif afficher_chronometre.get():
        label_timer.pack(padx=15, pady=10, ipadx=5)
        les_boutons.pack_forget()
    else:
        les_boutons.pack_forget()
        label_timer.pack_forget()


def ouvre_lien(event):
    """
    Ouvre le lien github dans le navigateur
    """
    open_new(event.widget.cget("text"))


def apropos():
    """
    Fenêtre à propos: renseigne sur l'auteur et date
    """
    global langue
    top = Toplevel(root)
    titre_fenetre = {'fr': 'À propos de SUDOKU SudoCool',
                     'en': 'About SUDOKU SudoCool',
                     'el': 'Σχετικά με SUDOKU SudoCool'}[langue]
    top.title(titre_fenetre)
    auteur = Label(top, text="Raoul HATTERER")
    date = Label(top, text="2019")
    auteur.pack(padx=20, pady=10)
    date.pack(padx=20, pady=5)
    lien = Label(top, text=r"https://github.com/raoulhatterer",
                 fg="blue", cursor="hand2")
    lien.pack(padx=5)
    lien.bind("<Button-1>", ouvre_lien)
    if system() == 'Darwin':
        # effets de bord avec Toplevel sous mac
        # pis allé : on quitte l'application 
        bouton_quitter_top = Button(top, text='Quitter', command=top.quit)
    else:
        bouton_quitter_top = Button(top, text='OK', command=top.destroy)        
    bouton_quitter_top.pack(padx=40, pady=10)

# CONSTANTES

COULEUR_CADRE_HAUT = 'lavender'
COULEUR_CADRE_GAUCHE = 'lavender'
COULEUR_CADRE_CENTRAL = 'lavender'
COULEUR_CADRE_DROITE = 'lavender'
COULEUR_SEPARATION = 'lavender'
COULEUR_PIOCHE = 'lavender'
COULEUR_TIMER = 'lavender'
COULEUR_CADRE_BAS = 'lavender'
COULEUR_VICTOIRE = 'green2'
COULEUR_BOUTON = '#d9d9d9'
# Niveau par défaut
niveau = 30


# APPLICATION Tkinter

root = Tk()
root.title('SUDOKU SudoCool')
# Aides checkbox grille et pioche
aide_grille = IntVar()
aide_pioche = IntVar()
# Timer
duree = StringVar()
duree.set("0:00:00")
after_id = None

# Création des conteneurs principaux
cadre_haut = Frame(root,
                   background=COULEUR_CADRE_HAUT,
                   width=640, height=20)
cadre_gauche = Frame(root,
                     background=COULEUR_CADRE_GAUCHE,
                     height=400)
cadre_central = Frame(root,
                      background=COULEUR_CADRE_CENTRAL)
cadre_droite = Frame(root,
                     background=COULEUR_CADRE_DROITE)
cadre_separation_verticale = Frame(root,
                                   background=COULEUR_SEPARATION,
                                   height=20)
cadre_pioche = Frame(root,
                     background=COULEUR_PIOCHE,
                     height=120)
cadre_bas = Frame(root,
                  background=COULEUR_CADRE_BAS,
                  height=60)

# Placement des conteneurs principaux
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
les_boutons = Frame(cadre_gauche, background=COULEUR_CADRE_GAUCHE)

bouton_effacer_grille = Button(les_boutons,
                               background=COULEUR_BOUTON, # linux et windows
                               highlightbackground=COULEUR_BOUTON, # mac osx
                               command=effacer_grille)
bouton_remplissage = Button(les_boutons,
                            background=COULEUR_BOUTON, # linux et windows
                            highlightbackground=COULEUR_BOUTON, # mac osx
                            command=remplissage)
bouton_congeler = Button(les_boutons,
                         background=COULEUR_BOUTON, # linux et windows
                         highlightbackground=COULEUR_BOUTON, # mac osx
                         command=congeler)
bouton_exemple = Button(les_boutons,
                        background=COULEUR_BOUTON, # linux et windows
                        highlightbackground=COULEUR_BOUTON, # mac osx
                        command=exemple_diffile)
bouton_solveur = Button(les_boutons,
                        background=COULEUR_BOUTON, # linux et windows
                        highlightbackground=COULEUR_BOUTON, # mac osx
                        foreground='saddle brown',
                        command=solveur)
label_timer = Label(cadre_gauche, textvariable=duree,
                    font=('Helvetica', 24), relief=SUNKEN)
jauge_de_remplissage = ttk.Progressbar(cadre_gauche,
                                       orient="vertical",
                                       length=200,
                                       maximum=81,
                                       mode="determinate")

# Création des éléments dans le cadre de droite

cadre_pretendants = Frame(cadre_droite, background=COULEUR_CADRE_DROITE)
label_pretendants = Label(cadre_pretendants,
                          background=COULEUR_CADRE_DROITE)
cadre_jouer = Frame(cadre_droite, background=COULEUR_CADRE_DROITE)
cadre_aides = LabelFrame(cadre_jouer,
                         background=COULEUR_CADRE_DROITE)
check_grille = Checkbutton(cadre_aides,
                           variable=aide_grille,
                           onvalue=1, offvalue=0,
                           background=COULEUR_CADRE_DROITE,
                           command=affichage_pretendants)
check_pioche = Checkbutton(cadre_aides,
                           variable=aide_pioche, onvalue=1,
                           offvalue=0,
                           background=COULEUR_CADRE_DROITE)
bouton_index_cases = Button(cadre_jouer,
                            background=COULEUR_BOUTON)
bouton_niveaux = Button(cadre_jouer,
                        font=('Helvetica', 12),
                        background='LightSteelBlue3', # linux windows
                        highlightbackground='LightSteelBlue3', # mac osx                       
                        command=choix_du_niveau)
echelle_niveaux = Scale(cadre_jouer, orient='horizontal',
                        from_=30, to=70,
                        background=COULEUR_CADRE_DROITE,
                        resolution=1, tickinterval=5,
                        length=200)
label_patientez = Label(cadre_jouer,
                        background=COULEUR_CADRE_DROITE)
bouton_commencer = Button(cadre_jouer,
                          font=('Helvetica', 16),
                          background='LightSteelBlue3', # linux et windows
                          highlightbackground='LightSteelBlue3', # mac osx       
                          command=commencer_la_partie)
bouton_recommencer = Button(cadre_jouer,
                            background=COULEUR_BOUTON, # linux et windows
                            highlightbackground=COULEUR_BOUTON, # mac osx
                            state=DISABLED,
                            command=recommencer_la_partie)

# placement des widgets à l'écran
les_boutons.pack(padx=5, pady=5, side=TOP)
bouton_effacer_grille.pack(fill=X)
bouton_remplissage.pack(fill=X)
bouton_congeler.pack(fill=X)
bouton_exemple.pack(fill=X)
bouton_solveur.pack(fill=X, pady=10)
label_timer.pack(padx=15, pady=10, ipadx=5)
cadre_pretendants.pack(padx=5)
cadre_jouer.pack(padx=5, pady=5)
cadre_aides.pack(fill=X, pady=15)
check_grille.pack(fill=X, side=LEFT)
check_pioche.pack(fill=X, side=LEFT)
bouton_index_cases.pack(fill=X)
bouton_niveaux.pack(fill=X, pady=5)
bouton_recommencer.pack(fill=X)
jauge_de_remplissage.pack(side=BOTTOM)

# Disposition du conteneur cadre_bas
cadre_bas.columnconfigure(0, weight=1)

# Création du bouton quitter dans cadre_bas
bouton_quitter = Button(cadre_bas,
                        background=COULEUR_BOUTON, # linux et windows
                        highlightbackground=COULEUR_BOUTON, # mac osx
                        command=root.quit)

# Disposition du bouton quitter
bouton_quitter.grid(sticky="nsew")
localisation(langue)


# MENU

# Ne pas afficher les outils développeur au démarrage
afficher_outils = BooleanVar()
afficher_outils.set(False)
# Afficher le chronomètre au démarrage
afficher_chronometre = BooleanVar()
afficher_chronometre.set(True)

# crée une barre de menu
menubar = Menu(root)
# crée un menu pulldown 'menu_fichier'
menu_fichiers = Menu(menubar, tearoff=0, postcommand=updatemenu)
menu_fichiers.add_command(command=effacer_grille)
menu_fichiers.add_command(command=file_load)
menu_fichiers.add_command(command=file_save)
menu_fichiers.add_separator()
menu_fichiers.add_command(command=root.quit)
# ajoute 'menu_fichier' à 'menubar'
menubar.add_cascade(menu=menu_fichiers, label='Fichier')
# crée un menu pulldown 'menu_langue'
menu_langue = Menu(menubar, tearoff=0, postcommand=updatemenu)
menu_langue.add_command(label='English', command=anglais)
menu_langue.add_command(label='Français', command=francais)
menu_langue.add_command(label='Ελληνικά', command=grec)
# ajoute 'menu_langue' à 'menubar'
menubar.add_cascade(menu=menu_langue, label='Langue')
# crée un menu pulldown 'menu_langue'
menu_afficher = Menu(menubar, tearoff=0, postcommand=updatemenu)
menu_afficher.add_checkbutton(onvalue=True, offvalue=False, variable=afficher_outils)
menu_afficher.add_checkbutton(onvalue=True, offvalue=False, variable=afficher_chronometre)
menu_afficher.add_command(command=apropos)
# ajoute 'menu_afficher' à 'menubar'
menubar.add_cascade(menu=menu_afficher, label='Afficher')
# affiche le menu
updatemenu()
root.config(menu=menubar)


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
