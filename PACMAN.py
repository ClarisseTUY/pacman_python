import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
score = 0  # Initialisation du score
nb_pac_gommes = 0  # Nombre initial de pac-gommes
END_FLAG = False  # indiquer la fin du jeu
MODE_CHASSE= False #indiquer le mode chasse

# Plan du labyrinthe

# 0 vide
# 1 mur 
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            if((x==1 and y==1) or (x==1 and y==HAUTEUR-2) or (x==LARGEUR-2 and y==1) or (x==LARGEUR-2 and y==HAUTEUR-2)):
               GUM[x][y] = 3
            else:
               GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   
   
pacman_color = "yellow"

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink" ,"left",False]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange","left",False] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ,"left",False]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"  ,"left",False ]     )         

# Création de la carte des distances pour Pac-Man
def create_distance_map(grid):
    global HAUTEUR, LARGEUR, nb_pac_gommes
    T = np.array(grid, dtype=np.int32)
    G = 1000  # Valeur G très grande pour représenter les murs
    M = HAUTEUR * LARGEUR  # Valeur M correspondant à la surface totale du labyrinthe
    for i in range(LARGEUR):  # Boucle sur la largeur
        for j in range(HAUTEUR):  # Boucle sur la hauteur
            if grid[i][j] == 1:  # Mur
                T[i][j] = G
            elif grid[i][j] == 0:  # Espace vide avec pac-gomme
                nb_pac_gommes += 1
                T[i][j] = 0
            else:  # Maison des fantômes
                T[i][j] = M
    return T


# Création de la carte des distances pour les fantômes
def create_distance_map_ghost(grid):
    global HAUTEUR, LARGEUR
    T = np.array(grid, dtype=np.int32)
    G = 1000  # Valeur G très grande pour représenter les murs
    M = HAUTEUR * LARGEUR  # Valeur M correspondant à la surface totale du labyrinthe
    for i in range(LARGEUR):  # Boucle sur la largeur
        for j in range(HAUTEUR):  # Boucle sur la hauteur
            T[i][j] = G
    for F in Ghosts:
        T[F[0]][F[1]] = 0  # Position initiale des fantômes
    return T


# Création de la carte des distances
distance_map = create_distance_map(TBL)
distance_map_G = create_distance_map_ghost(TBL)
# placements des pacgums et des fantomes


##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche, pacman_color
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e=5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
         elif(GUM[x][y]==3):
            xx=To(x)
            yy=To(y)
            e=8
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="#00FF04")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman          
      if MODE_CHASSE:
         pacman_color="#FB00FF" #rose
      else :
         pacman_color="yellow" #jaune
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = pacman_color)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      if MODE_CHASSE:
         eyes_color="white" #blanc
      else :
         eyes_color="black" #noir

      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,eyes_color)
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,eyes_color)
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################
      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x, y, is_outside):
    L = []
    if (TBL[x][y-1] == 0) or (not is_outside and TBL[x][y-1] == 2): L.append(((0, -1), "up"))
    if (TBL[x][y+1] == 0) or (not is_outside and TBL[x][y+1] == 2): L.append(((0, 1), "down"))
    if (TBL[x+1][y] ==0) or (not is_outside and TBL[x+1][y] == 2): L.append(((1, 0), "right"))
    if (TBL[x-1][y] == 0) or (not is_outside and TBL[x-1][y] == 2): L.append(((-1, 0), "left"))
    return L


# Indicateur de collision entre Pac-Man et un fantôme
collision = False

# Copie de la carte des distances pour les fantômes
new_distance_map_G = distance_map_G

# Liste des positions des fantômes dans la maison des fantômes
maison = [(F[0], F[1]) for F in Ghosts if TBL[F[0]][F[1]] == 2]

