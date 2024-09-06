from tsanap import *

tabl = [[0 for _ in range(4)] for _ in range(4)]
tabl[0][0] = 2; tabl[-1][-1] = 2
lt = 2

def add_new(t) -> bool:
    c = []
    for x, row in enumerate(t):
        for y, case in enumerate(row):
            if case == 0:
                c.append([x,y])
    if len(c) == 0: return False
    p = rd.choice(c)
    t[p[0]][p[1]] = rd.choice([2,4])
    return True

cols = []

def img2048(t) -> image:
    img = image("2048", img=image.new_img(fond=col.cyan))
    p1, p2 = [(screen[0]-screen[1])/2, 0], [(screen[0]-screen[1])/2+screen[1], 0]
    p3, p4 = [p1[0], screen[1]], [p2[0], screen[1]]
    img.rectangle(p1, p4, col.new("#D2B48C"), 0, lt)
    x_, y_ = diff(p1[0], p2[0]), diff(p1[1], p3[1])
    for x in range(len(t)):
        for y in range(len(t[x])):
            pt1 = [p1[0]+x_/len(t)*x, p1[1]+y_/len(t[x])*y]
            pt2 = [p1[0]+x_/len(t)*(x+1), p1[1]+y_/len(t[x])*(y+1)]
            img.rectangle(pt1, pt2, [i-20 for i in col.new("#D2B48C")], 3, lt)
            if t[x][y] != 0:
                a,b=[i+20 for i in pt1],[i-20 for i in pt2]
                img.ecris(t[x][y], ct_sg(a,b), col.white, 3, 2, cv2.FONT_HERSHEY_SIMPLEX)
                img.rectangle(a,b
                )
            

    return img

def main():
    while True:
        img = img2048(tabl)
        while True:
            match img.montre(1, fullscreen=True):
                case 27: return
            if img.is_closed(): return
        if not add_new(tabl): break

main()