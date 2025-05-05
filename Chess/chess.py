from pyimager import *

def ran(*args): return range(*(round(i) for i in args))

COL.marron = [157, 113, 83]
COL.gris = [30, 30, 30]
COL.argent = [200, 200, 200]
COL.dore = [200, 200, 100]
COL.marron_clair = [181, 113, 77]
COL.marron_clair2 = [120, 60, 30]
COL.marron_fonce = [101, 53, 37]
COL.blanc = [215, 215, 215]
COL.noir = [40, 40, 40]
COL.noir2 = [15, 15, 15]
COL.col_sel = COL.new('800080')
COL.bois_noir = [70, 43, 27]
COL.bord_bois_noir = [50, 23, 7]
COL.col_lin = [20, 20, 20]

class chess:
    def new_matrix(self):
        pcs = [i+"." if i in "TR" else i for i in "TCFDRFCT"]
        return np.array([[p for p in pcs], ["P"]*8, *[[" "]*8]*4, ["p"]*8, [p.lower() for p in pcs]])
    def __str__(self):
        return "\n".join("".join(self.m[7-y, x][0] for x in range(8)) for y in range(8))+f"\n{self.trait}"
    def __init__(self, name="PyChess", matrix=None, trait=True):
        self.trait = trait
        self.m = matrix if matrix!=None else self.new_matrix()
        self.play = True
        self.img = new_img(name=name)
    def end_game(self): ... # Détermine si la partie est finie
    def draw_piece(self, img, p, a, b, c=3):
        p1, p2 = pt_sg(a, b, c), pt_sg(b, a, c)
        p3, p4 = [p2[0], p1[1]], [p1[0], p2[1]]
        ct = ct_cr(p1, p2, p3, p4)
        c1, c2 = COL.blanc, COL.noir2
        if p.islower(): c1, c2 = c2, c1
        p = p.lower()
        if p != ' ' and p != '·':
            img.rectangle(p1, p2, c2, 0)
            img.rectangle(p1, p2, c1, 3)
            x, y = diff(a[0], b[0]), diff(a[1], b[1])
        if p == "c":
            pt1, pt2 = ct_sg(a, p1), coosCircle(p2, dist(a, p1)*1.25, angleInterPoints(p1, a))
            img.rectangle(pt1, pt2, c2, 0)
            img.rectangle(pt1, pt2, c1, 3)
        elif p in "fdr":
            pt1, pt2 = [a[0]+x*0.425, moyenne(a[1], p1[1])], [a[0]+x*0.575, p1[1]]
            img.rectangle(pt1, pt2, c2, 0)
            img.rectangle(pt1, pt2, c1, 3)
        if p in "rd":
            pg1, pg2 = [a[0]+x*0.1, moyenne(a[1], p1[1])], [p1[0], p1[1]+diff(a[1], p1[1])*0.7]
            pd1, pd2 = [b[0]-x*0.1, moyenne(a[1], p1[1])], [p2[0], p1[1]+diff(a[1], p1[1])*0.7]
            img.rectangle(pg1, pg2, c2, 0)
            img.rectangle(pg1, pg2, c1, 3)
            img.rectangle(pd1, pd2, c2, 0)
            img.rectangle(pd1, pd2, c1, 3)
        if p == "t":
            pg1, pg2 = [a[0]+x*0.1, moyenne(a[1], p1[1])], pt_sg(p1, p2, 3)
            pd1, pd2 = [b[0]-x*0.1, moyenne(a[1], p1[1])], pt_sg(p3, p4, 3)
            img.rectangle(pg1, pg2, c2, 0)
            img.rectangle(pg1, pg2, c1, 3)
            img.rectangle(pd1, pd2, c2, 0)
            img.rectangle(pd1, pd2, c1, 3)
        if p in "rf":
            img.line(pt_sg(ct_sg(p1, p3), ct), pt_sg(ct_sg(p2, p4), ct), c1, 3)
            img.line(pt_sg(ct_sg(p1, p4), ct), pt_sg(ct_sg(p3, p2), ct), c1, 3)
    def image(self) -> image:
        ct = COL.bord_bois_noir
        tt, ep = 5, 3
        img = new_img(background=COL.black)
        M = min(img.size())
        pt1 = [(img.size()[0]-M)/2, (img.size()[1]-M)/2]
        pt4 = [i+M for i in pt1]
        pt2, pt3 = [pt4[0], pt1[1]], [pt1[0], pt4[1]]
        cases = []
        img.rectangle(pt1, pt4, COL.marron_fonce, 0)
        a = 15; p1, p4 = pt_sg(pt1, pt4, a), pt_sg(pt4, pt1, a)
        p2, p3 = [p4[0], p1[1]], [p1[0], p4[1]]
        DX, DY = diff(pt1[0], p1[0]), diff(pt1[1], p1[1])
        for a, b in [(pt1, p1), (pt2, p2), (pt3, p3), (pt4, p4)]:
            img.rectangle(a, b, COL.bord_bois_noir, 0)
        dx, dy = diff(p1[0], p4[0])/8, diff(p1[1], p4[1])/8
        for Y, y in enumerate(ran(p1[1], p4[1], dy)):
            img.text(str(8-Y), [pt1[0]+DX/2, y+dy/2], ct, ep, tt)
            img.text(str(8-Y), [pt4[0]-DX/2, y+dy/2], ct, ep, tt)
        for X, x in enumerate(ran(p1[0], p4[0], dx)):
            img.text("ABCDEFGH"[X], [x+dx/2, DY/2], ct, ep, tt)
            img.text("ABCDEFGH"[X], [x+dx/2, pt4[1]-DY/2], ct, ep, tt)
            cases.append([])
            for Y, y in enumerate(ran(p1[1], p4[1], dy)):
                a, b = [x, y], [x+dx, y+dy]
                cases[X].append([a, b])
                img.rectangle(a, b, COL.marron_clair if X%2==Y%2 else COL.marron_clair2, 0)
                self.draw_piece(img, self.m[Y, X][0], a, b)
        self.img.img = img.img
        self.pe1, self.pe2 = p1, p4
        self.cases = cases
    def move(self, p1, p2):
        pass
    def click(self):
        return self.img.mouse.new and self.img.mouse.event == cv2.EVENT_LBUTTONDOWN
    def get_case(self, p):
        x, y = p
        x -= self.pe1[0]
        y += self.pe1[1]
        X, Y = diff(self.pe1[0], self.pe2[0]), diff(self.pe1[1], self.pe2[1])
        a = round(x/X*8), round(y/Y*8)
        print(a)
        return a
    def start(self):
        self.image()
        self.img.setMouseCallback(self.img.mouse.get)
        self.img.build()
        p1 = p2 = None
        while self.play and self.img.is_opened():
            if self.end_game():
                if not self.replay_q():
                    return
            self.img.show()
            while p1 == None and self.img.is_opened():
                self.img.show()
                if self.click():
                    pos = [self.img.mouse.x, self.img.mouse.y]
                    if clicked_in(pos, [self.pe1, self.pe2]):
                        p1 = self.get_case(pos)
            self.img.rectangle(*self.cases[p1[0]][p1[1]])
            while p2 == None and self.img.is_opened():
                self.img.show()
                if self.click():
                    pos = [self.img.mouse.x, self.img.mouse.y]
                    if clicked_in(pos, [self.pe1, self.pe2]):
                        p2 = self.get_case(pos)
            self.move(p1, p2)

a = chess()
print(a)
a.start()