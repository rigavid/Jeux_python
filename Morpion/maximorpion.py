from tsanap import *

matrix = [[0 for _ in range(9)] for _ in range(9)]

class mmp: ## Maximorpion (MMP)
    p1, p2 = [screen[0]/2-screen[1]/2, 0], [screen[0]/2+screen[1]/2, 0]
    p3, p4 = [screen[0]/2-screen[1]/2, screen[1]], [screen[0]/2+screen[1]/2, screen[1]]
    cases = 9
    def __init__(self, name="MaxiMorpion") -> None:
        self.name = name; self.x, self.y = 9, 9
        self.matrix = np.array([[0 for _ in range(self.x)] for _ in range(self.y)])
        self.trait = True
        self.lastm = -1
    def __str__(self) -> str:
        return "\n".join(" ".join(str(self.matrix[x,y]) for x in range(self.x)) for y in range(self.y))
    def image(self) -> image:
        img = image(nom=self.name, img=image.new_img(fond=col.green, dimensions=screen))
        p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
        c = [0, 3, 6, 9]
        X = [p1[0]+(p4[0]-p1[0])/self.cases*n for n in range(self.cases)] + [p4[0]]
        Y = [p1[1]+(p4[1]-p1[1])/self.cases*n for n in range(self.cases)] + [p4[1]]
        for n, x in enumerate(X): img.ligne([x, p1[1]], [x, p4[1]], col.noir, 10 if n in c else 3, 2)
        for n, y in enumerate(Y): img.ligne([p1[0], y], [p4[0], y], col.noir, 10 if n in c else 3, 2)
        for x in range(9):
            for y in range(9):
                c = self.matrix[x,y]
                if c==0: continue
                img.ecris("X" if c==1 else "O", [moyenne(X[x], X[x+1]), moyenne(Y[y], Y[y+1])], col.blue)
        return img
    def legal(self, game, case) -> bool:
        if self.lastm in [-1, game]:
            if self.matrix[case[0],case[1]] == 0:
                return True
        return False
    def start(self) -> bool | None:
        fs = False
        while True:
            img = self.image()
            img.montre(1, fullscreen=fs)
            cv2.setMouseCallback(img.nom, get_mouse)
            while True:
                if mouse.click:
                    if self.legal(mouse.game, mouse.case):
                        self.matrix[mouse.case[0], mouse.case[1]] = 1 if self.trait else 2
                        self.lastm = mouse.game
                    mouse.click = False
                wk = img.montre(1, fullscreen=fs)
                if img.is_closed(): return
                match wk:
                    case 27: return
                    case 32: fs = not fs
                    case -1: ...
                    case _: ...


class mouse:
    click = False
    pos = [0, 0]

def get_mouse(event, x, y, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = [x,y]
        if clicked_in(pos, [mmp.p1, mmp.p4]):
            mouse.click = True
            mouse.pos = pos
            mouse.game = [int(i) for i in [(pos[0]-p1[0])/dist(p1, p2)*3, (pos[1]-p1[1])/dist(p1, p3)*3]]
            mouse.case = [int(i) for i in [(pos[0]-p1[0])/dist(p1, p2)*mmp.cases, (pos[1]-p1[1])/dist(p1, p3)*mmp.cases]]

def main():
    jeu = mmp()
    jeu.start()
    

if __name__ == "__main__":
    main()