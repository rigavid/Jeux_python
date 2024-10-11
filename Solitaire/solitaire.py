from tsanap import *

class res:
    resses = [screen, [1680, 1050], [1366, 768]]
    resind = -1
    res = resses[resind]
    def update():
        res.resind = (res.resind+1)%len(res.resses)
        res.res = res.resses[res.resind]
        mouse.reload = True

def get_cartes():
    cartes = [f"¬{n}{p}" for p in "♦♥♠♣" for n in "A 2 3 4 5 6 7 8 9 10 J Q K".split()]
    np.random.shuffle(cartes)
    return cartes

actions = ["Pioche", "Sel_carte", "Game_carte", "Res_carte", "Show_carte"]

class mouse:
    click = False
    pos = [-1, -1]
    action = None
    reload = False

def get_mouse(event, x, y, flags, params) -> None:
    pos = (x, y)
    sol = params
    pcs, pcp, psp, pcr = sol.pcs, sol.pcp, sol.psp, sol.pcr
    if event == cv2.EVENT_LBUTTONDOWN and not mouse.click:
        if clicked_in(pos, pcp): mouse.action = actions[0] ## Pioche
        if clicked_in(pos, psp):
            mouse.action = actions[1]
            mouse.reload = True
            mouse.pos = pos
        if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]): ## Jeu
            for n, column in enumerate(pcs):
                if clicked_in(pos, column):
                    mouse.action = actions[2]
                    break
        if mouse.action != None: mouse.click = True
    elif event == cv2.EVENT_LBUTTONUP and mouse.click:
        if clicked_in(pos, pcp) and mouse.action == actions[0]:
            sol.update_sel()
            mouse.click = False
        elif mouse.action == actions[1]:
            if clicked_in(pos, [pcs[0][0], pcs[-1][-1]]):
                for n, column in enumerate(pcs):
                    if clicked_in(pos, column):
                        sol.jeu[n].append(sol.sel.pop(-1)) ## TODO ## Add rules to when I can put a card here
            elif clicked_in(pos, pcr):
                x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
                for c in range(4):
                    if clicked_in(pos, [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]): break
                sol.end[c].append(sol.sel.pop(-1))
            mouse.click = False
        if not mouse.click:
            mouse.reload = True
            mouse.action = None
    elif event == cv2.EVENT_MOUSEMOVE and mouse.click:
        if mouse.action == actions[1]:
            mouse.pos = pos
            mouse.reload = True

class sol:
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
    def update_sel(self) -> None:
        if self.cartes != []:
            l = self.cartes[:3:]
            for i in l:
                self.cartes.remove(i)
                self.sel.append(i[1::])
        else:
            self.cartes = [f"¬{i}" for i in self.sel]
            self.sel = []
    def dessin_carte(self, img, pos, val="¬") -> image:
        p1, p2 = pos
        offset = dist(p1, p2)/20
        p1, p2 = [i+offset for i in p1], [i-offset for i in p2]
        if val == None or len(val) == 0: img.rectangle(p1, p2, col.black, 1)
        else:
            if type(val) != str and len(val) > 0: val = val[-1]
            if val[0] == "¬": ##TODO## Faire une couverture jolie pour les cartes
                img.rectangle(p1, p2, col.blue, 0)
                img.rectangle(p1, p2, col.black, 2)
                img.ecris("?", ct_sg(p1, p2), col.black, 2, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
            else:  ##TODO## Faire un design joli pour les cartes
                img.rectangle(p1, p2, col.blanc, 0)
                img.rectangle(p1, p2, col.black, 2)
                img.ecris(val[:-1:], ct_sg(p1, p2), col.noir if val[-1] in "♠♣" else col.red, 3, 3, cv2.FONT_HERSHEY_SIMPLEX)
        return img
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
        h = diff(pcr[0][1], pcr[1][1])
        w = diff(pcp[0][0], pcp[1][0])
        self.pcr, self.pcc, self.pcp, self.psp, self.pcs = pcr, pcc, pcp, psp, pcs
        img = image(nom=self.name, img=image.new_img(dimensions=res.res, fond=col.green))
        if r: img.ecris(f"{res.res[0]}x{res.res[1]}", [100, 25], col.black, 1, 1, cv2.FONT_HERSHEY_SIMPLEX, 2)
        self.dessin_carte(img, pcp, "" if self.cartes == [] else "¬")
        x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
        for c in range(4):
            pos = [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]
            self.dessin_carte(img, pos, self.end[c])
        x_ = lambda i: psp[0][0]+w*i
        for i, n in enumerate([0, 0.5, 1][:min(3, len(self.sel))-1:] if mouse.click and mouse.action == actions[1] else [0, 0.5, 1]):
            pos = [[x_(n), psp[0][1]], [x_(n+1), psp[1][1]]]
            try: val = self.sel[-3::][i]
            except: continue
            self.dessin_carte(img, pos, val)
        for x, column in enumerate(self.jeu):
            pc = pcs[x]
            Y = diff(pc[0][1], pc[1][1])-h
            for y, card in enumerate(column):
                X = (diff(pc[0][0], pc[1][0])-w)/2
                pt1, pt2 = [pc[0][0]+X, pc[0][1]+Y/12*y], [pc[1][0]-X, pc[0][1]+Y/12*y+h]
                self.dessin_carte(img, [pt1, pt2], self.jeu[x][y])
        img.rectangle(p1, p4, col.noir, 2, 2) #Bord de la zone de jeu
        img.ligne([pcc[0][0], pcr[1][1]], pcr[1], col.noir, 2, 2) #Bord2 de la zone de jeu
        ## TODO ## TOREMOVE ## DEBUG ##
        if self.debug:
            img.rectangle(pcr[0], pcr[1], col.magenta, 3, 2)
            img.rectangle(psp[0], psp[1], col.blue, 2, 2)
            img.rectangle(pcp[0], pcp[1], col.cyan, 1, 2)
            for c in pcs: img.rectangle(c[0], c[-1], col.red, 2, 2)
        ## Mise à jour de la carte en déplacement
        sel_c, game_c, res_c, show_c = actions[1::]
        if mouse.click:
            val = False
            match mouse.action:
                case sel_c:
                    try: val = self.sel[-1]
                    except: return img
            if val:
                try: self.dessin_carte(img, [[mouse.pos[i]-[w, h][i]/2 for i in [0, 1]], [mouse.pos[i]+[w, h][i]/2 for i in [0, 1]]], val)
                except: return img
        return img
    def game(self) -> bool:
        fs = False
        r = False # Afficher la resolution
        img = self.image(r=r)
        img.montre(1, fullscreen=fs)
        cv2.setMouseCallback(img.nom, get_mouse, self)
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): break
            match wk:
                case 27: break
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