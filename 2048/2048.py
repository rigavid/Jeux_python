from tsanap import *

lt = 2
beige = col.new("#D2B48C")
class s:
    size = [4, 4]
    offset = 100
    font = cv2.FONT_HERSHEY_COMPLEX

class res:
    resols = [copy.deepcopy(screen), [1680, 1050]]
    resind = 0
    res = resols[resind]

def score(t) -> int:
    return sum(t[x][y] for x in range(len(t)) for y in range(len(t[x])))

def change_res() -> None:
    res.resind += 1
    res.resind = res.resind%len(res.resols)
    res.res = res.resols[res.resind]

def getTabl() -> list: ## [Y,X] et non pas [X,Y]
    tabl = [[0 for _ in range(s.size[0])] for _ in range(s.size[1])]
    tabl[0][0] = 2; tabl[-1][-1] = 2
    return tabl
def down(t) -> bool:
    a=copy.deepcopy(t)
    for x, c in enumerate(t):
        cl = [i for i in c if i]
        if len(set(cl)) == len(cl):
            t[x] = [0 for _ in range(len(c)-len(cl))] + cl
            continue
        lst = 0
        cl_ = []
        for caz in cl[::-1]:
            if caz==lst:
                cl_[-1] *= 2
                lst = 0
            else:
                cl_.append(caz)
                lst = caz
        t[x] = [0 for _ in range(len(c)-len(cl_))] + cl_[::-1]
    return True

def add_new(t) -> bool:
    c = [[x,y] for y, row in enumerate(t) for x, case in enumerate(row) if case==0]
    if len(c) == 0: return False
    p = rd.choice(c)
    t[p[1]][p[0]]=rd.choice([2,4])
    return True

cols = {'2':'ede5da', '4':'ebe1c8', '8':'f2b177', '16':'eb8e53', '32':'f57c5f', '64':'e95937', '128':'f3d96b', '256':'f1d04b', '512':'e4c02a', '1024':'f7d639', '2048':'ecc400', '4096':'f0a0a0'}
for c in cols: cols[c] = col.new(cols[c])
keys = [65363, 65361, 65362, 65364]

def img2048(t) -> image:
    img = image("2048", img=image.new_img(dimensions=res.res, fond=col.cyan))
    texte(f"Score: {s.score}", [res.res[0]/2, s.offset], 4, 2).ecris(img)
    p1, p2 = [(res.res[0]-res.res[1])/2+s.offset, s.offset*1.5], [(res.res[0]-res.res[1])/2+res.res[1]-s.offset, s.offset*1.5]
    p3, p4 = [p1[0], res.res[1]-s.offset/2], [p2[0], res.res[1]-s.offset/2]
    img.rectangle(p1, p4, beige, 0, lt) ## Dessin du plateau
    x_, y_ = diff(p1[0], p2[0]), diff(p1[1], p3[1]) ## Grandeur des cases
    for x in range(len(t)): ## Dessin des cases et des pièces
        for y in range(len(t[x])):
            pt1 = [p1[0]+x_/len(t)*x, p1[1]+y_/len(t[x])*y]
            pt2 = [p1[0]+x_/len(t)*(x+1), p1[1]+y_/len(t[x])*(y+1)]
            img.rectangle(pt1, pt2, [i-20 for i in beige], 3, lt)
            if t[x][y] != 0:
                a,b=[i+20 for i in pt1],[i-20 for i in pt2]
                try: c, c2 = cols[str(t[x][y])], col.black
                except: c, c2 = col.black, col.white
                img.rectangle(a,b, c, 0, lt)
                img.ecris(t[x][y], ct_sg(a,b), c2, 2/200*dist(a,b), 1/200*dist(a,b), s.font)
    return img

class texte:
    def __init__(self, text, pos, taille=1, ep=1) -> None:
        self.text = text
        self.pos = pos
        self.t = taille
        self.ep = ep
    def ecris(self, img) -> image:
        p, e = self.pos, self.ep
        img.ecris(self.text, [p[0]+e*2, p[1]-e], col.black, e*5, self.t, s.font, lt)
        img.ecris(self.text, p, col.red, e, self.t, s.font, lt)
        return image

def transpose(t) -> list:
    t = [[t[y][x] for y in range(len(t[x]))] for x in range(len(t))]
    return t

def move(t, sens) -> list:
    match sens:
        case 0: moved = down(t)
        case 1:
            t = [x[::-1] for x in transpose(t)]
            moved = down(t)
            t = transpose([x[::-1] for x in t])
        case 2:
            t = [i[::-1] for i in t[::-1]]
            moved = down(t)
            t = [i[::-1] for i in t[::-1]]
        case 3:
            t = [x for x in transpose(t)[::-1]]
            moved = down(t)
            t = transpose([x for x in t[::-1]])
    return t, moved

def gam_o(t) -> bool:
    return [move(copy.deepcopy(t), n)[0] for n in range(4)].count(t) == 4

def go_img(t) -> image:
    img = img2048(t)
    texte("Game over", [res.res[0]/2, res.res[1]/2.75], 5, 3).ecris(img)
    texte("f3 to restart", [res.res[0]/2, res.res[1]/1.75], 2.5, 3).ecris(img)
    texte(f"{s.size[0]}x{s.size[1]}", [res.res[0]/2, res.res[1]/1.375], 1.75, 3).ecris(img)
    return img

def main():
    fs = False
    r = False
    while True:
        t = getTabl()
        breyk = False
        s.score = 0
        while True:
            s.score = score(t)
            img = img2048(t)
            while True: ## Get a key with WaitKey (wk)
                wk = img.montre(1, fullscreen=fs)
                if r and wk not in [27, 114, 8, 32, 102, 65470, 65471]:
                    wk = 116
                match wk:
                    case 27: return
                    case 8|102: fs = not fs
                    case 32:
                        change_res()
                        img = img2048(t)
                    case 114: r = not r
                    case 101: ## <e>
                        breyk = True
                        break
                    case 65470: cv2.moveWindow(img.nom, 0, 0) ## F1
                    case 65471: cv2.moveWindow(img.nom, 1920, 0) ## F2
                    case 116: wk = rd.choice(keys); break
                    case a if a in keys: break
                if img.is_closed(): return
            if breyk: break
            sens = [3, 1, 2, 0][keys.index(wk)]
            moved = False
            comp = copy.deepcopy(t)
            t, moved = move(t, sens)
            if not moved: break
            if comp!=t:
                if not add_new(t): break
            if gam_o(t): break
        img = go_img(t)
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): return
            match wk:
                case 27: return
                case 8|102: fs = not fs
                case 32:
                    change_res()
                    img = go_img(t)
                case 65470: cv2.moveWindow(img.nom, 0, 0) ## F1
                case 65471: cv2.moveWindow(img.nom, 1920, 0) ## F2
                case 65472: break ## F3
                case 65473: s.size = [max(i-1, 3) for i in s.size]; img = go_img(t) ## F4
                case 65474: s.size = [min(i+1, 9) for i in s.size]; img = go_img(t) ## F5
main()