# Fonction d'intelligence artificielle pour Pac-Man
def IAPacman():
    global PacManPos, Ghosts, score, nb_pac_gommes, collision, new_distance_map_G, MODE_CHASSE
    
    # Mise à jour de la carte des distances pour Pac-Man
    new_map = update_distance_map(distance_map)
    # Mise à jour de la carte des distances pour les fantômes
    new_distance_map_G = update_distance_map_ghost(distance_map_G)
    
    # Détermination des mouvements possibles pour Pac-Man
    L = PacManPossibleMove()
    
    # Vérifie si Pac-Man mange une pac-gomme ou une super pac-gomme
    gum_val = GUM[PacManPos[0]][PacManPos[1]]
    if gum_val == 1 or gum_val == 3:
        GUM[PacManPos[0]][PacManPos[1]] = 0  # Enlève la pac-gomme de la grille
        score += 100  # Augmente le score de 100 points
        nb_pac_gommes -= 1  # Décrémente le nombre de pac-gommes restantes

        if gum_val == 3:
            MODE_CHASSE = True  # Active le mode chasse si Pac-Man mange une super pac-gomme
    
    # Choix du mouvement de Pac-Man en fonction du mode chasse et des distances aux fantômes
    if MODE_CHASSE:
        # Recherche un fantôme à chasser
        choix = recherche(new_distance_map_G, L)
    elif new_distance_map_G[PacManPos[0]][PacManPos[1]] > 3:
        # Se déplace normalement si les fantômes sont éloignés
        choix = recherche(new_map, L)
    else:
        # Fuit les fantômes s'ils sont proches
        choix = fuite(new_distance_map_G, L)
    
    # Met à jour la position de Pac-Man en ajoutant les coordonnées du mouvement choisi
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]

    # Vérifie les collisions entre Pac-Man et les fantômes
    test_collision()
    
    # Affiche les distances mises à jour sur la grille (à des fins de débogage)
    affichage_distances(new_map, new_distance_map_G)


def affichage_distances(new_map, new_distance_map_G):
   # juste pour montrer comment on se sert de la fonction SetInfo1
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         info = "{}".format(new_map[x][y])
         if(new_map[x][y]<HAUTEUR*LARGEUR and new_map[x][y]!=0):
            SetInfo1(x,y,info)
         info2 = "{}".format(new_distance_map_G[x][y])
         if(new_distance_map_G[x][y]<HAUTEUR*LARGEUR ):
            SetInfo2(x,y,info2)

def recherche(new_map, L):
    # Fonction qui recherche le meilleur mouvement possible pour Pac-Man en fonction de la carte des distances

    # Initialiser une liste pour stocker les distances valides et leurs indices
    distances_voisins = []
    
    # Vérifier chaque mouvement possible
    for index, (dx, dy) in enumerate(L):
        # Calculer la nouvelle position en ajoutant le déplacement à la position actuelle de Pac-Man
        new_x = PacManPos[0] + dx
        new_y = PacManPos[1] + dy
        
        # Vérifie que la nouvelle position est dans la grille
        if 0 <= new_x < LARGEUR and 0 <= new_y < HAUTEUR:
            # Vérifie que la nouvelle position n'est pas un obstacle
            if new_map[new_x][new_y] != 1000:
                # Ajouter la distance et l'index du mouvement à la liste des distances valides
                distances_voisins.append((new_map[new_x][new_y], index))
    
    # Initialiser les variables pour trouver l'index du mouvement avec la plus petite distance
    min_distance_index = None
    min_distance = float('inf')
    
    # Si des mouvements valides ont été trouvés, trouver l'index du mouvement avec la distance minimale
    if distances_voisins:
        for distance, index in distances_voisins:
            # Mettre à jour la distance minimale et l'index correspondant
            if distance < min_distance:
                min_distance = distance
                min_distance_index = index
    
    # Retourner l'index du mouvement avec la plus petite distance trouvée
    return min_distance_index
