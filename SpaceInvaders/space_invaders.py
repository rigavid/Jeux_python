from pyimager import *
import time

class game:
    laser_speed = 10
    bomb_speed = 15
    cooldown = 0.5
    class bomb:
        def __init__(self, pos, vel): slef.pos, self.vel = pos, vel
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 90)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.bombs.pop(gam.bombs.index(self))
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[0]-10, self.pos[1]-20], [self.pos[0]+10, self.pos[1]+20], COL.blue, 0, 2)
    class laser:
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 270)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.lasers.pop(gam.lasers.index(self))
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[0]-2, self.pos[1]-20], [self.pos[0]+2, self.pos[1]+20], COL.red, 0, 2)
    class Invader:
        def __init__(self, pos, typ): self.pos, self.type = pos, typ
        def update(self, vel, ang): self.pos = coosCircle(self.pos, vel, ang)
        def bomb(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > game.cooldown:
                self.last_shoot_t = time.time()
                jeu.bombs.append(game.bomb(self.pos, game.bomb_speed))
    class canon:
        def __init__(self, pos=[RES.resolution[0]/2, RES.resolution[1]*0.9], hitbox=[20, 20], vel=10):
            self.pos, self.hitbox, self.vel, self.last_shoot_t = pos, hitbox, vel, time.time()
        def move_(self, ang): self.pos = coosCircle(self.pos, self.vel, ang)
        def move(self, ang):
            self.move_(ang)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]):
                self.pos = [min(self.pos[i], RES.resolution[i]) for i in [0, 1]]
                self.pos = [max(self.pos[i], 0) for i in [0, 1]]
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[i]-self.hitbox[i]/2 for i in [0,1]], [self.pos[i]+self.hitbox[i]/2 for i in [0,1]], COL.green, 0, 2)
            img.rectangle([self.pos[0]-self.hitbox[0]/5, self.pos[1]-self.hitbox[0]], [self.pos[0]+self.hitbox[0]/5, self.pos[1]-self.hitbox[0]/2], COL.green, 0, 2)
        def shoot(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > game.cooldown:
                self.last_shoot_t = time.time()
                jeu.lasers.append(game.laser(self.pos, game.laser_speed))
    def __init__(self, vel_p=10):
        self.player = self.canon(vel=vel_p)
        self.bombs = []
        self.lasers = []
    def update(self):
        for i in self.bombs+self.lasers: i.update(self)
    def image(self) -> image:
        img = new_img(background=COL.black, name="Space Invaders")
        for i in self.bombs+self.lasers: i.draw(img)
        self.player.draw(img)
        return img
img = new_img(background=COL.black, name="Space Invaders")
jeu = game(20)
img.img = jeu.image().img
img.build()
t_b_f = 1/60
lst_t = time.time()
while img.is_opened():
    wk = img.show()
    match wk:
        case 65363: ## Right arrow
            jeu.player.move(0)
        case 65361: ## Left arrow
            jeu.player.move(180)
        case 65362: ## Up arrow
            jeu.player.shoot(jeu)
        # case 8: RES.update()
        case -1: ...
        case _: print(wk)
    if diff(time.time(), lst_t) > t_b_f:
        jeu.update()
        img.img = jeu.image().img
        lst_t = time.time()