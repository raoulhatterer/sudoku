# -*- coding: cp1252 -*-
#------------------------------------------------------------------
#
#              SUDOKU
#
#        Jean-Luc COSSALTER
#        06/2019
#
#------------------------------------------------------------------
import csv
import random
from random import *

try :
    from Tkinter import *
except :
    from tkinter import *

from FoncSudo import *

larg_carre=40





# GRILLE SERVANT A L ELABORATION DES GRILLES


grille_depart=[[9,4,1,5,8,2,6,7,3],
               [7,6,2,4,3,1,8,9,5],
               [5,8,3,7,6,9,2,1,4],
               [8,9,6,3,1,4,5,2,7],
               [3,1,7,8,2,5,4,6,9],
               [2,5,4,6,9,7,3,8,1],
               [6,3,5,9,7,8,1,4,2],
               [1,7,8,2,4,3,9,5,6],
               [4,2,9,1,5,6,7,3,8]]

chiffre=10

#------------------------------------------------------------------------------------------------------------------------------
#
#                                   AFFICHAGE
#
#-----------------------------------------------------------------------------------------------------------------------------

def Clic(event):
    """ Gestion de l'evenement Clic gauche """
    global chiffre
    before=20
   
    # position du pointeur de la souris
    X = (event.x-5)//larg_carre
    Y = (event.y-5)//larg_carre
    
    if X<10 and Y<10 and grille_depart[Y][X]==0 and (chiffre in range(10)):
        
        grille_sudoku[Y][X]=chiffre
        chiffre=10
        
    elif Y==10 and X<10 :
        chiffre = X+1

    elif Y==10 and X==10 :
        chiffre=0

    dessiner_tableau_vide()
    remplir_tableau(grille_sudoku,grille_depart)
   

def dessiner_tableau_vide() :
    for i in range(9) :
        rect_choix=can.create_rectangle(larg_carre*i+5,larg_carre*10+5,larg_carre*(i+1)+5,larg_carre*(10+1)+5,fill="chartreuse2")
        for j in range(9):
            rect=can.create_rectangle(larg_carre*i+5,larg_carre*j+5,larg_carre*(i+1)+5,larg_carre*(j+1)+5,fill="lightyellow")
        for i in range(4) :
            ligne_1=can.create_line(3*larg_carre*i+5,5,3*larg_carre*(i)+5,9*larg_carre+5,fill="red",width=3)
            ligne_2=can.create_line(5,3*larg_carre*i+5,9*larg_carre+5,3*larg_carre*(i)+5,fill="red",width=3)