def fuite(new_distance_map_G, L):
    # Fonction qui recherche le meilleur mouvement pour fuir les fantômes en fonction de la carte des distances des fantômes

    # Initialiser une liste pour stocker les distances valides et leurs indices
    distances_voisins = []
    
    # Vérifier chaque mouvement possible
    for index, (dx, dy) in enumerate(L):
        # Calculer la nouvelle position en ajoutant le déplacement à la position actuelle de Pac-Man
        new_x = PacManPos[0] + dx
        new_y = PacManPos[1] + dy
        
        # Vérifie que la nouvelle position est dans la grille
        if 0 <= new_x < LARGEUR and 0 <= new_y < HAUTEUR:
            # Vérifie que la nouvelle position n'est pas un obstacle
            if new_distance_map_G[new_x][new_y] != 1000:
                # Ajouter la distance et l'index du mouvement à la liste des distances valides
                distances_voisins.append((new_distance_map_G[new_x][new_y], index))
    
    # Initialiser les variables pour trouver l'index du mouvement avec la plus grande distance
    max_distance_index = None
    max_distance = -1
    
    # Si des mouvements valides ont été trouvés, trouver l'index du mouvement avec la distance maximale
    if distances_voisins:
        for distance, index in distances_voisins:
            # Mettre à jour la distance maximale et l'index correspondant
            if distance > max_distance:
                max_distance = distance
                max_distance_index = index
    
    # Retourner l'index du mouvement avec la plus grande distance trouvée
    return max_distance_index
def update_distance_map(distance_map):
    global PacManPos 
    changement = True 
    while changement:  
        changement = False 
        for j in range(1, HAUTEUR - 1):  # Parcours les lignes de la carte de distance
            for i in range(1, LARGEUR - 1):  # Parcours les colonnes de la carte de distance
                if distance_map[i][j] < (HAUTEUR - 1) * (LARGEUR - 1):                    
                    # Si Pac-Man est sur cette case et il y a une pac-gomme
                    if distance_map[i][j] == 0 and PacManPos[0] == i and PacManPos[1] == j:
                        # Recherche la case voisine avec la distance la plus petite
                        min_neighbor = min(
                            distance_map[PacManPos[0] - 1][PacManPos[1]], 
                            distance_map[PacManPos[0] + 1][PacManPos[1]], 
                            distance_map[PacManPos[0]][PacManPos[1] - 1], 
                            distance_map[PacManPos[0]][PacManPos[1] + 1]
                        )
                        #distance +1
                        new_distance = min_neighbor + 1

                        #si elle est différente, mise à jour de la distance de la case actuelle
                        if distance_map[i][j] != new_distance:
                            distance_map[i][j] = new_distance
                            changement = True #un changement à eu lieu

                    # Si la case n'est pas une pac-gomme, calcule la distance basée sur les voisins
                    elif distance_map[i][j] != 0:
                        min_neighbor = min(
                            distance_map[i - 1][j], 
                            distance_map[i + 1][j], 
                            distance_map[i][j - 1], 
                            distance_map[i][j + 1]
                        )
                        new_distance = min_neighbor + 1
                        # Si la nouvelle distance est différente de la distance actuelle, met à jour et marque un changement
                        if distance_map[i][j] != new_distance:
                            distance_map[i][j] = new_distance
                            changement = True
    return distance_map  # Renvoie la carte de distances mise à jour

