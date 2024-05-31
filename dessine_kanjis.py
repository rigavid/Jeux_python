from koma import *
from Outils.cvt2 import *

def dessine_kanji_soleil(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image:
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    lines = [ [p1, p3], [p1, p2], [p2, p4], [cg, cd], [p3, p4] ]
    for a, b in lines:
        img.ligne(a, b, c, ep, l_t)
    return img
def dessine_kanji_cereale(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image:
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    ah, ab = ch, cb
    pa = pt_sg(ah, ab, 3, 2)
    d1 = dist(p1, ch) * 0.6
    d2 = dist(p1, ch) * 0.9
    d3 = dist(p1, p3) * 0.8
    hag, had = coosCercle(ah, d1, 180+ori), coosCercle(ah, d1, ori)
    a1, a2 = coosCercle(pa, d2, 180+ori), coosCercle(pa, d2, ori)
    a3, a4 = coosCercle(pa, d3, 150+ori), coosCercle(pa, d3, 30+ori)
    lines = [ [had, hag], [a1, a2], [ah, ab], [pa, a3], [pa, a4] ]
    for a, b in lines:
        img.ligne(a, b, c, ep, l_t)
    return img
def dessine_kanji_encens(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image:
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    dessine_kanji_cereale(img, p1, p2, cg, cd, c, ep, ori, l_t)
    dessine_kanji_soleil(img, cg, cd, p3, p4, c, ep, ori, l_t)
    return img
def dessine_kanji_arbre(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ah, ab = ct_sg(p1, p2), ct_sg(p3, p4)
    pa = pt_sg(ah, ab, 3)
    d = dist(p1, ah) * 0.9
    d2 = dist(p1, p3) * 0.7
    a1, a2 = coosCercle(pa, d, 180+ori), coosCercle(pa, d, ori)
    a3, a4 = coosCercle(pa, d2, 110+ori), coosCercle(pa, d2, 70+ori)
    lines = [ [a1, a2], [ah, ab], [pa, a3], [pa, a4] ]
    for a, b in lines:
        img.ligne(a, b, c, ep, l_t)
    return img
def dessine_kanji_terre(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    a, b = 17, 2
    lines = [[pt_sg(cg, cd, a, b), pt_sg(cd, cg, a, b)], [pt_sg(ch, cb, a, b*2), cb], [p3, p4]]
    for a, b in lines:
        img.ligne(a, b, c, ep, l_t)
    return img
def dessine_kanji_cannellier(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    ct, cd = ct_cr(p1, p2, p3, p4), ct_sg(p2, p4)
    dessine_kanji_arbre(img, p1, ch, p3, cb, c, ep, ori, l_t)
    dessine_kanji_terre(img, ch, p2, ct, cd, c, ep, ori, l_t)
    dessine_kanji_terre(img, ct, cd, cb, p4, c, ep, ori, l_t)
    return img
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
def dessine_kanji_argent(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## TODO ##
    dessine_kanji_or(img, p1, ct_sg(p1, p2), p3, ct_sg(p3, p4), c, ep, ori, l_t)
    return img
def dessine_kanji_dragon(img:image, p1, p2, p3, p4, c=col.black, ep=1, ori=0, l_t=2) -> image: ## TODO ##
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
    plhdg = pt_sg(p1,pt_sg(ch,ct,2),2,3)
    lines = [[plgh,plgb],[plgch,coosCercle(plgch,d*1.5,245+ori)],[plgch,coosCercle(plgcb,d,170+ori)],[p2,plhdg]]
    a, b = 4, 11
    lines += [[pt_sg(p3, ct, a, b), pt_sg(p4, cd, a, b)], [pt_sg(cb, p4, a, b), pt_sg(ct, cd, a, b)], [ct_sg(plhdg, ct), ct]]
    for pa, pb in lines: img.ligne(pa, pb, c, ep, l_t) ## Dessin des lignes ##
    return image