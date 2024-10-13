from tsanap import *

class res:
    resses, resind = [screen, [1680, 1050], [1366, 768]], 0
    res = resses[resind]
    def update():
        res.resind = (res.resind+1)%len(res.resses)
        res.res = res.resses[res.resind]
        mouse.reload = True

cartes_types = "A 2 3 4 5 6 7 8 9 10 V D R".split()
noirs, rouges = "♠♣", "♦♥"
def get_cartes():
    cartes = [f"¬{n}{p}" for p in "♦♥♠♣" for n in cartes_types]
    np.random.shuffle(cartes)
    return cartes

actions = ["Pioche", "Sel_carte", "Game_carte", "Res_carte"]

class mouse:
    click = False
    pos = [-1, -1]
    action = None
    reload = False

def check_retourne_cartes(sol) -> None:
    for n in range(len(sol.jeu)):
        if sol.jeu[n] != [] and sol.jeu[n][-1][0] == "¬":
            sol.jeu[n][-1] = sol.jeu[n][-1][1::]

def legal(a, b) -> bool:
    if b == None: return False
    return ((a[-1] in rouges) == (b[-1] in noirs)) and (cartes_types.index(b[:-1:])-cartes_types.index(a[:-1:]) == 1)

def get_mouse(event, x, y, flags, params) -> None:
    pos, sol = (x, y), params
    pcs, pcp, psp, pcr = sol.pcs, sol.pcp, sol.psp, sol.pcr
    if event == cv2.EVENT_LBUTTONDOWN and not mouse.click:
        if clicked_in(pos, pcp): mouse.action = actions[0] ## Nouvelle pioche
        if clicked_in(pos, psp): ## Prends carte dans la pioche
            mouse.action = actions[1]
            mouse.reload = True
            mouse.pos = pos
        if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]): ## Prends carte(s) dans le jeu
            w, h, pcs = sol.w, sol.h, sol.pcs
            for x, column in enumerate(sol.jeu):
                pc = pcs[x]
                Y = diff(pc[0][1], pc[1][1])-h
                for y, card in [[a, b] for a, b in enumerate(column)][::-1]:
                    X = (diff(pc[0][0], pc[1][0])-w)/2
                    pt1, pt2 = [pc[0][0]+X, pc[0][1]+Y/12*y], [pc[1][0]-X, pc[0][1]+Y/12*y+h]
                    if clicked_in(pos, [pt1, pt2]):
                        if sol.jeu[x][y][0] != "¬":
                            mouse.action, mouse.column, mouse.row = actions[2], x, y
                        break
        if clicked_in(pos, pcr): ## Prends carte dans la resolution
            mouse.action, mouse.column = actions[3], int(diff(pcr[0][0], x)/diff(pcr[0][0], pcr[1][0])*4)
        if mouse.action != None: mouse.click = True
    elif event == cv2.EVENT_LBUTTONUP and mouse.click:
        if clicked_in(pos, pcp) and mouse.action == actions[0]: sol.update_sel(1) # Nouvelle pioche
        elif mouse.action == actions[1]: ## Carte venant de la pioche
            if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]): ## Cartes dans le jeu
                for n, column in enumerate(pcs):
                    if clicked_in(pos, column):
                        if (sol.jeu[n] == [] and sol.sel[0].lower()=="r") or legal(sol.sel[-1], None if len(sol.jeu[n]) == 0 else sol.jeu[n][-1]):
                            sol.jeu[n].append(sol.sel.pop(-1))
            elif clicked_in(pos, pcr): ## Cartes dans la résolution
                x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
                for c in range(4):
                    if clicked_in(pos, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]): break
                if sol.end[c] == []:
                    if sol.sel[-1][0].lower() == "a": sol.end[c].append(sol.sel.pop(-1))
                else:
                    if sol.end[c][-1][-1] == sol.sel[-1][-1]:
                        if cartes_types.index(sol.sel[-1][:-1:])-cartes_types.index(sol.end[c][-1][:-1:]) == 1:
                            sol.end[c].append(sol.sel.pop(-1))
        elif mouse.action == actions[2]: ## Carte(s) venant du jeu
            if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]): ## Carte(s) dans le jeu
                for x, column in enumerate(pcs):
                    if clicked_in(pos, column) and not x == mouse.column:
                        if (sol.jeu[x] == [] and sol.jeu[mouse.column][mouse.row][0].lower()=="r") or legal(sol.jeu[mouse.column][mouse.row], None if len(sol.jeu[x]) == 0 else sol.jeu[x][-1]):
                            cards = [sol.jeu[mouse.column].pop(y) for y in range(mouse.row, len(sol.jeu[mouse.column]))[::-1]][::-1]
                            for card in cards: sol.jeu[x].append(card)
                        break
                check_retourne_cartes(sol)
            elif clicked_in(pos, pcr) and mouse.row == len(sol.jeu[mouse.column])-1: ## Carte dans la résolution
                x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
                for c in range(4):
                    if clicked_in(pos, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]): break
                if sol.end[c] == []:
                    if sol.jeu[mouse.column][-1][0].lower() == "a":
                        sol.end[c].append(sol.jeu[mouse.column].pop(-1))
                else:
                    if sol.end[c][-1][-1] == sol.jeu[mouse.column][-1][-1]:
                        if cartes_types.index(sol.jeu[mouse.column][-1][:-1:])-cartes_types.index(sol.end[c][-1][:-1:]) == 1:
                            sol.end[c].append(sol.jeu[mouse.column].pop(-1))
                check_retourne_cartes(sol)
        elif mouse.action == actions[3]: ## Carte venant de la résolution
            if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]): ## Cartes dans le jeu
                for n, column in enumerate(pcs):
                    if clicked_in(pos, column):
                        if (sol.jeu[n] == [] and sol.end[mouse.column][0].lower()=="r") or legal(sol.end[mouse.column][-1], None if len(sol.jeu[n]) == 0 else sol.jeu[n][-1]):
                            sol.jeu[n].append(sol.end[mouse.column].pop(-1))
            elif clicked_in(pos, pcr): ## Cartes dans la résolution
                x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
                for c in range(4):
                    if clicked_in(pos, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]): break
                if sol.end[c] == []:
                    if sol.end[mouse.column][-1][0].lower() == "a": sol.end[c].append(sol.end[mouse.column].pop(-1))
                    else: sol.end[c], sol.end[mouse.column] = sol.end[mouse.column], []
                else:
                    if sol.end[c][-1][-1] == sol.end[mouse.column][-1][-1]:
                        if cartes_types.index(sol.end[mouse.column][-1][:-1:])-cartes_types.index(sol.end[c][-1][:-1:]) == 1:
                            sol.end[c].append(sol.end[mouse.column].pop(-1))
        mouse.click, mouse.reload, mouse.action = False, True, None
    elif event == cv2.EVENT_MOUSEMOVE and mouse.click: ## Deplacement d'une carte
        if mouse.action in actions[1::]: mouse.pos, mouse.reload = pos, True

