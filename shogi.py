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

def dessine_koma(img:image, taille:int=100, c1=col.blanc, c2=col.bleu) -> image:
    pts = [
        [100, 100],
        [ 60, 130],
        [ 50, 200],
        [150, 200],
        [140, 130],
    ]
    pts = np.array(pts, np.int32)
    cv2.fillPoly(img.img, [pts], c1)
    cv2.polylines(img.img, [pts], True, c2, 10)
    return img

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
    plateau = [[[[x, y], [x+diff(470, 1420)/9, y+diff(100, 980)/9]] ## Création de l'array qui contient toutes les coos des cases
    for x in range2(470, 1450, diff(470, 1450)/9)] for y in range2(100, 980, diff(100, 980)/9)]; plateau = np.array(plateau)
    for x in range(len(plateau)):
        for y in range(len(plateau[x])):
            for c in range(len(plateau[x, y])):
                plateau[x, y, c] = [round(i) for i in plateau[x, y, c]]
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
                img.ecris(shoginame(t), ct_sg(self.plateau[x, y, 0], self.plateau[x, y, 1]), col.blue[::-1] if t.isupper() else col.red[::-1], 3, 2, cv2.FONT_HERSHEY_SIMPLEX)
        dessine_koma(img)
        return img

pt = Shogi()

print(pt)
im = pt.image()
wk = -1
im.montre(1, fullscreen=True)
while wk != 27:
    wk = im.montre(1, fullscreen=True)
    