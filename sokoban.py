from Outils.cvt2 import *
import keyboard as kb

class invalidLevel(Exception):
    def __init__(self) -> None:
        super().__init__('Le niveau est invalide')

class tableau:
    def __init__(self, level=0) -> None:
        level_names = os.listdir('./Sokoban_levels')
        if level > 0 and level < len(level_names):
            with open(f'./Sokoban_levels/{level_names[level]}') as file:
                lev = file.read()
        else:
            with open(f'./Sokoban_levels/{level_names[0]}') as file:
                lev = file.read()
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
        if nb[0] != nb[1]: raise invalidLevel()
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
    def move(self, v=[0,0]) -> None:
        if abs(sum(v)) != 1 : return
        else:
            pos = self.pos
            a = [pos[i]+v[i] for i in [0,1]]
            if self.level[a[1], a[0]] in '+_':
                self.level[a[1], a[0]] = 's' if self.level[a[1], a[0]] != '+' else 'S'
                self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                self.pos = a
            elif self.level[a[1], a[0]].lower() == 'k':
                if self.level[a[1]+v[1], a[0]+v[0]].lower() in '+_':
                    self.level[a[1]+v[1], a[0]+v[0]] = 'k' if self.level[a[1]+v[1], a[0]+v[0]] != '+' else 'K'
                    self.level[a[1], a[0]] = 'S' if self.level[a[1], a[0]].isupper() else 's'
                    self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                    self.pos = a
    def is_fini(self) -> bool:
        for c in self.__str__():
            if c in 'k+': return False
        return True

'''
ly = layout()
jeu = ly.frame()
'''

arr = tableau(2)
moves =  [[ 0, 0],[ 0,-1],[ 0, 0]][::-1]+[[-1, 0],[ 0, 0],[ 1, 0]][::-1]+[[ 0, 0],[ 0,1],[ 0, 0]][::-1]+[[ 0, 0]]
clear_terminal()
r = False;arr.imprimme()
try:
    while True:
        if kb.is_pressed('a'): r=True;val=[-1, 0]
        if kb.is_pressed('d'): r=True;val=[ 1, 0]
        if kb.is_pressed('w'): r=True;val=[ 0,-1]
        if kb.is_pressed('s'): r=True;val=[ 0, 1]
        if r: arr.move(val);r = False;clear_terminal();arr.imprimme();time.sleep(0.2)
        if arr.is_fini(): print('Well done!');break
except KeyboardInterrupt: pass