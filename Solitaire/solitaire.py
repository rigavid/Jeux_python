from tsanap import *

class res:
    resses = [screen, [1680, 1050], [1366, 768]]
    resind = -1
    res = resses[resind]
    def update():
        res.resind = (res.resind+1)%len(res.resses)
        res.res = res.resses[res.resind]

def get_cartes():
    cartes = [f"¬{n}{p}" for p in "♦♥♠♣" for n in "A 2 3 4 5 6 7 8 9 10 J Q K".split()]
    np.random.shuffle(cartes)
    return cartes

class mouse:
    click = False
    pos = [-1, -1]
    action = None

def get_mouse(event, x, y, flags, params) -> None:
    pos = (x, y)
    if event == cv2.EVENT_LBUTTONDOWN: ...
        # if clicked_in(pos, [sol.p1, sol.p2]):
        #     for i in sol.get_pickable_cards():
        #         if clicked_in(pos, i):
        #             sol.picked_card = i
        #             click = True
        #             return
    elif event == cv2.EVENT_LBUTTONUP and click: ...

class sol:
    x, y = diff(screen[0], screen[1])/4, screen[1]/20
    p1, p2, p3, p4 = [x, y], [screen[0]-x, y], [x, screen[1]-y], [screen[0]-x, screen[1]-y]
    x, y = dist(p1, p2), dist(p1, p3)
    pcr = [[p1[0]+x/2, p1[1]], [p2[0], p2[1]+y/4]] #Points cartes resolues
    pcc = [p1, [p1[0]+x/2, p2[1]+y/4]] #Points cartes cachées
    pcp = [pcc[0], pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 3)] #Points cartes pioche
    psp = [pt_sg(pcc[0], [pcc[1][0], pcc[0][1]], 3), pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 1, 3)] #Points shown pioche
    def __init__(self, nom="Solitaire") -> None:
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
            if val[0] == "¬":
                img.rectangle(p1, p2, col.blue, 0)
                img.rectangle(p1, p2, col.black, 2)
                img.ecris("?", ct_sg(p1, p2), col.black, 2, 2, cv2.FONT_HERSHEY_SIMPLEX, 2) ##TODO## Faire une couverture jolie pour les cartes
            else:
                img.rectangle(p1, p2, col.blanc, 0)
                img.rectangle(p1, p2, col.black, 2)
                img.ecris(val[:-1:], ct_sg(p1, p2), col.noir if val[-1] in "♠♣" else col.red, 3, 3, cv2.FONT_HERSHEY_SIMPLEX)
        return img
    def image(self) -> image:
        x, y = diff(res.res[0], res.res[1])/4, res.res[1]/20
        p1, p2, p3, p4 = [x, y], [res.res[0]-x, y], [x, res.res[1]-y], [res.res[0]-x, res.res[1]-y]
        x, y = dist(p1, p2), dist(p1, p3)
        pcr = [[p1[0]+x/2, p1[1]], [p2[0], p2[1]+y/4]] #Points cartes resolues
        pcc = [p1, [p1[0]+x/2, p2[1]+y/4]] #Points cartes cachées
        pcp = [pcc[0], pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 3)] #Points cartes pioche
        psp = [pt_sg(pcc[0], [pcc[1][0], pcc[0][1]], 3), pt_sg([pcc[0][0], pcc[1][1]], pcc[1], 1, 3)] #Points shown pioche
        x_ = lambda i: (p2[0]-p1[0])/7*i
        pcs = [[[p1[0]+x_(x), pcc[1][1]], [p1[0]+x_(x+1), p4[1]]] for x in range(7)] #Points colonnes solitaire
        img = image(nom=self.name, img=image.new_img(dimensions=res.res, fond=col.green))
        val = "" if self.cartes == [] else "¬"
        self.dessin_carte(img, pcp, val)
        self.end = [[], ["3a", "qp"], [], []]
        for c in range(4):
            x_ = lambda i: pcr[0][0]+(pcr[1][0]-pcr[0][0])/4*i
            pos = [[x_(c), pcr[0][1]], [x_(c+1), pcr[1][1]]]
            self.dessin_carte(img, pos, self.end[c])
        for i in range(3):
            x_ = lambda i: psp[0][0]+diff(psp[1][0], psp[0][0])/3*i
            pos = [[x_(i), psp[0][1]], [x_(i+1.5), psp[1][1]]]
            try: val = self.sel[-i]
            except: continue
            self.dessin_carte(img, pos, val)
        img.rectangle(p1, p4, col.noir, 2, 2) #Bord de la zone de jeu
        img.rectangle(p1, pcr[1], col.noir, 2, 2)
        ## TODO ## TOREMOVE ## DEBUG ##
        for c in pcs:
            img.rectangle(c[0], c[-1], col.red, 2, 2)
        img.rectangle(pcc[0], pcc[1], col.yellow, 2, 2)
        img.rectangle(psp[0], psp[1], col.blue, 2, 2)
        img.rectangle(pcr[0], pcr[1], col.magenta, 2, 2)
        return img
    def game(self) -> bool:
        img = self.image()
        fs = False
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): break
            match wk:
                case 27: break
                case 32 | 102: fs = not fs
                case  8 | 114: res.update(); img = self.image()
                case 65470 | 49: cv2.moveWindow(img.nom,    0, 0) ## F1
                case 65471 | 50: cv2.moveWindow(img.nom, 1920, 0) ## F2

a = sol()
a.game()