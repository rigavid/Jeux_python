from pieces_tetris import *
from cvt2 import *
import keyboard

## TODO ##
## Save (high)scores in a highscores.txt ##


class layout:
    class frame_:
        def __init__(self, img=image.new_img(fond=col.white), pos=[0,0], name='frame0') -> None:
            self.name = name
            self.img = image(img=copy.deepcopy(img))
            self.pos = pos
        def __str__(self) -> str:
            return self.name
    def __init__(self, img=image.new_img(), frames=[]) -> None:
        self.img = image(img=copy.deepcopy(img))
        self.frames = frames
    def frame(self, img=image.new_img(fond=col.white, dimensions=[100, 100]), pos=[0,0], name=None):
        if name == None:
            name = 'frame' + str(len(self.frames))
        fenetre = self.frame_(img=img, pos=pos, name=name)
        self.frames.append(fenetre)
        return fenetre
    def montre(self, debug=False, frames=None, except_frames=[]):
        img = image(img=copy.deepcopy(self.img.img))
        if frames == None: frames = copy.deepcopy(self.frames)
        for frm in except_frames:
            ind = [i.name for i in frames].index(frm.name)
            if ind != -1: frames.pop(ind)
        for frame in frames:
            img.img = fusionImages(frame.img.img, img.img, frame.pos)
            if debug:
                img.rectangle(frame.pos, [frame.pos[0]+len(frame.img.img[0]), frame.pos[1]+len(frame.img.img)], col.red, 3)
        self.img = img
        return img.montre(1, fullscreen=True)

class toucheException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

class gameOverException(Exception):
    def __init__(self, score=""):
        self.message = f'Your score was: {score} points'
        super().__init__(self.message)

class stopGameException(Exception):
    def __init__(self, score=""):
        self.message = f'Your score was: {score} points'
        super().__init__(self.message)

class piece:
    def __init__(self, tipe) -> None:
        self.deployed = False
        self.tipe = pieces[tipe]
        self.rot = rd.randint(0,3)%len(self.tipe)
        self.forme = self.tipe[self.rot]
        self.pos = [round(n_c_X/2-2), 0]
        return None
    def rotate(self, v, arr) -> None:
        '''
        :v: doit être soit `1` soit `-1`
        '''
        for x in range(5):
            for y in range(5):
                if self.forme[y,x] != 0:
                    arr[y+self.pos[1],x+self.pos[0]] = 0        
        self.rot += v
        if self.rot < 0: self.rot += len(self.tipe)
        if self.rot >= len(self.tipe): self.rot -= len(self.tipe)
        self.forme = self.tipe[self.rot]
        try: self.set(arr)
        except toucheException:
            self.rot -= v
            if self.rot < 0: self.rot += 4
            if self.rot > 3: self.rot-=4
            self.forme = self.tipe[self.rot]
            self.set(arr)
        return None
    def set(self, arr) -> None:
        for x in range(5):
            for y in range(5):
                if self.forme[y,x] != 0:
                    iy, ix = y+self.pos[1],x+self.pos[0]
                    if iy>=n_c_Y or ix>=n_c_X or iy<0 or ix<0: raise toucheException
                    elif arr[iy, ix] != 0: raise toucheException
        for x in range(5):
            for y in range(5):
                if self.forme[y,x] != 0:
                    arr[y+self.pos[1],x+self.pos[0]] = self.forme[y,x]
        self.deployed = True
        return None
    def overset(self, arr) -> None:
        for x in range(5):
            for y in range(5):
                if self.forme[y,x] != 0:
                    arr[y+self.pos[1],x+self.pos[0]] = self.forme[y,x]
        self.deployed = True
        return None
    def remove(self, arr) -> None:
        for x in range(5):
            for y in range(5):
                try:
                    if self.forme[y,x] != 0:
                        arr[y+self.pos[1],x+self.pos[0]] = 0
                except IndexError: pass
        self.deployed = False
        return None
    def dessine(self, img, offset=[0,0]) -> None:
        ofs = 2
        dx, dy = offset
        for x in range(5):
            for y in range(5):
                if self.forme[y,x] != 0:
                    chg, cbd = [cols[self.pos[0]+x]+dx,rows[self.pos[1]+y]+dy], [cols[self.pos[0]+x+1]+dx,rows[self.pos[1]+y+1]+dy]
                    p1, p4 = [p+ofs for p in chg], [p-ofs for p in cbd]
                    p2, p3 = [p4[0],p1[1]], [p1[0],p4[1]]
                    ct = ct_cr(p1,p2,p3,p4)
                    c1, c2, c3, c4 = [ct_sg(ct, pt) for pt in [p1,p2,p3,p4]]
                    cg , cd  = ct_sg(p1, p3), ct_sg(p2, p4)
                    cgh, cgb = ct_sg(cg, p1), ct_sg(cg, p3)
                    cdh, cdb = ct_sg(cd, p2), ct_sg(cd, p4)
                    couls = [[n_entre(v-20*i, 0, 255) for v in couleurs[self.forme[y,x]-1]] for i in range(5)]
                    img.rectangle(c1, c4, couls[0],0)
                    img.rectangle(p1, cdh, couls[1], 0)
                    img.rectangle(c2, cdb, couls[2], 0)
                    img.rectangle(cgh, c3, couls[3], 0)
                    img.rectangle(cgb, p4, couls[4], 0)
                    img.triangle(p2, c2, cdh, couls[2], 0)
                    img.triangle(p4, c4, cdb, couls[2], 0)
                    img.triangle(p1, c1, cgh, couls[3], 0)
                    img.triangle(p3, c3, cgb, couls[3], 0)
                    img.ligne(p2, p4, couls[2], 1)
        return None
    def is_over(self, arr) -> bool:
        if self.deployed: return False
        for x in range(5):
            for y in range(5):
                try:
                    if arr[self.pos[1]+y, self.pos[0]+x] != 0:
                        if self.forme[y,x] != 0:
                            return True
                except IndexError: pass
        return False
    def move(self, arr, w=[0,1]) -> None:
        game_over = self.is_over(arr)
        if game_over:
            self.overset(arr)
            raise gameOverException(score)
        else:
            self.remove(arr)
            self.save_pos = self.pos
            self.pos = [self.pos[n]+w[n] for n in range(2)]
            self.set(arr)
        return None

