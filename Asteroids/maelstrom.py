try: from Outils.vecteurs import Vector2D
except: from Asteroids.Outils.vecteurs import Vector2D
try: from Outils.cvt import *
except: from Asteroids.Outils.cvt import *
try: from badges import *
except: from Asteroids.badges import *
import keyboard

## TODO ##
## Create spaceships that gives lives when you're colliding with you and disapears next ##
## Create vortex that creates gravitation to it and if the spaceship touch it: lives-=1 ##
## Create metal asteroids that have Vector2D and when u shoot it u give him a new force ##
## Create bonus scores and also multipliers. Bonus score diminues upon time: faster +xp ##

## Général ##
game_size = 1
game_vel = 1
shoot_range = 50
max_vel = 100
nom_fenetre = "Maelstrom"
## Astéroides ##
vel_min = 1.4142135623731
vel_max = vel_min*1.3
## Navette ##
immunity_time = 1.5

class EXIT(Exception):
    def __init__(self,*args):super().__init__(args)
    def __str__(self):return f'GAME EXIT'
class frame:
    size = [p*game_size for p in [long, haut]]
    points = 0
    def dessine_bonuses(navette, img):
        fz = bg
        for badge in set(navette.bonuses):
            oz = [fz[0], fz[1]-50]
            fz = [p+50 for p in oz]
            ct = ct_sg(oz, fz)
            match badge:
                case bonus.rafale: raffale(img, ct)
                case bonus.stabilisateur: stabilisateur(img, ct)
                case bonus.multi_shoot: multi_shoot(img, ct)
                case bonus.retro_thrusters: retro_fusee(img, ct)
                case _:
                    ligne(img, oz, fz, turquoise, 3)
                    ligne(img, [oz[0], fz[1]], [fz[0], oz[1]], turquoise, 3)
        return img
class bonus:
    rafale = 'rafale'
    stabilisateur = 'stabilisateur'
    multi_shoot = 'multi-shoot'
    retro_thrusters = 'retro-fusées'
    shield = 'shield'
    all = [rafale, stabilisateur, multi_shoot, retro_thrusters, shield]
class etoile_filante:
    def __init__(self) -> None:
        self.pos = [rd.randint(0, frame.size[axe]) for axe in [0, 1]]
        self.ori = rd.randint(0, 360)
        self.vel = vel_min*(rd.randint(100, 200)/100)
        self.remove = False
        self.spawn_t = time.time()
        self.live_t = rd.randint(1000, 2000)/100
    def move(self, tirs):
        if diff(self.spawn_t, time.time())>self.live_t: self.remove = True;return
        for tir in tirs:
            if dist(tir.pos, self.pos) < 10:
                tirs.remove(tir)
                self.remove = True
                return
            for pt in points_segment(coosCercle(self.pos, 100, self.ori+180), self.pos)[::3]:
                if dist(tir.pos, pt) < 12:
                    tirs.remove(tir)
                    self.remove = True
                    return
        self.pos = [p%frame.size[m] for m, p in enumerate(coosCercle(self.pos, self.vel, self.ori))]
    def dessine(self, img):
        ligne(img, coosCercle(self.pos, 100, self.ori+180), self.pos, turquoise, 3)
        cercle(img, self.pos, 5, nouvelle_couleur('804040'), 0)
        ellipse(img, ct_sg(coosCercle(self.pos, 100, self.ori+180), self.pos), [50, 2], nouvelle_couleur('a000a0'), 0, 0, 180, self.ori)
