from tsanap import *

def get_cartes():
    cartes = [f"¬{n}{p}" for p in "♦♥♠♣" for n in "A 2 3 4 5 6 7 8 9 10 J Q K".split()]
    np.random.shuffle(cartes)
    return cartes

class mouse:
    click = False
    pos = [-1, -1]

def get_mouse(event, x, y, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN: ...
    elif event == cv2.EVENT_LBUTTONUP: ...

class sol:
    x, y = screen[0]/9/2, screen[1]/4/2
    p1, p2, p3, p4 = [x, y], [screen[0]-x, y], [x, screen[1]-y], [screen[0]-x, screen[1]-y]
    def __init__(self, nom="Solitaire") -> None:
        self.name = nom
        self.cartes = get_cartes()
        self.jeu = self.sel = []
        self.end = [[] for _ in range(4)]
        for i in range(7):
            l = [self.cartes.pop(x) for x in range(i+1)]
            l[-1] = l[-1][1::]
            self.jeu.append(l)
    def restart(self) -> None:
        self.cartes = get_cartes()
        self.jeu = self.sel = []
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
        offset = dist(p1, p2)/10
        p1, p2 = [i+offset for i in p1], [i-offset for i in p2]
        if val[0] == "¬":
            img.rectangle(img, p1, p2, col.blue, 0)
        else:
            img.rectangle(img, p1, p2, col.blue, 4)
            img.ecris(val[:-1:], ct_sg(p1, p2), col.noir if val[-1] in "" else col.red, 1, 3, 2)
        return img
    def image(self) -> image:
        p1, p2, p3, p4 = sol.p1, sol.p2, sol.p3, sol.p4
        x, y = sol.x*2, sol.y*2
        img = image(nom=self.name, img=image.new_img(fond=col.green))
        pts_cartes_res = [[p2[0]-x*4, p2[1]], [p2[0], p2[1]+y]]
        return img
    def game(self) -> bool:
        img = self.image()
        fs = False
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): break
            match wk:
                case 27: break
                case 32: fs = not fs

a = sol()
a.game()