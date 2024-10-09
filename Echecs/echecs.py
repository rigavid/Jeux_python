from tsanap import *

class mouse:
    click = False
    pos = [-1, -1]
    case = -1

def get_mouse(event, x, y, flags, params) -> None:
    
    if event == cv2.EVENT_LBUTTONDOWN:
        p1, p4 = echecs.p1, echecs.p4
        if clicked_in([x, y], [p1, p4]):
            mouse.case = [round(i) for i in [8/diff(p1[0], p4[0])*x, 8/diff(p1[1], p4[1])*y]]
    elif event == cv2.EVENT_LBUTTONUP:
        p1, p4 = echecs.p1, echecs.p4
        if clicked_in([x, y], [p1, p4]):
            if mouse.case == [round(i) for i in [8/diff(p1[0], p4[0])*x, 8/diff(p1[1], p4[1])*y]]:
                mouse.click, mouse.pos = True, [x, y]

class echecs:
    p1, p2, p3, p4 = [screen[0]/2-screen[1]/2, 0], [screen[0]/2+screen[1]/2, 0], [screen[0]/2-screen[1]/2, screen[1]], [screen[0]/2+screen[1]/2, screen[1]]
    def pos_ini(self) -> np.array:
        l = "t._c_f_d_r_f_c_t."
        m = np.array([[" " for _ in range(8)] for _ in range(8)], dtype=object)
        m[0:8,0], m[0:8,7], m[0:8,1], m[0:8,6] = l.split("_"), l.upper().split("_")[::-1], "p.", "P."
        return m
    def __str__(self) -> str:
        return "\n".join(" ".join(self.matrix[x, y][0] for x in range(8)) for y in range(8))
    def __init__(self, name="Pychess") -> None:
        self.name = name
        self.matrix = self.pos_ini()
        self.p1 = None
        self.trait = True
    def sel_leg(self) -> bool:
        c = mouse.case
        p = self.matrix[c[0], c[1]]
        if p != " " and p[0].isupper() == self.trait:
            return True
        return False
    def legal(self) -> bool: # TODO
        cd, ca = self.p1, mouse.case
        if cd != ca:
            return True
        return False
    def image(self) -> image:
        img = image(nom=self.name, img=image.new_img(fond=col.cyan))
        pts = [echecs.p1, echecs.p2, echecs.p3, echecs.p4]
        p1, p2, p3, p4 = [pt_sg(i, ct, 5) for i in pts]
        img.rectangle(p1, p4, col.black, 0)
        X = [p1[0] + (p4[0]-p1[0])/8*n for n in range(8)] + [p4[0]]
        Y = [p1[1] + (p4[1]-p1[1])/8*n for n in range(8)] + [p4[1]]
        for x_, x in enumerate(X[:-1:]):
            for y_, y in enumerate(Y[:-1:]):
                pt1, pt2 = [x, y], [X[x_+1], Y[y_+1]]
                img.rectangle(pt1, pt2, col.noir if x_%2!=y_%2 else col.white, 0)
        for x_, x in enumerate(X[:-1:]):
            for y_, y in enumerate(Y[:-1:]):
                pt1, pt2 = [x, y], [X[x_+1], Y[y_+1]]
                if self.p1 == [x_, y_]:
                    img.rectangle(pt1, pt2, col.green, 3)
                p = self.matrix[x_, y_][0]
                img.ecris(p, ct_sg(pt1, pt2), col.blue if p.isupper() else col.red, 3, 3, cv2.FONT_HERSHEY_SIMPLEX)
        return img
    def start(self) -> None:
        img = self.image()
        img.montre(1)
        cv2.setMouseCallback(img.nom, get_mouse)
        fs = False
        while True:
            wk = img.montre(1, fullscreen= fs)
            if img.is_closed(): break
            match wk:
                case 27: break
                case 32: fs = not fs
            if mouse.click:
                if self.p1 == None: self.p1 = mouse.case if self.sel_leg() else None
                else:
                    if  self.legal():
                        a, b = self.p1, mouse.case
                        print(a, b)
                        self.matrix[b[0], b[1]] = self.matrix[a[0], a[1]]
                        self.matrix[a[0], a[1]] = " "
                        self.trait = not self.trait
                    self.p1 = None
                mouse.click = False
if __name__ == "__main__":
    a = echecs()
    a.start()