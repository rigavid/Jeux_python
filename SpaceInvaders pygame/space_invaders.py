import pygame, random, os
from pygame.locals import *
from images import *; images()

class player:
    vel_shoot = 1
    shoot_1 = -90
    def __init__(self, shoots=[]) -> None:
        self.shoots = shoots
    class shoot_:
        def __init__(self, pos, vel, a=-90) -> None:
            self.pos, self.vel, self.a = pos, vel, a
        def update(self) -> None: ## Changer la position ##
            self.pos = coosCercle()
    def shoot(self) -> None:
        self.shoots.append(self.shoot_(self.pos, player.vel_shoot, player.shoot_a))
    def update(self) -> None:
        for shoot in self.shoots: shoot.update()

class alien:
    alien_pos = [0,0]
    invaders = {"Small":0, "Medium":0, "Large":0}
    names = ["Small", "Medium", "Large"]
    types = ["Squid", "Crab", "Octopus"]
    def __init__(self, pos, type=0) -> None:
        self.pos, self.type = pos, type
        self.name = f"Invader <{alien.types[self.type]:<7}> nº{alien.invaders[alien.names[self.type]]:<2}"
        alien.invaders[alien.names[self.type]] += 1
        self.n = alien.invaders[alien.names[self.type]]
        self.img = pygame.image.load("./imgs/icon.png")
    def show(self, surface) -> None:
        w, h = pygame.display.get_surface().get_size()
        surface.blit(self.img, self.get_coos())
    def get_coos(self):
        return [round(alien.alien_pos[i]+self.pos[i]) for i in [0,1]]
    def __str__(self) -> str:
        return f"{self.name} @ [{self.pos[0]:<4}, {self.pos[1]:<4}]"
class game:
    offset = [5, 10]
    start_pos, end_pos = [offset[0], offset[1]], [resolution[0]-offset[0], resolution[1]/3-offset[1]]
    print(start_pos, end_pos)
    with open("./highscores.txt", "r") as file:
        highscores = eval(file.read())
    def __init__(self, joueur:player=player([])) -> None:
        self.player = joueur
        
        lx, ly = game.start_pos; gx, gy = game.end_pos
        self.enemis = [ alien([x,y], round(typ/6*3))
            for x in range2(lx,gx,diff(lx, gx)/11) ## 11 columns
            for typ, y in enumerate(range2(ly,gy+1,diff(ly, gy)/5)) ## 5 rows 
        ]
pygame.init()
def main():
    min_w, min_h = resolution
    surface = pygame.display.set_mode(resolution, RESIZABLE)
    ts = pygame.image.load("./imgs/ts_img.png") ## titlescreen
    bg = pygame.image.load("./imgs/bg_img.png") ## background
    pygame.mouse.set_visible(False)
    pygame.display.set_icon(pygame.image.load("./imgs/icon.png"))
    pygame.display.set_caption(__file__[::-1].split("/")[0][::-1])
    surface.blit(ts, (0, 0))
    gaming = True; startGame = False
    while gaming:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:  
                return
            elif event.type == pygame.KEYDOWN:
                key = event.dict["key"]
                match key:
                    case 27: gaming = False
                    case 102: pygame.display.toggle_fullscreen()
                    case 13: startGame = True
                    case 99: pass ## Key c -> configuration
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.size
                surface.blit(pygame.transform.scale(ts, event.dict['size']), (0,0))
        if startGame:
            running  = True
            joueur = player([])
            jeu = game(joueur)
            surface.blit(pygame.transform.scale(bg, surface.get_size()), (0,0))
            while running:
                for enemi in jeu.enemis: enemi.show(surface)
                for event in pygame.event.get():
                    print(event)
                    if event.type == pygame.QUIT:  
                        return
                    elif event.type == pygame.KEYDOWN:
                        key = event.dict["key"]
                        match key:
                            case 27: running = False
                            case 102: pygame.display.toggle_fullscreen()
                    elif event.type == pygame.VIDEORESIZE:
                        w, h = event.size; r = False
                        if w < min_w: w = min_w;r=True
                        if h < min_h: h = min_h;r=True
                        surface.blit(pygame.transform.scale(bg, event.dict['size']), (0,0))
                pygame.display.update()
                startGame = False
            surface.blit(pygame.transform.scale(ts, surface.get_size()), (0,0))
        pygame.display.update()
    return

if __name__ == "__main__":
    main()