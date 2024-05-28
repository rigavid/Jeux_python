#############################
## Author: T-Sana ###########
## 24/5/2024 -> XX/XX/202X ##
#############################
## TODO ###################################################
## Dessin des noms japonais en mode graphique - EN COURS ##
## Légalité des mouvements des pièces #####################
## Promotion des pièces ################
## Parachutage des pièces ##
############################

### INFO-HERE ###
### https://gist.github.com/greduan/3763b7d9d5c1d6a4916f?permalink_comment_id=4292174#gistcomment-4292174
### https://fr.wikipedia.org/wiki/Sh%C5%8Dgi#Pi%C3%A8ces

GUIDES = False ## TODO -> TO REMOVE ##
from Outils.cvt2 import *
from sty import bg as STY_BG

def defTab() -> list:
    l = [
        ['l', 'c', 'a', 'o', 'j', 'o', 'a', 'c', 'l'],
        [' ', 't', ' ', ' ', ' ', ' ', ' ', 'f', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P+', 'P', 'P', 'P', 'P'],
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

angles_koma = [81, 117, 85]
angles_koma.append(360-90-angles_koma[0]-angles_koma[1])
tailles_koma = {'R': [32, 28.7, 9.7], 'T': [31, 27.7, 9.3], 'O': [30, 26.7, 8.8],
                'C': [29, 25.5, 8.3], 'L': [28, 23.5, 8.0], 'P': [27, 22.5, 7.75]}
for s in 'JR FT AO'.split(): tailles_koma[s[0]]=tailles_koma[s[1]]
for km in tailles_koma: tailles_koma[km] = [27.22222222222222*(v/10) for v in tailles_koma[km]]
def dessine_kanji_or(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    a = 20
    pcg = coosCercle(ch, dist(ch, p1), ori+180-a)
    pcd = coosCercle(ch, dist(ch, p1), ori+a)
    img.ligne(ch, pcg, c, ep, l_t)
    img.ligne(ch, pcd, c, ep, l_t)
    clh, clb = coosCercle(ch, tailles_koma['O'][1]/2/5, 90+ori), cb
    ctl = ct_sg(clh, clb)
    pts = [clh, ctl, clb]
    dts = [dist(p1, ch)*i for i in [0.8, 0.7, 1]]
    for i in range(3):
        img.ligne(coosCercle(pts[i], dts[i], ori), coosCercle(pts[i], dts[i], ori+180), c, ep, l_t)
    img.ligne(clh, clb, c, ep, l_t)
    pt1 = coosCercle(pts[1], dts[1], ori)
    pt2 = coosCercle(pts[1], dts[1], ori+180)
    a, b = 5, 3
    img.ligne(pt_sg(pt1, clb, a, b), pt_sg(pt1, clb, b, a), c, ep, l_t)
    img.ligne(pt_sg(pt2, clb, a, b), pt_sg(pt2, clb, b, a), c, ep, l_t)
    return img
def dessine_kanji_charriot(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    pts = []
    for i, y in enumerate(float_range(p1[1], p3[1], 6)):
        match i:
            case b if b in [i for i in range(2, 5)]:
                pt1, pt2 = [pt_sg(p1, ch, 5, 3)[0], y], [pt_sg(p2, ch, 5, 3)[0], y]
                img.ligne(pt1, pt2, c, ep, l_t)
                pts.append([pt1, pt2])
            case a if a in [i for i in range(1, 6)]:
                img.ligne([p1[0], y], [p2[0], y], c, ep, l_t)
    img.ligne(pts[0][0], pts[-1][0], c, ep, l_t)
    img.ligne(pts[0][1], pts[-1][1], c, ep, l_t)
    img.ligne(ch, cb, c, ep, l_t)
    return img
def dessine_kanji_cheval(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    ptbd, pttbd = pt_sg(p4, pt_sg(cb, ct, 2), 2), pt_sg(p4, cd, 4.5)
    ptcg, ptcd = pt_sg(cg, ct, 2), pt_sg(cd, ct, 2)
    ptsh = [ptcg, pt_sg(ptcg, ptcd, 2), pt_sg(ptcd, ptcg, 2), ptcd]
    ptsb = [p3, pt_sg(p3, ptbd, 2), pt_sg(ptbd, p3, 2), ptbd]
    lines = [
        [p2, p1], [p1, cg], [cg, cd], [cd, pttbd], [pttbd, ptbd], [ch, ct],
        [pt_sg(p1, cg, 2), pt_sg(p2, cd, 2)], [pt_sg(cg, p1, 2), pt_sg(cd, p2, 2)],
    ]
    a, b = 5, 2
    lines += [[pt_sg(ptsh[i], ptsb[i], a, b), pt_sg(ptsh[i], ptsb[i], b, a)] for i in range(4)]
    for pa, pb in lines: img.ligne(pa, pb, c, ep, l_t)
    return img
def dessine_kanji_general(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## TODO ##
    ch, cb, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    d = dist(p1, p2)/6; a, b = 5, 4
    plgh, plgb = coosCercle(p1, d, ori), coosCercle(p3, d, ori)
    plgch, plgcb = (pt_sg(plgh, plgb, [a,b][i], [b,a][i]) for i in range(2))
    lines = [[plgh,plgb],[plgch,coosCercle(plgch,d*1.5,245+ori)],[plgch,coosCercle(plgcb,d,170+ori)],[p2,pt_sg(p1,pt_sg(ch,ct,2),2,3)]]
    a, b = 4, 11
    lines += [[pt_sg(p3, ct, a, b), pt_sg(p4, cd, a, b)], [pt_sg(cb, p4, a, b), pt_sg(ct, cd, a, b)]]
    for pa, pb in lines: img.ligne(pa, pb, c, ep, l_t) ## Dessin des lignes ##
    return image
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
        cv2.fillPoly(img.img, [pts], c1) ## Dessin pièce ##
        cv2.polylines(img.img, [pts], True, c2, 2) ## Dessin bord de la pièce ##
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
            lines = [
                [pt_sg(ph1, chh, 7), pt_sg(ph2, chh, 7)],
                [pt_sg(chg, cth, 3), pt_sg(chd, cth, 3)],
                [chh, chb], [ph3, ph4]
            ]
            if koma.upper() == 'J':
                lines.append([pt_sg(cth, ph4, 5, 2), pt_sg(ph4, cth, 5, 4)])
            for pa, pb in lines: img.ligne(pa, pb, c2, ep_l, l_t) ## Dessin des lignes ##
            dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
        case 'P': ## 歩兵 ## DONE ##
            if True: ## 歩 ## DONE ##
                img.ligne(chg, chd, c2, ep_l)
                pthg = pt_sg(ph1, chh)
                ptcg = pt_sg(chg, cth)
                pthd = pt_sg(ph2, chh, 5)
                ptcd = pt_sg(chd, cth, 5)
                img.ligne(ptcg, pt_sg(ptcg, pthg, 5, 4), c2, ep_l, l_t)
                img.ligne(pt_sg(cth, chh), pt_sg(ptcd, pthd), c2, ep_l, l_t)
                img.ligne(chh, cth, c2, ep_l, l_t)
                img.ligne(pt_sg(cth, ph3, 5, 2), pt_sg(ph3, cth, 5, 2), c2, ep_l, l_t)
                plbdh, plbdb = pt_sg(ct_sg(cth, chd), ph4, 5, 2), pt_sg(pt_sg(ph4, chd, 3), ct_sg(cth, chd), 5)
                img.ligne(plbdh, plbdb, c2, ep_l, l_t)
                length = dist(ct_sg(phg, ph1), ct_sg(plbdh, plbdb))
                a, b = 4, 1; c, d = 15, 3
                pthc, pthb = pt_sg(cth, chd, c, d), pt_sg(chb, ph4, c, d)
                img.ligne(pt_sg(pthc, pthb, a, b), pt_sg(pthb, pthc, a, b), c2, ep_l, l_t)
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
        case 'P+': ## と ## DONE ##
            img.ellipse(pt_sg(cd, pt_sg(ct, cb, 2), 5, 3), (dist(cd, pb4)*0.5, dist(cd, cb)*0.7), c3, ep_l, l_t, 20, 230, 45+ori)
            img.ellipse(pt_sg(cg, pt_sg(ct, cb, 2), 5, 3), (dist(cd, pb4)*0.5, dist(cd, cb)*0.7), c3, ep_l, l_t, 125, 175, 135+ori)
        case 'L':
            dessine_kanji_cheval(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
        case 'T':
            dessine_kanji_charriot(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
        case 'O': ## Général d'or ## DONE ##
            dessine_kanji_or(img, ph1, ph2, ph3, ph4, c2, ep_l, ori, l_t)
            dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
        case 'A': ## Général d'argent ##
            dessine_kanji_or(img, ph1, chh, ph3, chb, c2, ep_l, ori, l_t)
            dessine_kanji_general(img, pb1, pb2, pb3, pb4, c2, ep_l, ori, l_t)
        case _: ## Unmapped piece ## TODO -> TO REMOVE ##
            char = koma[0].upper() if len(koma)>1 or koma in 'RJO' else koma[0].lower()
            img.ecris(char, [ct[0], ct[1]+5], col.blue[::-1] if koma.isupper() else col.red[::-1], 3, 2, cv2.FONT_HERSHEY_SIMPLEX, l_t)
    if GUIDES: ### Guides ## TODO -> TO REMOVE ###
        for p in [p1, p2, p3, p4, ct, ch, cb, cg, cd]:
            img.cercle(p, 3, col.red, 0)
        img.rectangle(p1, p4, col.green, 1)
        img.rectangle(ph1, ph4, col.green, 1)
        img.rectangle(pb1, pb4, col.green, 1)
    return img
class EXIT(Exception):
    def __init__(self, *args):
        super().__init__(args)
    def __str__(self):
        return f'GAME EXIT'
class mouse:
    click = False
    pos = [0, 0]
def mouse_get_case(event, x, y, flags, params) -> None:
    if event==cv2.EVENT_LBUTTONDOWN:
        if clicked_in((x,y), [Shogi.p1, Shogi.p4]):
            mouse.click = True
            mouse.pos = [x, y]
        
save = {}
class Shogi:
    if True: ### CONSTANTES ###
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
    ex = 3
    if True: ### Création de l'image ###
        img = image('Shogi', image.new_img(fond=col.bg)) ## Création de l'image
        img.rectangle([p1[0]-px*ex, p1[1]-py*ex], [p4[0]+px*ex, p4[1]+py*ex], fond, 0) ## Dessin du shogiban
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
        return Shogi(name=self.name, j1=self.j1, j2=self.j2)
    def __str__(self) -> str:
        cl1, cl2, cl3 = 200, 150, 120
        matrix = self.matrix; s = f' {STY_BG(cl1, cl2, cl3)},--------------------------------------------¬{STY_BG.rs}'
        for i, l in enumerate(matrix):
            s += f'{STY_BG.rs}\n {STY_BG(cl1, cl2, cl3)}|'
            for c in l:
                t = (fg.blue if c.isupper() else fg.red) + shoginame(c) + fg.rs 
                s += f' {t} |'
            if not i in [2, 5, 8]: s += f'{STY_BG.rs}\n {STY_BG(cl1, cl2, cl3)}|----+----+----+----+----+----+----+----+----|'
            elif i == 8: s += f'{STY_BG.rs}\n {STY_BG(cl1, cl2, cl3)}`--------------------------------------------´' + STY_BG.rs
            else: s += f'{STY_BG.rs}\n {STY_BG(cl1, cl2, cl3)}|----+----+----X----+----+----X----+----+----|'
        return s
    def __init__(self, tableau=defTab(), name:str='Shogi', j1:str='J1', j2:str='J2', fullscreen:bool=True) -> None:
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
    def image(self) -> image:
        img = image(self.name, img=copy.deepcopy(Shogi.img))
        for x in range(9):
            for y in range(9):
                t = self.matrix[x, y]
                if t in ["", " ", ".", "·"]: continue
                dessine_koma(img, self.plateau[x, y, 0], self.plateau[x, y, 1], t, col.blanc, col.black)
        return img
    def vide(self, x, y) -> bool:
        return shoginame(self.matrix[x, y]) == '  '
    def legal(self, xo, yo, xa, ya) -> bool: ## TODO ##
        if xo==xa and yo==ya: return False ## Suicide de pièce ##
        print(self.matrix[xa, ya])
        if not self.vide(xa, ya) and self.matrix[xa, ya][0].isupper() == self.trait: ## Autocapture ##
            return False
        
        return True
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
                pt = mouse.pos
                break
        for x in range(len(self.plateau)):
            for y in range(len(self.plateau[x])):
                if clicked_in(pt, self.plateau[x, y]):
                    return [x, y]
        raise ValueError
    def move(self):
        img = self.image()
        xo, yo = self.get_case(img)
        if self.matrix[xo, yo] in ' ._·': return ## Bouge que des pièces
        elif self.matrix[xo, yo][0].isupper() != self.trait: return ## Bouge que celui qui a le trait
        img.rectangle(self.plateau[xo, yo, 0], self.plateau[xo, yo, 1], col.green, 3) ## Cadre de selection
        xa, ya = self.get_case(img)
        if self.legal(xo, yo, xa, ya):
            if self.matrix[xo, yo].lower() in "plcatf" and len(self.matrix[xo, yo]) == 1: ## Promotion ## TODO ##
                if (self.trait and xa<3) or (not self.trait and xa>5):
                    self.matrix[xo, yo] = f'{self.matrix[xo, yo]}+'
                print(self.matrix)
            self.matrix[xa, ya] = self.matrix[xo, yo]
            self.matrix[xo, yo] = ' '
            self.trait = not self.trait
        else: print('Illegal move')
    def jouable(self): return True ## TODO ##
    def start(self, out=False):
        while self.jouable():
            if out: print(self)
            self.move()
        if out: print(self)
            


if __name__ == '__main__' and True:
    try: pt = Shogi(); pt.start()
    except EXIT: print('GAME ENDED!'); raise SystemExit