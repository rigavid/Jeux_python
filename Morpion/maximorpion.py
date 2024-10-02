from tsanap import *
class endGame(Exception): ...
class mouse: click, pos, game, case = False, [-1, -1], -1, None
def get_case(pos) -> list: return [int(i) for i in [(pos[0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*mmp.cases, (pos[1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*mmp.cases]]
def get_mouse(event, x, y, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN and clicked_in([x, y], [mmp.p1, mmp.p4]): mouse.case, mouse.game = get_case([x, y]), [int(i) for i in [([x, y][0]-mmp.p1[0])/dist(mmp.p1, mmp.p2)*3, ([x, y][1]-mmp.p1[1])/dist(mmp.p1, mmp.p3)*3]]
    elif event == cv2.EVENT_LBUTTONUP and clicked_in([x, y], [mmp.p1, mmp.p4]) and get_case([x, y]) == mouse.case: mouse.click = True
class mmp:
    p1, p2, p3, p4 = [screen[0]/2-screen[1]/2, 0], [screen[0]/2+screen[1]/2, 0], [screen[0]/2-screen[1]/2, screen[1]], [screen[0]/2+screen[1]/2, screen[1]]
    cases, fs = 9, False
    def __init__(self, name="MaxiMorpion") -> None:
        self.name, self.x, self.y, self.wgames, self.pgames = name, 9, 9, [0, 0], 0
        self.matrix = np.array([[0 for _ in range(self.x)] for _ in range(self.y)])
        self.shifumi, self.ended, self.trait = False, [], True; self.winner = self.lastm = -1
    def restart(self) -> None:
        self.matrix = np.array([[0 for _ in range(self.x)] for _ in range(self.y)])
        self.shifumi, self.ended, self.trait = False, [], self.pgames%2==0; self.winner = self.lastm = -1
        mouse.game, mouse.click, mouse.pos = -1, False, [-1, -1]; self.pgames += 1
    def __str__(self) -> str: return "\n".join(" ".join(str(self.matrix[x, y]) for x in range(self.x)) for y in range(self.y))
    def image(self) -> image:
        img = image(nom=self.name, img=image.new_img(fond=col.green, dimensions=screen))
        p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
        X, Y = ([p1[i]+(p4[i]-p1[i])/self.cases*n for n in range(self.cases)] + [p4[i]] for i in (0, 1))
        for n, x in enumerate(X): img.ligne([x, p1[1]], [x, p4[1]], col.noir, 10 if n in range(0, 10, 3) else 3, 2)
        for n, y in enumerate(Y): img.ligne([p1[0], y], [p4[0], y], col.noir, 10 if n in range(0, 10, 3) else 3, 2)
        for x in range(9):
            for y in range(9):
                match self.matrix[x, y]:
                    case 1:
                        for a, b in [[coosCercle([moyenne(X[x], X[x+1]), moyenne(Y[y], Y[y+1])], dist([X[0], Y[0]], [X[1], Y[1]])*0.3, an+45+i) for an in (0, 180)] for i in (0, 90)]: img.ligne(a, b, col.bleu, 5, 2)
                    case 2: img.cercle([moyenne(X[x], X[x+1]), moyenne(Y[y], Y[y+1])], diff(X[0], X[1])*0.3, col.red, 5, 2)
        img.ecris(f"A {"X" if self.trait else "O"} de\njouer", ct_sg([0, 0], p3), col.blue if self.trait else col.red, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        for s, c in [[f"X: {self.wgames[0]}\n", col.blue], [f"\nO: {self.wgames[1]}", col.red]]: img.ecris(s, ct_sg(p2, screen), c, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        for game in [[x, y] for x in range(3) for y in range(3)]:
            playable = [self.legal([game[0], game[1]], [game[0]*3+x_, game[1]*3+y_]) for x_ in range(3) for y_ in range(3)]
            if True in playable: img.rectangle([i+3 for i in [X[game[0]*3], Y[game[1]*3]]], [i-3 for i in [X[(game[0]+1)*3], Y[(game[1]+1)*3]]], col.red, 3, 2)
            elif game==self.lastm and self.winner==-1:
                for c, t in [[col.red, 16], [col.noir, 8]]: img.ecris("Shi-fu-mi !", ct_sg(mmp.p1, mmp.p4), c, t, 3, lineType=2)
                self.shifumi = True
        for game in self.ended:
            a, b = [X[game[0]*3], Y[game[1]*3]], [X[game[0]*3+3], Y[game[1]*3+3]]
            match self.winned(game):
                case 1:
                    for a, b in [[coosCercle(ct_sg(a, b), dist(a, b)*0.45, an+45+i) for an in (0, 180)] for i in [0, 90]]: img.ligne(a, b, col.blue, 15, 2)
                case 2: img.cercle(ct_sg(a, b), diff(a[0], b[0])*0.45, col.red, 15, 2)
        return img
    def winned(self, game) -> int | None:
        g = self.matrix[game[0]*3:game[0]*3+3, game[1]*3:game[1]*3+3]
        for m in [g[0:3, n] for n in range(3)] + [g[n, 0:3] for n in range(3)] + [[g[n, n] for n in range(3)], [g[2-n, n] for n in range(3)]]:
            if not 0 in set(m) and len(set(m)) == 1: return m[0]
        return None
    def finished(self) -> None:
        games = np.array([[0 for _ in range(3)] for _ in range(3)])
        N = [[x, y] for x in range(3) for y in range(3)]
        for n, game in enumerate([self.matrix[x:x+3, y:y+3] for x in range(0, 9, 3) for y in range(0, 9, 3)]):
            M = [game[0:3, n] for n in range(3)] + [game[n, 0:3] for n in range(3)] + [[game[n, n] for n in range(3)], [game[2-n, n] for n in range(3)]]
            for m in M:
                if not 0 in m and len(set(m)) == 1:
                    games[N[n][0], N[n][1]] = m[0]
                    if mouse.game not in self.ended and N[n]==mouse.game: self.ended.append(mouse.game)
        for m in [games[0:3, n] for n in range(3)] + [games[n, 0:3] for n in range(3)] + [[games[n, n] for n in range(3)], [games[2-n, n] for n in range(3)]]:
            if not 0 in m and len(set(m)) == 1:
                self.winner = m[0]
                self.wgames[m[0]-1] += 1
                return
    def playable(self) -> bool: return not (not 0 in self.matrix and len(self.ended) <= 9 or self.winner != -1)
    def legal(self, game, case) -> bool: return self.lastm in [-1, game] and self.matrix[case[0], case[1]] == 0 and not game in self.ended
    def game(self) -> None:
        img = self.image(); img.montre(1, fullscreen=mmp.fs); cv2.setMouseCallback(img.nom, get_mouse)
        while self.playable():
            if mouse.click:
                if self.legal(mouse.game, mouse.case):
                    self.matrix[mouse.case[0], mouse.case[1]] = 1 if self.trait else 2
                    self.lastm, self.trait = [i%3 for i in mouse.case], not self.trait
                    self.finished(); img = self.image()
                mouse.click = False
            if img.is_closed(): raise endGame
            match img.montre(1, fullscreen=mmp.fs):
                case 27: raise endGame
                case 32|8: mmp.fs = not mmp.fs
                case 114: return self.restart()
                case 115:
                    if self.shifumi: self.lastm = -1; img = self.image()
                case 65470: cv2.moveWindow(img.nom, 0, 0) #f1
                case 65471: cv2.moveWindow(img.nom, screen[0], 0) #f2
        img = self.image()
        for c, t in[[col.red, 12], [col.black, 5]]:img.ecris(f"{"J1"if self.winner==1 else"J2"} won!", ct_sg(mmp.p1, mmp.p4), c, t, 3, lineType=2)
        while True:
            if img.is_closed():raise endGame
            match img.montre(1, fullscreen=mmp.fs):
                case 27:raise endGame
                case 32|8:mmp.fs=not mmp.fs
                case -1:...
                case _:return self.restart()
    def st(self)->None:
        while True:self.game()
    def start(self)->None:
        try:self.st()
        except endGame:return
if __name__ == "__main__": mmp().start()