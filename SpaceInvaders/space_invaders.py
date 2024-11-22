from pyimager import *
import time

class config:
    t_x, t_y = 400, 225

class game:
    def tile_(self, x, y):
        return [[RES.resolution[i]/[config.t_x, config.t_y][i]*([x, y][i]+[0, 1][j]) for i in [0, 1]] for j in [0, 1]]
    def get_tile(self, x, y):
        return [[x, y][i]/RES.resolution[i]*[config.t_x, config.t_y][i] for i in [0, 1]]
    def tile(self, x, y):
        return self.tile_(*self.get_tile(x, y))
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
    class Invader:
        def __init__(self, pos): self.pos = pos
        def update(self, vel, ang): self.pos = coosCircle(self.pos, vel, ang)
        def bomb(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > game.cooldown:
                self.last_shoot_t = time.time()
                jeu.bombs.append(game.bomb(self.pos, game.bomb_speed))
    class squid(Invader):
        def __init__(self, *args, **kwargs) -> None: game.Invader.__init__(self, *args, **kwargs)
        def draw(self, img:image, jeu, frame=0):
            tile = jeu.get_tile(*self.pos)
            carres = [[x, y] for i, y in enumerate(range(0, 3)[::-1]) for x in range(0-i, i+2)   
            ]+[[x, y] for x in range(-3, 5) for y in [-1, -2] if y!=-1 or x not in [-1, 2]]
            if frame%2==0:
                carres += [[-1, -3], [2, -3]]+[[x, -4] for x in range(-2, 4) if not x in [-1, 2]]+[[x, -5] for x in []] ## TODO ##
            else:
                carres += []
            for c in carres:
                img.rectangle(*jeu.tile_(*[tile[i]-c[i]for i in[0,1]]), COL.green, 0)
    class laser:
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 270)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.lasers.pop(gam.lasers.index(self))
        def draw(self, img:image) -> None:
            img.rectangle([self.pos[0]-2, self.pos[1]-20], [self.pos[0]+2, self.pos[1]], COL.red, 0, 2)
    class canon:
        def __init__(self, pos=[RES.resolution[0]/2, RES.resolution[1]*0.9], hitbox=[20, 20], vel=10):
            self.pos, self.hitbox, self.vel, self.last_shoot_t = pos, hitbox, vel, time.time()
        def move_(self, ang): self.pos = coosCircle(self.pos, self.vel, ang)
        def move(self, ang):
            self.move_(ang)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]):
                self.pos = [min(self.pos[i], RES.resolution[i]) for i in [0, 1]]
                self.pos = [max(self.pos[i], 0) for i in [0, 1]]
        def draw(self, img:image, jeu) -> None:
            tile = jeu.get_tile(*self.pos)
            carres = [[x, y] for x in range(-6, 7) for y in range(-3, 1)]+[[x, 1] for x in range(-5, 6)]+[[x, y] for x in [-1, 0, 1] for y in [2, 3]]+[[0, 4]]
            for c in carres:
                img.rectangle(*jeu.tile_(*[tile[i]-c[i]for i in[0,1]]), COL.green, 0)
        def shoot(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > game.cooldown:
                self.last_shoot_t = time.time()
                jeu.lasers.append(game.laser(self.pos, game.laser_speed))
    def __init__(self, vel_p=10):
        self.player = self.canon(vel=vel_p)
        self.bombs = []
        self.lasers = []
        self.invaders = [self.squid([300, 300])]
    def update(self):
        for i in self.bombs+self.lasers: i.update(self)
    def image(self) -> image:
        
        img = new_img(background=COL.black, name="Space Invaders")
        for INV in self.invaders: INV.draw(img, self)
        for i in self.bombs+self.lasers: i.draw(img)
        self.player.draw(img, self)
        return img
img = new_img(background=COL.black, name="Space Invaders")
jeu = game(20)
img.img = jeu.image().img
img.build()
t_b_f = 1/60
lst_t = time.time()
while img.is_opened():
    wk = img.show(built_in_functs=False)
    match wk:
        case 27: img.close()
        case 8: img.fullscreen = not img.fullscreen
        case 65363: ## Right arrow
            jeu.player.move(0)
        case 65361: ## Left arrow
            jeu.player.move(180)
        case 32: ## Space bar
            jeu.player.shoot(jeu)
        case -1: ...
        case _: print(wk)
    if diff(time.time(), lst_t) > t_b_f:
        jeu.update()
        img.img = jeu.image().img
        lst_t = time.time()