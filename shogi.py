from Outils.cvt2 import *

def defTab() -> list:
    l = [
        ['l', 'c', 'a', 'o', 'r', 'o', 'a', 'c', 'l'],
        [' ', 't', ' ', ' ', ' ', ' ', ' ', 'f', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        [' ', 'F', ' ', ' ', ' ', ' ', ' ', 'T', ' '],
        ['L', 'C', 'A', 'O', 'R', 'O', 'A', 'C', 'L']
    ]; return l

class Shogi:
    fond = [200, 150, 120]; col.li = [40, 23, 17] ## Couleurs
    xa, xb = 470, 1450; ya, yb = 100, 980 ## Numéros des bords du shogiban
    p1, p2, p3, p4 = [xa, ya], [xb, ya], [xa, yb], [xb, yb] ## Points des bords du shogiban
    ep_li = 3; ep_c = 10 # Eppaisseur des lignes et des cercles du shogiban
    pkda = [ [1500,  305], [1870,  305], [1500,  675], [1870,  675] ] ## Points des bords du komadai A
    pkdb = [ [  50,  305], [ 420,  305], [  50,  675], [ 420,  675] ] ## Points des bords du komadai B
    dy = diff(ya, yb)/9; dx = diff(xa, xb)/9 ## Distance entre les lignes du tableau (axes X et Y)
    img = image('Shogi', image.new_img(fond=[0, 0, 0])) ## Création de l'image
    img.rectangle([i-20 for i in p1], [i+20 for i in p4], fond, 0) ## Dessin du fond
    for y in range2(ya, yb+1, dy): img.ligne([xa, y], [xb, y], col.li, ep_li) ## Lignes horizontales
    for x in range2(xa, xb+1, dx): img.ligne([x, ya], [x, yb], col.li, ep_li) ## Lignes verticales
    plateau = [[[[x, y], [x+diff(470, 1420)/9, y+diff(100, 980)/9]] ## Création de l'array
    for y in range2(100, 980, diff(100, 980)/9)] for x in range2(   ## qui contient toutes
    470, 1450, diff(470, 1450)/9)]; plateau = np.array(plateau)     ## les coos des cases
    for x in range(len(plateau)):
        for y in range(len(plateau[x])):
            for c in range(len(plateau[x, y])):
                plateau[x, y, c] = [round(i) for i in plateau[x, y, c]]
    for y in range2(ya+diff(ya, yb)/3, yb, diff(ya, yb)/3):
        for x in range2(xa+diff(xa, xb)/3, xb, diff(xa, xb)/3):
            img.cercle([x, y], ep_c, col.li, 0) ## Dessin des points d'aide du shogiban
    img.rectangle(pkda[0], pkda[3], fond, 0) ## Komadai A
    img.rectangle(pkdb[0], pkdb[3], fond, 0) ## Komadai B
    


    def __str__(self):
        t = self.matrix; s = ' .-----------------------------------.'
        for i, l in enumerate(t):
            s += '\n |'
            for c in l: s += f' {c} |'
            if not i in [2, 5, 8]: s += '\n |---+---+---+---+---+---+---+---+---|'
            elif i == 8: s += '\n `-----------------------------------´'
            else: s += '\n |---+---+---*---+---+---*---+---+---|'
        return s
    def __init__(self, tableau=defTab()) -> None:
        self.matrix = np.array(tableau)
    def image(self):
        img = image('Shogi', img=copy.deepcopy(Shogi.img))
        ### Dessiner les pièces
        return img

pt = Shogi()

print(pt)
im = pt.image()
wk = -1
while wk != 27:
    wk = im.montre(fullscreen=True)