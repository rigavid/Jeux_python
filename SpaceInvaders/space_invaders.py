from operator import add, sub
from pyimager import *
import time

highscores_path = "/".join(__file__.split("/")[:-1:])+"/highscores.txt"

class config:
    n = 2
    t_x, t_y = 192*n, 108*n

def sumL(l1, l2): return tuple(map(add, l1, l2))
def subL(l1, l2): return tuple(map(sub, l1, l2))

class game:
    with open(highscores_path, "r", encoding="utf8") as file:
        highscores = eval(file.read())
    def new_highscore(self):
        with open(highscores_path, "w", encoding="utf8") as file:
            file.write(self.highscores)
    def tile_(self, x, y): return [[RES.resolution[i]/[config.t_x, config.t_y][i]*([x, y][i]+[0, 1][j]) for i in [0, 1]] for j in [0, 1]]
    def get_tile(self, x, y): return [round(v) for v in [[x, y][i]/RES.resolution[i]*[config.t_x, config.t_y][i] for i in [0, 1]]]
    def tile(self, x, y): return self.tile_(*self.get_tile(x, y))
    laser_speed, bomb_speed, cooldown, bg_color, max_n_l, mult_vel, ground = 10, 8, 0.5, COL.black, 1, 3, [(0, RES.resolution[1]*0.92), (RES.resolution[0], RES.resolution[1]*0.925)]
    class bunker: ... ## TODO Build the bunkers
    class explosion:
        def __init__(self, pos) -> None:
            self.frame, self.pos = 0, pos
        def draw(self, img:image, gam) -> None: ## TODO Make the explosion beautifull
            for p in range(0, 360, 20):
                img.line(coosCircle(self.pos, self.frame, p), coosCircle(self.pos, self.frame+4, p), COL.red, 2, 2)
        def update(self, gam) -> None:
            self.frame += 1
            if self.frame >= 20: gam.explosions.pop(gam.explosions.index(self))
    class bomb:
        score, carres = 1, [[0, y] for y in range(-1, 3)]+[[1,2],[-1,2]]
        def __init__(self, pos, vel):
            self.pos, self.vel = pos, vel
        def get_tiles(self, jeu):
            return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def update(self, gam):
            self.pos = coosCircle(self.pos, self.vel, 90)
            if not clicked_in(self.pos, [[0, 0], [RES.resolution[0], gam.tile(*gam.ground[0])[0][1]]]):
                gam.explosions.append(game.explosion(gam.bombs.pop(gam.bombs.index(self)).pos))
            if dist(gam.player.pos, self.pos)<30:
                if any(i in gam.player.get_tiles(gam) for i in self.get_tiles(gam)):
                    gam.player.pos[0] = RES.resolution[0]/2
                    gam.bombs.pop(gam.bombs.index(self))
                    gam.lives -= 1
        def tile(self, which, jeu): return jeu.tile_(*subL(jeu.get_tile(*self.pos), which))
        def draw(self, img:image, jeu) -> None:
            for c in [(self.tile(self.carres[0], jeu)[1], self.tile(self.carres[2], jeu)[0]), (self.tile(self.carres[-2],jeu)[0], self.tile(self.carres[-1],jeu)[1])]:
                img.rectangle(*c, COL.blue, 0)
    class Invader:
        last_shoot_t = time.time()
        def __init__(self, pos):
            self.pos = pos
        def update(self, vel, ang):
            self.pos = coosCircle(self.pos, vel, ang)
        def bomb(self, jeu) -> None:
            if diff(jeu.last_bomb_t, t:=time.time()) > jeu.cooldown*2 and rd.randint(len(jeu.invaders), 11*5) == 11*5:
                jeu.bombs.append(game.bomb(self.pos, game.bomb_speed))
                jeu.last_bomb_t = t
        def draw(self, img:image, jeu): ## REMEMBER ## This function shouldn't be used as it takes too much memory
            for c in self.carres1 if int(jeu.frame)%2==0 else self.carres2:
                img.rectangle(*jeu.tile_(*[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]]), self.color, 0)
        def get_tiles(self, jeu):
            return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in (self.carres1 if int(jeu.frame)%2==0 else self.carres2)]
        def tile(self, which, jeu):
            return jeu.tile_(*subL(jeu.get_tile(*self.pos), which))
    # input([self.tile(t, jeu) for t in self.carres2])
    class squid(Invader):
        score, color, carres = 30, COL.lime, [[x, y] for i, y in enumerate(range(0, 3)[::-1]) for x in range(0-i, i+2)]+[[x, y] for x in range(-3, 5) for y in [-1, -2] if y!=-1 or x not in [-1, 2]]
        carres1, carres2 = [[x, y+2] for x, y in carres + [[-1, -3], [2, -3]]+[[x, -4] for x in range(-2, 4) if not x in [-1, 2]]+[[x, -5] for x in [-3, -1, 2, 4]]], [[x, y+2] for x, y in carres + [[x, -3] for x in range(-2, 4) if not x in [-1, 2]]+[[-3, -4],[4, -4]]+[[-2, -5], [3, -5]]]
        def draw(self, img:image, jeu):
            for a,b in[(1,0),(5,2),(11,6),(24,23),(19,17),(14,13),(21, 16),(30,29)]+[(i,i)for i in range(26,36)if not i in(29,30)]if int(jeu.frame)%2==0 else[(1,27),(24,25),(11,29),(6,26),(12,13),(21,21),(16,16),(5,10),(2,7)]+[(i,i)for i in range(30,34)]:
                img.rectangle(*((self.tile(self.carres1[a],jeu)[0],self.tile(self.carres1[b],jeu)[-1])if int(jeu.frame)%2==0 else(self.tile(self.carres2[a],jeu)[0],self.tile(self.carres2[b],jeu)[-1])),self.color,0)
    class crab(Invader):
        score, color, carres = 20, COL.cyan, [[-3,4],[3,4],[-2,3],[2,3]]+[[x,2]for x in range(-4,5)]+[[x,1]for x in range(-5,6)if not x in[-2,2]]+[[x,0]for x in range(-6,7)]+[[x,-1]for x in range(-4,5)]
        carres1, carres2 = carres + [[-6,-1],[6,-1],[-6,-2],[6,-2],[-4,-2],[4,-2]]+[[x,-3]for x in range(-3,4)if x!=0], carres + [[[-6,6][i],y]for y in[3,2,1]for i in[0,1]]+[[[-3,-4][i],y]for i,y in enumerate([-2,-3])]+[[[3,4][i],y]for i,y in enumerate([-2,-3])]+[[-5,-1],[5,-1]]
        def draw(self, img:image, jeu):
            for a, b in [(34, 47), (21, 33), (12, 49), (11, 42), (3, 10), (9, 16), (30, 37), (2, 6), (5, 36), (4, 48), (13, 23), (22, 46), (55, 53), (52, 50), (1, 1), (0, 0)] if int(jeu.frame)%2==0 else [(1, 1), (0, 0), (45, 34), (44, 22), (21, 55), (13, 54), (12, 43), (11, 52), (3, 10), (2, 6), (30, 41), (9, 38), (26, 37), (5, 50), (4, 35), (53, 53), (51, 51)]:
                img.rectangle(self.tile((self.carres1 if int(jeu.frame)%2==0 else self.carres2)[a], jeu)[0], self.tile((self.carres1 if int(jeu.frame)%2==0 else self.carres2)[b], jeu)[-1], self.color, 0)
    class octopus(Invader):
        score, color, carres = 10, COL.yellow, [[x,4]for x in range(-1,3)]+[[x,3]for x in range(-4,6)]+[[x,y]for x in range(-5,7)for y in [2,1,0]if not(y==1 and x in[-2,-1,2,3])]+[[x,-1]for x in[-2,-1,2,3]]+[[0,-2],[1,-2],[-3,-2],[4,-2]]
        carres1, carres2 = carres + [[-3,-1],[4,-1],[-4,-2],[5,-2],[-3,-3],[-2,-3],[4,-3],[3,-3]], carres + [[-5,-3],[-4,-3],[6,-3],[5,-3],[-2,-2],[3,-2]]
        def draw(self, img:image, jeu):
            for a, b in [(3, 0), (13, 4), (31, 29), (36, 48), (26, 46), (51, 50)]+([(43, 42), (17, 16), (35, 23), (37, 55), (20, 54), (57, 53), (52, 56), (60, 61), (59, 58)] if int(jeu.frame)%2==0 else [(43, 14), (44, 39), (21, 16), (58, 52), (53, 59), (56, 57), (55, 54)]):
                img.rectangle(self.tile((self.carres1 if int(jeu.frame)%2==0 else self.carres2)[a], jeu)[0], self.tile((self.carres1 if int(jeu.frame)%2==0 else self.carres2)[b], jeu)[-1], self.color, 0)
    class UFO(Invader): ## TODO appear sometimes randomly
        color, carres = COL.purple, [[x, 6] for x in range(-2, 4)]+[[x, 5] for x in range(-4, 6)]+[[x, 4] for x in range(-5, 7)]+[[x, 3] for x in range(-6, 8) if not x in (-4, -1, 2, 5)]+[[x, 2] for x in range(-7, 9)]+[[x, 1] for x in range(-5, 7) if not x in (-2, -1, 2, 3)]+[[-4, 0], [5, 0]]
        def get_tiles(self, jeu):
            return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def __init__(self, *args, **kwargs) -> None:
            self.score = rd.choice((50, 100, 150, 200, 300))
            game.Invader.__init__(self, *args, **kwargs)
        def update(self, jeu):
            self.pos = coosCircle(self.pos, jeu.vel, 0)
            if not clicked_in(self.pos, [(0, 0), RES.resolution]):
                jeu.invaders.pop(jeu.invaders.index(self))
        def draw(self, img:image, jeu): ## TODO Finish to draw it
            for a, b in [(5, 23), (1, 19), (3, 57), (15, 14), (7, 6), (27, 25), (18, 16), (37, 36), (29, 28)]:
                img.rectangle(self.tile(self.carres[a], jeu)[0], self.tile(self.carres[b], jeu)[-1], COL.purple, 0)
    class laser:
        carres = [[0, y] for y in range(-3, 2)]
        def __init__(self, pos, vel): self.pos, self.vel = pos, vel
        def get_tiles(self, jeu): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def update(self, gam) -> None:
            self.pos = coosCircle(self.pos, self.vel, 270)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]): gam.lasers.pop(gam.lasers.index(self))
            for inv in [inv for inv in gam.invaders if dist(inv.pos, self.pos)<50]:
                if any(i in inv.get_tiles(gam) for i in self.get_tiles(gam)):
                    gam.score += gam.invaders.pop(gam.invaders.index(inv)).score
                    gam.lasers.pop(gam.lasers.index(self))
            for bomb in [b for b in gam.bombs if dist(b.pos, self.pos)<30]:
                if any(i in bomb.get_tiles(gam) for i in self.get_tiles(gam)):
                    gam.score += gam.bombs.pop(gam.bombs.index(bomb)).score
                    gam.lasers.pop(gam.lasers.index(self))
        def draw(self, img:image, jeu) -> None:
            img.rectangle(*[jeu.tile_(*self.get_tiles(jeu)[i])[j] for i, j in [(0, -1), (-1, 0)]], COL.white, 0)
    class canon:
        carres = [[x, y] for x in range(-6, 7) for y in range(-3, 1)]+[[x, 1] for x in range(-5, 6)]+[[x, y] for x in [-1, 0, 1] for y in [2, 3]]+[[0, 4]]
        def get_tiles(self, jeu): return [[jeu.get_tile(*self.pos)[i]-c[i]for i in[0,1]] for c in self.carres]
        def __init__(self, vel, pos=[RES.resolution[0]/2, RES.resolution[1]*0.9], hitbox=[20, 20]):
            self.pos, self.hitbox, self.vel, self.last_shoot_t = pos, hitbox, vel, time.time()
        def move_(self, ang): self.pos = coosCircle(self.pos, self.vel, ang)
        def move(self, ang):
            self.move_(ang)
            if not clicked_in(self.pos, [[0, 0], RES.resolution]):
                self.pos = [min(self.pos[i], RES.resolution[i]) for i in [0, 1]]
                self.pos = [max(self.pos[i], 0) for i in [0, 1]]
        def tile(self, which, jeu): return jeu.tile_(*subL(jeu.get_tile(*self.pos), which))
        def draw(self, img:image, jeu) -> None:
            for a, b in ((0, 51), (52, 62), (63, -2), (-1, -1)):
                img.rectangle(self.tile(self.carres[a], jeu)[-1], self.tile(self.carres[b], jeu)[0], COL.lime, 0)
        def shoot(self, jeu) -> None:
            if diff(self.last_shoot_t, t:=time.time()) > game.cooldown and len(jeu.lasers)<jeu.max_n_l:
                self.last_shoot_t = t
                jeu.lasers.append(game.laser(self.pos, game.laser_speed))
    def new_wave(self) -> None:
        esp = 150/config.n
        offsetx, offsety = 100, 100
        squids = [self.squid([offsetx+esp*x, offsety]) for x in range(11)]
        crabs = [self.crab([offsetx+esp*x, offsety+esp+y]) for x in range(11) for y in [0, esp]]
        octopuses = [self.octopus([offsetx+esp*x, offsety+3*esp+y]) for x in range(11) for y in [0, esp]]
        self.invaders += squids+crabs+octopuses
        self.vel = self.player.vel
        self.ang = 0
    def __init__(self):
        self.player, self.score, self.frame, self.bombs, self.lasers, self.lives = self.canon(vel=dist(self.tile_(0, 0)[0], self.tile_(1, 0)[0])), 0, 0, [], [], 3
        self.invaders, self.explosions, self.last_bomb_t = [], [], time.time()
        self.wave, self.UFOS = 1, 0
    def update(self):
        self.frame += 1/5
        for i in self.bombs+self.lasers+self.explosions:
            i.update(self)
        for i in self.invaders:
            if type(i) != game.UFO:
                i.update(self.vel, self.ang)
            else:
                i.update(self)
        if any(not clicked_in(i.pos, [[0,0],RES.resolution]) for i in self.invaders if type(i) != game.UFO): ## Dépassent le bord de l'écran
            self.ang += 180
            for i in self.invaders:
                if type(i) != game.UFO:
                    i.update(self.vel, 90)
                    i.update(self.vel, self.ang)
        if int(self.frame)%5==0:
            try:
                if type(inv:=rd.choice(self.invaders)) != game.UFO:
                    inv.bomb(self)
            except: ...
        elif int(self.frame)%6 and self.UFOS<self.wave:
            self.invaders.append(self.UFO([0, 100]))
            self.UFOS += 1
        if len(self.invaders)==0:
            self.new_wave()
    def image(self) -> image:
        img = new_img(background=self.bg_color)
        img.rectangle(*(self.tile(*self.ground[i])[i] for i in [0, -1]), COL.darkGreen, 0)
        for i in self.bombs+self.lasers+self.explosions+self.invaders+[self.player]:
            i.draw(img, self)
        img.write(f"{self.score:0>6}", [10, 30], COL.white, 2, 2, FONT_HERSHEY_PLAIN)
        img.write(f"{self.lives}", [10, RES.resolution[1]-30], COL.white, 2, 2, FONT_HERSHEY_PLAIN)
        return img
    def reset(self) -> None:
        self.__init__()
    def close(self, img) -> bool:
        im = new_img(dimensions=img.size(), background=COL.black)
        im.write_centered("Do you really want to quit?\n\n(y/N)", ct_sg((0, 0), RES.resolution), COL.red, 4, 3, FONT_HERSHEY_COMPLEX, 2)
        img.img = im.img
        return img.show_(0, built_in_functs=False) in [ord("y"), 27]
    def play(self, img) -> None:
        tick, last_tick = 1/30, time.time()
        while img.is_opened() and self.lives>0:
            match img.show(built_in_functs=False):
                case 27:
                    if self.close(img):
                        img.close()
                case 8: img.fullscreen = not img.fullscreen
                case 65363: self.player.move(0) ## Right arrow
                case 65361: self.player.move(180) ## Left arrow
                case 32: self.player.shoot(self) ## Space bar
                case 65470: cv2.moveWindow(img.name, 0, 0) #f1
                case 65471: cv2.moveWindow(img.name, 1920, 0) #f2
            if diff(t:=time.time(), last_tick) > tick:
                self.update()
                last_tick = t
            img.img = self.image().img
    def titlescreen(self, img) -> None:
        im = new_img(dimensions=img.size(), background=COL.black)
        im.write_centered("TITLESCREEN!\n\n Spacebar to continue", ct_sg((0, 0), RES.resolution), COL.red, 4, 3, FONT_HERSHEY_COMPLEX, 2)
        img.img = im.img
        while img.is_opened():
            match img.show_(0, built_in_functs=False):
                case 8: img.fullscreen = not img.fullscreen
                case 27:
                    if self.close(img):
                        img.close()
                    else: img.img = im.img
                case 32: return
    def save_highscore(self) -> None: ...

def main():
    jeu = game()
    img = new_img(name="Space Invaders").build()
    img.fullscreen = True
    jeu.max_n_l = 10 ## TODO REMOVE IT
    while img.is_opened():
        jeu.titlescreen(img)
        jeu.play(img)
        jeu.reset()
        jeu.save_highscore()

if __name__ == "__main__":
    main()