def updateImg(jeu):
    jeu.img = image(img=copy.deepcopy(imgJeu.img))
    for x in range(n_c_X):
        for y in range(n_c_Y):
            if matrice[y,x] != 0:
                chg, cbd = [cols[x],rows[y]], [cols[x+1],rows[y+1]]
                p1, p4 = [p+ofst for p in chg], [p-ofst for p in cbd]
                p2, p3 = [p4[0],p1[1]], [p1[0],p4[1]]
                ct = ct_cr(p1,p2,p3,p4)
                c1, c2, c3, c4 = [ct_sg(ct, pt) for pt in [p1,p2,p3,p4]]
                cg , cd  = ct_sg(p1, p3), ct_sg(p2, p4)
                cgh, cgb = ct_sg(cg, p1), ct_sg(cg, p3)
                cdh, cdb = ct_sg(cd, p2), ct_sg(cd, p4)
                couls = [[n_entre(v-20*i, 0, 255) for v in couleurs[matrice[y,x]-1]] for i in range(5)]
                jeu.img.rectangle(c1, c4, couls[0],0)
                jeu.img.rectangle(p1, cdh, couls[1], 0)
                jeu.img.rectangle(c2, cdb, couls[2], 0)
                jeu.img.rectangle(cgh, c3, couls[3], 0)
                jeu.img.rectangle(cgb, p4, couls[4], 0)
                jeu.img.triangle(p2, c2, cdh, couls[2], 0)
                jeu.img.triangle(p4, c4, cdb, couls[2], 0)
                jeu.img.triangle(p1, c1, cgh, couls[3], 0)
                jeu.img.triangle(p3, c3, cgb, couls[3], 0)
                jeu.img.ligne(p2, p4, couls[2], 1)
    return jeu