def carreau(img:image, ct, taille, an=0) -> None:
    v = 1920/res.res[0]+2
    a, b = taille*5/v, taille*3/v
    pts = [coosCercle(ct, [a, b][ind%2], [i+90 for i in range(0, 360, 90)][ind]+an) for ind in range(4)]
    cv2.fillPoly(img.img, [np.array(pts, np.int32)], col.red[::-1], cv2.LINE_AA)
def coeur(img, ct, taille=1, an=0) -> None:
    v = 1920/res.res[0]+2
    a, b = taille*3/v, taille*5/v
    pts = [coosCercle(ct, [a, b][ind%2], [i for i in range(0, 270, 90)][ind]+an) for ind in range(3)] + [coosCercle(ct, a, 240+an), coosCercle(ct, a/2, 270+an), coosCercle(ct, a, 300+an)]
    cv2.fillPoly(img.img, [np.array(pts, np.int32)], col.red[::-1], cv2.LINE_AA)
def pique(img, ct, taille=1, an=0) -> None:
    v = 1920/res.res[0]+2
    a, b = taille*3/v, taille*5/v
    pts = [coosCercle(ct, [a, b][ind%2], [i+180 for i in range(0, 270, 90)][ind]+an) for ind in range(3)] + [coosCercle(ct, a, 60+an), ct, coosCercle(ct, b, 85+an), coosCercle(ct, b, 95+an), ct, coosCercle(ct, a, 120+an)]
    cv2.fillPoly(img.img, [np.array(pts, np.int32)], col.black[::-1], cv2.LINE_AA)
