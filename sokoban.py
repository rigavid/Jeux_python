from Outils.cvt2 import *
from touches_sokoban import keys_j1
import keyboard as kb
class invalidLevel(Exception):
    def __init__(self) -> None:
        super().__init__('Le niveau est invalide')
num_v = 30
num_v2 = 10
class tableau:
    champs_infos = ['Nom du niveau', 'Niveau par', 'Date de création']
    def __init__(self, level=0, ly=layout()) -> None:
        self.ly = layout()
        self.img_jeu = image.new_img(dimensions=[1920,980], fond=col.cyan)
        self.img_inf = image.new_img(dimensions=[1920, 100], fond=col.new('808080'))
        self.fr_jeu = self.ly.frame(img=copy.deepcopy(self.img_jeu))
        self.fr_inf = self.ly.frame(img=copy.deepcopy(self.img_inf), pos=[0,980])
        self.infos = {}
        level_names = os.listdir('./Sokoban_levels')
        if level > 0 and level < len(level_names):
            nom = level_names[level]
            with open(f'./Sokoban_levels/{nom}', 'r', encoding='utf8') as file:
                lev = file.read()
        else:
            nom = level_names[level]
            with open(f'./Sokoban_levels/{nom}', 'r', encoding='utf8') as file:
                lev = file.read()
        format = nom[len(nom)-nom[::-1].index('.')::]
        print(f'Format "{format}"')
        if format == 'xsb':
            lev=lev.replace('-', '_')
            lev=lev.replace('@', 's')
            lev=lev.replace('+', 'S')
            lev=lev.replace('$', 'k')
            lev=lev.replace('*', 'K')
            lev=lev.replace('#', 'X')
            lev=lev.replace('.', '+')
            self.infos = nom[::-1].split('.',1)[1][::-1]
        if format == 'txt':
            lev2 = '';i=0
            for l in lev.splitlines():
                if l.count('#')==0:
                    lev2+=l+'\n'
                else:
                    self.infos[tableau.champs_infos[i]] = l.replace('#','')
                    i += 1
            lev = lev2
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
        self.size = [len(self.level[0]), len(self.level)]
        x, y = [[diff(num_v+20,1900-num_v), diff(num_v+20,960-num_v)][n]//self.size[n] for n in (0,1)]
        self.s = s = min(x, y)
        lignes = []
        colonnes = []
        for x in range(num_v+20,1870,s)[0:self.size[0]:]: colonnes.append(x)
        for y in range(num_v+20,930,s)[0:self.size[1]:]: lignes.append(y)
        cases = []
        for y, l in enumerate(lignes):
            cases.append([])
            for c in colonnes:
                cases[y].append([c,l])
        self.cases = np.array(cases)
        self.moves = 0
        self.pushes = 0
    def replaces(self, s='') -> str:
        s=s.replace(' ', '  ')
        s=s.replace('!', '  ')
        s=s.replace('_', '  ')
        s=s.replace('-', '  ')
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
            if self.level[a[1], a[0]] in '+_ ':
                self.level[a[1], a[0]] = 's' if self.level[a[1], a[0]] != '+' else 'S'
                self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                self.pos = a
                self.moves += 1
            elif self.level[a[1], a[0]].lower() == 'k':
                if self.level[a[1]+v[1], a[0]+v[0]].lower() in '+_ ':
                    self.level[a[1]+v[1], a[0]+v[0]] = 'k' if self.level[a[1]+v[1], a[0]+v[0]] != '+' else 'K'
                    self.level[a[1], a[0]] = 'S' if self.level[a[1], a[0]].isupper() else 's'
                    self.level[pos[1], pos[0]] = '+' if self.level[pos[1], pos[0]].isupper() else '_'
                    self.pos = a
                    self.moves += 1
                    self.pushes += 1
    def is_fini(self) -> bool:
        for c in self.__str__():
            if c in 'k+': return False
        return True
    def montre(self):
        img = self.fr_jeu.img
        img.img = copy.deepcopy(self.img_jeu)
        for x in range(len(self.cases)):
            for y in range(len(self.cases[0])):
                a,d=self.cases[x,y],[v+self.s for v in self.cases[x,y]]
                b,c=[d[0],a[1]],[a[0],d[1]]
                p1,p2,p3,p4=[[v1-num_v+num_v2,v2-num_v] for v1,v2 in [a,b,c,d]]
                kase = self.level[x,y]
                match kase:
                    case 'k' | 'K': ## Caisse en fausse 3D
                        if kase.isupper():
                            img.ligne(a,d,col.red, 2)
                            img.ligne(b,c,col.red, 2)
                        coul = col.new('808080')
                        img.rectangle(p1,p4,coul, 0)
                        img.rectangle(p1,p4,col.black, 2)
                        img.rectangle(a,d,coul, 2)
                        for pt1,pt2 in [[p2,b],[p3,c],[p4,d]]:
                            img.ligne(pt1,pt2,coul,2)
                    case 's' | 'S': ## Perso
                        if kase.isupper():
                            img.ligne(a,d,col.red, 2)
                            img.ligne(b,c,col.red, 2)
                        coul = col.green
                        img.rectangle(p1,p4,coul, 0)
                        img.rectangle(p1,p4,col.black, 2)
                        img.rectangle(a,d,coul, 2)
                        for pt1,pt2 in [[p2,b],[p3,c],[p4,d]]:
                            img.ligne(pt1,pt2,coul,2)
                    case 'X': ## Mur en briques en fausse 3D
                        coul = col.magenta
                        img.rectangle(p1,p4,coul, 0)
                        img.rectangle(p1,p4,col.black, 2)
                        img.rectangle(a,d,coul, 2)
                        for pt1,pt2 in [[p2,b],[p3,c],[p4,d]]:
                            img.ligne(pt1,pt2,coul,2)
                    case '-' | '_': ## Espace pour marcher
                        pass
                    case '+': ## Espace pour marcher plus ZA
                        img.ligne(a,d,col.red, 2)
                        img.ligne(b,c,col.red, 2)
        if type(self.infos) == str:
            txt = f'{self.infos}'
        else:
            txt = '  '.join(f'{s}: {self.infos[s]}' for s in list(self.infos.keys()))
        txt += f'\t\tMoves: {self.moves:0>4}\tPushes: {self.pushes:0>4}'
        self.fr_inf.img.img = copy.deepcopy(self.img_inf)
        self.fr_inf.img.ecris(txt, [1920/2, 50])
        return self.ly.montre(True)

def main() -> None:
    minimum, maximum = 0, len(os.listdir('./Sokoban_levels'))
    try:
        n_lev = 0
        while n_lev < maximum:
            arr=tableau(n_lev);r=False
            clear_terminal();print(f'Level {n_lev:0>2}\nMoves {arr.moves:0>4}');arr.imprimme()
            h=False;arr.montre()
            while True:
                if True in [kb.is_pressed(k) for k in keys_j1.keys_left ]: r=True;val=[-1, 0]
                if True in [kb.is_pressed(k) for k in keys_j1.keys_right]: r=True;val=[ 1, 0]
                if True in [kb.is_pressed(k) for k in keys_j1.keys_up   ]: r=True;val=[ 0,-1]
                if True in [kb.is_pressed(k) for k in keys_j1.keys_down ]: r=True;val=[ 0, 1]
                if True in [kb.is_pressed(k) for k in keys_j1.keys_reset]: arr=tableau(n_lev);r=True
                if True in [kb.is_pressed(k) for k in keys_j1.keys_prev ]: n_lev=n_entre(n_lev-1,minimum,maximum-1);arr=tableau(n_lev);r=True;val=[0,0];h=False
                if True in [kb.is_pressed(k) for k in keys_j1.keys_next ]: n_lev=n_entre(n_lev+1,minimum,maximum-1);arr=tableau(n_lev);r=True;val=[0,0];h=False
                if True in [kb.is_pressed(k) for k in keys_j1.keys_endg ]: clear_terminal(); return
                if r:
                    arr.move(val);clear_terminal();print(f'Level {n_lev:0>2}\nMoves {arr.moves:0>4}\nPushes: {arr.pushes:0>4}');arr.imprimme()
                    r=False
                    if h: print(arr.help)
                    arr.montre()
                    time.sleep(0.2)
                arr.montre()
                if arr.is_fini(): break
                if kb.is_pressed('esc'): return
            n_lev+=1
        print('Well done!')
    except invalidLevel as e:
        arr.imprimme()
        print(e)
    except KeyboardInterrupt: pass
if __name__ == '__main__': main()