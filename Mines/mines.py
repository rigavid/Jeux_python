from tsanap import *

class flags:
    list = []
    mines = -1
class res:
    resols = [copy.deepcopy(screen), [1680, 1050]]
    resind = 0; res = resols[resind]
def change_res() -> None:
    res.resind = (res.resind+1)%len(res.resols)
    res.res = res.resols[res.resind]

class mouse:
    click = False
    pos = [-1,-1]

class GAMEOVER(Exception):
    ...

nf = "Mines"; lt = 2
grisclair = col.new("#D3D3D3")
grisfonce = col.new("#A9A9A9")
cols = [col.black, col.blue, col.green, col.yellow, col.new("#800080"), col.red, col.new("#a00000"), col.new("#ff8000"), col.new("#808080")]

class pts: ...

def mouse_get_case(event,x,y,flags,params)->None:
    if event==cv2.EVENT_LBUTTONDOWN:
        mouse.click = True
        mouse.pos = [x,y]
        mouse.type = True
    elif event==cv2.EVENT_MBUTTONDOWN:
        mouse.click = True
        mouse.pos = [x,y]
        mouse.type = False

def uncover(map, case) -> list:
    map[case[0]][case[1]] = int(map[case[0]][case[1]])
    c=map[case[0]][case[1]]
    if c == 0:
        for x,y in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
            x += case[0]; y += case[1]
            if x<0 or y<0: continue
            try:
                if type(map[x][y]) == str:
                    map = uncover(map, [x,y])
            except: ...
    elif c == -1:
        raise GAMEOVER
    return map

def count_a(map, pos):
    if int(map[pos[0]][pos[1]]) == -1: return -1
    r = []
    for x,y in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
        a, b = pos[0]+x, pos[1]+y
        if a<0 or b<0: continue
        try: r.append(int(map[a][b]))
        except: pass
    return r.count(-1)

def get_lev(size=[10, 10], mines=10) -> list:
    flags.mines = mines
    l = ['0' for y in range(size[1]) for x in range(size[0])]
    l[0:mines:] = ['-1' for _ in range(mines)]
    rd.shuffle(l)
    o = []
    for y in range(size[1]): o.append(l[size[0]*y:size[0]*(y+1)])
    for x in range(size[0]):
        for y in range(size[1]):
            o[x][y] = str(count_a(o, [x, y]))
    return o

def img_mines(map) -> image:
    offset = 20
    img = image(nf, img=image.new_img(dimensions=res.res, fond=col.cyan))
    p1, p2 = [(res.res[0]-res.res[1])/2+offset, offset], [res.res[0]-((res.res[0]-res.res[1])/2), offset]
    p3, p4 = [p1[0], res.res[1]-offset], [p2[0], res.res[1]-offset]
    img.rectangle(p1, p4, col.blanc, 0, lt)
    img.rectangle(p1, p4, grisfonce, 3, lt)
    x_, y_ = dist(p1, p2), dist(p1, p3)
    for x in range(len(map)):
        for y in range(len(map[x])):
            pt1 = [p1[0]+x_/len(map)*x, p1[1]+y_/len(map[x])*y]
            pt2 = [p1[0]+x_/len(map)*(x+1), p1[1]+y_/len(map[x])*(y+1)]
            p = map[x][y]
            if type(p) == str:
                img.rectangle(pt1, pt2, grisclair, 0, lt)
                if [x,y] in flags.list:
                    img.ligne(pt1, pt2, col.red, 3, lt)
            else:
                if p != 0:
                    img.ecris(p, ct_sg(pt1, pt2), cols[p], 2)
            img.rectangle(pt1, pt2, grisfonce, 3, lt)
    pts.p1, pts.p2 = p1, p4
    pts.x_, pts.y_ = x_, y_
    return img

def ended(map) -> bool:
    a = len(map[0])*len(map[1])-flags.mines
    b = sum(1 for x in range(len(map)) for y in range(len(map[x])) if type(map[x][y]) != str)
    return (b - a) == 0 and len(flags.list) == flags.mines

def main():
    map = get_lev()
    img = img_mines(map)
    fs = False
    img.montre(1, fullscreen=fs)
    cv2.setMouseCallback(nf, mouse_get_case)
    while True:
        wk = img.montre(1, fullscreen=fs)
        match wk:
            case 27: return img
            case 8|102: fs = not fs
            case 32: change_res(); img = img_mines(map)
            case 114: r = not r
            case 101: breyk = True; break ## <e>
            case 65470: cv2.moveWindow(img.nom, 0, 0) ## F1
            case 65471: cv2.moveWindow(img.nom, 1920, 0) ## F2
            case 116: wk = rd.choice(keys); break
        if mouse.click:
            mouse.click = False
            pos = mouse.pos
            p1, p4 = pts.p1, pts.p2
            x_, y_ = pts.x_, pts.y_
            if clicked_in(pos, [p1, p4]):
                pt = [pos[i]-p1[i] for i in (0, 1)]
                case = [int(i) for i in [pt[0]/x_*len(map), pt[1]/y_*len(map[0])]]
                if mouse.type:
                    if not case in flags.list:
                        try: map = uncover(map, case)
                        except GAMEOVER:
                            break
                else:
                    if type(map[case[0]][case[1]]) == str:
                        if case in flags.list: flags.list.remove(case)
                        else: flags.list.append(case)
                img = img_mines(map)
        if ended(map):
            print("You won !")
            break

main()