from pyimager import *

def ran(*args): return range(*(round(i) for i in args))

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
    def move(self):
        ...
    def image(self) -> image:
        img = new_img()
        M = min(img.size())
        p1 = [(img.size()[0]-M)/2, (img.size()[1]-M)/2]
        p4 = [i+M for i in p1]
        img.rectangle(p1, p4, COL.brown, 0) ## TODO Change color
        ## Draw the countours of the board
        a = 15; p1, p4 = pt_sg(p1, p4, a), pt_sg(p4, p1, a)
        dx, dy = diff(p1[0], p4[0])/8, diff(p1[1], p4[1])/8
        for X, x in enumerate(ran(p1[0], p4[0], dx)):
            for Y, y in enumerate(ran(p1[1], p4[1], dy)):
                a, b = [x, y], [x+dx, y+dy]
                img.rectangle(a, b, COL.white if X%2==Y%2 else COL.black, 0)
                img.text(self.m[Y, X][0], ct_sg(a, b), COL.red, 3, 10)
        self.img.img = img.img
    def start(self):
        while self.play:
            self.move()
            if self.end_game():
                if not self.replay_q():
                    return

a = chess()
a.image()
a.img.build()
while a.img.is_opened():
    a.img.show()