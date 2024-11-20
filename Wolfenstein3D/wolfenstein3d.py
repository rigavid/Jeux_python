from tsanap import *

class res:
    resses, resind = [screen, [1680, 1050], [1366, 768]], 0
    res = resses[resind]
    def update():
        res.resind = (res.resind+1)%len(res.resses)
        res.res = res.resses[res.resind]

_ = False
matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class wst:
    def __init__(self) -> None:
        self.map = matrix
    def img(self) -> image:
        img = image(img=image.new_img(dimensions=res.res))
        return img

a = wst()
img = a.img()
fs = False
while True:
    wk = img.montre(1, fullscreen=fs)
    if img.is_closed(): break
    match wk:
        case 27: break
        case 32: fs = not fs