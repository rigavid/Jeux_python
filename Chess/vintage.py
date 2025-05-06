from pyimager import *



class chess:
    gris = [30, 30, 30]
    def __init__(self, name="PyChess") -> None:
        self.name = name
        self.trait = True
        self.epaisseur = 5
        self.img = self.new_img()
    def __str__(self) -> str:
        ...
    def image(self) -> None:
        ...

    def new_img(self) -> image:
        img = new_img(name=self.name)
        M = min(img.size())
        sz, lt, ft, col, ep = 1.5, lineTypes[2], cv2.FONT_HERSHEY_TRIPLEX, self.gris, self.epaisseur*M//1080
        sz *= M/1080
        ptt1 = [0, 0]
        ptt4 = [i+M for i in ptt1]
        ptt2, ptt3 = (ptt4[0], ptt1[1]), (ptt1[0], ptt4[1])
        d = dist(ptt2, ptt1) / 9
        img.rectangle(ptt1, ptt4, [157, 113, 83], 0)
        for n in range(8):
            L, N = "ABCDEFGH"[n], "87654321"[n]
            x, y = round(ptt1[0] + d * (0.9+n)), round(ptt1[1] + d * (1.1+n))
            cv2.putText(img.img, L, (x, round(ptt1[1] + d * 0.375)), ft, sz, COL.black, ep//4, lt)
            cv2.putText(img.img, L, (x, round(ptt1[1] + d * 8.875)), ft, sz, COL.black, ep//4, lt)
            cv2.putText(img.img, N, (round(ptt1[0] + d * 8.625), y), ft, sz, COL.black, ep//4, lt)
            cv2.putText(img.img, N, (round(ptt1[0] + d * 0.125), y), ft, sz, COL.black, ep//4, lt)
        # Remplissage des coins de l'échequier.
        for p, c in [
                (ptt1, (ptt1[0]+d/2, ptt1[1]+d/2)), (ptt2, (ptt2[0]-d/2, ptt2[1]+d/2)),
                (ptt3, (ptt3[0]+d/2, ptt3[1]-d/2)), (ptt4, (ptt4[0]-d/2, ptt4[1]-d/2))
            ]: img.rectangle(p, c, COL.new("3d3d3d"), 0)
        # Délimitations des lignes sur les bords de l'échequier.
        for i in range(9):
            i += 0.5
            img.line((round(ptt1[0]+d*i),ptt1[1]), (round(ptt1[0]+d*i),ptt3[1]), col, ep)
            img.line((ptt1[0],round(ptt1[1]+d*i)), (ptt2[0],round(ptt1[1]+d*i)), col, ep)
        img.rectangle(ptt1, ptt4, col, ep)
        self.cases = [[[(d*(x+0.5), d*(y+0.5)), (d*(x+1.5), d*(y+1.5))] for x in range(8)] for y in range(8)]
        return img

a = chess()
img = a.new_img().build()
while img.is_opened():
    img.show()