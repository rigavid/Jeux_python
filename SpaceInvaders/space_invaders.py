from pyimager import *
import time

class game:
    class bomb:
        def __init__(self, pos, vel): slef.pos, self.vel = pos, vel
        def update(self): self.pos = coosCircle(self.pos, self.vel, 90)
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[0]-10, self.pos[1]-20], [self.pos[0]+10, self.pos[1]+20], COL.blue, 0, 2)
    class laser:
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def update(self): self.pos = coosCircle(self.pos, self.vel, 270)
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[0]-10, self.pos[1]-20], [self.pos[0]+10, self.pos[1]+20], COL.red, 0, 2)
    class Invader:
        def __init__(self, pos, typ): self.pos, self.type = pos, typ
        def update(self, vel, ang): self.pos = coosCircle(self.pos, vel, ang)
    class canon:
        def __init__(self, pos=[RES.resolution[0]/2, RES.resolution[1]*0.9], hitbox=[20, 20], vel=10):
            self.pos, self.hitbox, self.vel = pos, hitbox, vel
        def move(self, ang): self.pos = coosCircle(self.pos, self.vel, ang)
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[i]-self.hitbox[i]/2 for i in [0,1]], [self.pos[i]+self.hitbox[i]/2 for i in [0,1]], COL.green, 0, 2)
    def __init__(self):
        self.player = self.canon()
        self.bombs = []
        self.lasers = []
    def update(self):
        for i in self.bombs+self.lasers: i.update()
    def image(self) -> image:
        img = new_img(background=COL.black, name="Space Invaders")
        self.player.draw(img)
        return img
img = new_img(background=COL.black, name="Space Invaders")
jeu = game()
img.img = jeu.image().img
img.build()
t_b_f = 1/60
lst_t = time.time()
while img.is_opened():
    wk = img.show()
    match wk:
        case 65363: jeu.player.move(0) ## Right arrow
        case 65361: jeu.player.move(180) ## Left arrow
        case 65362: jeu.player.shoot() ## Up arrow

        case -1: ...
        case _: print(wk)
    if diff(time.time(), lst_t) > t_b_f:
        jeu.update()
        img.img = jeu.image().img
        lst_t = time.time()
        