try: from Outils.cvt import *
except: from Asteroids.Outils.cvt import *
def flatten(L) -> list:
    o = []
    for l in L: o += l
    return o
def multi_shoot(img, ct, size=1):
    b = [p+25*size for p in ct]
    a = [p-25*size for p in ct]
    rectangle(img, a, b, noir, 2)
    pto = coosCercle(ct, size*20, 135)
    pts = flatten([[coosCercle(pto, n*17*size, a) for a in [-65, -45, -25]] for n in range(1, 3)])
    for pt in pts+[pto]: cercle(img, pt, 1, rouge)
    return img
def raffale(img, ct, size=1):
    b = [p+25*size for p in ct]
    a = [p-25*size for p in ct]
    rectangle(img, a, b, noir, 2)
    pto = coosCercle(ct, size*23, 135)
    pts = [coosCercle(pto, n*12*size, -45) for n in range(1, 5)]
    for pt in pts+[pto]: cercle(img, pt, 1, rouge)
    return img
def retro_fusee(img, ct, size=1):
    b = [p+25*size for p in ct]
    a = [p-25*size for p in ct]
    rectangle(img, a, b, noir, 2)
    pto = coosCercle(ct, size*23, 135+180)
    pta, ptb = [coosCercle(pto, 17*size, a+180) for a in [-63, -27]]
    triangle(img, pto, pta, ptb, rouge, 0)
    pto = coosCercle(ct, size*23, 135)
    pta, ptb = [coosCercle(pto, 17*size, a) for a in [-63, -27]]
    triangle(img, pto, pta, ptb, rouge, 0)
    cercle(img, ct, 9, bleu, 0)
    return img
def stabilisateur(img, ct, size=1):
    b = [p+25*size for p in ct]
    a = [p-25*size for p in ct]
    rectangle(img, a, b, noir, 2)
    cercle(img, ct, 7*size, bleu, 0)
    cercle(img, ct, 15*size, vert, 1)
    return img

if __name__ == '__main__':montre(retro_fusee(image(), ct, 1))