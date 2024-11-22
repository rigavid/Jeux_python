from pyimager import *
import time

class config:
    t_x, t_y = 192, 108

class game:
    def tile_(self, x, y):
        return [[RES.resolution[i]/[config.t_x, config.t_y][i]*([x, y][i]+[0, 1][j]) for i in [0, 1]] for j in [0, 1]]
    def get_tile(self, x, y):
        return [round(v) for v in [[x, y][i]/RES.resolution[i]*[config.t_x, config.t_y][i] for i in [0, 1]]]
    def tile(self, x, y):
        return self.tile_(*self.get_tile(x, y))
    laser_speed = 10
    bomb_speed = 15
    cooldown = 0.5
    class bomb:
        carres = [[0, y] for y in range(-3, 1)]
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 90)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.bombs.pop(gam.bombs.index(self))
            if any(i in gam.player.get_tiles() for i in self.get_tiles()):
                gam.player.pos[0] = RES.resolution[0]/2
                gam.bombs.pop(gam.bombs.index(self))
        def draw(self, img:image) -> None:
            for c in self.carres: img.rectangle(*jeu.tile_(*[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]]), COL.blue, 0)
    class Invader:
        def __init__(self, pos): self.pos, self.last_shoot_t = pos, time.time()
        def update(self, vel, ang): self.pos = coosCircle(self.pos, vel, ang)
        def bomb(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > 1:
                jeu.bombs.append(game.bomb(self.pos, game.bomb_speed))
                self.last_shoot_t = time.time()
        def draw(self, img:image, jeu):
            for c in self.carres1 if int(jeu.frame)%2==0 else self.carres2:
                img.rectangle(*jeu.tile_(*[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]]), COL.lime, 0)
    class squid(Invader):
        score = 30
        carres = [[x, y] for i, y in enumerate(range(0, 3)[::-1]) for x in range(0-i, i+2)]+[[x, y] for x in range(-3, 5) for y in [-1, -2] if y!=-1 or x not in [-1, 2]]
        carres1 = [[x, y+2] for x, y in carres + [[-1, -3], [2, -3]]+[[x, -4] for x in range(-2, 4) if not x in [-1, 2]]+[[x, -5] for x in [-3, -1, 2, 4]]]
        carres2 = [[x, y+2] for x, y in carres + [[x, -3] for x in range(-2, 4) if not x in [-1, 2]]+[[-3, -4],[4, -4]]+[[-2, -5], [3, -5]]]
        def __init__(self, *args, **kwargs) -> None: game.Invader.__init__(self, *args, **kwargs)
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
    class crab(Invader):
        score = 20
        carres = [[-3,4],[3,4],[-2,3],[2,3]]+[[x,2]for x in range(-4,5)]+[[x,1]for x in range(-5,6)if not x in[-2,2]]+[[x,0]for x in range(-6,7)]+[[x,-1]for x in range(-4,5)]
        carres1 = carres + [[-6,-1],[6,-1],[-6,-2],[6,-2],[-4,-2],[4,-2]]+[[x,-3]for x in range(-3,4)if x!=0]
        carres2 = carres + [[[-6,6][i],y]for y in[3,2,1]for i in[0,1]]+[[[-3,-4][i],y]for i,y in enumerate([-2,-3])]+[[[3,4][i],y]for i,y in enumerate([-2,-3])]
        def __init__(self, *args, **kwargs) -> None: game.Invader.__init__(self, *args, **kwargs)
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
    class octopus(Invader):
        score = 10
        carres = [[x,4]for x in range(-1,3)]+[[x,3]for x in range(-4,6)]+[[x,y]for x in range(-5,7)for y in [2,1,0]if not(y==1 and x in[-2,-1,2,3])]+[[x,-1]for x in[-2,-1,2,3]]+[[0,-2],[1,-2],[-3,-2],[4,-2]]
        carres1 = carres + [[-3,-1],[4,-1],[-4,-2],[5,-2],[-3,-3],[-2,-3],[4,-3],[3,-3]]
        carres2 = carres + [[-5,-3],[-4,-3],[6,-3],[5,-3],[-2,-2],[3,-2]]
        def __init__(self, *args, **kwargs) -> None: game.Invader.__init__(self, *args, **kwargs)
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
    class laser:
        carres = [[0, y] for y in range(-3, 1)]
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 270)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.lasers.pop(gam.lasers.index(self))
            for inv in gam.invaders:
                if any(i in inv.get_tiles() for i in self.get_tiles()):
                    gam.score += gam.invaders.pop(gam.invaders.index(inv)).score
                    gam.lasers.pop(gam.lasers.index(self))
        def draw(self, img:image) -> None:
            for c in self.carres: img.rectangle(*jeu.tile_(*[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]]), COL.red, 0)
    class canon:
        carres = [[x, y] for x in range(-6, 7) for y in range(-3, 1)]+[[x, 1] for x in range(-5, 6)]+[[x, y] for x in [-1, 0, 1] for y in [2, 3]]+[[0, 4]]
        def get_tiles(self): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def __init__(self, pos=[RES.resolution[0]/2, RES.resolution[1]*0.9], hitbox=[20, 20], vel=10):
            self.pos, self.hitbox, self.vel, self.last_shoot_t = pos, hitbox, vel, time.time()
        def move_(self, ang): self.pos = coosCircle(self.pos, self.vel, ang)
        def move(self, ang):
            self.move_(ang)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]):
                self.pos = [min(self.pos[i], RES.resolution[i]) for i in [0, 1]]
                self.pos = [max(self.pos[i], 0) for i in [0, 1]]
        def draw(self, img:image, jeu) -> None:
            for c in self.carres: img.rectangle(*jeu.tile_(*[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]]), COL.green, 0)
        def shoot(self, jeu) -> None:
            if diff(self.last_shoot_t, time.time()) > game.cooldown:
                self.last_shoot_t = time.time()
                jeu.lasers.append(game.laser(self.pos, game.laser_speed))
    def __init__(self, vel_p=10):
        self.player, self.score, self.frame, self.bombs, self.lasers = self.canon(vel=vel_p), 0, 0, [], []
        self.invaders = [self.squid([300, 300]), self.crab([400, 300]), self.octopus([500, 300])]
    def update(self):
        self.frame += 1/15
        for i in self.bombs+self.lasers: i.update(self)
        if int(self.frame)%5==0: ## TODO - get shoot by the invaders
            try: self.invaders[0].bomb(self)
            except: ...
    def image(self) -> image:
        img = new_img(background=COL.black)
        for INV in self.invaders: INV.draw(img, self)
        for i in self.bombs+self.lasers: i.draw(img)
        self.player.draw(img, self)
        img.write(f"{self.score:0>6}", [10, 30], COL.white, 2, 2, FONT_HERSHEY_PLAIN, )
        return img
img = new_img(name="Space Invaders")
jeu = game(20)
img.img = jeu.image().img
img.build()
t_b_f = 1/30
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
        lst_t = time.time()
    img.img = jeu.image().img