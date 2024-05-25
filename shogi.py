#############################
## Author: T-Sana ###########
## 24/5/2024 -> XX/XX/202X ##
#############################
## TODO #################################
## Dessin des pièces en mode graphique ##
## Déplacement des pièces ###############
## Légalité des mouvements des pièces ###
## Promotion des pièces #################
## Parachutage des pièces ###############
#########################################

from Outils.cvt2 import *

def defTab() -> list:
    l = [
        ['l', 'c', 'a', 'o', 'j', 'o', 'a', 'c', 'l'],
        [' ', 't', ' ', ' ', ' ', ' ', ' ', 'f', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        [' ', 'F', ' ', ' ', ' ', ' ', ' ', 'T', ' '],
        ['L', 'C', 'A', 'O', 'R', 'O', 'A', 'C', 'L']
    ]; return l

def shoginame(p) -> str:
    eq = {
        'R':'王', 'J':'玉', 'T':'飛', 'T+':'龍', 'F':'角', 'F+':'馬', 'O':'金',
        'A':'銀', 'A+':'全', 'C':'桂', 'C+':'圭', 'L':'香', 'L+':'杏', 'P':'歩', 'P+':'と'
    }
    if not p in list(eq.keys())+[k.lower() for k in eq.keys()]: return '  '
    return eq[p.upper()]

angles_koma = [81, 117, 85]
tailles_koma = {
    'R': [32, 28.7, 9.7], 'T': [32, 28.7, 9.7], 'O': [32, 28.7, 9.7],
    'C': [32, 28.7, 9.7], 'L': [32, 28.7, 9.7], 'P': [32, 28.7, 9.7]}
for s in 'JR FT AO'.split(): tailles_koma[s[0]]=tailles_koma[s[1]]
for i in tailles_koma: print(i, ':', tailles_koma[i])
def dessine_koma(img:image, ct:(int, int), koma:str, taille:int=100, c1=col.blanc, c2=col.bleu) -> image:
    ori = 0 if koma.isupper() else 180
    return img

class Shogi:
    fond = col.new('#C89678', 'rgb'); col.li = col.new('#281711', 'rgb') ## Couleurs
    proportions_sb = (33, 36) ## Proportions du shogiban
    height_sb = (screen[1]-100) ## Hauteur du shogiban
    width_sb = height_sb/proportions_sb[1]*proportions_sb[0] ## Largeur du shogiban
    xa, xb = screen[0]/2-width_sb/2, screen[0]/2+width_sb/2 ## Numéros des bords du shogiban
    ya, yb = screen[1]/2-height_sb/2, screen[1]/2+height_sb/2 ## Numéros des bords du shogiban
    p1, p2, p3, p4 = [xa, ya], [xb, ya], [xa, yb], [xb, yb] ## Points des bords du shogiban
    ep_li = 3; ep_c = 10 # Eppaisseur des lignes et des cercles du shogiban
    pkda = [ [1500,  305], [1870,  305], [1500,  675], [1870,  675] ] ## Points des bords du komadai A
    pkdb = [ [  50,  305], [ 420,  305], [  50,  675], [ 420,  675] ] ## Points des bords du komadai B
    dy = diff(ya, yb)/9; dx = diff(xa, xb)/9 ## Distance entre les lignes du tableau (axes X et Y)
    img = image('Shogi', image.new_img(fond=[0, 0, 0])) ## Création de l'image
    img.rectangle([i-20 for i in p1], [i+20 for i in p4], fond, 0) ## Dessin du fond
    for y in range2(ya, yb+1, dy): img.ligne([xa, y], [xb, y], col.li, ep_li) ## Lignes horizontales
    for x in range2(xa, xb+1, dx): img.ligne([x, ya], [x, yb], col.li, ep_li) ## Lignes verticales
    for y in range2(ya+diff(ya, yb)/3, yb, diff(ya, yb)/3):
        for x in range2(xa+diff(xa, xb)/3, xb, diff(xa, xb)/3):
            img.cercle([x, y], ep_c, col.li, 0) ## Dessin des points d'aide du shogiban
    img.rectangle(pkda[0], pkda[3], fond, 0) ## Komadai A
    img.rectangle(pkdb[0], pkdb[3], fond, 0) ## Komadai B
    
    def reset(self):
        self.matrix = np.array(defTab())
        self.trait = True

    def __str__(self) -> str:
        t = self.matrix; s = ' ,--------------------------------------------¬'
        for i, l in enumerate(t):
            s += '\n |'
            for c in l:
                t = (fg.blue if c.isupper() else fg.red) + shoginame(c) + fg.rs 
                s += f' {t} |'
            if not i in [2, 5, 8]: s += '\n |----+----+----+----+----+----+----+----+----|'
            elif i == 8: s += '\n `--------------------------------------------´'
            else: s += '\n |----+----+----X----+----+----X----+----+----|'
        return s
    def __init__(self, tableau=defTab()) -> None:
        plateau = [ ## Création de l'array qui contient toutes les coos des cases
            [
                [
                    [x, y],
                    [x+self.dx, y+self.dy]
                ] for x in range2(self.xa, self.xb, self.dx)
            ] for y in range2(self.ya, self.yb, self.dy)
        ]
        self.plateau = np.array(plateau)
        self.trait = True
        self.matrix = np.array(tableau)
    def image(self) -> image:
        img = image('Shogi', img=copy.deepcopy(Shogi.img))
        for x in range(9):
            for y in range(9):
                t = self.matrix[x, y]
                if t in ["", " ", ".", "·"]: continue
                img.ligne(self.plateau[x, y, 0], self.plateau[x, y, 1], col.green, 1)
                img.ligne([self.plateau[x, y, 0, 0], self.plateau[x, y, 1, 1]], [self.plateau[x, y, 1, 0], self.plateau[x, y, 0, 1]], col.green, 1)
                img.ecris(t, ct_sg(self.plateau[x, y, 0], self.plateau[x, y, 1]), col.blue[::-1] if t.isupper() else col.red[::-1], 3, 2, cv2.FONT_HERSHEY_SIMPLEX)
        dessine_koma(img, [0, 0], "r")
        return img

pt = Shogi()

print(pt)
im = pt.image()
wk = -1
im.montre(1, fullscreen=True)
while wk != 27:
    wk = im.montre(1, fullscreen=True)
    