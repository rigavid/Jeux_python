try: from koma import *
except: from Shogi.koma import *
from pyimager import *
def float_range(start, stop, number=1):
    if stop==start: return [start for _ in range(number)]
    else:
        d = diff(start, stop)
        s = d/number
        o = []
        if start>stop:
            for n in range(number)[::-1]:
                o.append(stop+abs(s*n))
        else:
            for n in range(number):
                o.append(start+abs(s*n))
        return o
def dessine_kanji_roi(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2, koma='R'): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    lines = [[pt_sg(p1, ch, 7), pt_sg(p2, ch, 7)], [pt_sg(cg, ct, 3), pt_sg(cd, ct, 3)], [ch, cb], [p3, p4]]
    if koma.upper() == 'J': lines.append([pt_sg(ct, p4, 5, 2), pt_sg(p4, ct, 5, 4)])
    for pa, pb in lines: img.line(pa, pb, c, ep, l_t) ## Dessin des lignes ##
def dessine_kanji_soleil(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    lines = [ [p1, p3], [p1, p2], [p2, p4], [cg, cd], [p3, p4] ]
    for a, b in lines: img.line(a, b, c, ep, l_t)
def dessine_kanji_cereale(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    ah, ab = ch, cb
    pa = pt_sg(ah, ab, 3, 2)
    d1 = dist(p1, ch) * 0.6
    d2 = dist(p1, ch) * 0.9
    d3 = dist(p1, p3) * 0.8
    hag, had = coosCircle(ah, d1, 180+ori), coosCircle(ah, d1, ori)
    a1, a2 = coosCircle(pa, d2, 180+ori), coosCircle(pa, d2, ori)
    a3, a4 = coosCircle(pa, d3, 150+ori), coosCircle(pa, d3, 30+ori)
    lines = [ [had, hag], [a1, a2], [ah, ab], [pa, a3], [pa, a4] ]
    for a, b in lines: img.line(a, b, c, ep, l_t)
def dessine_kanji_encens(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    dessine_kanji_cereale(img, p1, p2, ct_sg(p1, p3), ct_sg(p2, p4), c, ep, ori, l_t)
    dessine_kanji_soleil(img, ct_sg(p1, p3), ct_sg(p2, p4), p3, p4, c, ep, ori, l_t)
def dessine_kanji_arbre(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ah, ab = ct_sg(p1, p2), ct_sg(p3, p4)
    pa = pt_sg(ah, ab, 3)
    d = dist(p1, ah) * 0.9
    d2 = dist(p1, p3) * 0.7
    a1, a2 = coosCircle(pa, d, 180+ori), coosCircle(pa, d, ori)
    a3, a4 = coosCircle(pa, d2, 110+ori), coosCircle(pa, d2, 70+ori)
    lines = [ [a1, a2], [ah, ab], [pa, a3], [pa, a4] ]
    for a, b in lines: img.line(a, b, c, ep, l_t)
def dessine_kanji_terre(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    a, b = 17, 2
    lines = [[pt_sg(cg, cd, a, b), pt_sg(cd, cg, a, b)], [pt_sg(ch, cb, a, b*2), cb], [p3, p4]]
    for a, b in lines: img.line(a, b, c, ep, l_t)
def dessine_kanji_cannellier(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    ct, cd = ct_cr(p1, p2, p3, p4), ct_sg(p2, p4)
    dessine_kanji_arbre(img, p1, ch, p3, cb, c, ep, ori, l_t)
    dessine_kanji_terre(img, ch, p2, ct, cd, c, ep, ori, l_t)
    dessine_kanji_terre(img, ct, cd, cb, p4, c, ep, ori, l_t)
def dessine_kanji_or(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    cg, cd = ct_sg(p1, p3), ct_sg(p2, p4)
    a = 20
    pcg, pcd = coosCircle(ch, dist(ch, p1), ori+180-a), coosCircle(ch, dist(ch, p1), ori+a)
    LINES = [[ch, pcg], [ch, pcd]]
    a, b = 5, 3
    clh, clb = coosCircle(ch, tailles_koma['O'][1]/2/5, 90+ori), cb
    ctl = ct_sg(clh, clb)
    pts = [clh, ctl, clb]
    dts = [dist(p1, ch)*i for i in [0.8, 0.7, 1]]
    for i in range(3): LINES.append([coosCircle(pts[i], dts[i], ori), coosCircle(pts[i], dts[i], ori+180)])
    LINES.append([clh, clb])
    pt1, pt2 = coosCircle(pts[1], dts[1], ori), coosCircle(pts[1], dts[1], ori+180)
    LINES += [[pt_sg(pt1, clb, a, b), pt_sg(pt1, clb, b, a)], [pt_sg(pt2, clb, a, b), pt_sg(pt2, clb, b, a)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_argent(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    dessine_kanji_or(img, p1, ct_sg(p1, p2), p3, ct_sg(p3, p4), c, ep, ori, l_t)
    d = dist(p1, p2)/10
    p1, p3 = coosCircle(ct_sg(p1, p2), d, ori), coosCircle(ct_sg(p3, p4), d, ori)
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    pt1, pt2 = ct_sg(cg, ct), pt_sg(cb, p4, 1, 4)
    LINES = [[p1, p3], [p1, p2], [p2, cd], [cg, cd], [ct_sg(p1, cg), ct_sg(p2, cd)], [pt1, pt2],
    [pt_sg(pt1, pt2), pt_sg(pt_sg(cd, ct, 2), p4, 2)], [p3, pt_sg(cb, ct, 3)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_promu(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    a, b = 3, 2
    pt = pt_sg(p1, p3, a, b)
    ctg, ctd = pt_sg(pt, pt_sg(ch, cb, a, b)), pt_sg(p2, p4, a, b)
    ptt = pt_sg(ctd, ctg, 4)
    d = dist(p1, p2)/4
    img.ellipse(pt, (dist(pt, ctg), dist(pt, p3)), c, ep, l_t, 0, 90, ori)
    img.ellipse(ptt, (dist(ptt, ct)*0.75, dist(ptt, p4)), c, ep, l_t, 90, 225, ori-20)
    peg = coosEllipse(pt, (dist(pt, ctg), dist(pt, p3)), 20, ori)
    pfeg = coosCircle(peg, d, ori)
    img.ellipse(peg, (dist(peg, pfeg), dist(peg, p3)*0.85), c, ep, l_t, 0, 100, ori)
    img.ellipse(ct, (dist(ct, cd)*0.7, dist(ct, cb)), c, ep, l_t, 30, 110, -20+ori)
    ctb = ct_sg(ct, cb)
    img.ellipse(ctb, (dist(ctb, cd), dist(ctb, ch)*0.9), c, ep, l_t, 315, 335, -20+ori)
    for a, b in [[ctg, ctd], [peg, pfeg]]: img.line(a, b, c, ep, l_t)
def dessine_kanji_diagonale(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    img.ellipse(p1, (dist(p1, ch)*0.8, dist(p1, ct_sg(ct_sg(p1, ch), cg))/2), c, ep, l_t, 0, 110, ori-20)
    img.ellipse(ct_sg(p1, cg), (dist(p1, ch)/4, dist(ct_sg(p1, cg), p3)), c, ep, l_t, 0, 90, ori)
    p = coosEllipse(p1, (dist(p1, ch)*0.8, dist(p1, ct_sg(ct_sg(p1, ch), cg))/2), 45-180, ori)
    d = dist(p1, p)
    a = angleInterPoints(p1, p)
    pt = coosCircle(p1, d, a-20)
    LINES = [[ct_sg(ct_sg(p1, ch), cg), ct_sg(p2, cd)], [ct_sg(p2, cd), p4], [p4, ct_sg(p4, cb)],
    [pt, pt_sg(ch, p2, 2)], [pt_sg(ch, p2, 2), ct_sg(ct_sg(ct_sg(p1, ch), cg), ct_sg(p2, cd))],
    [ct_sg(ct_sg(ct_sg(p1, ch), cg), ct_sg(p2, cd)), cb],
    [coosEllipse(ct_sg(p1, cg), (dist(p1, ch)/4, dist(ct_sg(p1, cg), p3)), 17, ori), pt_sg(ct_sg(p2, cd), p4, 3)],
    [coosEllipse(ct_sg(p1, cg), (dist(p1, ch)/4, dist(ct_sg(p1, cg), p3)), 35, ori), pt_sg(ct_sg(p2, cd), p4, 4, 5)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_volant(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    a, b = 2, 3
    an = -20
    pt = ct_sg(ch, cg)
    d = dist(p1, p2)/6
    LINES = [[p1, pt_sg(p2, ch, a, b)], [cg, pt_sg(cd, ct, a, b)], [ct_sg(ch, ct), cb], [pt, ct_sg(p3, cb)],
    [coosCircle(pt, d, an+ori), coosCircle(pt, d, an+180+ori)],
    [coosEllipse(p2, (dist(pt_sg(p2, ch, a, b), p2), dist(p2, cd)), 135, ori), p2],
    [ct_sg(coosEllipse(p2, (dist(pt_sg(p2, ch, a, b), p2), dist(p2, cd)), 135, ori), p2), ct_sg(p2, cd)],
    [coosEllipse(cd, (dist(pt_sg(cd, ct, a, b), cd), dist(cd, p4)), 135, ori), cd],
    [ct_sg(coosEllipse(cd, (dist(pt_sg(cd, ct, a, b), cd), dist(cd, p4)), 135, ori), cd), ct_sg(cd, p4)],]
    img.ellipse(p2, (dist(pt_sg(p2, ch, a, b), p2), dist(p2, cd)), c, ep, l_t, 90, 180, ori)
    img.ellipse(cd, (dist(pt_sg(cd, ct, a, b), cd), dist(cd, p4)), c, ep, l_t, 90, 180, ori)
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_marcheur(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    an = -20
    pt = ct_sg(cg, ct_sg(ch, ct))
    ptb = ct_sg(p1, ct_sg(ch, ct))
    d = dist(p1, p2)/6
    LINES = [[coosCircle(pt, d, an+ori), coosCircle(pt, d, an+180+ori)], [coosCircle(ptb, d, an+ori),
    coosCircle(ptb, d, an+180+ori)], [pt, ct_sg(p3, cb)], [pt_sg(ch, ct, 3), pt_sg(p2, cd, 3)],
    [pt_sg(ch, ct, 1, 2), pt_sg(p2, cd, 1, 2)], [pt_sg(pt_sg(ch, ct, 1, 2), pt_sg(p2, cd, 1, 2), 1, 2),
    pt_sg(cb, p4, 1, 2)], [pt_sg(cb, p4, 1, 2), pt_sg(p4, p3, 2)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_lune(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    a, b = 1, 2
    LINES = [[p1, p3], [p1, p2], [p2, p4], [p4, pt_sg(p4, cb, 2)], [pt_sg(p1, cg, a, b),
    pt_sg(p2, cd, a, b)], [pt_sg(p3, cg, a, b), pt_sg(p4, cd, a, b)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_debout(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    col = c
    a, b = 7, 2
    c, d = 7, 4
    cth = pt_sg(ch, ct, 3, 2)
    phg, phd = pt_sg(p1, cg, 3, 2), pt_sg(p2, cd, 3, 2)
    pbg, pbd = pt_sg(p3, cg, 3, 2), pt_sg(p4, cd, 3, 2)
    LINES = [[ch, cth], [phg, phd], [pbg, pbd], [pt_sg(phg, phd, a, b), pt_sg(pbg, pbd, c, d)],
    [pt_sg(phg, phd, b, a), pt_sg(pbg, pbd, d, c)]]
    for a, b in LINES: img.line(a, b, col, ep, l_t)
def dessine_kanji_brutal(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    col = c
    a, b = 3, 1
    c, d = 2, 1
    e, f = 3, 1
    g = 10
    LINES = [ [pt_sg(p1, cg, a, b), pt_sg(p2, cd, a, b)], [p1, pt_sg(cg, p1, c, d)], [pt_sg(cg, p1, c, d),
    pt_sg(cd, p2, c, d)], [pt_sg(cd, p2, c, d), cd], [cd, cg], [cg, p3], [p3, p4], [p4, pt_sg(p4, cd, 5)],
    [pt_sg(cg, p3, e, f), pt_sg(pt_sg(cd, p4, e, f), pt_sg(cg, p3, e, f), g)], [ct_sg(cg, p3), pt_sg(ct_sg(
    cd, p4), ct_sg(cg, p3), g)], [pt_sg(cg, p3, f, e), pt_sg(pt_sg(cd, p4, f, e), pt_sg(cg, p3, f, e), g)]]
    for a, b in LINES: img.line(a, b, col, ep, l_t)
def dessine_kanji_dragon_t(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    dessine_kanji_debout(img, p1, ch, cg, ct, c, ep, ori, l_t)
    dessine_kanji_lune(img, cg, ct, p3, cb, c, ep, ori, l_t)
    a,b = 4, 1
    dessine_kanji_brutal(img, pt_sg(ch, p2, a, b), p2, pt_sg(cb, p4, a, b), p4, c, ep, ori, l_t)
def dessine_kanji_dragon_s(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    dessine_kanji_debout(img, p1, p2, cg, cd, c, ep, ori, l_t)
    LINES = [[cg, pt_sg(p3, cg, 2)], [cg, cd], [cd, pt_sg(p4, cd, 2)], [pt_sg(cg, p3, 2), pt_sg(cd, p4, 2)],
    [pt_sg(p3, cg, 2), pt_sg(p4, cd, 2)], [ct, cb], [cb, p4], [p4, pt_sg(p4, cd, 4)]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_dragon(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2, option:int=0): ## DONE ##
    '''`option` must be `0` or `1` for Simplified or Trditional kanji form.'''
    if option==0:
        dessine_kanji_dragon_s(img, p1, p2, p3, p4, c, ep, ori, l_t)
    else:
        dessine_kanji_dragon_t(img, p1, p2, p3, p4, c, ep, ori, l_t)
def dessine_kanji_charriot(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb = ct_sg(p1, p2), ct_sg(p3, p4)
    pts = []
    LINES = []
    for i, y in enumerate(float_range(p1[1], p3[1], 6)):
        match i:
            case b if b in [i for i in range(2, 5)]:
                pt1, pt2 = [pt_sg(p1, ch, 5, 3)[0], y], [pt_sg(p2, ch, 5, 3)[0], y]
                LINES.append([pt1, pt2])
                pts.append([pt1, pt2])
            case a if a in [i for i in range(1, 6)]: img.line([p1[0], y], [p2[0], y], c, ep, l_t)
    LINES += [[pts[0][0], pts[-1][0]], [pts[0][1], pts[-1][1]], [ch, cb]]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_cheval(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    ptbd, pttbd = pt_sg(p4, pt_sg(cb, ct, 2), 2), pt_sg(p4, cd, 4.5)
    ptcg, ptcd = pt_sg(cg, ct, 2), pt_sg(cd, ct, 2)
    ptsh = [ptcg, pt_sg(ptcg, ptcd, 2), pt_sg(ptcd, ptcg, 2), ptcd]
    ptsb = [p3, pt_sg(p3, ptbd, 2), pt_sg(ptbd, p3, 2), ptbd]
    LINES = [ [p2, p1], [p1, cg], [cg, cd], [cd, pttbd], [pttbd, ptbd], [ch, ct], [pt_sg(p1, cg, 2),
    pt_sg(p2, cd, 2)], [pt_sg(cg, p1, 2), pt_sg(cd, p2, 2)]]
    a, b = 5, 2
    LINES += [[pt_sg(ptsh[i], ptsb[i], a, b), pt_sg(ptsh[i], ptsb[i], b, a)] for i in range(4)]
    for a, b in LINES: img.line(a, b, c, ep, l_t)
def dessine_kanji_general(img:image, p1, p2, p3, p4, c=COL.black, ep=1, ori=0, l_t=2): ## DONE ##
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    ct = ct_cr(p1, p2, p3, p4)
    img.ellipse(p2, (dist(p2, ch)*0.75, dist(p2, p4)), c, ep, l_t, 157, 172, ori)
    img.ellipse(p2, (dist(p2, ch)*1.25, dist(p2, p4)), c, ep, l_t, 157, 171, ori)
    img.ellipse(p2, (dist(p2, p1)*0.8, dist(p2, p4)), c, ep, l_t, 120, 140, ori)
    col = c
    a, b = 4, 1
    c, d = 4, 3
    vh, vb = pt_sg(p1, p2, a, b), pt_sg(p3, p4, a, b)
    cvh, cvb = pt_sg(vh, vb, c, d), pt_sg(vb, vh, c, d)
    cgh, cgb = pt_sg(p1, cg, c, d), pt_sg(p3, cg, c, d)
    LINES = [[vh, vb], [cvh, ct_sg(cvh, cgh)], [cvb, ct_sg(cvb, cgb)], [p2, ct_sg(ct_sg(vh, cvh), ch)],
    [ct_sg(p2, cd), pt_sg(pt_sg(ct_sg(ct_sg(vh, vb), ct), cd, 2, 5), ch, 2)], [ct_sg(ct_sg(vh, vb), ct), cd],
    [pt_sg(ct_sg(ct_sg(vh, vb), ct), cd, 2, 5), pt_sg(ct_sg(vb, cb), p4, 2, 5)], [pt_sg(ct_sg(vb, cb), p4,
    2, 5), pt_sg(ct_sg(vb, cb), p4, 3, 5)]]
    for a, b in LINES: img.line(a, b, col, ep, l_t)