#importer NumPy qui est une bibliothèque pour langage de programmation Python, destinée à manipuler des tableaux multidimensionnels 
# NB numpy doit etre installée avant l'utiliser 
import numpy as np 
# importer Pygame : un module qui offre des outils permettant de créer des jeux.
import pygame
from pygame.locals import QUIT
# pour pouvoir utilser la methode sys.exit() 
import sys
#pour pouvoir utiliser floor
import math
#class Matrice a comme attributs les dimensions de la matrice que les joueurs modifient NB la matrice ets un atribut d'instance c'est pour qu'on puisse améliorer le jeux si on veut par exemple jouer par deux groupe chaque membre joue sur une matrice contre un membre de l'autre groupe  


########################classe Matrice#########################
class Matrice:
    def __init__(self,l,c):
        self.nb_Ligne=l 
        self.nb_Colonne=c
        self.matrice=np.zeros((self.nb_Ligne,self.nb_Colonne)) # si vous voulez que matrice soit un attribut de classe utilsez : Matrice.matrice=np...
#m est un objet global de la classe Matrice sert à contrôler les conditions du jeux 
m=Matrice(6,7)

BEIGE=(167,139,113)   
ROUGE=(255,0,0) 
BLAN=(229,227,228)

pygame.font.init()
FONT=pygame.font.SysFont('Algerian', 40, bold=False, italic=True)

