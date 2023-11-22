from Outils.cvt2 import *

class tableau:
    def __init__(self, level=0) -> None:
        level_names = os.listdir('./Sokoban_levels')
        if level > 0 and level < len(level_names):
            with open(f'./Sokoban_levels/{level_names[level]}') as file:
                lev = file.read()
        else:
            with open(f'./Sokoban_levels/{level_names[0]}') as file:
                lev = file.read()
        self.level = np.array([[c for c in l] for l in lev.split('\n')])
    def get_skbn_pos(self) -> list:
        for y in range(len(self.level)):
                for x in range(self.level[y]):
                    if self.level[x, y].lower() == 's':
                        return [x, y]
    def move(self, v=[0,0]) -> None:
        if sum(v) != 1 : return
        else:
            pos = self.get_skbn_pos()
            a = [pos[i]+v[i] for i in [0,1]]
            if self.level[a[1], a[0]] in '+_':
                self.level[a[1], a[0]] = 's' if self.level[a[1], a[0]] != '+' else 'S'
                self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
            elif self.level[a[1], a[0]].lower() == 'k':
                if self.level[a[1]+v[1], a[0]+v[0]].lower() in '+_':
                    self.level[a[1]+v[1], a[0]+v[0]] = 'k' if self.level[a[1]+v[1], a[0]+v[0]] != '+' else 'K'
                    self.level[a[1], a[0]] = 's' if self.level[a[1], a[0]].isupper() else 'S'
                    self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'

            



ly = layout()
jeu = ly.frame()

arr = tableau(1)
for l in arr.level:
    print(''.join(i for i in l))
