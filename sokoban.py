from Outils.cvt2 import *
from touches_sokoban import keys_j1
import keyboard as kb
class invalidLevel(Exception):
    def __init__(self) -> None:
        super().__init__('Le niveau est invalide')
class tableau:
    def __init__(self, level=0) -> None:
        level_names = os.listdir('./Sokoban_levels')
        if level > 0 and level < len(level_names):
            nom = level_names[level]
            with open(f'./Sokoban_levels/{nom}') as file:
                lev = file.read()
        else:
            nom = level_names[level]
            with open(f'./Sokoban_levels/{nom}') as file:
                lev = file.read()
        if nom[len(nom)-4::] == '.xsb':
            lev=lev.replace('-', ' ')
            lev=lev.replace('@', 's')
            lev=lev.replace('+', 'S')
            lev=lev.replace('$', 'k')
            lev=lev.replace('*', 'K')
            lev=lev.replace('#', 'X')
            lev=lev.replace('.', '+')
        r_l = [[c for c in l] for l in lev.split('\n')]
        lns = [len(l) for l in r_l]
        for ind in range(len(lns)):
            for _ in range(diff(lns[ind], max(lns))):
                r_l[ind].append(' ')
        self.level = np.array(r_l)
        self.pos = self.get_skbn_pos()
        nb = [0,0]
        for c in str(self):
            if c in 'SK+': nb[0] += 1
            if c in  'Kk': nb[1] += 1
        if nb[0] != nb[1]:
            print(lev)
            raise invalidLevel()
    def replaces(self, s='') -> str:
        s=s.replace(' ', '  ')
        s=s.replace('_', '  ')
        s=s.replace('X', '██')
        s=s.replace('s', '--')
        s=s.replace('S', '==')
        s=s.replace('k', '[]')
        s=s.replace('K', '##')
        s=s.replace('+', '<>')
        return s
    def __str__(self) -> str:
        s = ""
        for l in self.level:
            s += ''.join(i for i in l) + "\n"
        return s[:len(s)-1:]
    def imprimme(self) -> None:
        print(self.replaces(self.__str__()))
    def get_skbn_pos(self) -> list:
        for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    if self.level[y,x].lower() == 's':
                        return [x, y]
    def move(self, v=[0,0]) -> int:
        if abs(sum(v)) != 1 : return 0
        else:
            pos = self.pos
            a = [pos[i]+v[i] for i in [0,1]]
            if self.level[a[1], a[0]] in '+_ ':
                self.level[a[1], a[0]] = 's' if self.level[a[1], a[0]] != '+' else 'S'
                self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                self.pos = a
                return 1
            elif self.level[a[1], a[0]].lower() == 'k':
                if self.level[a[1]+v[1], a[0]+v[0]].lower() in '+_ ':
                    self.level[a[1]+v[1], a[0]+v[0]] = 'k' if self.level[a[1]+v[1], a[0]+v[0]] != '+' else 'K'
                    self.level[a[1], a[0]] = 'S' if self.level[a[1], a[0]].isupper() else 's'
                    self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                    self.pos = a
                    return 1
        return 0
    def is_fini(self) -> bool:
        for c in self.__str__():
            if c in 'k+': return False
        return True
moves =  [[ 0, 0],[ 0,-1],[ 0, 0]][::-1]+[[-1, 0],[ 0, 0],[ 1, 0]][::-1]+[[ 0, 0],[ 0,1],[ 0, 0]][::-1]+[[ 0, 0]]
minimum, maximum = 0, len(os.listdir('./Sokoban_levels'))
try:
    n_lev = 0
    while n_lev < maximum:
        arr=tableau(n_lev);r=False;moves=0
        clear_terminal();print(f'Level {n_lev:0>2}\nMoves {moves:0>4}');arr.imprimme()
        h=False
        while True:
            if True in [kb.is_pressed(k) for k in keys_j1.keys_left ]: r=True;val=[-1, 0]
            if True in [kb.is_pressed(k) for k in keys_j1.keys_right]: r=True;val=[ 1, 0]
            if True in [kb.is_pressed(k) for k in keys_j1.keys_up   ]: r=True;val=[ 0,-1]
            if True in [kb.is_pressed(k) for k in keys_j1.keys_down ]: r=True;val=[ 0, 1]
            if True in [kb.is_pressed(k) for k in keys_j1.keys_reset]: arr=tableau(n_lev);r=True;val=[0,0];moves=0
            if True in [kb.is_pressed(k) for k in keys_j1.keys_prev ]: n_lev=n_entre(n_lev-1,minimum,maximum-1);arr=tableau(n_lev);r=True;val=[0,0];moves=0;h=False
            if True in [kb.is_pressed(k) for k in keys_j1.keys_next ]: n_lev=n_entre(n_lev+1,minimum,maximum-1);arr=tableau(n_lev);r=True;val=[0,0];moves=0;h=False
            if r: moves+=arr.move(val);r=False;clear_terminal();print(f'Level {n_lev:0>2}\nMoves {moves:0>4}');arr.imprimme();print(arr.help);time.sleep(0.3)
            if arr.is_fini(): break
        n_lev+=1
    print('Well done!')
except invalidLevel as e:
    arr.imprimme()
    print(e)
except KeyboardInterrupt: pass