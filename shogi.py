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

GUIDES = True ## TODO -> TO REMOVE ##

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
    'R': [32, 28.7, 9.7],
    'T': [31, 27.7, 9.3],
    'O': [30, 26.7, 8.8],
    'C': [29, 25.5, 8.3],
    'L': [28, 23.5, 8.0],
    'P': [27, 22.5, 7.75]}
for s in 'JR FT AO'.split(): tailles_koma[s[0]]=tailles_koma[s[1]]
for km in tailles_koma:
    tailles_koma[km] = [27.22222222222222*(v/10) for v in tailles_koma[km]]

for i in tailles_koma: print(i, ':', tailles_koma[i])
def dessine_koma(img:image, p1:(int, int), p2:(int, int), koma:str, taille:int=100, c1=col.blanc, c2=col.bleu) -> image:
    ori = 0 if koma.isupper() else 180
    ct = ct_sg(p1, p2)
    ch = coosCercle(ct, tailles_koma[koma.upper()][0]/2, 270+ori)
    img.cercle(ch, 5, col.bleu, 0)

    if GUIDES: ### Guides ## TODO -> TO REMOVE ###
        img.ligne(p1, p2, col.green, 1)
        img.ligne([p1[0], p2[1]], [p2[0], p1[1]], col.green, 1)
        img.ecris(koma, ct_sg(p1, p2), col.blue[::-1] if koma.isupper() else col.red[::-1], 3, 2, cv2.FONT_HERSHEY_SIMPLEX)
        img.cercle(ct_sg(p1, p2), 5, col.red, 0)
    return img
save = {}
class Shogi:
    ### CONSTANTES ###
    col.bg=col.new('#1340ff', 'rgb')
    fond = col.new('#C89678', 'rgb'); col.li = col.new('#281711', 'rgb') ## Couleurs
    proportions_sb = (33, 36) ## Proportions des lignes du shogiban
    proportions_sb_ext = (33.33, 36.36) ## Proportions du shogiban (10x11 sun (mesure japonaise (~3.03cm)))
    proportions_kd = 12.12 ## Proportions des komadai (4x4 sun)
    height_sb = (screen[1]-100) ## Hauteur du shogiban sur l'écran en pixels
    conversion = height_sb/proportions_sb[1] ## ~27.22222222222222 ## px/cm
    width_sb = conversion*proportions_sb[0] ## Largeur du shogiban sur l'écran en pixels
    xa, xb = screen[0]/2-width_sb/2, screen[0]/2+width_sb/2 ## Numéros des bords du shogiban
    ya, yb = screen[1]/2-height_sb/2, screen[1]/2+height_sb/2 ## Numéros des bords du shogiban
    p1, p2, p3, p4 = [xa, ya], [xb, ya], [xa, yb], [xb, yb] ## Points des bords du shogiban
    ep_li = 3; ep_c = 10 # Eppaisseur des lignes et des cercles du shogiban
    dy = diff(ya, yb)/9; dx = diff(xa, xb)/9 ## Distance entre les lignes du tableau (axes X et Y)
    px, py = conversion*proportions_sb_ext[1]-height_sb, width_sb/proportions_sb[0]*proportions_sb_ext[0]-width_sb
    ctkda, ctkdb = (moyenne(xb+px, screen[0]), screen[1]/15*8), (moyenne(0, xa-px), screen[1]/15*7) ## Points du centre des komadai
    mgkd = 20 ## Émargements des komadai (en pixels)
    save['ctkda'] = ctkda; save['ctkdb'] = ctkdb
    save['dist'] = racine_carree((conversion*(proportions_kd/2))**2*2)
    pkda = [ coosCercle(save['ctkda'], save['dist'], 90*i+45) for i in range(4) ] ## Points des bords du komadai A
    pkda = [pkda[0], pkda[1], pkda[3], pkda[2]]
    pkdb = [ coosCercle(save['ctkdb'], save['dist'], 90*i+45) for i in range(4) ] ## Points des bords du komadai B
    pkdb = [pkdb[0], pkdb[1], pkdb[3], pkdb[2]]
    ### Création de l'image
    img = image('Shogi', image.new_img(fond=col.bg)) ## Création de l'image
    img.rectangle([p1[0]-px, p1[1]-py], [p4[0]+px, p4[1]+py], fond, 0) ## Dessin du shogiban
    for y in range2(ya, yb+1, dy): img.ligne([xa, y], [xb, y], col.li, ep_li) ## Lignes horizontales
    for x in range2(xa, xb+1, dx): img.ligne([x, ya], [x, yb], col.li, ep_li) ## Lignes verticales
    for y in range2(ya+diff(ya, yb)/3, yb, diff(ya, yb)/3): ## Dessin des points d'aide du shogiban
        for x in range2(xa+diff(xa, xb)/3, xb, diff(xa, xb)/3): img.cercle([x, y], ep_c, col.li, 0)
    img.rectangle(pkda[0], pkda[3], fond, 0) ## Komadai A
    img.rectangle(pkdb[0], pkdb[3], fond, 0) ## Komadai B
    if GUIDES: ### Guides ## TODO -> TO REMOVE ###
        img.ligne((screen[0]/2, 0), (screen[0]/2, screen[1]), col.red, 1)
        img.ligne((0, screen[1]/2), (screen[0], screen[1]/2), col.red, 1)
        img.ligne((0,0), screen, col.red, 1); img.ligne((screen[0],0), (0,screen[1]), col.red, 1)
        img.ligne(pkda[0], pkda[3], col.green, 1);img.ligne(pkda[1], pkda[2], col.green, 1) ## Komadai A
        img.ligne(pkdb[0], pkdb[3], col.green, 1);img.ligne(pkdb[1], pkdb[2], col.green, 1) ## Komadai B
    
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
                dessine_koma(img, self.plateau[x, y, 0], self.plateau[x, y, 1], t)
        return img

if __name__ == '__main__' and True:
    pt = Shogi()

    print(pt)
    im = pt.image()
    wk = -1
    im.montre(1, fullscreen=True)
    while wk != 27:
        wk = im.montre(1, fullscreen=True)
        