def update_distance_map_ghost(distance_map):
    global Ghosts  # Permet d'accéder aux positions des fantômes depuis l'extérieur de cette fonction
    G = 1000  # Valeur très grande pour les murs et les obstacles
    M = HAUTEUR * LARGEUR  # Valeur correspondant à la surface totale du labyrinthe

    # Initialiser la carte de distances tout en maintenant les murs à 1000
    for i in range(LARGEUR):
        for j in range(HAUTEUR):
            if TBL[i][j] == 1:  # Mur
                distance_map[i][j] = G
            else:
                distance_map[i][j] = M

    # Placer les fantômes avec une distance initiale de 0
    for F in Ghosts:
        distance_map[F[0]][F[1]] = 0
    
    # Utiliser une file d'attente pour la recherche 
    queue = [(F[0], F[1]) for F in Ghosts]

    while queue:
        x, y = queue.pop(0)  # Prendre le premier élément de la file d'attente
        # Vérifier si la case est dans la maison des fantômes
        # auquel cas la distance devient la distance maximale
        if TBL[x][y] == 2:
            distance_map[x][y] = HAUTEUR * LARGEUR
        else:
            # La distance actuelle 
            current_distance = distance_map[x][y]

            # Vérifie les voisins dans les quatre directions: haut, bas, gauche, droite
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
               # Calcule les nouvelles coordonnées en ajoutant les déplacements dx et dy
               nx, ny = x + dx, y + dy
               
               # Vérifie si les nouvelles coordonnées sont à l'intérieur des limites du labyrinthe
               if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                     # Vérifie si la case n'est pas un mur et si la nouvelle distance est plus courte que la distance actuelle
                     if TBL[nx][ny] != 1 and distance_map[nx][ny] > current_distance + 1:
                        # Met à jour la distance vers la case voisine avec une distance plus courte
                        distance_map[nx][ny] = current_distance + 1
                        # Ajoute les nouvelles coordonnées à la file d'attente pour les traiter ultérieurement
                        queue.append((nx, ny))


    return distance_map  # Renvoyer la carte de distances mise à jour


def IAGhosts():
    global collision, distance_map_G

    for F in Ghosts:
        possible_moves = GhostsPossibleMove(F[0], F[1], F[4])
        next_move = None
        
        # Si le fantôme peut continuer dans sa direction actuelle
        for move in possible_moves:
            if move[1] == F[3]:  # Compare avec la direction courante
                next_move = move
                break
        
        # Si le fantôme ne peut pas continuer dans sa direction actuelle ou un croisement
        if not next_move or len(possible_moves) > 2:
            next_move = random.choice(possible_moves)
        
        # Mise à jour de la position et de la direction courante
        F[0] += next_move[0][0]
        F[1] += next_move[0][1]
        F[3] = next_move[1]


        # On met à jour l'état du fantôme que s'il est sorti de la maison des fantômes
        if TBL[F[0]][F[1]] != 2:
            F[4] = True

    test_collision()

def test_collision():
    global PacManPos, collision, END_FLAG, score, maison
    
    # Initialisation de la variable de collision à False
    collision = False
    
    # Parcours de chaque fantôme pour vérifier s'il y a une collision avec Pac-Man
    for F in Ghosts:
        # Vérifie si la position de Pac-Man correspond à la position du fantôme actuel
        collision = PacManPos[0] == F[0] and PacManPos[1] == F[1]
        
        # Si une collision est détectée
        if collision == True:
            # Si le mode de jeu est MODE_CHASSE
            if MODE_CHASSE:
                # Sélectionne aléatoirement une nouvelle position dans la maison pour le fantôme
                new_coord = random.choice(maison)
                F[0] = new_coord[0]
                F[1] = new_coord[1]
                F[4] = False 
                score += 2000  # Augmente le score du joueur de 2000 points
                
            # Si le mode de jeu n'est pas MODE_CHASSE
            else: 
                # Définit la fin de partie à True
                END_FLAG = True

 
#  Boucle principale de votre jeu appelée toutes les 500ms
cpt=0
iteration = 0
def PlayOneTurn():
   global iteration, END_FLAG, cpt, MODE_CHASSE
   if not PAUSE_FLAG and not END_FLAG :    
      iteration += 1
      if iteration % 2 == 0 :   
         IAPacman()
         if nb_pac_gommes==0 :
            END_FLAG=True
      else:                    
         IAGhosts()

      if MODE_CHASSE :
         cpt+=1 
         if cpt==16:
            MODE_CHASSE=False
            cpt=0
   Affiche(pacman_color, message="Score : {}".format(score))
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   