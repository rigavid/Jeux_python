#############################
## Author: T-Sana ###########
## 24/5/2024 -> **/**/202* ##
#############################
## TODO ##########################################
## Inerdire parachutage de pion si échec et mat ##
## Roi en rouge lorsqu'il est en échec ###########
## Promotion des pièces #################
## Écran de fin de partie ##
############################

### INFO-HERE ###
### https://gist.github.com/greduan/3763b7d9d5c1d6a4916f?permalink_comment_id=4292174#gistcomment-4292174
### https://fr.wikipedia.org/wiki/Sh%C5%8Dgi#Pi%C3%A8ces

if True: ## IMPORTS ##
    from sty import bg as STY_BG
    from dessine_kanjis import *
if True: ## FUNCTIONS & CONSTANTS ##
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
    eq = {
        'R':'王', 'J':'玉', 'T':'飛', 'T+':'龍', 'F':'角', 'F+':'馬', 'O':'金',
        'A':'銀', 'A+':'全', 'C':'桂', 'C+':'圭', 'L':'香', 'L+':'杏', 'P':'歩', 'P+':'と'
    }
    def shoginame(p) -> str:
        if not p in list(eq.keys())+[k.lower() for k in eq.keys()]: return '  '
        return eq[p.upper()]
    def dessine_koma(img:image, p1, p2, koma:str, c1=col.blanc, c2=col.bleu, c3=col.red, ep_l=1, l_t=2) -> image:
        if True: ## VARS ##
            ori = 0 if koma.isupper() else 180
            if True: ## Coos ##
                ct = ct_sg(p1, p2)
                ch = coosCercle(ct, tailles_koma[koma[0].upper()][0]/2, 270+ori)
                cb = coosCercle(ct, tailles_koma[koma[0].upper()][0]/2, 90+ori)
                cbd, cbg = (coosCercle(cb, tailles_koma[koma[0].upper()][1]/2, i+ori) for i in [0, 180])
                chbg = coosCercle(cbg, tailles_koma[koma[0].upper()][0], ori-angles_koma[0])
                chhg = coosCercle(ch, tailles_koma[koma[0].upper()][1], angles_koma[3]+90+ori)
                chbd = coosCercle(cbd, tailles_koma[koma[0].upper()][0], ori+angles_koma[0]+180)
                chhd = coosCercle(ch, tailles_koma[koma[0].upper()][1], 90-angles_koma[3]+ori)
                breyk = False
                for pt1 in points_segment(pt_sg(chbg, cbg, 4), chbg):
                    for pt2 in points_segment(pt_sg(chhg, ch, 4), ch):
                        if dist(pt1, pt2) <= 1:
                            phg = pt1
                            breyk = True
                            break
                    if breyk: break
                breyk = False
                for pt1 in points_segment(pt_sg(chbd, cbd, 4), chbd):
                    for pt2 in points_segment(pt_sg(chhd, ch, 4), ch):
                        if dist(pt1, pt2) <= 1:
                            phd = pt1
                            breyk = True
                            break
                    if breyk: break
                pts = np.array([ch, phd, cbd, cbg, phg], np.int32)
            cv2.fillPoly(img.img, [pts+round(tailles_koma[koma.upper()[0]][0]/27)], c2, lineType=cv2.LINE_AA) ## Dessin pièce ##
            cv2.fillPoly(img.img, [pts], c1) ## Dessin pièce ##
            cv2.polylines(img.img, [pts], True, c2, 2, lineType=cv2.LINE_AA) ## Dessin bord de la pièce ##
            if True: ## Coos du texte ##
                a, b = 5, 1
                dtp = tailles_koma[koma[0].upper()][1]/11
                p1, p2 = coosCercle(phg, dtp, ori), coosCercle(phd, dtp, 180+ori)
                ch_y = p1[1] - phg[1]
                p3, p4 = pt_sg([p1[0], cb[1]-ch_y], p1, 12), pt_sg([p2[0], cb[1]-ch_y], p2, 12)
                ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
                ct = ct_cr(p1, p2, p3, p4)
                ph1, ph2, ph3, ph4 = (pt_sg(i, ct_sg(p1, cd), a, b) for i in [p1, p2, cg, cd])
                pb1, pb2, pb3, pb4 = (pt_sg(i, ct_sg(cg, p4), a, b) for i in [cg, cd, p3, p4])
                cth = ct_cr(ph1, ph2, ph3, ph4)
                ctb = ct_cr(pb1, pb2, pb3, pb4)
                chh, chb = ct_sg(ph1, ph2), ct_sg(ph3, ph4)
                chg, chd = ct_sg(ph1, ph3), ct_sg(ph2, ph4)
                cbh, cbb = ct_sg(pb1, pb2), ct_sg(pb3, pb4)
                cbg, cbd = ct_sg(pb1, pb3), ct_sg(pb2, pb4)
        match koma.upper():
            case a if a in 'RJ': ## DONE ##
                dessine_kanji_roi(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t, koma)
                dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'P': ## DONE ##
                if True: ## 歩 ## DONE ##
                    img.ligne(chg, chd, c2, ep_l)
                    pthg = pt_sg(ph1, chh)
                    ptcg = pt_sg(chg, cth)
                    pthd = pt_sg(ph2, chh, 5)
                    ptcd = pt_sg(chd, cth, 5)
                    img.ligne(ptcg, pt_sg(ptcg, pthg, 5, 4), c2, ep_l, l_t)
                    img.ligne(pt_sg(cth, chh), pt_sg(ptcd, pthd), c2, ep_l, l_t)
                    img.ligne(chh, pt_sg(cth, chb), c2, ep_l, l_t)
                    img.ligne(pt_sg(cth, ph3, 5, 2), pt_sg(ph3, cth, 5, 2), c2, ep_l, l_t)
                    plbdh, plbdb = pt_sg(ct_sg(cth, ct_sg(cth, chd)), ph4, 5, 2), pt_sg(pt_sg(ph4, chd, 3), ct_sg(cth, chd), 5)
                    img.ligne(plbdh, plbdb, c2, ep_l, l_t)
                    length = dist(ct_sg(phg, ph1), ct_sg(plbdh, plbdb))*0.9
                    img.ellipse(ph1, (length, length), c2, ep_l, anD=55, anF=75, ang=ori, lineType=l_t)
                if True: ## 兵 ## DONE ##
                    a, b = 5, 3
                    plg, pld = pt_sg(cbg, pb3, a, b), pt_sg(cbd, pb4, a, b)
                    img.ligne(plg, pld, c2, ep_l, l_t)
                    a, b = 3, 1
                    pthlg = pt_sg(pt_sg(pb1, pb2, a, b), pt_sg(cbg, cbd, a, b))
                    pthld = pt_sg(pt_sg(pb1, pb2, b, a), pt_sg(cbg, cbd, b, a), 3)
                    img.ligne(pthlg, pt_sg(plg, pld, a, b), c2, ep_l, l_t)
                    img.ligne(pthlg, pthld, c2, ep_l, l_t)
                    c, d = 1, 3
                    img.ligne(pt_sg(pt_sg(pb1, pb2, a, b), pt_sg(cbg, cbd, a, b), c, d), pt_sg(pt_sg(pb1, pb2, b, a), pt_sg(cbg, cbd, b, a), c, d), c2, ep_l, l_t)
                    img.ligne(pt_sg(pt_sg(pb1, pb2, b, a), pt_sg(cbg, cbd, b, a), c, d), pt_sg(plg, pld, b, a), c2, ep_l, l_t)
                    ptctb = ct_sg(ctb, cbb)
                    img.ligne(pt_sg(ptctb, pb3, a, b), pt_sg(ptctb, pb3, b, a), c2, ep_l, l_t)
                    img.ligne(pt_sg(ptctb, pb4, a, b), pt_sg(ptctb, pb4, b, a), c2, ep_l, l_t)
            case 'P+':## DONE ##
                img.ellipse(pt_sg(cd, pt_sg(ct, cb, 2), 5, 3), (dist(cd, pb4)*0.5, dist(cd, cb)*0.7), c3, ep_l, l_t, 20, 230, 45+ori)
                img.ellipse(pt_sg(cg, pt_sg(ct, cb, 2), 5, 3), (dist(cd, pb4)*0.5, dist(cd, cb)*0.7), c3, ep_l, l_t, 125, 175, 135+ori)
            case 'L': ## DONE ##
                dessine_kanji_encens(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_charriot(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'L+':## DONE ##
                dessine_kanji_promu(img, ph1, ph2, ph3, ph4, c3, ep_l, ori, l_t)
                dessine_kanji_encens(img, pb1, pb2, pb3, pb4, c3, ep_l, ori, l_t)
            case 'C': ## DONE ##
                dessine_kanji_cannellier(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_cheval(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'C+':## DONE ##
                dessine_kanji_promu(img, ph1, ph2, ph3, ph4, c3, ep_l, ori, l_t)
                dessine_kanji_cannellier(img, pb1, pb2, pb3, pb4, c3, ep_l, ori, l_t)
            case 'T': ## DONE ##
                dessine_kanji_volant(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_charriot(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'T+':## DONE ##
                dessine_kanji_dragon(img, ph1, ph2, ph3, ph4, c3, ep_l, ori, l_t, 1)
                dessine_kanji_roi(img, pb1, pb2, pb3, pb4, c3, ep_l, ori, l_t, 'R')
            case 'O': ## DONE ##
                dessine_kanji_or(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'A': ## DONE ##
                dessine_kanji_argent(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'A+':## DONE ##
                dessine_kanji_promu(img, ph1, ph2, ph3, ph4, c3, ep_l, ori, l_t)
                dessine_kanji_argent(img, pb1, pb2, pb3, pb4, c3, ep_l, ori, l_t)
            case 'F': ## DONE ##
                dessine_kanji_diagonale(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
                dessine_kanji_marcheur(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
            case 'F+':## DONE ##
                dessine_kanji_dragon(img, ph1, ph2, ph3, ph4, c3, ep_l, ori, l_t, 0)
                dessine_kanji_cheval(img, pb1, pb2, pb3, pb4, c3, ep_l, ori, l_t)
        return img
    class EXIT(Exception):
        def __init__(self, *args):
            super().__init__(args)
        def __str__(self):
            return f'GAME EXIT'
    class mouse:
        click = False
        pos = [-1, -1]
    def mouse_get_case(event, x, y, flags, params) -> None:
        if event==cv2.EVENT_LBUTTONDOWN:
            mouse.click = True
            pt = [x, y]
            if clicked_in(pt, [Shogi.p1, Shogi.p4]):
                mouse.pos = pt
            elif clicked_in(pt, [Shogi.pkda[0], Shogi.pkda[3]]):
                mouse.pos = pt
            elif clicked_in(pt, [Shogi.pkdb[0], Shogi.pkdb[3]]):
                mouse.pos = pt
save = {}
class Shogi:
    if True: ### CONSTANTES ###
        col.bg=col.new('#1340ff', 'rgb'); fond = col.new('#C89678', 'rgb'); col.li = col.new('#281711', 'rgb') ## Couleurs
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
        save['ctkda'] = ctkda; save['ctkdb'] = ctkdb; save['dist'] = racine_carree((conversion*(proportions_kd/2))**2*2)
        pkda = [ coosCercle(save['ctkda'], save['dist'], 90*i+45) for i in range(4) ] ## Points des bords du komadai A
        pkdb = [ coosCercle(save['ctkdb'], save['dist'], 90*i+45) for i in range(4) ] ## Points des bords du komadai B
        pkda = [pkda[2], pkda[3], pkda[1], pkda[0]]; pkdb = [pkdb[2], pkdb[3], pkdb[1], pkdb[0]]; ex = 3; l_t = 1
    if True: ### Création de l'image ###
        img = image('Shogi', image.new_img(fond=col.bg)) ## Création de l'image
        img.rectangle([p1[0]-px*ex, p1[1]-py*ex], [p4[0]+px*ex, p4[1]+py*ex], fond, 0, l_t) ## Dessin du shogiban
        for y in range2(ya, yb+1, dy): img.ligne([xa, y], [xb, y], col.li, ep_li, l_t) ## Lignes horizontales
        for x in range2(xa, xb+1, dx): img.ligne([x, ya], [x, yb], col.li, ep_li, l_t) ## Lignes verticales
        for y in range2(ya+diff(ya, yb)/3, yb, diff(ya, yb)/3): ## Dessin des points d'aide du shogiban
            for x in range2(xa+diff(xa, xb)/3, xb, diff(xa, xb)/3): img.cercle([x, y], ep_c, col.li, 0, l_t)
        img.rectangle(pkda[0], pkda[3], fond, 0, l_t) ## Komadai A
        img.rectangle(pkdb[0], pkdb[3], fond, 0, l_t) ## Komadai B
    def reset(self):
        return Shogi(name=self.name, j1=self.j1, j2=self.j2)
    def get_pieces_ligne(self, y:int) -> list:
        pcs = []; espaces = 4
        for x in range(9):
            n = shoginame(self.matrix[y, x]) if not self.vide(x, y) else ' '*espaces
            if not n == ' '*espaces:
                s = f' {fg.blue if self.matrix[y, x][0].isupper() else fg.red}{n}{fg.rs} '
                pcs.append(s)
            else: pcs.append(n)
        return pcs
    def get_pieces_capturees(self, c:int) -> list:
        espaces = 5
        s = self.str_p if c == 0 else self.str_p[::-1]
        k = [i.upper() for i in (self.captures[0] if c == 0 else self.captures[1])]
        pcs = []
        for p in s:
            if not p in k: pcs.append(' '*espaces); continue
            else:
                n = k.count(p)
                pc = f'{fg.blue if c==0 else fg.red}{f"{shoginame(p)}{n if n>1 else ''}":^4}{fg.rs}'
                pcs.append(pc)
        return pcs
    def __str__(self) -> str:
        cl1, cl2, cl3 = 200, 150, 120
        sy, ns = STY_BG(cl1, cl2, cl3), STY_BG.rs
        a1, a2, a3, a4, a5, a6, a7, a8, a9 = self.get_pieces_ligne(0)
        b1, b2, b3, b4, b5, b6, b7, b8, b9 = self.get_pieces_ligne(1)
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = self.get_pieces_ligne(2)
        d1, d2, d3, d4, d5, d6, d7, d8, d9 = self.get_pieces_ligne(3)
        e1, e2, e3, e4, e5, e6, e7, e8, e9 = self.get_pieces_ligne(4)
        f1, f2, f3, f4, f5, f6, f7, f8, f9 = self.get_pieces_ligne(5)
        g1, g2, g3, g4, g5, g6, g7, g8, g9 = self.get_pieces_ligne(6)
        h1, h2, h3, h4, h5, h6, h7, h8, h9 = self.get_pieces_ligne(7)
        i1, i2, i3, i4, i5, i6, i7, i8, i9 = self.get_pieces_ligne(8)
        kdO, kdA, kdC, kdP, kdL, kdF, kdT = self.get_pieces_capturees(0)
        kdo, kda, kdc, kdp, kdl, kdf, kdt = self.get_pieces_capturees(1)
        if True: ## Plateau en str ##
            o = f'''{' '*22}{sy},--------------------------------------------¬{ns}\n{' '*22}{sy}|{a1}|{a2}|{a3}|{a4}|{a5}|{a6}|{a7}|{a8}|{a9}|{ns}\n{' '*22}{sy}|----+----+----+----+----+----+----+----+----|{ns}\n{' '*22}{sy}|{b1}|{b2}|{b3}|{b4}|{b5}|{b6}|{b7}|{b8}|{b9}|{ns}\n {sy},-----------------¬{ns}  {sy}|----+----+----+----+----+----+----+----+----|{ns}  {sy},-----------------¬{ns}\n {sy}|  {kdo} | {kda}  |{ns}  {sy}|{c1}|{c2}|{c3}|{c4}|{c5}|{c6}|{c7}|{c8}|{c9}|{ns}  {sy}|  {kdT} | {kdF}  |{ns}\n {sy}|-----+-----+-----|{ns}  {sy}|----+----+----X----+----+----X----+----+----|{ns}  {sy}|-----+-----+-----|{ns}\n {sy}|{kdc}|{kdp}|{kdl}|{ns}  {sy}|{d1}|{d2}|{d3}|{d4}|{d5}|{d6}|{d7}|{d8}|{d9}|{ns}  {sy}|{kdL}|{kdP}|{kdC}|{ns}\n {sy}|-----+-----+-----|{ns}  {sy}|----+----+----+----+----+----+----+----+----|{ns}  {sy}|-----+-----+-----|{ns}\n {sy}|  {kdf} | {kdt}  |{ns}  {sy}|{e1}|{e2}|{e3}|{e4}|{e5}|{e6}|{e7}|{e8}|{e9}|{ns}  {sy}|  {kdA} | {kdO}  |{ns}\n {sy}`-----------------´{ns}  {sy}|----+----+----+----+----+----+----+----+----|{ns}  {sy}`-----------------´{ns}\n{' '*22}{sy}|{f1}|{f2}|{f3}|{f4}|{f5}|{f6}|{f7}|{f8}|{f9}|{ns}\n{' '*22}{sy}|----+----+----X----+----+----X----+----+----|{ns}\n{' '*22}{sy}|{g1}|{g2}|{g3}|{g4}|{g5}|{g6}|{g7}|{g8}|{g9}|{ns}\n{' '*22}{sy}|----+----+----+----+----+----+----+----+----|{ns}\n{' '*22}{sy}|{h1}|{h2}|{h3}|{h4}|{h5}|{h6}|{h7}|{h8}|{h9}|{ns}\n{' '*22}{sy}|----+----+----+----+----+----+----+----+----|{ns}\n{' '*22}{sy}|{i1}|{i2}|{i3}|{i4}|{i5}|{i6}|{i7}|{i8}|{i9}|{ns}\n{' '*22}{sy}`--------------------------------------------´{ns}'''
        return o
    def __init__(self, tableau=defTab(), name:str='Shogi', j1:str='J1', j2:str='J2', fullscreen:bool=True) -> None:
        self.str_p = 'TFLPCAO'
        self.fullscreen = fullscreen
        self.name = name
        self.last_move = None
        self.j1, self.j2 = j1, j2
        plateau = [ ## Création de l'array qui contient toutes les coos des cases
            [
                [
                    [x, y],
                    [x+self.dx, y+self.dy]
                ] for x in range2(self.xa, self.xb, self.dx)
            ] for y in range2(self.ya, self.yb, self.dy)
        ]
        self.plateau = copy.deepcopy(np.array(plateau))
        self.trait = True
        self.matrix = np.array(tableau, dtype=object)
        self.captures = [[], []]
        coef = 1
        nx, ny = [2, 3, 2], 3
        ## KOMADAI A ##
        coos_kd_a = []
        for i, y in enumerate(range(self.pkda[0][1], self.pkda[2][1], round(self.dy*coef))[:ny:]):
            x_, y_ = (diff(self.pkda[0][0], self.pkda[1][0])-self.dx*coef*nx[i])/2, (diff(self.pkda[0][1], self.pkda[2][1])-self.dy*coef*ny)/2
            for x in range(self.pkda[0][0], self.pkda[1][0], round(self.dx*coef))[:nx[i]:]:
                coos_kd_a.append([[x+x_,y+y_], [x+x_+self.dx*coef,y+y_+self.dy*coef]])
        ## KOMADAI B ##
        coos_kd_b = []
        for i, y in enumerate(range(self.pkdb[0][1], self.pkdb[2][1], round(self.dy*coef))[:ny:]):
            x_, y_ = (diff(self.pkdb[0][0], self.pkdb[1][0])-self.dx*coef*nx[i])/2, (diff(self.pkdb[0][1], self.pkdb[2][1])-self.dy*coef*ny)/2
            for x in range(self.pkdb[0][0], self.pkdb[1][0], round(self.dx*coef))[:nx[i]:]:
                coos_kd_b.append([[x+x_,y+y_], [x+x_+self.dx*coef,y+y_+self.dy*coef]])
        coos_komadai = [coos_kd_a, coos_kd_b]
        self.coos_komadai = np.array(coos_komadai)
    def gdye(self, p='R') -> list:
        for y in range(9):
            for x in range(9):
                if self.matrix[y, x] == p:
                    return [x, y]
        return [-1, -1]
    def echec(self, c='R') -> bool: ### TODO ### TODO ###
        xa, ya = self.gdye('R' if c == 'R' else 'J')
        change = (c == 'R') != self.trait
        if change: self.trait = not self.trait
        for yo in range(9):
            for xo in range(9):
                if self.legal(yo, xo, xa, ya):
                    if change: self.trait = not self.trait
                    return True
        if change: self.trait = not self.trait
        return False
    def image(self) -> image:
        c1, c2, c3 = col.blanc, col.black, col.red
        ep_l, l_t = 1, 2
        img = image(self.name, img=copy.deepcopy(Shogi.img))
        for x in range(9):
            for y in range(9):
                t = self.matrix[y, x]
                if self.last_move != None:
                    if [x, y] in self.last_move:
                        img.rectangle(self.plateau[y, x, 0], self.plateau[y, x, 1], col.cyan, Shogi.ep_li, l_t)
                if t in ["", " ", ".", "·"]: continue
                dessine_koma(img, self.plateau[y, x, 0], self.plateau[y, x, 1], t, c1, c2, c3, ep_l, l_t)
        ind = 0
        for c in range(len(self.coos_komadai[0])):
            p1, p2 = self.coos_komadai[0, c]
            c = self.str_p[ind]
            n = ''.join(c.upper() for c in self.captures[0]).count(c)
            if n > 0: dessine_koma(img, p1, p2, c, c1, c2, c3, ep_l, l_t)
            if n > 1:
                sz = 2; pt = pt_sg(p1, p2, 1, 5); ckd1, ckd2 = col.black, col.white
                img.ecris(n, pt_sg(p1, p2, 1, 5), ckd1, ep_l*3, sz, cv2.FONT_HERSHEY_COMPLEX_SMALL, l_t)
                img.ecris(n, [pt[0]-2, pt[1]+1], ckd2, ep_l, sz, cv2.FONT_HERSHEY_COMPLEX_SMALL, l_t)
            ind += 1
        ind = 0
        for c in range(len(self.coos_komadai[1])):
            p1, p2 = self.coos_komadai[1, c]
            c = self.str_p[::-1][ind]
            n = ''.join(c.upper() for c in self.captures[1]).count(c)
            if n > 0: dessine_koma(img, p1, p2, c.lower(), c1, c2, c3, ep_l, l_t)
            if n > 1:
                sz = 2; pt = pt_sg(p1, p2, 1, 5); ckd1, ckd2 = col.black, col.white
                img.ecris(n, pt_sg(p1, p2, 1, 5), ckd1, ep_l*3, sz, cv2.FONT_HERSHEY_COMPLEX_SMALL, l_t)
                img.ecris(n, [pt[0]-2, pt[1]+1], ckd2, ep_l, sz, cv2.FONT_HERSHEY_COMPLEX_SMALL, l_t)
            ind += 1
        return img
    def vide(self, x, y) -> bool:
        return shoginame(self.matrix[y, x]) == '  '
    def legal_gen_or(self, xo, yo, xa, ya) -> bool:
        x, y = self.depl_piece(xo, yo, xa, ya)
        if y==1 and abs(x)<=1: return True
        elif y==-1 and x==0: return True
        elif y==0 and abs(x)==1: return True
        return False
    def depl_piece(self, xo, yo, xa, ya):
        if self.trait: return (xo-xa, yo-ya)
        else: return (xa-xo, ya-yo)
    def leg_roi(self, xo, yo, xa, ya):
        return max([abs(i) for i in self.depl_piece(xo, yo, xa, ya)])==1
    def legal(self, xo, yo, xa, ya) -> bool:
        if xo == -1:
            if yo == 3:
                if ('P' if self.trait else 'p') in [self.matrix[i, xa] for i in range(9)]: return False
            return self.vide(xa, ya)
        if xo==xa and yo==ya: return False ## Suicide de pièce ##
        if not self.vide(xa, ya) and self.matrix[ya, xa][0].isupper() == self.trait: ## Autocapture ##
            return False
        piece = self.matrix[yo, xo]
        match piece.upper():
            case 'R' | 'J': return self.leg_roi(xo, yo, xa, ya)
            case Or if Or in ['O', 'A+', 'C+', 'L+', 'P+']: return self.legal_gen_or(xo, yo, xa, ya)
            case 'A': x,y=self.depl_piece(xo,yo,xa,ya);return(y==1 and abs(x)<=1)or(y==-1 and abs(x)==1)
            case 'C':
                x, y = self.depl_piece(xo, yo, xa, ya)
                if (y==2 and abs(x)==1): return True
                else: return False
            case 'P':
                x, y = self.depl_piece(xo, yo, xa, ya)
                if (y==1 and x==0): return True
                else: return False
            case 'L':
                x, y = self.depl_piece(xo, yo, xa, ya)
                if x==0 and y>0:
                    for y_ in range(y)[1::]:
                        if not self.vide(xo, (yo-y_ if self.trait else yo+y_)):
                            return False
                    return True
            case 'F' | 'F+': ## TODO : vérifier qu'il ne saute aucune pièce ##
                if '+' in piece and self.leg_roi(xo, yo, xa, ya): return True
                x, y = self.depl_piece(xo, yo, xa, ya)
                return abs(x)==abs(y)
            case 'T' | 'T+': ## TODO : vérifier qu'elle ne saute aucune pièce ##
                if '+' in piece and self.leg_roi(xo, yo, xa, ya): return True
                x, y = self.depl_piece(xo, yo, xa, ya)
                return x==0 or y == 0
        return False
    def get_case(self, img):
        img.montre(1, fullscreen=self.fullscreen)
        cv2.setMouseCallback(self.name, mouse_get_case)
        while True:
            match img.montre(1, fullscreen=self.fullscreen):
                case 27: raise EXIT
                case 32:
                    img.ferme()
                    self.fullscreen = not self.fullscreen
                    img.montre(1, fullscreen=self.fullscreen)
                    cv2.setMouseCallback(self.name, mouse_get_case)
            if mouse.click:
                mouse.click = False
                if mouse.pos == [-1, -1]: return [-1, -1]
                pt = mouse.pos
                mouse.pos = [-1, -1]
                break
        for y in range(len(self.plateau)):
            for x in range(len(self.plateau[y])):
                if clicked_in(pt, self.plateau[y, x]):
                    return [x, y]
        kd = self.coos_komadai[0 if self.trait else 1]
        x = -1
        for y in range(len(kd)):
            if clicked_in(pt, kd[y]):
                return [x, y]
        return -1, -1
    def move(self):
        img = self.image()
        co = False
        col.violet = col.new("#800080", 'rgb')
        l_t = 2
        while not co:
            xo, yo = self.get_case(img)
            if xo==-1:
                if self.str_p[::1 if self.trait else -1][yo] in ''.join(i for i in self.captures[0 if self.trait else -1]).upper():
                    co = True ## From KOMADAI ##
            elif self.matrix[yo, xo] in ' ._·': continue ## Bouge que des pièces
            elif self.matrix[yo, xo][0].isupper() != self.trait: continue ## Bouge que celui qui a le trait
            else: co = True
        ca = False
        while not ca:
            s_img = image(nom=img.nom, img=copy.deepcopy(img.img))
            if self.echec('R'):
                x, y = self.gdye('R')
                s_img.rectangle(self.plateau[y, x, 0], self.plateau[y, x, 1], col.red, 0)
            if xo>=0: s_img.rectangle(self.plateau[yo, xo, 0], self.plateau[yo, xo, 1], col.green, Shogi.ep_li) ## Cadre de selection
            else: s_img.rectangle(self.coos_komadai[0 if self.trait else 1, yo, 0], self.coos_komadai[0 if self.trait else 1, yo, 1], col.green, Shogi.ep_li, l_t) ## Cadre de selection
            for x in range(9):
                for y in range(9):
                    if self.legal(xo, yo, x, y):
                        c = self.plateau[y, x]
                        s_img.cercle(ct_sg(c[0], c[1]), 10, col.violet, 0, l_t)
            xa, ya = self.get_case(s_img)
            if xa<0 or ya<0: return
            if xa==xo and ya==yo: return
            if not self.vide(xa, ya):
                if self.matrix[ya, xa].isupper() == self.trait:
                    xo, yo = xa, ya; continue
            ca = True
        if self.legal(xo, yo, xa, ya):
            if self.matrix[yo, xo].lower() in "plcatf" and len(self.matrix[yo, xo]) == 1: ## Promotion ## TODO ##
                if (self.trait and ya<3) or (not self.trait and ya>5):
                    self.matrix[yo, xo] = f'{self.matrix[yo, xo]}+'
            if not self.vide(xa, ya):
                if self.trait:
                    self.captures[0].append(self.matrix[ya, xa][0].upper())
                else:
                    self.captures[1].append(self.matrix[ya, xa][0].lower())
            if xo == -1:
                if self.trait: piece = self.str_p[yo].upper()
                else: piece = self.str_p[::-1][yo].lower()
                self.matrix[ya, xa] = piece
                self.captures[0 if self.trait else 1].pop(self.captures[0 if self.trait else 1].index(piece))
            else:
                self.matrix[ya, xa] = self.matrix[yo, xo]
                self.matrix[yo, xo] = ' '
            self.last_move = [[xo, yo], [xa, ya]]
            self.trait = not self.trait
        else: print('Illegal move')
    def jouable(self):
        return [self.matrix[y, x].upper() in 'RJ' for x in range(9) for y in range(9)].count(True) == 2
    def start(self, out=False):
        while self.jouable():
            if out: print(self)
            self.move()
        if out: print(self)

if __name__ == '__main__' and True:
    try: pt = Shogi(); pt.start(True)
    except EXIT: print('GAME ENDED!'); raise SystemExit