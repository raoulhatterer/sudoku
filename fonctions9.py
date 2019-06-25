#------------------------------------------------------------------
#
#              SUDOKU
#
#        Jean-Luc COSSALTER
#       8/4/2019
#
#------------------------------------------------------------------
import random
from random import randint

try :
    from Tkinter import *
except :
    from tkinter import *
larg_carre=40




grille_essai=[[1,0,3,4,5,6,7,8,9],
               [2,1,1,2,2,2,3,3,3],
               [3,1,0,2,2,2,3,3,3],
               [4,4,4,5,5,5,6,6,6],
               [5,4,4,5,0,5,6,6,6],
               [6,4,4,5,5,5,6,6,6],
               [7,7,7,8,8,8,9,9,9],
               [8,7,7,8,8,8,9,9,9],
               [9,7,7,8,8,8,9,9,9]]

# GRILLE SERVANT A L ELABORATION DES GRILLES
grille_sudoku=[[1,2,3,4,5,6,7,8,9],
               [7,8,9,1,2,3,4,5,6],
               [4,5,6,7,8,9,1,2,3],
               [2,3,4,5,6,7,8,9,1],
               [8,9,1,2,3,4,5,6,7],
               [5,6,7,8,9,1,2,3,4],
               [3,4,5,6,7,8,9,1,2],
               [9,1,2,3,4,5,6,7,8],
               [6,7,8,9,1,2,3,4,5]]

             
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
 
 
#print intersection_2_listes([1, 2, 3, 4], [1, 2, 2, 5, 6])


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

#print(est_complet([1,2,5,4,0,0,0,0,0]))


#----------- pour savoir les chiffres qui restent ----------------------------
def reste(liste_a_tester):
    liste=[1,2,3,4,5,6,7,8,9]
    for index in range(9):
        if liste_a_tester[index] in liste :
            liste.remove(liste_a_tester[index])
    return liste

#print(reste([1,3,0,0,5,0,8,0,0]))



# -------------teste si les 9 chiffres sont presents dans toutes les ligne
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











# -------------quels sont les chiffres qui restent dans la  colonne
def reste_colonne(grille_a_tester,colonne):
    mot_a_tester=[]
    for i in range(9) :
        mot_a_tester.append(grille_a_tester[i][colonne])
    return reste(mot_a_tester)

#print(reste_colonne(grille_sudoku,0))


# -------------quels sont les chiffres qui restent dans la  ligne
def reste_ligne(grille_a_tester,ligne):
    mot_a_tester=[]
    for index in range(9) :
        mot_a_tester.append(grille_a_tester[ligne][index])
    return reste(mot_a_tester)

#print(reste_ligne(grille_sudoku,1))


