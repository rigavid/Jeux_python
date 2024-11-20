from tsanap import *

def update_m(pt, *args, **kwargs) -> np.array:
    print(pt, args, kwargs)
    return pt+1
updt_m = np.vectorize(update_m)

class gom:
    def __init__(self, size=[1080, 1080]) -> None:
        self.matrix = np.zeros(size)
    def image(self):
        img = image(img=self.matrix)
        return img
    def update(self) -> None:
        self.matrix = updt_m(self.matrix, self.matrix)

g = gom(size=[3, 3])
img = g.image()
fs = False
while True:
    match img.montre(1, fullscreen=fs):
        case 27: break
        case 32: fs = not fs
        case 8: g.update()
    if img.is_closed(): break
    img = g.image()