### GAME VARS ###
n_c_X, n_c_Y = [10, 22]
gameType = 0
n_of_levels = 30
level = 0
#################
couleurs = [col.red, col.blue, col.green, col.cyan, col.magenta, col.yellow, col.new('535353'), col.new('808080'), col.new('d0d0d0'), col.red, col.blue, col.green, col.cyan, col.magenta, col.yellow, col.new('535353'), col.new('808080'), col.new('d0d0d0'), col.red, col.blue, col.green, col.cyan, col.magenta, col.yellow, col.new('535353'), col.new('808080'), col.new('d0d0d0'), col.red, col.blue, col.green, col.cyan, col.magenta, col.yellow, col.new('535353'), col.new('808080'), col.new('d0d0d0')]
rd.shuffle(couleurs) ## TO REMOVE ##
#################
if True: ## Vars ##
    n_c_X, n_c_Y = n_entre(n_c_X, 10, 20), n_entre(n_c_Y, 12, 30)
    sep_d = 20
    x, y = diff(p1[0], p4[0]), diff(p1[1], p4[1])
    r_x, r_y = x/n_c_X, y/n_c_Y
    d_x=d_y=r_y if r_x>r_y else r_x
    if True: ## Image de fond du jeu ##
        imgJeu = image('grilleJeu', image.new_img(dimensions=[round(d_x*n_c_X), round(d_y*n_c_Y)], fond=col.white))
        offset_jeu = [round((x-(d_x*n_c_X))/2)+ct[0]-round(len(imgJeu.img)/2), round((y-(d_y*n_c_Y))/2)]
        for line_n in range(n_c_Y):
            imgJeu.ligne([0, d_y*line_n], [len(imgJeu.img), d_y*line_n], col.noir, 2)
        for col_n in range(n_c_X):
            imgJeu.ligne([d_x*col_n, 0], [d_x*col_n, len(imgJeu.img)], col.noir, 2)
    if True: ## Img next ##
        imgNext = image('grilleNext', image.new_img(dimensions=[round(d_x*5), round(d_y*5)*3+sep_d*2], fond=col.white))
        offset_next = [offset_jeu[0]+len(imgJeu.img[0])+sep_d, 0]
        strt = [0, 0]
        for _ in range(3):
            for colon in range(5):
                imgNext.ligne([strt[0]+d_x*colon, strt[1]], [strt[0]+d_x*colon, strt[1]+d_y*5], col.noir, 2)
            for ligne in range(5):
                imgNext.ligne([strt[0], strt[1]+d_y*ligne], [strt[0]+d_x*5, strt[1]+d_y*ligne], col.noir, 2)
            strt[1] += d_y*5
            imgNext.rectangle(strt, [strt[0]+d_x*5, strt[1]+sep_d], col.noir, 0)
            strt[1] += sep_d
    if True: ## Img hold ##
        imgHold = image('grilleHold', image.new_img(dimensions=[round(d_x*5), round(d_y*5)], fond=col.white))
        for colon in range(5):
            imgHold.ligne([d_x*colon, 0], [d_x*colon, d_y*5], col.noir, 2)
        for ligne in range(5):
            imgHold.ligne([0, d_y*ligne], [d_x*5, d_y*ligne], col.noir, 2)
        offset_hold = [offset_jeu[0]-sep_d-len(imgHold.img[0]), 0]
    if True: ## Img pause ##
        imgPause = image(img=image.new_img(dimensions=[d_x*(n_c_X-1), d_y*(n_c_Y-1)], fond=col.cyan))
        offset_pause = [offset_jeu[0]+d_x/2, offset_jeu[1]+d_y/2]
    if True: ## Img scores ##
        offset_score = [offset_jeu[0]-sep_d-len(imgHold.img[0]), round(d_y*5+sep_d)]
        imgScore = image('scores', image.new_img(dimensions=[round(d_x*5), round(d_y*5)], fond=col.white))
    match gameType:
        case 0: pieces = tetraminos
        case 1: pieces = miniminos  + tetraminos
        case 2: pieces = tetraminos + pentaminos
        case 3: pieces = miniminos
        case 4: pieces = pentaminos
        case 5: pieces = miniminos  + tetraminos + pentaminos
    pieces = np.array(pieces)
    ly = layout()
    jeu = ly.frame(copy.deepcopy(imgJeu.img), offset_jeu, 'Matrix_frame')
    nex = ly.frame(copy.deepcopy(imgNext.img), offset_next, 'Nexts_frame')
    hol = ly.frame(copy.deepcopy(imgHold.img), offset_hold, 'Hold_frame')
    sco = ly.frame(copy.deepcopy(imgScore.img), offset_score, 'Score_frame')
    pause = ly.frame(copy.deepcopy(imgPause.img), offset_pause, 'Pause_frame')

    ht = len(jeu.img.img)+2
    lg = len(jeu.img.img[0])+2
    cols = [x for x in np.arange(0,lg,d_x)]
    rows = [y for y in np.arange(0,ht,d_y)]
    matrice = np.array([[0 for _ in range(n_c_X)] for _ in range(n_c_Y)])
    playing = piece(tipe=rd.randint(0, len(pieces)-1))
    playing.set(matrice)
    playing.dessine(jeu.img)
    next_ps = [piece(rd.randint(0,len(pieces)-1)) for _ in range(3)]
    holding = None
    temps = time.time()
    t = time.time()
    scoring = [0, 100, 300, 600, 1000, 1500]
    score = 9000
    last_score = 0
    ofst = 2
    vitesse = float_range(1, 0.13, n_of_levels)
if True: ## Controls ##
    fl_g = 2424832
    fl_d = 2555904
    fl_h = 2490368
    fl_b = 2621440
    keys_hold = [ord('c')]
    keys_soft_drop = [fl_b]
    keys_rotate = [fl_h]
    keys_left = [fl_g]
    keys_right = [fl_d]