# -------------quels sont les chiffres qui restent dans le carre
def reste_carre(grille_a_tester,ligne,colonne):
    mot_a_tester=[]
    position_carre=3*(ligne//3)+colonne//3
    for index in range(9) :
        mot_a_tester.append(grille_a_tester[index // 3 + 3 * (position_carre // 3)][index % 3 + 3 * (position_carre % 3)])
        #print(mot_a_tester)
    return reste(mot_a_tester)

#print(reste_carre(grille_sudoku,1,2))


# -------------- finalement aux coordonnees donnees que reste-t-il comme chiffre possible

def reste_possible(grille_a_tester,ligne,colonne):
    if (grille_a_tester[ligne][colonne]>0) :
        return []
    reste1=reste_ligne(grille_a_tester,ligne)
    #print reste1
    reste2=reste_colonne(grille_a_tester,colonne)
    #print reste2
    reste3=reste_carre(grille_a_tester,ligne,colonne)
    #print reste3
    reste4 = intersection_2_listes(reste1,reste2)
    #print reste4
    reste=intersection_2_listes(reste4,reste3)
    
    return reste

#print(reste_possible(grille_sudoku,2,5))






# -------------teste si les 9 chiffres sont presents dans toutes les colonnes
def teste_colonne(grille_a_tester):
    colonne=0
    while colonne<9 :
        mot_a_tester=[]
        for index in range(9) :
            mot_a_tester.append(grille_a_tester[index][colonne])
        #print(mot_a_tester) 
        if not est_complet(mot_a_tester):
            return False
        colonne= colonne + 1
    return True


# -------------teste si les 9 chiffres sont presents dans tous les carres
def teste_carre(grille_a_tester) :
    carre=0
    while carre<9 :
        mot_a_tester=[]
        for i in range(9) :
            mot_a_tester.append(grille_a_tester[i % 3 + 3 * (carre % 3)][i // 3 + 3 * (carre // 3)])
        #print(mot_a_tester) 
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


#print(test_complet(grille_sudoku))





    
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

#print(inverser_nombres_grille(grille_sudoku,2,8))
                
#________________inverser 2 colonnes ________________________________
                



def inverser_colonnes(tab,colonne1,colonne2):
    if colonne1//3==colonne2//3:
        for i in range(9):
            temp=tab[i][colonne1]
            tab[i][colonne1]=tab[i][colonne2]
            tab[i][colonne2]=temp
    return tab
    
#print(inverser_colonnes(grille_sudoku,1,2))



#________________inverser 2 lignes ________________________________
                

def inverser_lignes(tab,ligne1,ligne2):
    if ligne1//3==ligne2//3:
        for i in range(9):
            temp=tab[ligne1][i]
            tab[ligne1][i]=tab[ligne2][i]
            tab[ligne2][i]=temp
    return tab
    


#print(inverser_lignes(grille_sudoku,1,0))

#_________________melange aleatoir________________________________________

def melange_nombre_grille(tab):
    a = range(1,10)
    b = random.sample(a, len(a))
    for i in range(9):
        for j in range(9):
            if tab[i][j]>0:
                tab[i][j]=b[tab[i][j]-1]
    return tab
           

#print(melange_nombre_grille(grille_sudoku))

#_________________melange aleatoir 3 grandes colonnes__________

def change_3_col(tab):
    a = range(3)
    b = random.sample(a, len(a))
    #print a
    #print b
    tab_temp=[[1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9]]

    for colon in range(9):
        for lign in range(9):
            tab_temp[lign][colon]=tab[lign][colon]
   
    
    for colon in range(9):
        for lign in range(9):
            tab[lign][colon]=tab_temp[lign][(b[colon//3]-a[colon//3])*3+colon]
            
    return tab
           

#print(change_3_col(grille_sudoku))



#_________________melange aleatoir 3 grandes lignes____________________

def change_3_lign(tab):
    a = range(3)
    b = random.sample(a, len(a))
    #print a
    #print b
    tab_temp=[[1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9]]

    for lign in range(9):
        for colon in range(9):
            tab_temp[lign][colon]=tab[lign][colon]
   
    
    for lign in range(9):
        for colon in range(9):
            tab[lign][colon]=tab_temp[(b[lign//3]-a[lign//3])*3+lign][colon]
            
    return tab
           

#print(change_3_lign(grille_sudoku))



#_________________melange aleatoir 3 petites colonnes__________

def change_3_petites_col(tab):
    a = range(3)
    b = random.sample(a, len(a))
    #print a
    #print b
    tab_temp=[[1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9]]

    for colon in range(9):
        for lign in range(9):
            tab_temp[lign][colon]=tab[lign][colon]
   
    
    for colon in range(3):
        for lign in range(9):
            tab[lign][colon]=tab_temp[lign][b[colon]]
            
    b= random.sample(a, len(a))
    for colon in range(3,6):
        for lign in range(9):
            tab[lign][colon]=tab_temp[lign][b[colon-3]+3]

    b= random.sample(a, len(a))
    for colon in range(6,9):
        for lign in range(9):
            tab[lign][colon]=tab_temp[lign][b[colon-6]+6]
            
            
    return tab

#print(change_3_petites_col(grille_sudoku))


#_________________melange aleatoir 3 petites lignes__________

def change_3_petites_lignes(tab):
    a = range(3)
    b = random.sample(a, len(a))
    #print a
    #print b
    tab_temp=[[1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [1,1,1,2,2,2,3,3,3],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [4,4,4,5,5,5,6,6,6],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9],
              [7,7,7,8,8,8,9,9,9]]

    for colon in range(9):
        for lign in range(9):
            tab_temp[lign][colon]=tab[lign][colon]
   
    
    for lign in range(3):
        for colon in range(9):
            tab[lign][colon]=tab_temp[b[lign]][colon]
            
    b= random.sample(a, len(a))
    for lign in range(3,6):
        for colon in range(9):
            tab[lign][colon]=tab_temp[b[lign-3]+3][colon]

    b= random.sample(a, len(a))
    for lign in range(6,9):
        for colon in range(9):
            tab[lign][colon]=tab_temp[b[lign-6]+6][colon]
            
            
    return tab

#print(change_3_petites_lignes(grille_sudoku))


def supprimer_nombre(tab):
    i=randint(0,8)
    j=randint(0,8)
    if (tab[i][j] != 0) and  len(reste_possible(tab,i,j))<2:
        tab[i][j]=0
    
def double_clic(event):
    """ Gestion de l'evenement double clic gauche """
    global chiffre
    #text_choix=can.create_text(larg_carre*chiffre+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=chiffre,fill="black",font=("Helvetica",20))
    # position du pointeur de la souris
    X = (event.x-5)//larg_carre
    Y = (event.y-5)//larg_carre
    if Y==10 and X<9 :
        chiffre =X+1
        can.create_text(larg_carre*chiffre+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=chiffre,fill="red",font=("Helvetica",20))   
    elif Y==10 and X==10 :
        chiffre =0  

def Clic(event):
    """ Gestion de l'evenement Clic gauche """
    global chiffre
    before=20
   
    # position du pointeur de la souris
    X = (event.x-5)//larg_carre
    Y = (event.y-5)//larg_carre
    
    if X<10 and Y<10 and chiffre!=0 and grille_depart[Y][X]==0:
        before=tab[Y][X]
        tab[Y][X]=chiffre
    elif X<10 and Y<10 and chiffre==0 and grille_depart[Y][X]==0:
        tab[Y][X]=chiffre
        can.create_rectangle(larg_carre*X+5,larg_carre*Y+5,larg_carre*(X+1)+5,larg_carre*(Y+1)+5,fill="yellow")
    else : before = 20    
    #if valeur.get()>0 and valeur.get()<10:
     #   tab[Y][X]=valeur.get()

    if before==0 and tab[Y][X]!=0:
        can.create_text(larg_carre*X+5+larg_carre//2,larg_carre*Y+5+larg_carre//2,text=tab[Y][X],fill="blue",font=("Helvetica",20))
    
   
    text_choix=can.create_text(larg_carre*chiffre+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=chiffre,fill="black",font=("Helvetica",20))

def creation_aleatoire(tab) :
    melange_nombre_grille(tab)
    change_3_col(tab)
    change_3_lign(tab)
    change_3_petites_col(tab)
    change_3_petites_lignes(tab)
    for i in range(80):
       supprimer_nombre(tab)

creation_aleatoire(grille_sudoku)
#____________________________________________________________________________
#
#                FONCTIONS RESOLUTION
#____________________________________________________________________________


#----- singleton cache ------------------------------------------------------
def grille_des_possibles(tab):
    gdp=[]
    for ligne in range(9):
        ldp=[]
        for colonne in range(9):
            ldp.append(reste_possible(tab,ligne,colonne))
        gdp.append(ldp)
    return gdp
            

def ou_le_nombre_peut_etre(tab,nombre):
    possible=[[1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1]]
#remplissage matrice des possibles
    
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

#----- singleton cache fin       ______________________________________
                    
#--------------Elimination indirecte-----------------------------------
    for carre in range(9):
        #print(carre)
        debut_ligne=10
        fin_ligne=11
        for i in range(3) :
            for j in range(3):
                if possible[3*(carre//3) +i][3*(carre%3)+j]==1 and debut_ligne==10:
                    debut_ligne = 3*(carre//3) +i
                    #print("dl",debut_ligne)
                elif possible[3*(carre//3) +i][3*(carre%3)+j]==1:
                    fin_ligne = 3*(carre//3) +i
                    #print("fl",fin_ligne)
        if debut_ligne==fin_ligne :
            #print(nombre,carre,fin_ligne)
            for j in range(9):
                if j!=3*(carre%3) and j!=3*(carre%3)+1 and j!=3*(carre%3)+2 :
                    possible[debut_ligne][j]=0
  

    for carre in range(9):
        #print(carre)
        debut_colonne=10
        fin_colonne=11
        for j in range(3) :
            for i in range(3):
                if possible[3*(carre//3) +i][3*(carre%3)+j]==1 and debut_colonne==10:
                    debut_colonne = 3*(carre%3) +j
                    #print("dc",debut_colonne)
                elif possible[3*(carre//3) +i][3*(carre%3)+j]==1:
                    fin_colonne = 3*(carre%3) +j
                    #print("fc",fin_colonne)
        if debut_colonne==fin_colonne :
            for i in range(9):
                if i!=3*(carre//3) and i!=3*(carre//3)+1 and i!=3*(carre//3)+2 :
                    possible[i][debut_colonne]=0 

#Elimination indirecte fin _____________________________________________________    
                    
  
#analyse des lignes
    for i in range(9):
        resultat=[]
        nombre_de_1=0
        for k in range(9):
            if possible[i][k]==1:
                memo_de_k=k
                resultat.append([i,memo_de_k])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
        
    #return resultat

#analyse des colonnes

    for j in range(9):
    
        resultat=[]
        nombre_de_1=0
        for k in range(9):
            if possible[k][j]==1:
                memo_de_k=k
                resultat.append([memo_de_k,j])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
        
    #return resultat    
        
#analyse des carres 3x3

    for carre in range(9):
        resultat=[]
        nombre_de_1=0
        for k in range(9):
            if possible[3*(carre//3)+k//3][3*(carre%3)+k%3]==1:
                memo_de_k=k
                resultat.append([3*(carre//3)+k//3,3*(carre%3)+k%3])
                nombre_de_1+=1
        if nombre_de_1==1 :
            return resultat
    return resultat        
        
#___________________ fin ou_le_nombre_peut_etre_______________________________________      







"""grille_sudoku=[[0,0,7,1,0,8,0,0,0],
               [0,1,0,0,0,0,6,5,0],
               [8,3,0,0,0,4,7,0,0],
               [7,0,1,2,0,0,0,6,0],
               [0,0,0,0,8,0,0,0,0],
               [0,4,0,0,0,1,3,0,7],
               [0,0,2,8,0,0,0,9,3],
               [0,8,5,0,0,0,0,7,0],
               [0,0,0,5,0,9,2,0,0]]"""

"""grille_sudoku=[[1,0,0,0,0,0,5,2,0],
               [0,0,0,0,7,8,0,0,0],
               [0,0,0,0,0,0,6,0,0],
               [0,9,0,0,4,0,0,0,0],
               [0,0,0,5,0,0,1,0,0],
               [0,7,0,0,0,0,0,0,0],
               [0,0,6,2,0,0,0,0,0],
               [0,4,0,0,0,0,0,7,8],
               [0,0,0,0,0,0,0,0,3]]"""



def motifs_simples_ligne_2 (tab,ligne):
    
    for colonne in range(8):
        for index in range(colonne+1,9):
            if grille_possibles[ligne][colonne]==grille_possibles[ligne][index]and len(grille_possibles[ligne][index])==2:
                truc0=grille_possibles[ligne][colonne][0]
                truc1=grille_possibles[ligne][colonne][1]
                for i in range(9):
                    if i!=colonne and i!=index and truc0 in grille_possibles[ligne][i]:
                        grille_possibles[ligne][i].remove(truc0)
                    if i!=colonne and i!=index and truc1 in grille_possibles[ligne][i]:    
                        grille_possibles[ligne][i].remove(truc1)
    return tab
                
    
def motifs_simples_colonne_2 (tab,colonne):
    
    for ligne in range(8):
        for index in range(ligne+1,9):
            if grille_possibles[ligne][colonne]==grille_possibles[index][colonne]and len(grille_possibles[ligne][colonne])==2:
                truc0=grille_possibles[ligne][colonne][0]
                truc1=grille_possibles[ligne][colonne][1]
                for i in range(9):
                    if i!=ligne and i!=index and truc0 in grille_possibles[i][colonne]:
                        grille_possibles[i][colonne].remove(truc0)
                    if i!=ligne and i!=index and truc1 in grille_possibles[i][colonne]:
                        grille_possibles[i][colonne].remove(truc1)
    return tab


def motifs_simples_carre_2 (tab,carre):
    
    for index1 in range(8):
        for index2 in range(index1+1,9):
            if grille_possibles[3*(carre//3)+index1//3][3*(carre%3)+index1%3]==grille_possibles[3*(carre//3)+index2//3][3*(carre%3)+index2%3]and len(grille_possibles[3*(carre//3)+index2//3][3*(carre%3)+index2%3])==2:
                truc0=grille_possibles[3*(carre//3)+index1//3][3*(carre%3)+index1%3][0]
                truc1=grille_possibles[3*(carre//3)+index1//3][3*(carre%3)+index1%3][1]
                
                for i in range(9):
                    #print(i,truc1,3*(carre//3)+i//3,3*(carre%3)+i%3,grille_possibles[3*(carre//3)+i//3][3*(carre%3)+i%3])
                    if i!=index1 and i!=index2 and (truc0 in grille_possibles[3*(carre//3)+i//3][3*(carre%3)+i%3]):
                        grille_possibles[3*(carre//3)+i//3][3*(carre%3)+i%3].remove(truc0)
                        
                    if i!=index1 and i!=index2 and (truc1 in grille_possibles[3*(carre//3)+i//3][3*(carre%3)+i%3]):
                        grille_possibles[3*(carre//3)+i//3][3*(carre%3)+i%3].remove(truc1)
                        
    return tab
                                                           
                                                         


#____________________________________________________________________________
#
#                RESOLUTION
#____________________________________________________________________________




def resolution():
    global grille_possibles



    fait=True
    while fait == True:
        fait=False
        for i in range (1,10):
            if len(ou_le_nombre_peut_etre(grille_sudoku,i))==1:
                grille_sudoku[ou_le_nombre_peut_etre(grille_sudoku,i)[0][0]][ou_le_nombre_peut_etre(grille_sudoku,i)[0][1]]=i
                fait=True
            
    fait=True           
    while fait == True:
        fait=False    
        for i in range (9):
            for j in range(9):
                if len(reste_possible(grille_sudoku,i,j))==1 :
                    fait=True
                    oo=reste_possible(grille_sudoku,i,j)[0]
                    grille_sudoku[i][j]=oo
                #print(oo)


    grille_possibles=grille_des_possibles(grille_sudoku)

    #for i in range(9):
        #print(grille_possibles[i])


    for ligne in range(9):
        motifs_simples_ligne_2 (grille_possibles,ligne)

    
    for colonne in range(9):
        motifs_simples_colonne_2 (grille_possibles,colonne)

    for carre in range(9):
        motifs_simples_carre_2 (grille_possibles,carre)

    #for i in range(9):
     #   print(grille_possibles[i])

    for ligne in range(9) :
        for colonne in range(9):
            if len(grille_possibles[ligne][colonne])==1:
                grille_sudoku[ligne][colonne]=grille_possibles[ligne][colonne][0]


    fait=True
    while fait == True:
        fait=False
        for i in range (1,10):
            if len(ou_le_nombre_peut_etre(grille_sudoku,i))==1:
                grille_sudoku[ou_le_nombre_peut_etre(grille_sudoku,i)[0][0]][ou_le_nombre_peut_etre(grille_sudoku,i)[0][1]]=i
                fait=True
            
    fait=True           
    while fait == True:
        fait=False    
        for i in range (9):
            for j in range(9):
                if len(reste_possible(grille_sudoku,i,j))==1 :
                    fait=True
                    oo=reste_possible(grille_sudoku,i,j)[0]
                    grille_sudoku[i][j]=oo
                    #print(oo)

    grille_possibles=grille_des_possibles(grille_sudoku)
    for ligne in range(9):
        motifs_simples_ligne_2 (grille_possibles,ligne)

    
    for colonne in range(9):
        motifs_simples_colonne_2 (grille_possibles,colonne)

    for carre in range(9):
        motifs_simples_carre_2 (grille_possibles,carre)

    #for i in range(9):
        #print(grille_possibles[i])

    for ligne in range(9) :
        for colonne in range(9):
            if len(grille_possibles[ligne][colonne])==1:
                grille_sudoku[ligne][colonne]=grille_possibles[ligne][colonne][0]


#------------------------------------------------------------------------------------------------------------------------------
#
#                                   AFFICHAGE
#
#-----------------------------------------------------------------------------------------------------------------------------

def lignes(event):
    for i in range(4) :
        ligne_1=can.create_line(3*larg_carre*i+5,5,3*larg_carre*(i)+5,9*larg_carre+5,fill="red",width=3)
        ligne_2=can.create_line(5,3*larg_carre*i+5,9*larg_carre+5,3*larg_carre*(i)+5,fill="red",width=3)



grille_depart=list(grille_sudoku)
tab=grille_sudoku

fen = Tk()
can=Canvas(fen,width=500,height=500,background='white')
can.pack()
for i in range(9) :
    for j in range(9):
        rect=can.create_rectangle(larg_carre*i+5,larg_carre*j+5,larg_carre*(i+1)+5,larg_carre*(j+1)+5,fill="yellow")
for i in range(4) :
    ligne_1=can.create_line(3*larg_carre*i+5,5,3*larg_carre*(i)+5,9*larg_carre+5,fill="red",width=3)
    ligne_2=can.create_line(5,3*larg_carre*i+5,9*larg_carre+5,3*larg_carre*(i)+5,fill="red",width=3)
for i in range(9) :
    rect_choix=can.create_rectangle(larg_carre*i+5,larg_carre*10+5,larg_carre*(i+1)+5,larg_carre*(10+1)+5,fill="pink2")
for i in range(1,10):
    text_choix=can.create_text(larg_carre*i+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=i,fill="black",font=("Helvetica",20))
mon_image=PhotoImage(file="gomme.gif")
img=can.create_image(426,426,image=mon_image)

    
# CrÃ©ation d'un widget Entry
#valeur= IntVar()
#Champ = Entry(fen, textvariable= valeur, bg ='bisque', fg='maroon',font=("Helvetica",20))
#Champ.focus_set()
#Champ.pack(side = LEFT, padx = 5, pady = 5)


for i in range(9) :
    for j in range(9):
        if tab[i][j]!=0 :
            text=can.create_text(larg_carre*j+5+larg_carre//2,larg_carre*i+5+larg_carre//2,text=tab[i][j],fill="black",font=("Helvetica",20))  
# Création d'un widget Button (Resoudre)
BoutonResout = Button(fen, text ='Resoudre', command = resolution)
BoutonResout.pack(side = LEFT, padx = 5, pady = 5)
# Création d'un widget Button (New)
BoutonNew = Button(fen, text ='New', command = creation_aleatoire(grille_sudoku))
BoutonNew.pack(side = LEFT, padx = 10, pady = 10)



# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(fen, text ='Quitter', command = fen.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)


can.bind('<Button-1>',Clic)
can.bind("<Double-Button-1>", double_clic)
can.bind("<ButtonRelease-1>",lignes)
fen.mainloop()
                             

