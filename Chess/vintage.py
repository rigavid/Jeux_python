from pyimager import *

def cadre(img, p1, p2, c1, c2, ep, lt=0) -> None:
    img.rectangle(p1, p2, c1, 0)
    img.rectangle(p1, p2, c2, ep, lt)

class StopGame(Exception): pass
class chess:
    ## Vars ##
    gris = [30, 30, 30]
    marron = [181, 113, 77]
    blanc = [215, 215, 215]
    noir = [40, 40, 40]
    x, y = [i/2 for i in RES.resolution]
    PT1, PT2 = [x*0.5, y*0.8], [x*1.5, y*1.2]
    def new_matrix(self) -> np.array:
        pcs = [i+"." if i in "TR" else i for i in "TCFDRFCT"]
        return np.array([[p for p in pcs], ["P."]*8, *[[" "]*8]*4, ["p."]*8, [p.lower() for p in pcs]])
    def __init__(self, name="PyChess", j1="J1", j2="J2") -> None:
        self.epaisseur, self.size, self.lt = 5, 7, 2
        self.name, self.n_j1, self.n_j2 = name, j1, j2
        self.matrix, self.trait = self.new_matrix(), True
        self.img:image = self.new_img_()
        self.last_move = None
        self.m = copy.deepcopy(self.matrix)
        self.captures = [[], []]
    def __str__(self) -> str:
        return "\n".join("".join(self.m[7-y, x][0] for x in range(8)) for y in range(8))+f"\n{self.trait}"
    ### Infos ###
    def points(self, p) -> int:
        match p:
            case 'p': return 1
            case 'c' | 'f': return 3
            case 't': return 5
            case 'd': return 9
            case _: return 0
    def get_points(self) -> tuple:
        j1 = j2 = 0
        for c in "".join("".join(self.matrix[7-y, x][0] for x in range(8)) for y in range(8)):
            if c.isupper(): j1 += self.points(c.lower())
            else: j2 += self.points(c)
        return j1-j2, j2-j1
    def get_case(self, pos) -> tuple:
        x, y = pos
        x -= self.echq[0][0]
        y -= self.echq[0][1]
        X, Y = self.sz_echq
        return 7-int(y/Y*8), int(x/X*8)
    def get_cases_line(self, p1, p2) -> list:
        x1, y1, x2, y2 = *p1, *p2
        dx = (x2 - x1) // max(1, abs(x2 - x1))
        dy = (y2 - y1) // max(1, abs(y2 - y1))
        if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
            return ((x1 + i * dx, y1 + i * dy) for i in range(1, max(abs(x2 - x1), abs(y2 - y1))))
        return ()
    def where_is_king(self, t) -> tuple:
        for x in range(8):
            for y in range(8):
                if self.m[x, y][0] == ('R' if t else 'r'):
                    return x, y
    def est_echec(self, t) -> bool:
        king_pos = self.where_is_king(t)
        for x in range(8):
            for y in range(8):
                c = self.m[x, y]
                if c in " .·": continue
                if c.isupper() == t: continue  # Skip friendly pieces
                if self.legal_((x, y), king_pos, True):
                    return True
        return False
    ### Imagerie ###
    def input(self, p="") -> str:
        im = copy.deepcopy(self.img.img)
        s = ""
        majus = False
        while self.img.is_opened():
            self.img.img = copy.deepcopy(im)
            cadre(self.img, self.PT1, self.PT2, COL.red, COL.blue, self.epaisseur, self.lt)
            self.img.text(p+s, ct_sg(self.PT1, self.PT2), COL.green, self.epaisseur*0.7, self.size*2, 0, self.lt)
            wk = self.img.show(built_in_functs=False)
            if wk == -1: pass
            elif wk == 13:
                self.image()
                return s
            elif wk == 27:
                self.image()
                return None
            elif wk in [65509, 65505]: majus = not majus
            elif wk == 8: s = s[:-1:]
            elif majus: s += chr(wk).upper()
            else: s += chr(wk)
    def image(self) -> None:
        self.img.img = copy.deepcopy(self.img_)
        if self.est_echec(self.trait):
            self.img.rectangle(*self.cases[*self.where_is_king(self.trait)], COL.red, 0)
        self.img.rectangle(self.cases[-1,0][0], self.cases[0,-1][-1], self.gris, self.epaisseur*min(self.img.size())/1080, self.lt)
        for x in range(8):
            for y in range(8):
                self.draw_piece(self.matrix[x, y][0], *self.cases[x, y])
        pj1, pj2 = self.get_points()
        for jr, tb in (((pj1, self.n_j1), self.tj1), ((pj2, self.n_j2), self.tj2)):
            for i in (0, 1):
                t = jr[i] if i == 1 else f"{jr[i]:+}"
                self.img.text(t, ct_sg(*tb[i]), self.gris, self.epaisseur*0.7, self.size*1.25, 0, self.lt)
        if self.last_move != None:
            for i in self.last_move:
                self.img.rectangle(*self.cases[*i], COL.cyan, self.epaisseur)
        for t, cs in ((self.tj1[2], self.captures[0]), (self.tj2[2], self.captures[1])):
            for n, c in enumerate(cs):
                self.draw_piece(c, *t[n])
    def draw_player_table(self, img, p1, p4) -> None:
        ep, c1, c2 = self.epaisseur, self.marron, [101, 53, 37]
        p2, p3 = (p4[0], p1[1]), (p1[0], p4[1])
        cadre(img, p1, p4, c1, c2, ep, self.lt)
        pg, pd = (pt_sg(*pts, 3) for pts in ((p1, p3), (p2, p4)))
        ph, pb = (pt_sg(*pts, 2) for pts in ((p1, p2), (pg, pd)))
        img.line(pg, pd, c2, ep)
        img.line(ph, pb, c2, ep)
        a, b = (p1, pb), (ph, pd)
        x, y = diff(pg[0], p4[0]), diff(pg[1], p4[1])
        d = min(x/6, y/3)
        ox, oy = (x-d*6)/2+pg[0], (y-d*3)/2+pg[1]
        t = []
        for y in range(3):
            for x in range(6):
                p1, p2 = [ox+d*x, oy+d*y], [ox+d*(x+1), oy+d*(y+1)]
                t.append([p1, p2])
        return a, b, t
    def new_img(self) -> np.array:
        return self.new_img_().img
    def new_img_(self) -> image:
        img = new_img(background=COL.black, name=self.name)
        M = min(img.size())
        sz, lt, ft, col, ep = self.size*M/1080, lineTypes[2], cv2.FONT_HERSHEY_TRIPLEX, self.gris, self.epaisseur*M/1080
        ptt1 = [0, 0]
        ptt4 = [i+M for i in ptt1]
        ptt2, ptt3 = (ptt4[0], ptt1[1]), (ptt1[0], ptt4[1])
        d = dist(ptt2, ptt1) / 9
        img.rectangle(ptt1, ptt4, [157, 113, 83], 0)
        for n in range(8):
            for p in [(d*(n+1), d/4), (d*(n+1), M - d/4)]:
                for args in (("ABCDEFGH"[n], p), ("87654321"[n], p[::-1])):
                    img.text(*args, COL.black, ep*0.6, sz, 0, self.lt)
        # Remplissage des coins de l'échequier.
        for n, p in enumerate([ptt1, ptt2, ptt4, ptt3]):
            img.rectangle(p, coosCircle(p, square_root(((d/2)**2)*2), 90*n+45), COL.new("3d3d3d"), 0)
        # Délimitations des lignes sur les bords de l'échequier.
        self.cases = np.array([[[(d*(x+0.5), d*(7.5-y)), (d*(x+1.5), d*(8.5-y))] for x in range(8)] for y in range(8)])
        for i in range(9):
            img.line((round(ptt1[0]+d*(i+0.5)),ptt1[1]), (round(ptt1[0]+d*(i+0.5)),ptt3[1]), col, ep, self.lt)
            img.line((ptt1[0],round(ptt1[1]+d*(i+0.5))), (ptt2[0],round(ptt1[1]+d*(i+0.5))), col, ep, self.lt)
        for x in range(8):
            for y in range(8): img.rectangle(*self.cases[x, y], self.marron if x%2==y%2 else self.noir, 0)
        img.rectangle(ptt1, ptt4, col, ep)
        self.echq = self.cases[-1,0,0], self.cases[0,-1,-1]
        self.sz_echq = diff(self.echq[0][0], self.echq[1][0]), diff(self.echq[0][1], self.echq[1][1])
        p1, p2, p3, p4 = [M, 0], [img.size()[0], 0], [M, img.size()[1]], img.size()
        ct = ct_cr(p1, p2, p3, p4)
        self.tj1 = self.draw_player_table(img, *(pt_sg(p, pt_sg(ct_sg(p3, p4), ct, 2), 2) for p in (ct_sg(p1, p3), p4)))
        self.tj2 = self.draw_player_table(img, *(pt_sg(p, pt_sg(ct_sg(p1, p2), ct, 2), 2) for p in (p1, ct_sg(p2, p4))))
        self.img_ = copy.deepcopy(img.img)
        return img
    def draw_piece(self, p, a, b, c=3) -> None:
        ep = 4
        p1, p2 = pt_sg(a, b, c), pt_sg(b, a, c)
        p3, p4 = [p2[0], p1[1]], [p1[0], p2[1]]
        ct = ct_cr(p1, p2, p3, p4)
        c1, c2 = self.blanc, [15, 15, 15]
        if p.islower(): c1, c2 = c2, c1
        p = p.lower()
        if not p in ' .·':
            cadre(self.img, p1, p2, c1, c2, ep, self.lt)
            x, y = diff(a[0], b[0]), diff(a[1], b[1])
        if p == "c":
            cadre(self.img, ct_sg(a, p1), coosCircle(p2, dist(a, p1)*1.25, angleInterPoints(p1, a)), c1, c2, ep, self.lt)
        elif p in "fdr":
            cadre(self.img, [a[0]+x*0.425, moyenne(a[1], p1[1])], [a[0]+x*0.575, p1[1]], c1, c2, ep, self.lt)
        if p in "rd":
            cadre(self.img, [a[0]+x*0.1, moyenne(a[1], p1[1])], [p1[0], p1[1]+diff(a[1], p1[1])*0.7], c1, c2, ep, self.lt)
            cadre(self.img, [b[0]-x*0.1, moyenne(a[1], p1[1])], [p2[0], p1[1]+diff(a[1], p1[1])*0.7], c1, c2, ep, self.lt)
        if p == "t":
            cadre(self.img, [a[0]+x*0.1, moyenne(a[1], p1[1])], pt_sg(p1, p2, 3), c1, c2, ep, self.lt)
            cadre(self.img, [b[0]-x*0.1, moyenne(a[1], p1[1])], pt_sg(p3, p4, 3), c1, c2, ep, self.lt)
        if p in "rf":
            self.img.line(pt_sg(ct_sg(p1, p3), ct), pt_sg(ct_sg(p2, p4), ct), c2, ep, self.lt)
            self.img.line(pt_sg(ct_sg(p1, p4), ct), pt_sg(ct_sg(p3, p2), ct), c2, ep, self.lt)
    ### Jeu ###
    def promote(self, p1) -> bool:
        x = 2
        p = "CFTD"
        pieces = []
        for i in p: ## TODO Couleurs STP !
            a, b = copy.deepcopy(self.cases[4,x][0]), copy.deepcopy(self.cases[3,x+1][0])
            y = diff(a[1], b[1])/2
            a[1] += y
            b[1] += y
            pieces.append([a, b])
            cadre(self.img, a, b, self.blanc, self.noir, self.epaisseur*2*min(self.img.size())/1080)
            self.draw_piece(i if self.trait else i.lower(), a, b)
            x += 1
        while self.img.is_opened():
            self.img.show()
            if self.img.mouse.new:
                if self.img.mouse.event == cv2.EVENT_LBUTTONDOWN:
                    for i in range(len(pieces)):
                        if clicked_in(self.img.mouse.pos, pieces[i]):
                            self.m[*p1] = p[i] if self.trait else p[i].lower()
                            return True
                    return False
    def promotion(self, p1, p2, dry) -> bool:
        if p2[0] in (0, 7) and not dry: return self.promote(p1)
        return True
    def leg_p(self, x, y, p1, p2, dry) -> bool:
        if y==1 and x==0 and self.m[*p2] in " .·":
            return self.promotion(p1, p2, dry)
        elif y==2 and x==0 and len(self.m[*p1])>1 and self.m[*p2] in " .·" and self.m[*[int(moyenne(p1[n], p2[n])) for n in (0, 1)]] in " .·":
            self.m[*[int(moyenne(p1[n], p2[n])) for n in (0, 1)]] = "·"
            return True
        elif y==1 and abs(x)==1:
            if not self.m[*p2] in " .·": return self.promotion(p1, p2, dry)
            elif self.m[*p2] in "·.":
                if not dry: self.captures[0 if self.trait else 1].append(self.m[p2[0]-1,p2[1]][0])
                if self.m[*p1].isupper():
                    self.m[p2[0]-1,p2[1]] = " "
                else: self.m[p2[0]+1,p2[1]] = " "
                return True
        return False
    def leg_c(self, x, y) -> bool:
        return (abs(x)==2 and abs(y)==1) or (abs(x)==1 and abs(y)==2)
    def leg_t(self, x, y, p1, p2) -> bool:
        return (x==0 or y==0) and not False in (self.m[*p] in " .·" for p in self.get_cases_line(p1, p2))
    def leg_f(self, x, y, p1, p2) -> bool:
        return abs(x)==abs(y) and not False in (self.m[*p] in " .·" for p in self.get_cases_line(p1, p2))
    def leg_d(self, x, y, p1, p2) -> bool:
        return self.leg_f(x, y, p1, p2) or self.leg_t(x, y, p1, p2)
    def leg_r(self, x, y, p1, p2, dry) -> bool:
        if abs(x)<=1 and abs(y)<=1: return True
        elif self.m[*p1][-1]=="." and abs(x)==2 and y==0 and not self.est_echec(self.trait):
            if self.m[*[int(i) for i in ct_sg(p1, p2)]] == " ":
                self.m[*p1], self.m[*[int(i) for i in ct_sg(p1, p2)]] = " ", self.m[*p1]
                if not self.est_echec(self.trait):
                    self.m[*p1], self.m[*[int(i) for i in ct_sg(p1, p2)]] = self.m[*[int(i) for i in ct_sg(p1, p2)]], " "
                    if p2[1] > 4:
                        if self.m[p1[0], -1][-1]==".":
                            self.m[p1[0], 5], self.m[p1[0], -1] = self.m[p1[0], -1][0], " "
                            return True
                    else:
                        if self.m[p1[0], 0][-1]=="." and self.m[p1[0], 1]==" ":
                            self.m[p1[0], 3], self.m[p1[0], 0] = self.m[p1[0], 0][0], " "
                            return True
        return False
    def legal_(self, p1, p2, dry=False) -> bool:
        if None in (p1, p2): return False
        c = self.m[*p1]
        if c[0].isupper(): t, y, x = True, p2[0]-p1[0], p2[1]-p1[1]
        else: t, y, x = False, p1[0]-p2[0], p1[1]-p2[1]
        if not self.m[*p2] in " .·" in " .·" and self.m[*p2].isupper()==t: return False
        match c[0].lower():
            case 'p': legalite = self.leg_p(x, y, p1, p2, dry)
            case 'c': legalite = self.leg_c(x, y)
            case 'f': legalite = self.leg_f(x, y, p1, p2)
            case 't': legalite = self.leg_t(x, y, p1, p2)
            case 'd': legalite = self.leg_d(x, y, p1, p2)
            case 'r': legalite = self.leg_r(x, y, p1, p2, dry)
            case _: return False
        return legalite
    def legal(self, p1, p2, *args) -> bool:
        if self.legal_(p1, p2, *args):
            n = copy.deepcopy(self.m)
            self.m[*p2], self.m[*p1] = self.m[*p1][0], " "
            self.m[self.m=="."] = " "
            self.m[self.m=="·"] = "."
            if not self.est_echec(self.trait):
                self.m = n
                return True
        return False
    def get_case_click(self, p1=False) -> tuple:
        m, p = self.img.mouse, None
        while self.img.is_opened():
            wk = self.img.show()
            if wk == -1: pass
            elif chr(wk) == "h": print(self.matrix)
            if m.new and m.event == cv2.EVENT_LBUTTONDOWN:
                m.new = False
                if clicked_in(m.pos, (self.echq)):
                    p = self.get_case(m.pos)
                    c = self.matrix[*p][0]
                    if (not c in " .·" and c.isupper() == self.trait) or not p1:
                        return p
                if clicked_in(m.pos, self.tj1[1]):
                    if (nj1:=self.input("J1: ")) != None:
                        self.n_j1 = nj1
                        self.image()
                if clicked_in(m.pos, self.tj2[1]):
                    if (nj2:=self.input("J2: ")) != None:
                        self.n_j2 = nj2
                        self.image()
        raise StopGame
    def get_move(self) -> tuple:
        p1 = self.get_case_click(True)
        while self.img.is_opened():
            self.img.show()
            self.img.rectangle(*self.cases[*p1], COL.green, self.epaisseur)
            for x in range(8):
                for y in range(8):
                    self.m = copy.deepcopy(self.matrix)
                    if self.legal(p1, (x, y), True):
                        self.img.circle(ct_sg(*self.cases[x, y]), self.epaisseur*3, COL.purple, 0, self.lt)
            p2 = self.get_case_click()
            if not self.matrix[*p2] in " .·" and self.matrix[*p2].isupper() == self.trait:
                self.image()
                if p2 == p1: return self.get_move()
                p1 = p2
            else: return p1, p2
    def move(self, p1, p2) -> None:
        self.m = copy.deepcopy(self.matrix)
        cap = copy.deepcopy(self.captures)
        leg = self.legal(p1, p2)
        if leg:
            if not self.m[*p2] in " .·":
                self.captures[0 if self.trait else 1].append(self.m[*p2][0])
                for i in range(2):
                    for m, p in ((1, "d"), (2, "tfc")):
                        for c in p:
                            if self.captures[i].count(c) > m:
                                self.captures[i].remove(c)
                                self.captures[i].append("p" if i == 0 else "P")
                    self.captures[i].sort(key=lambda x: "pcftdPCFTD".index(x))
            self.m[*p2], self.m[*p1] = self.m[*p1][0], " "
            self.m[self.m=="."] = " "
            self.m[self.m=="·"] = "."
            self.last_move = p1, p2
            self.trait = not self.trait
            self.matrix = self.m
        else:
            self.m = copy.deepcopy(self.matrix)
            self.captures = cap
        self.image()
    def start_(self) -> None:
        self.image()
        m = self.img.mouse
        self.img.setMouseCallback(m.get)
        self.img.build()
        while self.img.is_opened():
            self.img.show()
            self.move(*self.get_move())
    def start(self) -> None:
        try: self.start_()
        except StopGame: pass

if __name__ == "__main__":
    a = chess()
    a.start()