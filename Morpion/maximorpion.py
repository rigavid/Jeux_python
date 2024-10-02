from tsanap import *
class endGame(Exception): ...
class mouse:
    click = False
    pos = [-1, -1]
    game = -1

def get_cases(pos) -> tuple:
    return ([int(i) for i in[(pos[0]-mmp.p1[0])/dist(mmp.p1,mmp.p2)*3,(pos[1]-mmp.p1[1])/dist(mmp.p1,mmp.p3)*3]] for n in [3, mmp.cases])

def get_mouse(event, x, y, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = [x,y]
        if clicked_in(pos, [mmp.p1, mmp.p4]):
            mouse.game = [int(i) for i in [(pos[0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*3, (pos[1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*3]]
            mouse.case = [int(i) for i in [(pos[0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*mmp.cases, (pos[1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*mmp.cases]]
    if event == cv2.EVENT_LBUTTONUP:
        pos = [x, y]
        if clicked_in(pos, [mmp.p1, mmp.p4]):
            game = [int(i) for i in [(pos[0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*3, (pos[1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*3]]
            case = [int(i) for i in [(pos[0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*mmp.cases, (pos[1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*mmp.cases]]
            if case == mouse.case: mouse.click = True


class mmp: ## Maximorpion (MMP)
    p1, p2 = [screen[0]/2-screen[1]/2, 0], [screen[0]/2+screen[1]/2, 0]
    p3, p4 = [screen[0]/2-screen[1]/2, screen[1]], [screen[0]/2+screen[1]/2, screen[1]]
    cases, fs = 9, False

    def __init__(self, name="MaxiMorpion") -> None:
        self.name = name; self.x, self.y = 9, 9
        self.matrix = np.array([[0 for _ in range(self.x)] for _ in range(self.y)])
        self.trait = True
        self.lastm = -1
        self.winner = -1
        self.wgames = [0, 0]
        self.ended = []

    def restart(self, trait=None) -> None:
        self.matrix = np.array([[0 for _ in range(self.x)] for _ in range(self.y)])
        self.trait = True if trait == None else trait
        self.lastm = -1
        self.ended = []
        self.winner = -1
        mouse.click = False
        mouse.pos = [-1, -1]
        mouse.game = -1

    def __str__(self) -> str:
        return "\n".join(" ".join(str(self.matrix[x,y]) for x in range(self.x)) for y in range(self.y))
    
    def image(self) -> image:
        self.finished()
        img = image(nom=self.name, img=image.new_img(fond=col.green, dimensions=screen))
        p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
        c = [0, 3, 6, 9]
        X = [p1[0]+(p4[0]-p1[0])/self.cases*n for n in range(self.cases)] + [p4[0]]
        Y = [p1[1]+(p4[1]-p1[1])/self.cases*n for n in range(self.cases)] + [p4[1]]
        for n, x in enumerate(X): img.ligne([x, p1[1]], [x, p4[1]], col.noir, 10 if n in c else 3, 2)
        for n, y in enumerate(Y): img.ligne([p1[0], y], [p4[0], y], col.noir, 10 if n in c else 3, 2)
        for x in range(9):
            for y in range(9):
                match self.matrix[x,y]:
                    case 0: continue
                    case 1:
                        ct = [moyenne(X[x], X[x+1]), moyenne(Y[y], Y[y+1])]
                        pts = [coosCercle(ct, dist([X[0],Y[0]],[X[1],Y[1]])*0.3, an+45) for an in range(0,360,90)]
                        img.ligne(pts[0], pts[2], col.bleu, 5, 2)
                        img.ligne(pts[1], pts[3], col.bleu, 5, 2)
                    case 2:
                        ct = [moyenne(X[x], X[x+1]), moyenne(Y[y], Y[y+1])]
                        img.cercle(ct, diff(X[0],X[1])*0.3, col.red, 5, 2)
        img.ecris(f"A {"X" if self.trait else "O"} de\njouer", ct_sg([0, 0], p3), col.blue if self.trait else col.red, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        img.ecris(f"X: {self.wgames[0]}\n", ct_sg(p2, screen), col.blue, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        img.ecris(f"\nO: {self.wgames[1]}", ct_sg(p2, screen), col.red,  3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        print(self.ended)
        for game in [[x, y] for x in range(3) for y in range(3)]:
            playable = [self.legal([game[0], game[1]], [game[0]*3+x_, game[1]*3+y_]) for x_ in range(3) for y_ in range(3)]
            print(f"{game} => {playable}")
            if True in playable:
                a, b = [X[game[0]*3], Y[game[1]*3]], [X[(game[0]+1)*3], Y[(game[1]+1)*3]]
                img.rectangle(a, b, col.red, 3, 2)
        for game in self.ended:
            a, b = [X[game[0]*3], Y[game[1]*3]], [X[game[0]*3+3], Y[game[1]*3+3]]
            ct = ct_sg(a, b)
            match self.winned(game):
                case 1:
                    pts = [coosCercle(ct, dist(a,b)*0.45, an+45) for an in range(0, 360, 90)]
                    img.ligne(pts[0], pts[2], col.blue, 15, 2)
                    img.ligne(pts[1], pts[3], col.blue, 15, 2)
                case 2:
                    img.cercle(ct, diff(a[0], b[0])*0.45, col.red, 15, 2)
        return img

    def winned(self, game) -> int | None:
        g = self.matrix[game[0]*3:game[0]*3+3, game[1]*3:game[1]*3+3]
        M = [g[0:3, n] for n in range(3)] + [g[n, 0:3] for n in range(3)]
        M += [[g[n, n] for n in range(3)],  [g[2-n, n] for n in range(3)]]
        for m in M:
            if not 0 in set(m) and len(set(m)) == 1:
                return m[0]
        return None

    def finished(self) -> None:
        N = [[x,y] for x in range(3) for y in range(3)]
        for n, game in enumerate([self.matrix[x:x+3, y:y+3] for x in range(0,9,3) for y in range(0,9,3)]):
            M = [game[0:3, n] for n in range(3)] + [game[n, 0:3] for n in range(3)]
            M += [[game[n, n] for n in range(3)],  [game[2-n, n] for n in range(3)]]
            for m in M:
                if not 0 in set(m) and len(set(m)) == 1:
                    if mouse.game not in self.ended:
                        if N[n]==mouse.game:
                            self.ended.append(mouse.game)

    def playable(self) -> bool:
        if not 0 in self.matrix and len(self.ended) <= 9:
            return False
        return True

    def legal(self, game, case) -> bool:
        r = False
        if self.lastm in self.ended: r = True
        if game in self.ended: return False
        if self.lastm in [-1, game] or r:
            if self.matrix[case[0],case[1]] == 0:
                return True
        return False

    def game(self) -> None:
        img = self.image()
        img.montre(1, fullscreen=mmp.fs)
        cv2.setMouseCallback(img.nom, get_mouse)
        while self.playable():
            if mouse.click:
                if self.legal(mouse.game, mouse.case):
                    self.matrix[mouse.case[0], mouse.case[1]] = 1 if self.trait else 2
                    self.lastm = [i%3 for i in mouse.case]
                    self.trait = not self.trait
                    img = self.image()
                mouse.click = False
            wk = img.montre(1, fullscreen=mmp.fs)
            if img.is_closed(): raise endGame
            match wk:
                case 27: raise endGame
                case 32 | 8: mmp.fs = not mmp.fs
                case 114: return self.restart(True)
                case -1: ...
                case 65470: cv2.moveWindow(img.nom, 0, 0) ## f1
                case 65471: cv2.moveWindow(img.nom, screen[0], 0) ## f2
        img = self.image()
        img.ecris(f"{"J1" if self.winner == 1 else "J2"} won!", ct_sg(mmp.p1, mmp.p4), col.red, 12, 3, lineType=2)
        img.ecris(f"{"J1" if self.winner == 1 else "J2"} won!", ct_sg(mmp.p1, mmp.p4), col.black, 5, 3, lineType=2)
        while True:
            wk = img.montre(1, fullscreen=mmp.fs)
            if img.is_closed(): raise endGame
            match wk:
                case 27: raise endGame
                case 32 | 8: mmp.fs = not mmp.fs
                case -1: ...
                case _: return self.restart()

    def start(self) -> None:
        while True: 
            try: self.game()
            except endGame: return

def main():
    jeu = mmp()
    jeu.start()
    

if __name__ == "__main__":
    main()