class ovni:
    class tir:
        def __init__(self, secoupe, navette) -> None:
            self.pos = secoupe.pos
            self.ori = angleEntrePoints(secoupe.pos, navette.pos)+rd.randint(0, 25)-12.5
            self.col = vert
            self.vel = rd.randint(10, 15)/10
            self.live = 100
        def move(self):
            self.pos = coosCercle(self.pos, self.vel*game_vel, self.ori)
            self.live -= 1
        def dessine(self, img) -> np.array:
            ellipse(img, self.pos, [3, 1], self.col, 0, angle=self.ori)
    def __init__(self):
        while True:
            pos = [rd.randint(0, n) for n in frame.size]
            if dist(pos, ct_sg([0, 0], frame.size)) > 300: break
        self.pos = pos
        self.vel = vel_min
        self.remove = False
        self.spawn_t = time.time()
        self.live_t = rd.randint(1000, 2000)/100
        self.last_tir = 0
        self.tirs = []
    def shoote(self, navette) -> None:
        self.tirs.append(self.tir(self, navette))
    def move(self, navette, tirs, asteroides):
        for shoot in tirs:
            if dist(shoot.pos, self.pos) < 15:
                tirs.remove(shoot)
                self.remove = True
        for shoot in self.tirs:
            if dist(shoot.pos, navette.pos) < 12:
                shoot.remove=True
                if not navette.shield_on:
                    navette.vies -= 1
                    if navette.vies <= 0:
                        navette.alive = False
                    navette.reset()
        for rock in asteroides:
            if dist(self.pos, rock.pos) <= 15+10*rock.type:
                if not rock.type == 1:
                    for a in range(0, 360, 360//rd.randint(2, 3)):
                        asteroides.append(asteroide(rock.pos, rock.type-1, rock.ori+a))
                rock.type = 0
                self.remove = True
        if rd.randint(0, 10)==0:
            a = angleEntrePoints(self.pos, navette.pos)
            self.pos = coosCercle(self.pos, self.vel, a)
    def dessine(self, img):
        cercle(img, self.pos, 15, rouge, 0)
        for shoot in self.tirs:
            if shoot.live <= 0: self.tirs.remove(shoot); continue
            shoot.move()
            shoot.dessine(img)
class asteroide:
    def __init__(self, pos=None, tipe=3, ori=rd.randint(0, 360)) -> None:
        if pos == None:
            while True:
                pos = [rd.randint(0, n) for n in frame.size]
                if dist(pos, ct_sg([0, 0], frame.size)) > 300: break
        self.pos = pos
        self.type = tipe
        self.vel = (vel_min+vel_max)/(rd.randint(1000, 2000)/1000)
        self.ori = ori
        self.points = 300-100*(self.type-1)
    def dessine(self, img) -> None:
        match self.type:
            case 3: cercle(img, self.pos, 30, nouvelle_couleur('606060'), 0)
            case 2: cercle(img, self.pos, 20, nouvelle_couleur('606060'), 0)
            case 1: cercle(img, self.pos, 10, nouvelle_couleur('606060'), 0)
    def move(self, tirs, asteroides):
        for tir in tirs:
            if dist(tir.pos, self.pos) < self.type*10:
                tirs.remove(tir)
                if not self.type == 1:
                    for a in range(0, 360, 360//rd.randint(2, 3)):
                        asteroides.append(asteroide(self.pos, self.type-1, self.ori+a))
                self.type = 0
        self.pos = [p%frame.size[m] if p != 0 else frame.size[m]-1 for m, p in enumerate(coosCercle(self.pos, self.vel*game_vel, self.ori))]
class power_up:
    def __init__(self, nav) -> None:
        self.remove = False
        while True:
            pos = [rd.randint(0, p) for p in frame.size]
            if dist(pos, nav.pos) > 300: break
        self.pos = pos
        self.visual_ori = self.ori = rd.randint(0, 3600)/10
        self.vel = vel_min*rd.randint(12, 16)/10
    def move(self, nav):
        self.pos = [p%frame.size[m] for m, p in enumerate(coosCercle(self.pos, self.vel, self.ori))]
        if dist(self.pos, nav.pos) < 10+12:
            choices = []
            for chc in bonus.all:
                if not chc in nav.bonuses: choices.append(chc)
            if len(choices) == 0: self.type = bonus.shield
            else: self.type = rd.choice(choices)
            if self.type == bonus.shield: nav.shield_qt += 10
            else: nav.bonuses.append(self.type)
            self.remove = True
    def dessine(self, img):
        pts = [coosCercle(self.pos, 17, a+self.visual_ori) for a in range(0, 360, 90)]
        triangle(img, pts[0], pts[1], pts[2], blanc, 0)
        triangle(img, pts[0], pts[2], pts[3], blanc, 0)
        pts2 = [coosCercle(self.pos, 6, 45+a+self.visual_ori) for a in range(0, 360, 90)]
        for i in [0, 1]:
            pts = pts2[i::2]
            ligne(img, pts[0], pts[1], rouge, 3)
        self.visual_ori += 1
class vaisseau:
    tirs = []
    class tir:
        cooldown = time.time()
        def __init__(self, pos, ori) -> None:
            self.pos = pos
            self.ori = ori
            self.col = rouge
            self.size = 1
            self.moved = 0
        def move(self):
            self.pos = [p%frame.size[m] for m, p in enumerate(coosCercle(self.pos, 10*self.size*game_size*game_vel, self.ori))]
            self.moved += 1
        def dessine(self, img) -> np.array:
            ellipse(img, self.pos, [3, 1], self.col, 0, angle=self.ori)
    def __init__(self) -> None:
        self.accel = False
        self.vies = 3
        self.pos = [p/2 for p in frame.size]
        self.ori = -90
        self.inercie = Vector2D()
        self.col = bleu
        self.size = 2
        self.shield_qt = 10
        self.shield_on = False
        self.bonuses = []
        self.alive = True
        self.spawn_t = time.time()
    def dessine(self, img):
        ligne(img, coosCercle(self.pos, game_size*10*self.size, self.ori), coosCercle(self.pos, game_size*13*self.size, self.ori), nouvelle_couleur('a0a0a0'), 2)
        triangle(img, coosCercle(self.pos, game_size*10*self.size, self.ori), coosCercle(self.pos, game_size*5*self.size, self.ori-120), coosCercle(self.pos, game_size*5*self.size, self.ori+120), self.col, 0)
        ellipse(img, pt_sg(coosCercle(self.pos, 10*game_size*self.size, self.ori), self.pos, 7, 15), [6, 3], jaune, 0, angle=self.ori)
        if self.shield_on: cercle(img, pt_sg(coosCercle(self.pos, 10*game_size*self.size, self.ori), self.pos, 14, 15), 20, rouge, 2)
        if diff(self.spawn_t, time.time()) < immunity_time: cercle(img, pt_sg(coosCercle(self.pos, 10*game_size*self.size, self.ori), self.pos, 14, 15), 20, rouge, 2)
        if self.accel:
            pt1, pt2 = [coosCercle(self.pos, 4*self.size, self.ori+180+a) for a in [-20, 20]]
            pt3 = coosCercle(self.pos, 12*self.size, self.ori+180)
            triangle(img, pt1, pt2, pt3, rouge, 0)
    def shield(self) -> None:
        if not self.shield_on:
            self.shield_t = time.time()
            self.shield_on = True
        if self.shield_qt-diff(self.shield_t, time.time())<0.2:
            self.shield_on = False
            self.shield_qt = 0
    def shoote(self) -> None:
        if diff(self.tir.cooldown, time.time()) >= 0.23 or (bonus.rafale in self.bonuses and diff(self.tir.cooldown, time.time()) >= 0.1):
            self.tirs.append(self.tir(coosCercle(self.pos, game_size*13*self.size, self.ori), self.ori))
            if bonus.multi_shoot in self.bonuses:
                for angle in [-10, 10]: self.tirs.append(self.tir(coosCercle(self.pos, game_size*13*self.size, self.ori), self.ori+angle))
            self.tir.cooldown = time.time()
    def move(self) -> None:
        pos = [self.pos[axe]+(eval(str(self.inercie))[axe]/10*game_vel) for axe in [0,1]]
        if bonus.stabilisateur in self.bonuses and not keyboard.is_pressed('up'):
            inercie = [v-(v/100) for v in eval(str(self.inercie))]
            self.inercie = Vector2D(inercie[0], inercie[1])
        self.pos = [p%frame.size[m] for m, p in enumerate(pos)]
    def reset(self):
        self.spawn_t = time.time()
        self.pos = [p/2 for p in frame.size]
        self.ori = -90
        self.inercie = Vector2D()
    def update(self, img, asteroides):
        if diff(self.spawn_t, time.time()) < immunity_time: self.shield_on
        for shoot in self.tirs:
            if shoot.moved>shoot_range*game_size/game_vel: self.tirs.remove(shoot); continue
            shoot.move()
            shoot.dessine(img)
        for rock in asteroides:
            if dist(rock.pos, self.pos) < (10*rock.type+10*self.size):
                if not self.shield_on and diff(self.spawn_t, time.time()) > 3:
                    if not rock.type == 1:
                        for a in range(0, 360, 360//rd.randint(2, 3)):
                            asteroides.append(asteroide(rock.pos, rock.type-1, rock.ori+a))
                    rock.type = 0
                    self.vies-=1
                    self.reset()
                    if self.vies<=0: self.alive=False
                else: rock.type-=1
        self.move()
        self.dessine(img)
def end(img_s, result=False):
    t = time.time()
    img = ecris(copy.deepcopy(img_s), ('You won' if result else 'Game Over') + f'\n{frame.points}', hg, bd, 3, rouge)
    while diff(t, time.time()) < 1:
        if montre(img, nom_fenetre, destroy=non, ) == 27: raise EXIT
    wk = montre(img, nom_fenetre, destroy=non, attente=0)
    match wk:
        case 27: raise EXIT
        case _: return
def nuit_etoilee(size=[1920, 1080]):
    img = image(dimensions=size[::-1]+[3], remplissage=noir)
    pts = []
    for _ in range(rd.randint(300, 500)):
        pts.append([rd.randint(0, m) for m in size])
    for etoile in pts:
        cercle(img, etoile, rd.randint(1, 2), blanc, 0)
    return(img)
def main_():
    t = time.time()
    img_s = nuit_etoilee(frame.size)
    while diff(t, time.time()) < 3:
        wk = montre(ecris(copy.deepcopy(img_s), 'Welcome commander!\nYou\'re in charge of\nthe Maelstrom spaceship.\nGood luck!', hg, bd, 3, bleu, 10), nom_fenetre, attente=1, destroy=non)
        match wk:
            case 27: raise EXIT
    while True:
        if True: ## Vars ##
            frame.points = 0
            navette = vaisseau()
            navette.tirs = []
            img_s = nuit_etoilee(frame.size)
            asteroides = [asteroide() for _ in range(5)]
            ovnis = []
            bonuses = []
            etoiles = []
        while True:
            if True: ## Vars ##
                if len(ovnis+etoiles+asteroides) == 0: end(img_s, True); break
                img = copy.deepcopy(img_s)
                frame.dessine_bonuses(navette, img)
                ecris(img, f'{navette.shield_qt:.2f}', hg, [400, 200], 1, cyan, 3)
                ecris(img, f'{navette.vies}', bd, [1920-400, 1080-200], 1, cyan, 3)
                ecris(img, f'{frame.points}', hd, [1920-400, 200], 1, cyan, 3)
                navette.update(img, asteroides)
                if not navette.alive: end(img_s); break
                asteroides_to_remove = []
            if True: ## Spawn ##
                if rd.randint(0, 1000)==0: ovnis.append(ovni())
                if rd.randint(0, 1000)==0: bonuses.append(power_up(navette))
            if True: ## Update ##
                for ufo in ovnis:
                    ufo.move(navette, navette.tirs, asteroides)
                    if rd.randint(0, 10)==0:
                        ufo.shoote(navette) 
                    ufo.dessine(img)
                for etoile in etoiles:
                    etoile.move(navette.tirs)
                    etoile.dessine(img)
                for rock in asteroides:
                    rock.move(navette.tirs, asteroides)
                    if rock.type == 0:
                        asteroides_to_remove.append(rock)
                        continue
                    rock.dessine(img)
                for p_u in bonuses:
                    p_u.move(navette)
                    p_u.dessine(img)
            if True: ## Remove ##
                for p_u in bonuses:
                    if p_u.remove:
                        bonuses.remove(p_u)
                for rock in asteroides_to_remove:
                    frame.points += rock.points
                    asteroides.remove(rock)
                for etoile in etoiles:
                    if etoile.remove:
                        frame.points += round((etoile.live_t-diff(etoile.spawn_t, time.time()))*50)
                        etoiles.remove(etoile)
                for ufo in ovnis:
                    if ufo.remove:
                        frame.points += 400
                        ovnis.remove(ufo)
            montre(img, nom_fenetre, attente=1, destroy=non)
            if True: ## Get actions ##
                if keyboard.is_pressed('esc'): raise EXIT
                try:
                    if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                        navette.accel = True
                        inercie = [p*rd.randint(700, 1300)/10000 for p in coosCercle([0, 0], 10, navette.ori)]
                        navette.inercie += Vector2D(inercie[0], inercie[1])
                        inercie = [max_vel if p > max_vel else -max_vel if p < -max_vel else p for p in eval(str(navette.inercie))]
                        navette.inercie = Vector2D(inercie[0], inercie[1])
                    else: navette.accel = False
                    if (keyboard.is_pressed('down') or keyboard.is_pressed('s')) and bonus.retro_thrusters in navette.bonuses:
                        inercie = [p*rd.randint(700, 1300)/10000 for p in coosCercle([0, 0], -10, navette.ori)]
                        navette.inercie += Vector2D(inercie[0], inercie[1])
                        inercie = [max_vel if p > max_vel else -max_vel if p < -max_vel else p for p in eval(str(navette.inercie))]
                        navette.inercie = Vector2D(inercie[0], inercie[1])
                    if keyboard.is_pressed('left') or keyboard.is_pressed('a'):navette.ori-=rd.randint(250, 350)/100*game_vel
                    if keyboard.is_pressed('right') or keyboard.is_pressed('d'):navette.ori+=rd.randint(250, 350)/100*game_vel
                    if keyboard.is_pressed(' '): navette.shield()
                    elif navette.shield_on and diff(navette.spawn_t,time.time())>=immunity_time:
                        navette.shield_qt -= diff(navette.shield_t, time.time())
                        navette.shield_on = False
                    if keyboard.is_pressed('tab') or keyboard.is_pressed('alt'): navette.shoote()
                except: pass
def main():
    try: main_()
    except EXIT: ferme(nom_fenetre)
if __name__ == "__main__":
    main()