def remplir_tableau(grille_s,grille_d) :
    
    for i in range(9) :
        for j in range(9):
            if grille_s[i][j]!=0 and grille_d[i][j]==0 :
                text=can.create_text(larg_carre*j+5+larg_carre//2,larg_carre*i+5+larg_carre//2,text=grille_s[i][j],fill="limegreen",font=("Helvetica",20))
            elif grille_sudoku[i][j]!=0 and grille_depart[i][j]!=0 :
                    text=can.create_text(larg_carre*j+5+larg_carre//2,larg_carre*i+5+larg_carre//2,text=grille_s[i][j],fill="black",font=("Helvetica",20))
    for i in range(1,10):
        if i==chiffre :
            can.create_text(larg_carre*i+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=i,fill="red",font=("Helvetica",20))
        else :
            can.create_text(larg_carre*i+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=i,fill="black",font=("Helvetica",20))

    
def nouveau_jeu() :
    global grille_sudoku
    grille_sudoku=[[9,4,1,5,8,2,6,7,3],
                   [7,6,2,4,3,1,8,9,5],
                   [5,8,3,7,6,9,2,1,4],
                   [8,9,6,3,1,4,5,2,7],
                   [3,1,7,8,2,5,4,6,9],
                   [2,5,4,6,9,7,3,8,1],
                   [6,3,5,9,7,8,1,4,2],
                   [1,7,8,2,4,3,9,5,6],
                   [4,2,9,1,5,6,7,3,8]]
    creation_aleatoire(grille_sudoku,grille_depart,int(val.get()))
    dessiner_tableau_vide()
    remplir_tableau(grille_sudoku,grille_depart)
    
def resolv():
    resolution(grille_sudoku)
    dessiner_tableau_vide()
    remplir_tableau(grille_sudoku,grille_depart)

def recommencer():
    global grille_sudoku
    global grille_depart
    for ligne in range(9):
        for colonne in range(9):
            grille_sudoku[ligne][colonne]= grille_depart[ligne][colonne]
    dessiner_tableau_vide()
    remplir_tableau(grille_sudoku,grille_depart)
    
def charger_partie() :
    global grille_sudoku
    global grille_depart
    
    grille_sudoku=[]
    grille_depart=[]
   
    nom_fich =nom_fichier.get()
    if len(nom_fich)<4 :
        nom_depart=nom_fich+'_d.csv'
        nom_fich+='.csv'
        
    elif (nom_fich[(len(nom_fich)-4):len(nom_fich)]!='.csv'):
        nom_depart=nom_fich+'_d.csv'
        nom_fich+='.csv'
    else :
        nom_depart = nom_fich[:(len(nom_fich)-4)]+'_d.csv'

    try :
        file = open(nom_fich, "r")
    except :
        return

    reader = csv.reader(file,delimiter = ";")
    for row in reader:   
        ligne=[]
        for i in range(len(row)):
            ligne.append(int(float(row[i])))
        grille_sudoku.append(ligne)
        
    file.close

    try :
        file = open(nom_depart, "r")
        reader = csv.reader(file,delimiter = ";")
        for row in reader:   
            ligne=[]
            for i in range(len(row)):
                ligne.append(int(float(row[i])))
            grille_depart.append(ligne)
        
        file.close
    except :
        grille_depart = [[0]*9 for i in range(9)]
        for i in range(9) :
            for j in range(9):
                grille_depart[i][j] = grille_sudoku[i][j]
                
    dessiner_tableau_vide()
    remplir_tableau(grille_sudoku,grille_depart)

def sauver_partie():
    global grille_sudoku
    global grille_depart
    
    nom_fich =nom_fichier.get()
    if len(nom_fich)<4 :
        nom_depart=nom_fich+'_d.csv'
        nom_fich+='.csv'
        
    elif (nom_fich[(len(nom_fich)-4):len(nom_fich)]!='.csv'):
        nom_depart=nom_fich+'_d.csv'
        nom_fich+='.csv'
    else :
        nom_depart = nom_fich[:(len(nom_fich)-4)]+'_d.csv'
    if len(nom_fich)>4 :
        with open(nom_fich, 'w',newline='') as f:
            writer = csv.writer(f,delimiter = ";")
            writer.writerows(grille_sudoku)
        
        with open(nom_depart, 'w',newline='') as f:
            writer = csv.writer(f,delimiter = ";")
            writer.writerows(grille_depart)
        

    
def maj():
    i=0  

fen = Tk()
can=Canvas(fen,width=500,height=500,background='white')
can.pack()
for i in range(9) :
    for j in range(9):
        rect=can.create_rectangle(larg_carre*i+5,larg_carre*j+5,larg_carre*(i+1)+5,larg_carre*(j+1)+5,fill="lightyellow")
for i in range(4) :
    ligne_1=can.create_line(3*larg_carre*i+5,5,3*larg_carre*(i)+5,9*larg_carre+5,fill="red",width=3)
    ligne_2=can.create_line(5,3*larg_carre*i+5,9*larg_carre+5,3*larg_carre*(i)+5,fill="red",width=3)
for i in range(9) :
    rect_choix=can.create_rectangle(larg_carre*i+5,larg_carre*10+5,larg_carre*(i+1)+5,larg_carre*(10+1)+5,fill="chartreuse2")
for i in range(1,10):
    text_choix=can.create_text(larg_carre*i+5-larg_carre//2,larg_carre*10+5+larg_carre//2,text=i,fill="black",font=("Helvetica",20))
mon_image=PhotoImage(file="gomme.gif")
img=can.create_image(426,426,image=mon_image)

cadre_0 = Frame(fen,borderwidth=2,relief=GROOVE)
cadre_0.pack(side=LEFT,padx=5,pady=5)
  
# widget Button (Resoudre)
BoutonResout = Button(cadre_0, text ='Resoudre', fg="blue", command = resolv)
BoutonResout.pack(side = TOP, padx = 5, pady = 5)

# widget Button (Recommeencer)
BoutonRecom = Button(cadre_0, text ='Recommencer', fg="purple", command = recommencer)
BoutonRecom.pack(side = TOP, padx = 5, pady = 5)


# création d'un widget frame dans la fenêtre principale
cadre_1 = Frame(fen,borderwidth=2,relief=GROOVE)
cadre_1.pack(side=LEFT,padx=5,pady=5)


# widget button (New) dans le cadre_1
BoutonNew = Button(cadre_1, text ='Nouveau', command = nouveau_jeu)
BoutonNew.pack(side = LEFT, padx = 10, pady = 10)

# widget label dans le cadre_1
Label(cadre_1,text="Difficulté").pack(padx=5,pady=5)

val = StringVar()
val.set(10.0)
# Création d'un widget spinbox dans le cadre_1
boite = Spinbox(cadre_1,from_=0,to=20,increment=1,textvariable=val,width=5)
boite.pack(padx=5,pady=5)


# création d'un deuxième widget Frame dans la fenêtre principale
cadre_2 = Frame(fen,borderwidth=2,relief=GROOVE)
cadre_2.pack(side=LEFT ,padx=5,pady=5)


# widget Button (bouton Charger)
BoutonCharger = Button(cadre_2, text ='Charger', command = charger_partie)
BoutonCharger.pack(side = TOP,padx = 5, pady = 5)
 
# widget Button (bouton Enregistrer)
BoutonEnregistr = Button(cadre_2, text ='Enregistrer', command = sauver_partie)
BoutonEnregistr.pack(side = TOP,padx = 5, pady = 5)

Label1 = Label(cadre_2, text = 'fichier ')
Label1.pack(side = LEFT, padx = 5, pady = 5)

# widget Entry(nom_fichier)
nom_fichier= StringVar()
Champ = Entry(cadre_2, textvariable= nom_fichier, bg ='bisque', fg='maroon',font=("Helvetica",10))
Champ.focus_set()
Champ.pack(side = LEFT, padx = 5, pady = 5)

# widget Button (bouton Quitter)
BoutonQuitter = Button(fen, text ='Quitter', fg="red", command = fen.destroy)
BoutonQuitter.pack(side = LEFT, padx = 5, pady = 5)

can.bind('<Button-1>',Clic)
fen.mainloop()
                             