#################classe Fenetre##################
# class Fenetre est celle qui contient l'interface graphique et les methodes pour gerer cette interface  
class Fenetre:
    #taille d'un petit carreau qui va contenir un pion 100 px
    taille_pion = 100
    #la largeure de l'interface graphique
    largeur = m.nb_Colonne * taille_pion
    #l'hauteur de l'interface graphique
    hauteur = (m.nb_Ligne+1) * taille_pion
    #C’est la fonction qui permet d’initialiser Pygame
    pygame.init()

    # set_mod c’est la fonction en charge de créer un nouvel objet Surface représentant le graphisme actuel à afficher
    window=pygame.display.set_mode((largeur,hauteur))

    # dessiner est une fonction qui sert à dessiner 42 carré dans lequels on dessine des cercles (vide) qui vont contenir les pions 
    def dessiner():
        pygame.display.set_caption("jeu puissance 4")
        for c in range(m.nb_Colonne):
            for l in range(m.nb_Ligne):
                #dessiner un rectangle BEIGE . rect(surface,color,pos_x,pos_y,width,height)
                pygame.draw.rect(Fenetre.window,BEIGE,(c*Fenetre.taille_pion , (l+1)*Fenetre.taille_pion ,Fenetre.taille_pion,Fenetre.taille_pion)) 
                #dessiner les cercles :  circle(surface,color,pos,radius,width)
                pygame.draw.circle(Fenetre.window,BLAN,((c+0.5)*Fenetre.taille_pion,(l+1.5)*Fenetre.taille_pion),Fenetre.taille_pion//2-5)
    
    # dessiner_pion est une fonction qui sert à dessiner un cercle dont la couleur est la position du centre entrés comme paramètres 
    def dessiner_pion(couleur,x,y):
        pygame.draw.circle(Fenetre.window,couleur,(x,y),Fenetre.taille_pion//2-5)
        pygame.display.update()

    #dessiner_rect sert à dessiner un rectangle de couleur entré comme paramètre de dimensions : hauteur=taille_pion , largeur=largeur du graphisme actuel 
    def dessiner_rect(couleur):
        pygame.draw.rect(Fenetre.window,couleur,(0,0,Fenetre.largeur,Fenetre.taille_pion))
        pygame.display.update()

    # sert à afficher un message cette fonction va etre appeler si l'un des deux joueurs gagne ou la matrice est chargée 
    def affiche_message(msg,couleur):
        label=FONT.render(msg,1,couleur)
        Fenetre.window.blit(label,(180,40))
        pygame.display.update()
        pygame.time.wait(6000)

    #cette fonction permet de lancer un son (music) en utilisant le module pygame.mixer.music     
    def music0(son,n):
        pygame.mixer.music.load(son) # chargement du son
        pygame.mixer.music.play(n) # lancement du son
    

###################class Joueur ####################
class Joueur:
    def __init__(self,symbol,couleur) :
        self.est_gagnant=False #indique si le joueur courant est gagnant
       
                             #va fixer 21 pions pour un joueur 
        self.symbol=symbol  #le numero avec lequel le joueur va remplir la case choisie
                            # dans ce as c'est 1 pour joueur 1 et 2 por joueur 2 
        self.couleur=couleur # cet attribut indique la couleur des pions du joueur courant 


    #cette methode affiche un message si le joueur courant est gagnant
    def gagnant(self): 
        self.est_gagnant=True
        Fenetre.music0('win.wav',0)
        Fenetre.affiche_message("Joueur "+str(self.symbol)+" est un gagnant !!! ",self.couleur)
    
    #cette methode consiste à diminuer le nombre des pions du joueur courant chaque fois qu'il pose un dans la matrice  Dans ce cas on ne va pas l'utiliser cela peut etre si on ajouter d'autres fonctions à ce jeux
   

######################class Jouer######################
# Dans cette classe les joueurs attributs jouent sur la matrice m declarée comme variable global
class Jouer:

    def __init__(self,J1,J2):
        self.Joueur1=J1
        self.Joueur2=J2

    # cette methode verifie que la colonne choisi a au moins une ligne ne contient pas un pion
    def est_valid(self,coll): 
        return m.matrice[0][coll]==0
    
    #cette methode trouve la ligne i la plus bas telque m[i][col]==0 et retourne son numero i
    def pos_exacte (self,col):
        for i in range (m.nb_Ligne):
            if (m.matrice[i][col]==0):
                l=i   #!!!! j'ai changé r => l ligne 
        return l
     
    # cette methode permet de  modifier une case de la matrice de m  bien définie par son num de ligne et num de colonne ,cités en paramètres 
    def modifier(self,lig,col,symb):
        m.matrice[lig][col]=symb

    # cette methode retourne 1 si l'un des joueurs gagne ou -1 si la matrice est pleine ou 0 sinon
    def verifier_matrice(self):
        for i in range(m.nb_Ligne):
            for j in range(m.nb_Colonne-3):
               if m.matrice[i][j]==m.matrice[i][j+1]==m.matrice[i][j+2]==m.matrice[i][j+3]!=0:
                  return 1
        
        for i in range(m.nb_Colonne):
            for j in range(m.nb_Ligne-3):
                if m.matrice[j][i]==m.matrice[j+1][i]==m.matrice[j+2][i]==m.matrice[j+3][i]!=0:
                    return 1
        for i in range(m.nb_Ligne-3):
            for j in range(m.nb_Colonne-3-i):
               if m.matrice[i][j]==m.matrice[i+1][j+1]==m.matrice[i+2][j+2]==m.matrice[i+3][j+3]!=0:
                  return 1
        if m.matrice[2][2]==m.matrice[3][3]==m.matrice[4][4]==m.matrice[5][5]!=0:
                  return 1
        for j in range(1,4):
            for i in range(4-j):
               if m.matrice[i+j-1][j+i]==m.matrice[i+j][j+1+i]==m.matrice[i+1+j][j+2+i]==m.matrice[i+j+2][i+j+3]!=0:
                  return 1
        
        for i in range(3,m.nb_Ligne):
            for j in range(i-2):
               if m.matrice[i-j][j]==m.matrice[i-1-j][j+1]==m.matrice[i-2-j][j+2]==m.matrice[i-j-3][j+3]!=0:
                  return 1
        
        for j in range(1,4):
            for i in range(4-j):
               if m.matrice[5-i][j+i]==m.matrice[5-i-1][j+1+i]==m.matrice[5-i-3][j+2+i]==m.matrice[5-i-4][i+j+3]!=0:
                  return 1
        for i in range (3):

            if(m.matrice[5-i][1+i]==m.matrice[4-i][2+i]==m.matrice[3-i][3+i]==m.matrice[2-i][4+i]!=0):
                return 1
        for i in range (2):
            if(m.matrice[5-i][2+i]==m.matrice[4-i][3+i]==m.matrice[3-i][4+i]==m.matrice[2-i][5+i]!=0):
                return 1
        if(m.matrice[5][3]==m.matrice[4][4]==m.matrice[3][5]==m.matrice[2][6]!=0):
                return 1        # for i in range(m.nb_Ligne-3,m.nb_Ligne):
       

        for i in range(m.nb_Ligne):
            for j in range(m.nb_Colonne):
                if(m.matrice[i][j]==0):
                    return 0
            return -1

    #cette methode permet aux joueurs de commencer à jouer 
    def allons_y(self):
        Fenetre.dessiner()
        #lancement de la musique 
        Fenetre.music0('background.wav',-1)
        tour = 0
        # les instruction se repètent tant qu'il y a des case valent 0 et aucun des joueurs gagne
        while(self.verifier_matrice()==0): 
            #pygame.event.get est un gestionnaire d'événements, dès que l'utilisateur du programme effectue une action quelconque (clavier, souris...), c'est cette boucle for qui s'en occupe.
            for event in pygame.event.get():
                if event.type==QUIT: #QUIT : X qui trouve dans toute fenetre,qui nous permet de quitter la fenetre
                    sys.exit()     #  quitter
                if event.type == pygame.MOUSEMOTION:#c'est l'evenement de mouvement  de la souris
                    Fenetre.dessiner_rect(BLAN) # dessiner un rectangle pour la mise à jour de l'espace d'affichage

                    posx= event.pos[0] #récuperer l'abscisse de la position de la souris  
                    if tour == 0: # indique le tour du joueur1 
                       Fenetre.dessiner_pion(self.Joueur1.couleur,posx,Fenetre.taille_pion//2) # on dessine une boule centrée à la position de la souris coloré par le meme couleur des pions du joueur 1 
                    else: # indique le tour du joueur2
                       Fenetre.dessiner_pion(self.Joueur2.couleur,posx,Fenetre.taille_pion//2) ## on dessine une boule centrée à la position de la souris coloré par le meme couleur des pions du joueur 2
                if event.type == pygame.MOUSEBUTTONDOWN:  #!!!! on doit ajouter une variable tour pour faire une condition quand il ajoute 1 et quand 
                                                             #!!!! il ajoute 2 puisque la fonction qui détecte 'click' est la meme pour les deux joueurs

                    Fenetre.dessiner_rect(BLAN) # mise à jour de la zone d'affichage c'est obligatoire au cas ou l'un des deux joueur gagne ou la matrice est pleine un message va etre affiché pour ne pas avoir une boule colorée dans la zone d'affichage
                    posx = event.pos[0] # récuperer l'abscisse de la position de la souris lors de la clique  
                    col = math.floor(posx/Fenetre.taille_pion) #fixer la colonne correspondante de la position  
                    if(self.est_valid(col)): # si la collonne est valide 
                        ligne=self.pos_exacte(col)
                    
                        if tour == 0: # tourne du joueur1
                            self.modifier(ligne,col,self.Joueur1.symbol) # on modifie la case exacte
                            print(m.matrice)
                            Fenetre.dessiner_pion(self.Joueur1.couleur,(col+0.5)*Fenetre.taille_pion,(ligne+1.5)*Fenetre.taille_pion)#on dessine un cercle coloré par le couleur des pions du joueur1
                            tour +=1

                            # on vérifie si le joueur gagne 
                            if(self.verifier_matrice()==1):
                                self.Joueur1.gagnant() #cette methode lance une autre musique qui indique le gain et affiche un message indiquant que le joueur courant est gagnant
                                m.matrice=np.zeros((m.nb_Ligne,m.nb_Colonne))
                                return
                            else :
                                if(self.verifier_matrice()==-1):# on verifie si la matrice est pleine 
                                    Fenetre.music0('game_over.wav') #on lance donc une musique qui indique la fin de jeux
                                    Fenetre.affiche_message("fin de jeux jouer de nouveau !!",ROUGE) 
                                    m.matrice=np.zeros((m.nb_Ligne,m.matrice.nb_Colonne))
                                    return
                        else:  # de meme si tour!=1 juste on remplace le joueur1 par le joueur2
                            self.modifier(ligne,col,self.Joueur2.symbol)
                            print(m.matrice)
                            Fenetre.dessiner_pion(self.Joueur2.couleur,(col+0.5)*Fenetre.taille_pion,(ligne+1.5)*Fenetre.taille_pion)
                            tour +=1
                            tour = tour % 2
                            if(self.verifier_matrice()==1): 
                                self.Joueur2.gagnant()
                                m.matrice=np.zeros((m.nb_Ligne,m.nb_Colonne))
                                return
                            else :
                                if(self.verifier_matrice()==-1):
                                    Fenetre.music0('game_over.wav')
                                    Fenetre.affiche_message("fin de jeux jouer de nouveau !!",ROUGE)
                                    m.matrice=np.zeros((m.nb_Ligne,m.nb_Colonne))
                                    return

    

