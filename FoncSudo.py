# -*- coding: cp1252 -*-
#------------------------------------------------------------------
#
#              Fonctions pour le SUDOKU
#
#        Jean-Luc COSSALTER
#           06/2019
#
#------------------------------------------------------------------
import random
from random import *


def intersection_2_listes(L1=[], L2=[]):
    result = []
    if len(L1)==0 or len(L2)==0:
        return []
    for n in L1:
        for x in L2:
            if n == x and n not in result:
                result.append(n)
    result.sort()
 
    return result


#------------   pour savoir si les 9 chiffres sont presents dans une liste de 9
def est_complet(a_tester=[1,2,3,4,5,6,7,8,9]):
    liste=[1,2,3,4,5,6,7,8,9]  
    index=0
    while index<9 :
        if a_tester[index] in liste :
            liste.remove(a_tester[index])
        else :
            return False
        index=index+1
    return True


#----------- pour savoir les chiffres qui restent ----------------------------
def reste(liste_a_tester):
    liste=[1,2,3,4,5,6,7,8,9]
    for index in range(9):
        if liste_a_tester[index] in liste :
            liste.remove(liste_a_tester[index])
    return liste


# -------------teste si les 9 chiffres sont presents dans toutes les lignes
def teste_ligne(grille_a_tester):
    j=0
    while j<9 :
        mot_a_tester=[]
        for i in range(9) :
            mot_a_tester.append(grille_a_tester[j][i])
        if not est_complet(mot_a_tester):
            return False
        j=j+1
    return True

# -------------teste si les 9 chiffres sont presents dans toutes les colonnes
def teste_colonne(grille_a_tester):
    colonne=0
    while colonne<9 :
        mot_a_tester=[]
        for index in range(9) :
            mot_a_tester.append(grille_a_tester[index][colonne])
        
        if not est_complet(mot_a_tester):
            return False
        colonne= colonne + 1
    return True


