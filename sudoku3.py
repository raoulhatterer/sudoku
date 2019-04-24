#------------------------------------------------------------------
#
#              SUDOKU
#
#        Jean-Luc COSSALTER
#       8/4/2019
#
#------------------------------------------------------------------
import random
grille_sudoku=[[1,2,3,4,5,6,7,8,9],
               [1,2,3,4,5,6,7,8,9],
               [1,2,3,4,5,6,7,0,0],
               [0,0,5,5,6,7,8,0,0],
               [0,0,7,5,6,7,8,9,1],
               [0,0,9,5,6,7,8,9,1],
               [7,3,4,5,6,7,8,9,1],
               [8,2,1,5,6,7,8,9,1],
               [9,5,6,5,6,7,8,9,1]]
             
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


# -------------teste si les 9 chiffres sont présents dans toutes les colonnes
def teste_colonne(grille_a_tester):
    j=0
    while j<9 :
        mot_a_tester=[]
        for i in range(9) :
            mot_a_tester.append(grille_a_tester[i][j])
        #print(mot_a_tester) 
        if not est_complet(mot_a_tester):
            return False
        j=j+1
    return True


# -------------teste si les 9 chiffres sont présents dans toutes les lignes
def teste_carre(grille_a_tester) :
    j=0
    while j<9 :
        mot_a_tester=[]
        for i in range(9) :
            mot_a_tester.append(grille_a_tester[i%3+3*(j%3)][i//3+3*(j//3)])
        #print(mot_a_tester) 
        if not est_complet(mot_a_tester):
            return False
        j=j+1
    return True

# -------------teste si les 9 chiffres sont présents dans toutes les carres

def test_complet(grille_a_tester):
    if not teste_ligne(grille_a_tester):
        return False
    elif not teste_colonne(grille_a_tester):
        return False
    elif not teste_carre(grille_a_tester):
        return False
    else :
        return True


    
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

print(inverser_nombres_grille(grille_sudoku,2,8))
                
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
