try:
    time_to_advance = vitesse[level]
    soft_drop = False
    while True:
        end_p = False
        if holding != None:
            img = image(img=copy.deepcopy(imgHold.img))
            holding.dessine(img)
            hol.img = img
        img = image(img=copy.deepcopy(imgNext.img))
        for n, p in enumerate(next_ps):
            start = [0, (d_y*5+sep_d)*n]
            p.pos = [0, 0]
            p.dessine(img, start)
            nex.img = img
        sco.img = image(img=copy.deepcopy(imgScore.img))
        sco.img.ecris(str(score)+f'\n{level}/{n_of_levels}\n{time_to_advance:.2f}', [round(v) for v in [len(sco.img.img[0])//2, len(sco.img.img)//2]])
        wk = ly.montre(debug=True, except_frames=[pause])
        if True: ## Inputs ##
            if wk == 27: raise stopGameException
            elif wk == ord('z'): playing.rotate(-1, matrice)
            elif wk == ord('x'): playing.rotate(1, matrice)
            elif wk == ord('p'): ## Pause ##
                temps2 = time.time()
                while True:
                    wk = ly.montre(debug=True)
                    if wk == 27: raise stopGameException
                    elif wk == ord('p'): break
                temps -= diff(temps2, time.time())
            elif wk in keys_left:
                try:
                    playing.move(matrice)
                    playing.move(matrice, [0, -1])
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)
                    time_to_advance = 0.5
                try: playing.move(matrice, [-1,0])
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)
            elif wk in keys_right:
                try:
                    playing.move(matrice)
                    playing.move(matrice, [0, -1])
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)
                    time_to_advance = 0.5
                try: playing.move(matrice, [1,0])
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)
            elif wk in keys_rotate:
                try:
                    playing.move(matrice)
                    playing.move(matrice, [0, -1])
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)
                    time_to_advance = 0.5
                playing.rotate(1, matrice)
            elif wk in keys_hold:
                playing.remove(matrice)
                holding, playing = playing, holding
                if playing == None:
                    playing = next_ps.pop(0)
                    next_ps.append(piece(tipe=rd.randint(0, len(pieces)-1)))
                playing.pos = [round(n_c_X/2-2), 0]
                playing.set(matrice)
                
                
                holding.pos = [0, 0]
                time.sleep(0.3)
            if wk in keys_soft_drop:
                time_to_advance = vitesse[level]/20
                soft_drop = True
                soft_drop_t = time.time()
            elif soft_drop:
                if diff(soft_drop_t, time.time()) >= 0.1:
                    time_to_advance = vitesse[level]
                    soft_drop = False
            if keyboard.is_pressed('+'):
                print('+++')
            if keyboard.is_pressed('space'):
                cases_parcourues = 0
                try:
                    while True:
                        playing.move(matrice)
                        cases_parcourues += 1
                except toucheException:
                    playing.pos = playing.save_pos
                    playing.set(matrice)

                    playing = next_ps.pop(0)
                    next_ps.append(piece(tipe=rd.randint(0, len(pieces)-1)))

                    playing.pos = [round(n_c_X/2-2), 0]
                    t = time.time()
                    end_p = True
                score += cases_parcourues*2*level
                time.sleep(0.2)
        if diff(t,time.time()) > time_to_advance and not end_p:
            if time_to_advance == 0.5: time_to_advance = vitesse[level]
            t = time.time()
            try: playing.move(matrice)
            except toucheException:
                playing.pos = playing.save_pos
                playing.set(matrice)
                playing = next_ps.pop(0)
                playing.pos = [round(n_c_X/2-2), 0]
                next_ps.append(piece(tipe=rd.randint(0, len(pieces)-1)))
                end_p = True
        updateImg(jeu)
        if end_p:
            m = [list(l) for l in matrice]
            lgs = []
            lns = 0
            for l in m:
                if l.count(0) == 0:
                    lgs.append(l)
                    lns += 1
            for l in lgs: m.remove(l)
            m = m[::-1]
            for l in range(lns): m.append([0 for _ in range(n_c_X)])
            matrice = np.array(m[::-1])
            score += scoring[lns]*round(n_c_X/10)
            for _ in range(diff(score//10000,last_score//10000)):
                level += 1
                time_to_advance = vitesse[level]
            last_score = score
except gameOverException as e:
    temps = diff(temps, time.time())
    h = round(temps//3600)
    m = round((temps%3600)//60)
    s = round(temps%60)
    temps = f'{h:0>2}:{m:0>2}:{s:0>2}'
    print(f'Game Over!\nPoints : {score:0>8}\nTemps  : {temps}')
    img = ly.img
    #img.rectangle(offset_jeu, [offset_jeu[0]+n_c_X*d_x, haut], col.red, 0)
    img.ecris('Game over', ct_sg(offset_jeu, [offset_jeu[0]+n_c_X*d_x, haut]), col.vert, 3, 2)
    img.montre(1, fullscreen=True)
    t = time.time()
    while diff(t, time.time()) < 2:
        if img.montre(1, fullscreen=True) == 27: t=None; break
    if t != None:
        img.montre(0, fullscreen=True)
    # fusee(score)
except stopGameException: print('Game ended.')
#except Exception as e: print(e)