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
    fond = [200, 150, 120]
    col.li = [40, 23, 17]
    xa, xb = 470, 1450
    ya, yb = 100, 980
    ep_li = 3
    ep_c = 10
    p1, p2, p3, p4 = [xa, ya], [xb, ya], [xa, yb], [xb, yb]
    
    img = image('Shogi', image.new_img(fond=[0, 0, 0]))
    img.rectangle([i-20 for i in p1], [i+20 for i in p4], fond, 0) ## Fond
    for y in range2(ya, yb+1, diff(ya, yb)/9): ## Lignes horizontales
        img.ligne([xa, y], [xb, y], col.li, ep_li)
    for x in range2(xa, xb+1, diff(xa, xb)/9): ## Lignes verticales
        img.ligne([x, ya], [x, yb], col.li, ep_li)
    for y in range2(ya+diff(ya, yb)/3, yb, diff(ya, yb)/3): ## Points d'aide
        for x in range2(xa+diff(xa, xb)/3, xb, diff(xa, xb)/3):
            img.cercle([x, y], ep_c, col.li, 0)
    
    pt


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
    def montre(self):
        img = image('Shogi', img=copy.deepcopy(Shogi.img))
        ### Dessiner les pièces
        img.montre(fullscreen=True)

pt = Shogi()

#print(pt)
pt.montre()