def trefle(img:image, ct, taille=1, an=0) -> None:
    v = 1920/res.res[0]+2
    a, b = taille*3/v, taille*5/v
    pts = [ct, coosCercle(ct, b, 85+an), coosCercle(ct, b, 95+an)]
    cv2.fillPoly(img.img, [np.array(pts, np.int32)], col.black[::-1], cv2.LINE_AA)
    for c in [coosCercle(ct, a, 270+an)] + [coosCercle(ct, a, ang+an) for ang in [0, 180]]:
        img.cercle(c, a/2, col.noir, 0, 2)
        img.ligne(ct, c, col.noir, 6/v, 2)

class sol:
    def positions_figures(self, p1, p4) -> list:
        p2, p3 = [p4[0], p1[1]], [p1[0], p4[1]]
        cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
        cth, ctb = ct_sg(p1, cd), ct_sg(p4, cg)
        ct = ct_sg(p1, p4)
        pts = [
            [ct], # As
            [cth, ctb], # 2
            [cth, ctb, ct], # 3
            [ct_sg(p, ct) for p in [p1, p2, p3, p4]], # 4
            [ct_sg(p, ct) for p in [p1, p2, p3, p4]] + [ct], # 5
            [ct_sg(p, ct) for p in [p1, p2, p3, p4]] + [ct_sg(pt, ct) for pt in[cg, cd]], # 6
            [ct_sg(p, ct) for p in [p1, p2, p3, p4]] + [ct_sg(pt, ct) for pt in[cg, cd]] + [pt_sg(cth, ctb, 2)], # 7
            [ct_sg(p, ct) for p in [p1, p2, p3, p4]] + [ct_sg(pt, ct) for pt in[cg, cd]] + [pt_sg(cth, ctb, 3), pt_sg(ctb, cth, 3)], # 8
            [ct_sg([cth, ctb][i], [[p1, p2, cg, cd], [cg, cd, p3, p4]][i][j]) for i in range(2) for j in range(4)] + [ct], # 9
            [ct_sg([cth, ctb][i], [[p1, p2, cg, cd], [cg, cd, p3, p4]][i][j]) for i in range(2) for j in range(4)] + [cth, ctb], # 10
        ]
        sens = [ [0], [0, 180], [0, 180, 0], [0, 0, 180, 180], [0, 0, 180, 180, 0], [0, 0, 180, 180, 0, 0],
            [0, 0, 180, 180, 0, 0, 0], [0, 0, 180, 180, 0, 0, 0, 180], [0, 0, 0, 0, 180, 180, 180, 180, 0],
            [0, 0, 0, 0, 180, 180, 180, 180, 0, 180] ]
        return [zip(pts[i], sens[i]) for i in range(min(len(pts), len(sens)))]
    def __init__(self, nom="Solitaire") -> None:
        self.debug = False
        self.name = nom
        self.cartes = get_cartes()
        self.jeu = []
        self.sel = []
        self.end = [[] for _ in range(4)]
        for i in range(7):
            l = [self.cartes.pop(x) for x in range(i+1)]
            l[-1] = l[-1][1::]
            self.jeu.append(l)
    def restart(self) -> None:
        self.cartes = get_cartes()
        self.jeu = []
        self.sel = []
        self.end = [[] for _ in range(4)]
        for i in range(7):
            l = [self.cartes.pop(x) for x in range(i+1)]
            l[-1] = l[-1][1::]
            self.jeu.append(l)
    def __str__(self) -> None:
        return len(self.cartes)
    def update_sel(self, n=3) -> None:
        if self.cartes != []:
            l = self.cartes[:n:]
            for i in l:
                self.cartes.remove(i)
                self.sel.append(i[1::])
        else:
            self.cartes = [f"¬{i}" for i in self.sel]
            self.sel = []
    def dessin_carte(self, img, pos, val="¬") -> None:
        p1, p2 = pos
        offset = dist(p1, p2)/20
        p1, p2 = [i+offset for i in p1], [i-offset for i in p2]
        if val == None or len(val) == 0: img.rectangle(p1, p2, col.black, 1)
        else:
            if type(val) != str and len(val) > 0: val = val[-1]
            if val[0] == "¬": ##TODO## Faire une couverture jolie pour les cartes
                img.rectangle(p1, p2, col.blue, 0)
                img.rectangle(p1, p2, col.black, 2)
                ## TODO ##
                img.ecris("?", ct_sg(p1, p2), col.black, 2, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
            else:
                img.rectangle(p1, p2, col.blanc, 0)
                img.rectangle(p1, p2, col.black, 2)
                color = col.noir if val[-1] in "♠♣" else col.red
                match val[-1]: # ♦♥♠♣
                    case "♦": forme = carreau
                    case "♥": forme = coeur
                    case "♠": forme = pique
                    case "♣": forme = trefle
                n = val[:-1:]
                if n.lower() not in "vdr":
                    t = 9
                    if n.lower() == "a": n, t = 1, 25
                    for pt, an in self.positions_figures(p1, p2)[int(n)-1]: forme(img, pt, t, an)
                for pt, a in [[pt_sg(p1, p2, 9), 0], [pt_sg([p2[0], p2[1]+diff(p1[1], p2[1])*0.055], p1, 9), 180]]:
                    v = diff(p1[1], p2[1])*0.2
                    forme(img, [pt[0], p1[1]+v if a==0 else p2[1]-v], 7)
                    img.ecris(val[:-1:], pt, color, 2, 1, cv2.FONT_HERSHEY_COMPLEX, 2) # TO DO ## Add rotated text (update tsanap)
    def image(self, r=False) -> image:
        x, y = diff(res.res[0], res.res[1])/4, res.res[1]/20
        p1, p2, p3, p4 = [x, y], [res.res[0]-x, y], [x, res.res[1]-y], [res.res[0]-x, res.res[1]-y]
        x, y = dist(p1, p2), dist(p1, p3)
        pcr = [[p1[0]+x/2, p1[1]], [p2[0], p2[1]+y/4]] #Points cartes resolues # Haut droite
        pcc = [p1, [p1[0]+x/2, p2[1]+y/4]] #Points cartes cachées # Haut gauche
        pcp = [pcc[0], pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 3)] #Points cartes pioche # Coin haut gauche
        psp = [pt_sg(pcc[0], [pcc[1][0], pcc[0][1]], 3), pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 1, 3)] #Points shown pioche # Centre haut gauche
        x_ = lambda i: (p2[0]-p1[0])/7*i
        pcs = [[[p1[0]+x_(x), pcc[1][1]], [p1[0]+x_(x+1), p4[1]]] for x in range(7)] #Points colonnes solitaire
        w, h = diff(pcp[0][0], pcp[1][0]), diff(pcr[0][1], pcr[1][1])
        self.w, self.h = w, w
        self.pcr, self.pcc, self.pcp, self.psp, self.pcs = pcr, pcc, pcp, psp, pcs
        img = image(nom=self.name, img=image.new_img(dimensions=res.res, fond=col.green))
        if r: img.ecris(f"{res.res[0]}x{res.res[1]}", [100, 25], col.black, 1, 1, cv2.FONT_HERSHEY_SIMPLEX, 2)
        self.dessin_carte(img, pcp, "" if self.cartes == [] else "¬")
        x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
        for c in range(4): ## Dessin cartes résolues
            if mouse.action == actions[3] and len(self.end[c]) > 0 and c == mouse.column: self.dessin_carte(img, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]], self.end[c][:-1:])
            else: self.dessin_carte(img, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]], self.end[c])
        x_ = lambda i: psp[0][0]+w*i
        for i, n in enumerate([0, 0.5, 1][:min(3, len(self.sel))-1:] if mouse.click and mouse.action == actions[1] else [0, 0.5, 1]): ## Dessine les cartes piochables
            pos = [[x_(n), psp[0][1]], [x_(n+1), psp[1][1]]]
            try: val = self.sel[-3::][i]
            except: continue
            self.dessin_carte(img, pos, val)
        X, Y = (diff(pcs[0][0][0], pcs[0][1][0])-w)/2, diff(pcs[0][0][1], pcs[0][1][1])-h
        for x, column in enumerate(self.jeu): ## Dessin cartes jeu
            pc = pcs[x]
            if mouse.action == actions[2] and x == mouse.column: column = column[:mouse.row:]
            for y, card in enumerate(column):
                pt1, pt2 = [pc[0][0]+X, pc[0][1]+Y/12*y], [pc[1][0]-X, pc[0][1]+Y/12*y+h]
                self.dessin_carte(img, [pt1, pt2], self.jeu[x][y])
        img.rectangle(p1, p4, col.noir, 2, 2) #Bord de la zone de jeu
        img.ligne([pcc[0][0], pcr[1][1]], pcr[1], col.noir, 2, 2) #Bord2 de la zone de jeu
        if self.debug: ## TOREMOVE ## DEBUG ##
            img.rectangle(pcr[0], pcr[1], col.magenta, 3, 2)
            img.rectangle(psp[0], psp[1], col.blue, 2, 2)
            img.rectangle(pcp[0], pcp[1], col.cyan, 1, 2)
            for c in pcs: img.rectangle(c[0], c[-1], col.red, 2, 2)
            x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
            for a, b in [[[x_(i), pcr[0][1]], [x_(i+1), pcr[1][1]]] for i in range(4)]: img.rectangle(a, b, col. magenta, 2, 2)
            for x, pc in enumerate(pcs):
                for y, card in [[a, b] for a, b in enumerate(self.jeu[x])][::-1]:
                    img.rectangle([pc[0][0]+X, pc[0][1]+Y/12*y], [pc[1][0]-X, pc[0][1]+Y/12*y+h], [255/12*y for _ in "123"], 2, 2)
        if mouse.click: ## Mise à jour de la carte en déplacement
            try:
                val = False
                if mouse.action == actions[1]: val = self.sel[-1]
                elif mouse.action == actions[2]:
                    for n, card in enumerate([self.jeu[mouse.column][r] for r in range(mouse.row, len(self.jeu[mouse.column]))]):
                        self.dessin_carte(img, [[mouse.pos[0]-w/2, mouse.pos[1]-(h*0.2)+Y/12*n], [mouse.pos[0]+w/2, mouse.pos[1]-(h*0.2)+h+Y/12*n]], card)
                if mouse.action == actions[3]: val = self.end[mouse.column][-1]
                if val: self.dessin_carte(img, [[mouse.pos[0]-w/2, mouse.pos[1]-h*0.2], [mouse.pos[0]+w/2, mouse.pos[1]-(h*0.2)+h]], val)
            except: ...
        return img
    def game(self) -> bool:
        fs = False
        r = False # Afficher la resolution
        img = self.image(r=r)
        img.montre(1, fullscreen=fs)
        cv2.setMouseCallback(img.nom, get_mouse, self)
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): return
            match wk:
                case 27: return
                case 32 | 102: fs = not fs
                case  8 | 114: res.update()
                case 65470 | 49: cv2.moveWindow(img.nom, 0, 0) ## F1 or 1
                case 65471 | 50: cv2.moveWindow(img.nom, 1920, 0) ## F2 or 2
                case 65472 | 51: ## F3 or 3
                    r = not r
                    img = self.image(r=r)
                case 65473 | 52: ## F4 or 4
                    self.debug = not self.debug
                    img=self.image(r=r)
                case 65474 | 53: ## F5 or 5
                    self.restart()
                    img = self.image(r=r)
            if mouse.reload:
                img = self.image(r=r)
                mouse.reload = False

if __name__ == "__main__":
    a = sol()
    a.game()