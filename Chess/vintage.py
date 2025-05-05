from pyimager import *



class chess:
    gris = [30, 30, 30]
    def __init__(self) -> None:
        self.tourne = False
        self.trait = True
        self.epaisseur = 9
    def __str__(self) -> str:
        ...
    def image(self) -> None:
        ...

a = chess()
img = a.new_img().build()
while img.is_opened():
    img.show()

"""def new_img(self) -> image:
        trait = self.trait
        sz = 1
        img = new_img()
        M = min(img.size())
        ptt1 = [0, 0]
        ptt4 = [i+M for i in ptt1]
        ptt2 = ptt4[0], ptt1[1]
        ptt3 = ptt1[0], ptt4[1]
        cases = 8
        cf = 0.5
        cmb = 1 if trait or not self.tourne else -1
        marron = [157, 113, 83]
        case = round((ptt2[0] - ptt1[0]) / (cases+1))
        img.rectangle(ptt1, ptt4, marron, 0)
        x = 0.9 if trait or not self.tourne else 7.9
        y = 0.3
        for l in "ABCDEFGH":
            cv2.putText(img.img, l, (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, sz, COL.black, round(sz * 2.5))
            x += cmb
        x = 0.9 if trait or not self.tourne  else 7.9
        y = 8.875
        for l in "ABCDEFGH":
            cv2.putText(img.img, l, (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, sz, COL.black, round(sz * 2.5))
            x += cmb
        x = 0.125
        y = 1.05 if trait or not self.tourne else 8.05
        for l in "87654321":
            cv2.putText(img.img, l, (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, sz, COL.black, round(sz * 2.5))
            y += cmb
        x = 8.69
        y = 1.05 if trait or not self.tourne else 8.05
        for l in "87654321":
            cv2.putText(img.img, l, (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, sz, COL.black, round(sz * 2.5))
            y += cmb
        # Remplissage des coins de l'échequier.
        coins = [61, 61, 61]
        for p, c in [
                (ptt1, (round(ptt1[0] + case * cf), round(ptt1[1] + case * cf))),
                (ptt2, (round(ptt2[0] - case * cf), round(ptt2[1] + case * cf))),
                (ptt3, (round(ptt3[0] + case * cf), round(ptt3[1] - case * cf))),
                (ptt4, (round(ptt4[0] - case * cf), round(ptt4[1] - case * cf)))]:
            img.rectangle(p, c, coins, 0)
        # Délimitations des lignes sur les bords de l'échequier.
        a1 = ptt1
        for i in range(1, cases+2):
            i -= 0.5
            img.line((round(a1[0] + case * i), a1[1]), (round(a1[0] + case * i), ptt3[1]), self.gris, self.epaisseur)
            img.line((a1[0], round(a1[1] + case * i)), (ptt2[0], round(a1[1] + case * i)), self.gris, self.epaisseur)
        self.taiy_caz = case
        return img"""