# -------------teste si les 9 chiffres sont presents dans tous les carres
def teste_carrlpe(grille_a_tester) :
    carre=0
    while carre<9 :
        mot_a_tester=[]
        for i in range(9) :
            mot_a_tester.append(
                grille_a_tester[i % 3 + 3 * (carre % 3)][i // 3 + 3 * (carre // 3)])
        if not est_complet(mot_a_tester):
            return False
        carre= carre + 1
    return True

# -------------teste si les 9 chiffres sont presents LCC

def test_complet(grille_a_tester):
    if not teste_ligne(grille_a_tester):
        return False
    elif not teste_colonne(grille_a_tester):
        return False
    elif not teste_carre(grille_a_tester):
        return False
    else :
        return True


# -------------quels sont les chiffres qui restent a mettre dans une  colonne
def reste_colonne(grille_a_tester,colonne):
    mot_a_tester=[]
    for i in range(9) :
        mot_a_tester.append(grille_a_tester[i][colonne])
    return reste(mot_a_tester)


# -------------quels sont les chiffres qui restent a mettre dans une ligne
def reste_ligne(grille_a_tester,ligne):
    mot_a_tester=[]
    for index in range(9) :
        mot_a_tester.append(grille_a_tester[ligne][index])
    return reste(mot_a_tester)

# -------------quels sont les chiffres qui restent a mettre dans le carre
def reste_carre(grille_a_tester,ligne,colonne):
    mot_a_tester=[]
    position_carre=3*(ligne//3)+colonne//3
    for index in range(9) :
        mot_a_tester.append(
            grille_a_tester[index//3+3*(position_carre//3)][index%3+3*(position_carre % 3)])
    return reste(mot_a_tester)


# ----------- finalement aux coordonnees donnees que reste-t-il comme chiffre possible

def reste_possible(grille_a_tester,ligne,colonne):
    if (grille_a_tester[ligne][colonne]>0) :
        return []
    reste1=reste_ligne(grille_a_tester,ligne)
    reste2=reste_colonne(grille_a_tester,colonne)
    reste3=reste_carre(grille_a_tester,ligne,colonne)
    reste4 = intersection_2_listes(reste1,reste2)
    reste=intersection_2_listes(reste4,reste3)
    return reste

# ----------------- Fonctions pour la création des grilles --------------------------------

def reste_possible_creation(grille_a_tester,ligne,colonne):
    
    reste1=reste_ligne(grille_a_tester,ligne)
    reste2=reste_colonne(grille_a_tester,colonne)
    reste3=reste_carre(grille_a_tester,ligne,colonne)
    reste4 = intersection_2_listes(reste1,reste2)
    reste=intersection_2_listes(reste4,reste3)
    return reste


    
#________________ inverser 2 chiffres d une grille ________________________


def inverser_nombres_grille(tab,nombre1,nombre2):
    for i in range(9):
        for j in range(9):
            fait=False
            if tab[i][j]==nombre1 and not fait:
                tab[i][j]=nombre2
                fait=True
            if tab[i][j]==nombre2 and not fait:
                tab[i][j]=nombre1
                fait=True
    return tab
               
#________________inverser 2 colonnes ________________________________
                

def inverser_colonnes(tab,colonne1,colonne2):
    if colonne1//3==colonne2//3:
        for i in range(9):
            temp=tab[i][colonne1]
            tab[i][colonne1]=tab[i][colonne2]
            tab[i][colonne2]=temp
    return tab
    

#________________inverser 2 lignes ________________________________
                

def inverser_lignes(tab,ligne1,ligne2):
    if ligne1//3==ligne2//3:
        for i in range(9):
            temp=tab[ligne1][i]
            tab[ligne1][i]=tab[ligne2][i]
            tab[ligne2][i]=temp
    return tab
    

#_________________melange aleatoire des nombres d'une grille________________

def melange_nombre_grille(tab):
    a = range(1,10)
    b = [1,2,3,4,5,6,7,8,9]
    shuffle(b)
    for i in range(9):
        for j in range(9):
            if tab[i][j]>0:
                tab[i][j]=b[tab[i][j]-1]
    return tab
           


#_________________melange aleatoire 3 grandes colonnes__________

def change_3_col(tableau):
    a = range(3)
    b = [0,1,2]
    shuffle(b)
    tab_temp=[]

    for lign in range(9):
        tab_temp.append(tableau[lign][:])  
    
    for colon in range(9):
        for lign in range(9):
            tableau[lign][colon]=tab_temp[lign][(b[colon//3]-a[colon//3])*3+colon]
            
    return tableau
           



#_________________melange aleatoire 3 grandes lignes____________________

def change_3_lign(tableau):
    a = range(3)
    b = [0,1,2]
    shuffle(b)
    tab_temp=[]

    for lign in range(9):
        tab_temp.append(tableau[lign][:])
    
    for lign in range(9):
        for colon in range(9):
            tableau[lign][colon]=tab_temp[(b[lign//3]-a[lign//3])*3+lign][colon]
            
    return tableau
           


#_________________melange aleatoire 3 petites colonnes__________

def change_3_petites_col(tableau):
    b = [0,1,2]
    
    tab_temp=[]
    for lign in range(9):
        tab_temp.append(tableau[lign][:])
   
    shuffle(b)
    for colon in range(3):
        for lign in range(9):
            tableau[lign][colon]=tab_temp[lign][b[colon]]

    shuffle(b)
    for colon in range(3,6):
        for lign in range(9):
            tableau[lign][colon]=tab_temp[lign][b[colon-3]+3]
            
    shuffle(b)
    for colon in range(6,9):
        for lign in range(9):
            tableau[lign][colon]=tab_temp[lign][b[colon-6]+6]
            
            
    return tableau


#_________________melange aleatoire 3 petites lignes__________

def change_3_petites_lignes(tableau):
    b = [0,1,2]
    tab_temp=[]
    for lign in range(9):
        tab_temp.append(tableau[lign][:])
   
    shuffle(b)
    for lign in range(3):
        for colon in range(9):
            tableau[lign][colon]=tab_temp[b[lign]][colon]
            
    shuffle(b)
    for lign in range(3,6):
        for colon in range(9):
            tableau[lign][colon]=tab_temp[b[lign-3]+3][colon]

    shuffle(b)
    for lign in range(6,9):
        for colon in range(9):
            tableau[lign][colon]=tab_temp[b[lign-6]+6][colon]
            
            
    return tableau

# ______________pour la creation : supprime la valeur d'une case aleatoirement

def supprimer_nombre_simple(tableau):
    lign=randint(0,8)
    colon=randint(0,8)
    
    if (tableau[lign][colon]!=0) and  len(reste_possible_creation(tableau,lign,colon))==0:
        tableau[lign][colon]=0
    return tableau

def supprimer_nombre(tableau):
    lign=randint(0,8)
    colon=randint(0,8)
    copie=[[0]*9 for i in range(9)]
    for i in range(9):
        copie[i]=tableau[i][:]
    copie[lign][colon]=0
    if teste_ligne(resolution(copie)):
        tableau[lign][colon]=0
    return tableau




#----------------------   CREATION GRILLE   ---------------------------------      
    
def creation_aleatoire(grille_s,grille_d,difficulte) :
    grille_s=melange_nombre_grille(grille_s)
    grille_s=change_3_col(grille_s)
    grille_s=change_3_lign(grille_s)
    grille_s=change_3_petites_col(grille_s)
    grille_s=change_3_petites_lignes(grille_s)
    if difficulte<5 :
        for i in range(10+8*difficulte):
           supprimer_nombre_simple(grille_s)
    elif difficulte<10 :
        for i in range(20):
            supprimer_nombre_simple(grille_s)
        for j in range(difficulte*5):
            supprimer_nombre(grille_s)
    elif difficulte<18 :
        for i in range(30+difficulte*3):
            supprimer_nombre(grille_s)
    elif difficulte<20 :
        for i in range(30+difficulte*3):
            supprimer_nombre(grille_s)
        for i in range(9):
            for j in range(9):
                if grille_s[i][j]!=0:
                    copie=[[0]*9 for i in range(9)]
                    for i in range(9):
                        copie[i]=grille_s[i][:]
                    copie[i][j]=0
                    if teste_ligne(resolution(copie)):
                        grille_s[i][j]=0
    else :
        grille17=[[1,0,0,0,0,0,5,2,0],
                  [0,0,0,0,7,8,0,0,0],
                  [0,0,0,0,0,0,6,0,0],
                  [0,9,0,0,4,0,0,0,0],
                  [0,0,0,5,0,0,1,0,0],
                  [0,7,0,0,0,0,0,0,0],
                  [0,0,6,2,0,0,0,0,0],
                  [0,4,0,0,0,0,0,7,8],
                  [0,0,0,0,0,0,0,0,3]]
        for i in range(9):
            for j in range(9):
                grille_s[i][j]=grille17[i][j]
        grille_s=melange_nombre_grille(grille_s)
        grille_s=change_3_col(grille_s)
        grille_s=change_3_lign(grille_s)
        grille_s=change_3_petites_col(grille_s)
        grille_s=change_3_petites_lignes(grille_s)
    for i in range(9) :
        for j in range(9):
            grille_d[i][j] = grille_s[i][j]
    return grille_s,grille_d
    
#___________creation_aleatoire(grille_sudoku,grille_depart)__________________













#----------------------------------------------------------------------------
#
#                FONCTIONS DE RESOLUTION
#____________________________________________________________________________


def grille_des_possibles(tab):
    gdp=[]
    for ligne in range(9):
        ldp=[]
        for colonne in range(9):
            ldp.append(reste_possible(tab,ligne,colonne))
        gdp.append(ldp)
    return gdp
            

def ou_le_nombre_peut_etre(tab,nombre):
    possible = [[1]*9 for i in range(9)]
    
#remplissage matrice des possibles
#----- singleton cache -------------------------------------------------  
    for i in range(9):
        for j in range(9) :
            if tab[i][j]!=0:
                possible[i][j]=0
            if tab[i][j]==nombre:
                carre=3*(i//3)+j//3
                for k in range(9):
                    possible[i][k]=0
                    possible[k][j]=0
                    possible[3*(carre//3)+k//3][3*(carre%3)+k%3]=0

#______ singleton cache fin       ______________________________________
                    
                    
#--------------Elimination indirecte-----------------------------------
    for carre in range(9):
        debut_ligne=10
        fin_ligne=11
        for i in range(3) :
            for j in range(3):
                if possible[3*(carre//3) +i][3*(carre%3)+j]==1 and debut_ligne==10:
                    debut_ligne = 3*(carre//3) +i
                elif possible[3*(carre//3) +i][3*(carre%3)+j]==1:
                    fin_ligne = 3*(carre//3) +i
        if debut_ligne==fin_ligne :
            for j in range(9):
                if j!=3*(carre%3) and j!=3*(carre%3)+1 and j!=3*(carre%3)+2 :
                    possible[debut_ligne][j]=0
  

    for carre in range(9):
        debut_colonne=10
        fin_colonne=11
        for j in range(3) :
            for i in range(3):
                if possible[3*(carre//3) +i][3*(carre%3)+j]==1 and debut_colonne==10:
                    debut_colonne = 3*(carre%3) +j
                elif possible[3*(carre//3) +i][3*(carre%3)+j]==1:
                    fin_colonne = 3*(carre%3) +j
        if debut_colonne==fin_colonne :
            for i in range(9):
                if i!=3*(carre//3) and i!=3*(carre//3)+1 and i!=3*(carre//3)+2 :
                    possible[i][debut_colonne]=0 

#Elimination indirecte fin _____________________________________________________    
                    
  
#analyse des lignes
    for lign in range(9):
        resultat=[]
        nombre_de_1=0
        for colon in range(9):
            if possible[lign][colon]==1:
                resultat.append([lign,colon])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
        
    

#analyse des colonnes

    for j in range(9):
    
        resultat=[]
        nombre_de_1=0
        for k in range(9):
            if possible[k][j]==1:
                resultat.append([k,j])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
        
     
        
#analyse des carres 3X3

    for carre in range(9):
        resultat=[]
        nombre_de_1=0
        for k in range(9):
            if possible[3*(carre//3)+k//3][3*(carre%3)+k%3]==1:
                resultat.append([3*(carre//3)+k//3,3*(carre%3)+k%3])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
    return resultat        
        
#___________________ fin ou_le_nombre_peut_etre_________________________________

# ---------  fonctions gerant a la fois tous les groupes nus de toutes tailles -------

def groupes_nus_ligne(grille_pos,ligne):
    for colonne in range(9):
        liste_index=[]
        liste=grille_pos[ligne][colonne]
        for index in range(9):
            if intersection_2_listes(liste,grille_pos[ligne][index])==\
               grille_pos[ligne][index]\
            and len(liste)>1\
            and len(grille_pos[ligne][index])>1:
                liste_index.append(index)
        if len(liste)==len(liste_index) :
            for index in range(9) :
                if index not in liste_index :
                    for element in liste :
                        if element in grille_pos[ligne][index] :
                            grille_pos[ligne][index].remove(element)
    return grille_pos

def groupes_nus_colonne(grille_pos,colonne):
    for ligne in range(9):
        liste_inclus=[]
        liste=grille_pos[ligne][colonne]
        for index in range(9):
            if intersection_2_listes(liste,\
                                     grille_pos[index][colonne])==grille_pos[index][colonne]\
            and len(liste)>1\
            and len(grille_pos[index][colonne])>1:
                liste_inclus.append(index)
        if len(liste)==len(liste_inclus) :
            for index in range(9) :
                if index not in liste_inclus :
                    for element in liste :
                        if element in grille_pos[index][colonne]:
                            grille_pos[index][colonne].remove(element)
    return grille_pos

def groupes_nus_carre(grille_pos,carre):
    for position in range(9):
        liste_inclus=[]
        liste=grille_pos[3*(carre//3)+position//3][3*(carre%3)+position%3]
        for index in range(9):
            if intersection_2_listes(liste,\
                                     grille_pos[3*(carre//3)+index//3][3*(carre%3)+index%3])==\
                                     grille_pos[3*(carre//3)+index//3][3*(carre%3)+index%3]\
            and len(liste)>1\
            and len(grille_pos[3*(carre//3)+index//3][3*(carre%3)+index%3])>1:
                liste_inclus.append(index)
        if len(liste)==len(liste_inclus) :
            for index in range(9) :
                if index not in liste_inclus :
                    for element in liste :
                        if element in grille_pos[3*(carre//3)+index//3][3*(carre%3)+index%3]:
                            grille_pos[3*(carre//3)+index//3]\
                                [3*(carre%3)+index%3].remove(element)
    return grille_pos

#____FIN  fonctions gerant a la fois les groupes nus de toutes tailles________________


# ---------  fonctions gerant tous les groupes cachés de toutes tailles -------

def groupes_caches_ligne(grille_pos):
    for ligne in range(9):
        liste_positions =[]
        for chiffre in range(1,10) :
            positions=[]
            for colonne in range(9) :
                if chiffre in grille_pos[ligne][colonne] :
                    positions.append(colonne)
            liste_positions.append(positions)
        for colonne in range(9):
            liste_index=[]
            liste=liste_positions[colonne]
            for index in range(9):
                if intersection_2_listes(liste,liste_positions[index])==\
                   liste_positions[index] and len(liste)>1\
                and len(liste_positions[index])>1:
                    liste_index.append(index)
            if len(liste_positions[colonne])==len(liste_index) and len(liste_index)>0 :
                valeurs=[]
                for j in range(len(liste_index)) : valeurs.append(liste_index[j]+1)
                for k in liste_positions[colonne] :
                    for val in range(1,10) :
                        if val in grille_pos[ligne][k] and val not in valeurs :
                            grille_pos[ligne][k].remove(val)
        
    return grille_pos


def groupes_caches_carre(grille_pos):
    for carre in range(9):
        liste_positions =[]
        for chiffre in range(1,10) :
            positions=[]
            for index_carre in range(9) :
                if chiffre in grille_pos[3*(carre//3)+index_carre//3]\
                   [3*(carre%3)+index_carre%3] :
                    positions.append(index_carre)
            liste_positions.append(positions)
        for index_carre in range(9):
            liste_index=[]
            liste=liste_positions[index_carre]
            for index in range(9):
                if intersection_2_listes(liste,liste_positions[index])==\
                   liste_positions[index] and len(liste)>1\
                and len(liste_positions[index])>1:
                    liste_index.append(index)
            if len(liste_positions[index_carre])==len(liste_index) and len(liste_index)>0 :
                valeurs=[]
                for j in range(len(liste_index)) : valeurs.append(liste_index[j]+1)
                for k in liste_positions[index_carre] :
                    for val in range(1,10) :
                        if val in grille_pos[3*(carre//3)+k//3][3*(carre%3)+k%3]\
                        and val not in valeurs :
                            grille_pos[3*(carre//3)+k//3][3*(carre%3)+k%3].remove(val)
    return grille_pos


def groupes_caches_colonne(grille_pos):
    for colonne in range(9):
        liste_positions =[]
        for chiffre in range(1,10) :
            positions=[]
            for ligne in range(9) :
                if chiffre in grille_pos[ligne][colonne] :
                    positions.append(ligne)
                    
            liste_positions.append(positions)
            
        for ligne in range(9):
            liste_index=[]
            liste=liste_positions[ligne]
            for index in range(9):
                if intersection_2_listes(liste,liste_positions[index])==liste_positions[index]\
                and len(liste)>1\
                and len(liste_positions[index])>1:
                    liste_index.append(index)
            if len(liste_positions[ligne])==len(liste_index) and len(liste_index)>0 :
                valeurs=[]
                for j in range(len(liste_index)) : valeurs.append(liste_index[j]+1)
                for k in liste_positions[ligne] :
                    for val in range(1,10) :
                        if val in grille_pos[k][colonne] and val not in valeurs :
                            grille_pos[k][colonne].remove(val)
        
    return grille_pos







#----------------------------X-WING--------------------------------------------

def x_wing_ligne(grille_pos,k):
    liste=[]
    for ligne in range(9):
        colonnes_de_k=[]
        for colonne in range(9) :
            if k in grille_pos[ligne][colonne]:
                colonnes_de_k.append(colonne)
        if len(colonnes_de_k)==2 :
            liste.append([ligne,colonnes_de_k[0],colonnes_de_k[1]])
    if len(liste)<2:
        return grille_pos
    for index1 in range(len(liste)-1):
        for index2 in range(index1+1,len(liste)):
            if liste[index1][1]==liste[index2][1] and liste[index1][2]==liste[index2][2]:
                for i in range(9) :
                    if k in grille_pos[i][liste[index1][1]]\
                    and i != liste[index1][0]\
                    and i != liste[index2][0]:
                        grille_pos[i][liste[index1][1]].remove(k)    
            
                for i in range(9) :
                    if k in grille_pos[i][liste[index1][2]]\
                    and i != liste[index1][0]\
                    and i != liste[index2][0]:
                        grille_pos[i][liste[index1][2]].remove(k)    
    return grille_pos

def x_wing_colonne(grille_pos,k):
    liste=[]
    for colonne in range(9):
        lignes_de_k=[]
        for ligne in range(9) :
            if k in grille_pos[ligne][colonne]:
                lignes_de_k.append(ligne)
        if len(lignes_de_k)==2 :
            liste.append([colonne,lignes_de_k[0],lignes_de_k[1]])
    if len(liste)<2:
        return grille_pos
    for index1 in range(len(liste)-1):
        for index2 in range(index1+1,len(liste)):
            if liste[index1][1]==liste[index2][1] and liste[index1][2]==liste[index2][2]:
                for i in range(9) :
                    if k in grille_pos[liste[index1][1]][i]\
                    and i != liste[index1][0]\
                    and i != liste[index2][0]:
                        grille_pos[liste[index1][1]][i].remove(k)    
            
                for i in range(9) :
                    if k in grille_pos[liste[index1][2]][i]\
                    and i != liste[index1][0]\
                    and i != liste[index2][0]:
                        grille_pos[liste[index1][2]][i].remove(k)    
    return grille_pos
#_____________________________________________FIN   X-WING_________________________________________________

#  ----------------------------------------- SWORD-fish ligne----------------------------------------------

    
def sword_fish(liste_des_sommets,grille_pos,valeur) :
    colonnes_trouvees=[]
    for indice in range(6) :
        if liste_des_sommets[indice][1] not in colonnes_trouvees :
            colonnes_trouvees.append(liste_des_sommets[indice][1])
    if len(colonnes_trouvees)!=3 :
        return grille_pos
    elif [liste_des_sommets[0][1],liste_des_sommets[1][1]]!=\
         [liste_des_sommets[2][1],liste_des_sommets[3][1]]\
    and [liste_des_sommets[0][1],liste_des_sommets[1][1]]!=\
            [liste_des_sommets[4][1],liste_des_sommets[5][1]]\
    and [liste_des_sommets[2][1],liste_des_sommets[3][1]]!=\
            [liste_des_sommets[4][1],liste_des_sommets[5][1]] :
        for colon in colonnes_trouvees :
            for lign in range(9) :
                if lign not in [liste_des_sommets[0][0],\
                                liste_des_sommets[2][0],\
                                liste_des_sommets[4][0]] and valeur in grille_pos[lign][colon] :
                    grille_pos[lign][colon].remove(valeur)
        return grille_pos
    else :
        return grille_pos
                           


def liste_des_sommets(grille_pos,valeur) :
    liste_des_sommets=[]
    for lign in range(9) :
        liste_sommets_ligne = []
        for colon in range(9) :
            if valeur in grille_pos[lign][colon]:
                liste_sommets_ligne.append([[lign,colon]])
        if len(liste_sommets_ligne)==2:
            liste_des_sommets += liste_sommets_ligne[0]
            liste_des_sommets += liste_sommets_ligne[1]
    return liste_des_sommets

def groupes_de_3 (grille_pos,liste_des_sommets,valeur): 
    liste =range(len(liste_des_sommets)//2)
    if len(liste)>2:
        for i in liste[:len(liste)-2] :
            for j in liste[i+1:len(liste)-1] :
                for k in liste[j+1:len(liste)] :
                    liste_des_sommets_a_tester = [liste_des_sommets[2*i],\
                                                  liste_des_sommets[2*i+1],\
                                                  liste_des_sommets[2*j],\
                                                  liste_des_sommets[2*j+1],\
                                                  liste_des_sommets[2*k],\
                                                  liste_des_sommets[2*k+1]]
                    sword_fish(liste_des_sommets_a_tester,grille_pos,valeur)
    return grille_pos
# _________________________________________fin SWORD-fish ligne________________________________________

#---------------------------------------Sword-Fish colonne---------------------------------------------

    
def sword_fish_c(liste_des_sommets,grille_pos,valeur) :
    lignes_trouvees=[]
    for indice in range(6) :
        if liste_des_sommets[indice][0] not in lignes_trouvees :
            lignes_trouvees.append(liste_des_sommets[indice][0])
    if len(lignes_trouvees)!=3 :
        return grille_pos
    elif [liste_des_sommets[0][0],liste_des_sommets[1][0]]!=\
         [liste_des_sommets[2][0],liste_des_sommets[3][0]]\
    and [liste_des_sommets[0][0],liste_des_sommets[1][0]]!=\
        [liste_des_sommets[4][0],liste_des_sommets[5][0]]\
    and [liste_des_sommets[2][0],liste_des_sommets[3][0]]!=\
        [liste_des_sommets[4][0],liste_des_sommets[5][0]] :
        for lign in lignes_trouvees :
            for colon in range(9) :
                if colon not in [liste_des_sommets[0][1],\
                                 liste_des_sommets[2][1],\
                                 liste_des_sommets[4][1]]\
                and valeur in grille_pos[lign][colon] :
                    grille_pos[lign][colon].remove(valeur)
        return grille_pos
    else :
        return grille_pos
                           


def liste_des_sommets_c(grille_pos,valeur) :
    liste_des_sommets=[]
    for colon in range(9) :
        liste_sommets_colonne = []
        for lign in range(9) :
            if valeur in grille_pos[lign][colon]:
                liste_sommets_colonne.append([[lign,colon]])
        if len(liste_sommets_colonne)==2:
            liste_des_sommets += liste_sommets_colonne[0]
            liste_des_sommets += liste_sommets_colonne[1]
    return liste_des_sommets

def groupes_de_3_c (grille_pos,liste_des_sommets,valeur):
    liste =range(len(liste_des_sommets)//2)
    if len(liste)>2:
        for i in liste[:len(liste)-2] :
            for j in liste[i+1:len(liste)-1] :
                for k in liste[j+1:len(liste)] :
                    liste_des_sommets_a_tester = [liste_des_sommets[2*i],\
                                                  liste_des_sommets[2*i+1],\
                                                  liste_des_sommets[2*j],\
                                                  liste_des_sommets[2*j+1],\
                                                  liste_des_sommets[2*k],\
                                                  liste_des_sommets[2*k+1]]
                    sword_fish_c(liste_des_sommets_a_tester,grille_pos,valeur)
    return grille_pos          

# _________________________________________fin SWORD-fish colonne______________________________________

        
def essai_erreur(grille_pos,grille_s,choix):
    for ligne in range(9):
        position=[]
        for colonne in range(9):
            if len(grille_pos[ligne][colonne])==2 :
                liste=grille_pos[ligne][colonne]
                position=[ligne,colonne]
                for li in range(9):
                    if li!=ligne :
                        if grille_pos[li][colonne]==liste:
                            for co in range(9):
                                if co!=colonne :
                                    if grille_pos[ligne][co]==liste:
                                        grille_pos[ligne][colonne]=[]
                                        grille_s[ligne][colonne]=liste[choix]

def essai_erreur2(grille_pos,grille_s,choix):
    for ligne in range(9):
        for colonne in range(9) :
            if len(grille_pos[ligne][colonne])==2 :
                memo = grille_pos[ligne][colonne]
                suivant=colonne+1
                if colonne<9 :
                    liste_ligne=grille_pos[ligne][suivant:]
                    if memo in liste_ligne :
                        grille_pos[ligne][colonne]=[]
                        grille_s[ligne][colonne]=memo[choix]
                        return "ligne"
                col=[]
                for i in range(9):
                    col.append(grille_pos[i][colonne])
                if ligne<9 :
                    if memo in col[ligne+1:]:
                        grille_pos[ligne][colonne]=[]
                        grille_s[ligne][colonne]=memo[choix]
                        return "colonne"
                carre =3*ligne//3 + colonne//3
                liste_carre =[]
                for index in range(9):
                    if (3*(carre//3)+index//3) != ligne or (3*(carre%3)+index%3) != colonne :
                        liste_carre.append(\
                            grille_pos[(3*(carre//3))+index//3][(3*(carre%3))+index%3])
                    if memo in liste_carre :
                        grille_pos[ligne][colonne]=[]
                        grille_s[ligne][colonne]=memo[choix]
                        return "carre"                                           


#______________________________________________________________________________________________________
#
#                                           RESOLUTION
#______________________________________________________________________________________________________


def resolution_(grille_s):
    global grille_possibles
    fait=True
    while fait == True:
        fait=False
        for i in range (1,10):
            if len(ou_le_nombre_peut_etre(grille_s,i))==1:
                grille_s[ou_le_nombre_peut_etre(grille_s,i)[0][0]]\
                    [ou_le_nombre_peut_etre(grille_s,i)[0][1]]=i
                fait=True        
    fait=True           
    while fait == True:
        fait=False    
        for i in range (9):
            for j in range(9):
                if len(reste_possible(grille_s,i,j))==1 :
                    fait=True
                    temp=reste_possible(grille_s,i,j)[0]
                    grille_s[i][j]=temp  
    grille_possibles=grille_des_possibles(grille_s)
    for lignes in range(9):
        grille_possibles=groupes_nus_ligne(grille_possibles,lignes)
    for colonne in range(9):
        grille_possibles=groupes_nus_colonne(grille_possibles,colonne)  
    for carre in range(9):
        grille_possibles=groupes_nus_carre(grille_possibles,carre)
    grille_possibles=groupes_caches_ligne(grille_possibles)
    grille_possibles=groupes_caches_colonne(grille_possibles)
    grille_possibles=groupes_caches_carre(grille_possibles)
    for valeur in range(1,10):
        grille_possibles=x_wing_ligne(grille_possibles,valeur)
    for valeur in range(1,10):
        grille_possibles=x_wing_colonne(grille_possibles,valeur)
    for valeur in range(9) :
        grille_possibles=groupes_de_3(grille_possibles,\
                                      liste_des_sommets(grille_possibles,valeur),\
                                      valeur)
    for valeur in range(9) :
        grille_possibles=groupes_de_3_c(grille_possibles,\
                                        liste_des_sommets_c(grille_possibles,valeur),\
                                        valeur)
    for ligne in range(9) :
        for colonne in range(9):
            if len(grille_possibles[ligne][colonne])==1:
                grille_s[ligne][colonne]=grille_possibles[ligne][colonne][0]
    return grille_s
#______________________fin 

def resolution(grille_s):
    global grille_possibles
    memogrille=[]
    memopossible=[]
    for i in range(9):
        memogrille.append([0,0,0,0,0,0,0,0,0])
        memopossible.append([0,0,0,0,0,0,0,0,0])
    essais=0  
    while not teste_ligne(grille_s) and essais!=3:
        resolution_(grille_s)
        essais+=1
    essais=0
#--memorisation
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                memogrille[i][j]=grille_s[i][j]
                memopossible[i][j] = grille_possibles[i][j]
#-------essai erreur        
        essai_erreur(grille_possibles,grille_s,0)
        while not teste_ligne(grille_s) and essais!=3:
            resolution_(grille_s)
            essais+=1
    essais=0
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                grille_s[i][j]=memogrille[i][j]
                grille_possibles[i][j]=memopossible[i][j]
        essai_erreur(grille_possibles,grille_s,1)
        while not teste_ligne(grille_s) and essais!=3:
            resolution_(grille_s)
            essais+=1
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                grille_s[i][j]=memogrille[i][j]
                grille_possibles[i][j]=memopossible[i][j]
# ______ fin essai erreur
#--memorisation 2
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                memogrille[i][j]=grille_s[i][j]
                memopossible[i][j] = grille_possibles[i][j]
#-------essai erreur 2       
        essai_erreur2(grille_possibles,grille_s,0)
        while not teste_ligne(grille_s) and essais!=3:
            resolution_(grille_s)
            essais+=1
    essais=0
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                grille_s[i][j]=memogrille[i][j]
                grille_possibles[i][j]=memopossible[i][j]
        essai_erreur2(grille_possibles,grille_s,1)
        while not teste_ligne(grille_s) and essais!=3:
            resolution_(grille_s)
            essais+=1
    if not teste_ligne(grille_s):
        for i in range(9):
            for j in range(9):
                grille_s[i][j]=memogrille[i][j]
                grille_possibles[i][j]=memopossible[i][j]
# ______ fin essai erreur
    return grille_s

#____________________________________________________________________________________

"""def groupes_caches_ligne(grille_pos):
    for ligne in range(9):
        liste_positions =[]
        for chiffre in range(1,10) :
            positions=[]
            for colonne in range(9) :
                if chiffre in grille_pos[ligne][colonne] :
                    positions.append(colonne)
                    
            liste_positions.append(positions)
            
        for colonne in range(9):
            liste_index=[]
            liste=liste_positions[colonne]
            for index in range(9):
                if intersection_2_listes(liste,liste_positions[index])==liste_positions[index] and len(liste)>1 and len(liste_positions[index])>1:
                    liste_index.append(index)
            if len(liste_positions[colonne])==len(liste_index) and len(liste_index)>0 :
                valeurs=[]
                for j in range(len(liste_index)) : valeurs.append(liste_index[j]+1)
                print (liste_positions[colonne],valeurs)
                for k in liste_positions[colonne] :
                    for val in range(1,10) :
                        if val in grille_pos[ligne][k] and val not in valeurs :
                            grille_pos[ligne][k].remove(val)
        
    return grille_pos


mat=[[6,0,0,4,1,0,5,7,9],
     [1,0,5,0,0,0,0,8,0],
     [0,2,0,8,5,0,3,0,0],
     [0,5,0,0,0,0,0,0,0],
     [7,0,3,5,2,1,0,6,0],
     [0,1,0,9,0,4,0,5,0],
     [5,0,1,2,0,8,0,4,0],
     [0,0,2,0,4,5,6,1,7],
     [0,0,4,0,9,0,0,2,5]]
     
grille=grille_des_possibles(mat)
for i in range(9) : print grille[i]
print"--------------------"    
groupes_caches_ligne(grille)"""



    
