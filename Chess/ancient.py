from pyimager import *

oui = True
non = False
vert = [0, 255, 0]
bleu = [0, 0, 255]
rouge = [255, 0, 0]
noir = [0, 0, 0]
blanc = [255, 255, 255]
epaisseur = 9
c1, c2, c3, c4 = (690, 270), (1230, 270), (690, 810), (1230, 810)
plein = -1
taille = 1

def ordre_alphabetique(texte):
    texte = list(texte)
    texte.sort()
    return ''.join(i for i in texte)

if oui: ## Fonctions ##
    def liste_pts_sg(p1, p2, n_pts): ## Returne une liste ayant n_pts équidistants sur le ségment donné ##
            pts = []
            for i in range(n_pts):
                pts.append(pt_sg(p1, p2, i, n_pts))
            return(pts)
    def liste_nbs_sg(a, b, n_sgs): ## Returne une liste avec len() = n_sgs ## La liste contient les numéros de (a->b)/i for i in n_sgs ##
        diff = abs(a-b)
        dist = diff/n_sgs
        c = min(a, b)
        nbs = []
        for i in range(n_sgs+1):
            nbs.append(c+dist*i)
        return(nbs)
    def liste_numbs(start, end, step=1): ## Comme celle de ci dessus ## ## WHY??? ##
        num = np.linspace(start, end,(end-start)*int(1/step)+1).tolist()
        return [round(i, 2) for i in num]
    def rectangle_dist(img, p1=ct, dists=[50, 50], couleur=vert, epaisseur=epaisseur): ## Dessine un réctangles à partir d'un point & deux longeurs ##
        img.rectangle(p1, (int(p1[0] + dists[0]), int(p1[1] + dists[1])), couleur, epaisseur)
        return(img)
    def clicked_in(pos, boutton): ## Is pos between boutton[0] (haut gauche) and boutton[1] (bas droite) ##
        a_l_interieur = pos[0] >= boutton[0][0] and pos[0] <= boutton[1][0] and pos[1] >= boutton[0][1] and pos[1] <= boutton[1][1]
        return(a_l_interieur)

pieces_d_chaque_cote = True ## TODO TODO le faire un paramètre par défaut ##
## TODO un menu in-game ##
class nom:
    nom = 'Echecs'
if oui: ## Commentaires et TODO ##
    '''Ceci est le TODO et le DONE'''
    ## ADDON ##########################################
    ## Annuler les mouvements ######################### ## Option avant le début de la partie (depuis jeux.py) ##
    ## Rétablir les mouvements annulés ################ ## Option avant le début de la partie (depuis jeux.py) ##

    ## TODO ###########################################
    ## Anoncer si on sauve ou on charge une partie ####
    ## quand on demande le nom de la sauvegarde #######

    ###################################################
    ## Parties nulles list : ## Avancement ### TODO ###
    #### Pactées ############## · ## ## Cõfirm TODO ###
    #### Manque de materiel ### o ## ## Finish fait ###
    #### 50 mouvements ######## o ## ## Bouton fait ###
    #### 75 mouvements ######## o ## ## Finish fait ###
    #### Répétition 3 ######### o ## ## Bouton fait ###
    #### Répétition 5 ######### o ## ## Finish fait ###
    #### Pat ################## o ## ## Finish fait ###
    ###################################################
    pass
class glob:
    path_sauv = 'Depandances/Outils/Jeux/parties_sauvees.txt'
class echecs: ########################### Terminé ##
    if oui: ## Dessin des pièces ######## Terminé ##
        if oui: ### Anciens ###
            def dessine_pion(self, img, pt1, pt2, pt3, pt4, col1, col2): ########################## Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c4 = pt_sg(pt4, ct)
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                return(img)
            def dessine_pions(self, img, pt1, pt2, pt3, pt4, col1, col2): ######################### Terminé ##
                ep = self.ep
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                a, b = 2, 5
                p1, p2, p3, p4 = pt_sg(ct, pt1, a, b), pt_sg(ct, pt2, a, b), pt_sg(ct, pt3, a, b), pt_sg(ct, pt4, a, b)
                cg, cd, ch, cb = pt_sg(p1, p3), pt_sg(p2, p4), pt_sg(p1, p2), pt_sg(p3, p4)
                cdb = ct_sg(cd, p4)
                cgb = ct_sg(cg, p3)
                cth = ct_cr(p1, p2, cg, cd)
                ctb = ct_sg(cgb, cdb)
                ctbg = ct_sg(ctb, cgb)
                ctbd = ct_sg(ctb, cdb)
                img.rectangle(cgb, p4, col1, 0)
                img.rectangle(cgb, p4, col2, ep)
                img.polygon((ctbd, ctbg, cth), col1, 0)
                img.polygon((ctbd, ctbg, cth), col2, ep)
                img.circle(cth, round(dist(cth, ch)/1.5), col1, 0)
                img.circle(cth, round(dist(cth, ch)/1.5), col2, ep)
                return(img)
            def dessine_cavalier(self, img, pt1, pt2, pt3, pt4, col1, col2): ###################### Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c4 = pt_sg(pt4, ct)
                a, b = 1, 3
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), pt_sg(c1, ct, a, b), col1, 0)
                img.rectangle(ct_sg(pt1, c1), pt_sg(c1, ct, a, b), col2, self.ep)
                return(img)
            def dessine_fou(self, img, pt1, pt2, pt3, pt4, col1, col2): ########################### Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c2 = pt_sg(pt2, ct)
                c3 = pt_sg(pt3, ct)
                c4 = pt_sg(pt4, ct)
                cg = pt_sg(c1, c3)
                cd = pt_sg(c2, c4)
                cb = pt_sg(c3, c4)
                ch = pt_sg(c1, c2)
                a, b = 7, 5
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col1, 0)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col2, self.ep)
                img.line(ct_sg(ch, ct), ct_sg(cb, ct), col2, self.ep)
                img.line(ct_sg(cg, ct), ct_sg(cd, ct), col2, self.ep)
                return(img)
            def dessine_tour(self, img, pt1, pt2, pt3, pt4, col1, col2): ########################## Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c2 = pt_sg(pt2, ct)
                c3 = pt_sg(pt3, ct)
                c4 = pt_sg(pt4, ct)
                cg = pt_sg(c1, c3)
                cd = pt_sg(c2, c4)
                cb = pt_sg(c3, c4)
                ch = pt_sg(c1, c2)
                a, b = 3, 1
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), pt_sg(c1, ct, a, b), col1, 0)
                img.rectangle(ct_sg(pt1, c1), pt_sg(c1, ct, a, b), col2, self.ep)
                img.rectangle(ct_sg(pt2, c2), pt_sg(c2, ct, a, b), col1, 0)
                img.rectangle(ct_sg(pt2, c2), pt_sg(c2, ct, a, b), col2, self.ep)
                return(img)
            def dessine_dame(self, img, pt1, pt2, pt3, pt4, col1, col2): ########################## Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c2 = pt_sg(pt2, ct)
                c3 = pt_sg(pt3, ct)
                c4 = pt_sg(pt4, ct)
                cg = pt_sg(c1, c3)
                cd = pt_sg(c2, c4)
                a, b = 7, 5
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), ct_sg(c1, cg), col1, 0)
                img.rectangle(ct_sg(pt2, c2), ct_sg(c2, cd), col1, 0)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col1, 0)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), ct_sg(c1, cg), col2, self.ep)
                img.rectangle(ct_sg(pt2, c2), ct_sg(c2, cd), col2, self.ep)
                return(img)
            def dessine_roi(self, img, pt1, pt2, pt3, pt4, col1, col2, echec=False): ############## Terminé ##
                ct = ct_sg(ct_sg(pt1, pt2), ct_sg(pt3, pt4))
                c1 = pt_sg(pt1, ct)
                c2 = pt_sg(pt2, ct)
                c3 = pt_sg(pt3, ct)
                c4 = pt_sg(pt4, ct)
                cg = pt_sg(c1, c3)
                cd = pt_sg(c2, c4)
                cb = pt_sg(c3, c4)
                ch = pt_sg(c1, c2)
                if echec:
                    img.rectangle(pt1, pt4, rouge, 0)
                a, b = 7, 5
                img.rectangle(c1, c4, col1, 0)
                img.rectangle(c1, c4, col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), ct_sg(c1, cg), col1, 0)
                img.rectangle(ct_sg(pt2, c2), ct_sg(c2, cd), col1, 0)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col1, 0)
                img.rectangle(pt_sg(ct_sg(pt1, c1), ct_sg(pt2, c2), a, b), pt_sg(c1, c2, b, a), col2, self.ep)
                img.rectangle(ct_sg(pt1, c1), ct_sg(c1, cg), col2, self.ep)
                img.rectangle(ct_sg(pt2, c2), ct_sg(c2, cd), col2, self.ep)
                img.line(ct_sg(ch, ct), ct_sg(cb, ct), col2, self.ep)
                img.line(ct_sg(cg, ct), ct_sg(cd, ct), col2, self.ep)
                return(img)
    if oui: ## Variables par défaut ##### Terminé ##
        if oui: ## Points ##
            a, b = 1, 1
            m = 1.125
            p1, p2, p3, p4 = (0, 0), (int(ch[0]*m), 0), (0, haut), (int(ch[0]*m), haut)
            ct = ct_sg(ct_sg(p1, p4), ct_sg(p2, p3))
            a, b = 2, 1
            c1, c2, c3, c4 = pt_sg(p1, ct, a, b), pt_sg(p2, ct, a, b), pt_sg(p3, ct, a, b), pt_sg(p4, ct, a, b)
            ptt1, ptt2, ptt3, ptt4 = pt_sg(p1, c1, a), pt_sg(p2, c2, a), pt_sg(p3, c3, a), pt_sg(p4, c4, a)
            a, b = 5, 4
            ct1, ct2, ct3, ct4 = pt_sg(p1, ct, a, b), pt_sg(p2, ct, a, b), pt_sg(p3, ct, a, b), pt_sg(p4, ct, a, b)
        if oui: ## Langues ##
            francais = 'fr'
            esperanto = 'eo'
            english = 'en'
            catala = 'ca'
            espanol = 'es'
            langues = [francais, esperanto, english, catala, espanol]
        if oui: ## Couleurs ##
            gris = [30, 30, 30]
            argent = [200, 200, 200]
            dore = [200, 200, 100]
            marron_clair = [181, 113, 77]
            marron_clair2 = [120, 60, 30]
            marron_fonce = [101, 53, 37]
            blanc = [215, 215, 215]
            noir = [40, 40, 40]
            noir2 = [15, 15, 15]
            col_sel = COL.new('800080')
            bois_noir = [70, 43, 27]
            bord_bois_noir = [50, 23, 7]
            col_lin = [20, 20, 20]
            col = blanc
        if oui: ## Autres ##
            j1 = 'J1'
            j2 = 'J2'
            ep = 5
            a = 4
            cases = 8
            attente = 1
            numeros = '\n\n1\n\n2\n\n\n3\n\n4\n\n\n5\n\n6\n\n\n7\n\n8\n\n'[::-1]
            s = 'search'
            lettres = ' A B C D E F G H '
            class joueur:
                def __init__(self, nom):
                    self.nom = nom
            class waitkey:
                wk = 0
            class mouse:
                pos = None
            def getmouse(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    echecs.mouse.pos = [x, y]
                    echecs.waitkey.wk = 27
            num = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
            let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if oui: ## Partie ## ################ Terminé ##
        def rename(self, nom): ################################################# Terminé ##
            self.nom = nom
        def parties_sauvees(self): ############################################# Terminé ##
            fs = open(glob.path_sauv, 'r')
            parties_sauvees = fs.read()
            fs.close()
            parties = {}
            partie = ''
            cherche_nom = True
            nom = ''
            for i in parties_sauvees:
                if i == '\n':
                    parties[nom] = partie
                    partie = ''
                    cherche_nom = True
                    nom = ''
                elif cherche_nom:
                    if i == ' ':
                        cherche_nom = False
                    else:
                        nom += i
                else:
                    partie += i
            return(parties)
        def sauve_partie(self, nom_sauvegarde='Default'): ###################### Terminé ##
            if nom_sauvegarde == '': return(None)
            if nom_sauvegarde == 'Default': nom_sauvegarde = self.nom
            nom_sauvegarde = str(nom_sauvegarde)
            a, nom_sauvegarde = nom_sauvegarde, ''
            for i in a:
                if i == ' ':
                    i = '_'
                nom_sauvegarde += i
            bo = '{'
            bf = '}'
            tableau = '\'disposition_actuelle\':{'
            for i in self.echiquier:
                tableau += f'\'{i}\':{self.echiquier[i]}, '
            tableau = tableau[0:len(tableau)-2]
            tableau += '}'
            histo = '\'historique\':['
            for echiquie in self.historique:
                histo += '{'
                for i in echiquie:
                    histo += f' \'{i}\':{self.echiquier[i]}, '
                histo = histo[0:len(histo)-2]
                histo += '}, '
            histo = histo[0:len(histo)-2]
            histo += ']'
            partie = f'''{bo}\'nom_partie\':\'{self.nom}\', \'nom_j1\':\'{self.j1.nom}\', \'nom_j2\':\'{self.j2.nom}\', {tableau}, \'trait\':{self.trait}, \'dernier_mouve\':{self.dernier_mouve}, {histo}{bf}'''
            parties = self.parties_sauvees()
            parties[nom_sauvegarde] = partie
            a_ecrire = ''
            for i in parties:
                a_ecrire += f'{i} {parties[i]}\n'
            fs = open(glob.path_sauv, 'w')
            fs.write(a_ecrire)
            fs.close()
        def charge_partie(self, nom_sauvegarde): ############################### Terminé ##
            a, nom_sauvegarde = nom_sauvegarde, ''
            for i in a:
                if i == ' ':
                    i = '_'
                nom_sauvegarde += i
            parties = self.parties_sauvees()
            ya_pa = True
            for i in parties:
                if nom_sauvegarde == i:
                    ya_pa = False
                    partie = eval(parties[i])
            if ya_pa:
                self.sauve_partie('auto')
                self.charge_partie('auto')
                return(None)
            self.echiquier = partie['disposition_actuelle']
            self.j1 = self.joueur(partie['nom_j1'])
            self.j2 = self.joueur(partie['nom_j2'])
            self.dernier_mouve = partie['dernier_mouve']
            self.historique = partie['historique']
            self.nulle = False
            self.regle50mov = 0
            self.played = 0
            self.trait = partie['trait']
            self.moves = 0
            self.legalite = [False]
            self.jouable = True
            self.cherchant_echecs = False
            self.piece = '_'
            self.wk = 0
            self.image()
            self.exit = False
            self.jouer()
    if oui: ## Infos ## ################# Terminé ##
        def points(self, p): ################################################### Terminé ##
            match p:
                case 'p': return 1
                case 'c' | 'f': return 3
                case 't': return 5
                case 'd': return 9
                case _: return 0
        def avantage(self, jr): ################################################ Terminé ##
            if jr == '1':
                jr = True
            else:
                jr = False
            e = self.echiquier
            a = 0
            for j in e:
                for i in e[j]:
                    p = e[j][i][0]
                    if p != '_' and p != '.':
                        if p.isupper() == jr:
                            a += self.points(p.lower())
                        else:
                            a -= self.points(p.lower())
            return(a)          
        def captures(self, joueur): ############################################ Terminé ##
            x = False if joueur == '1' else True
            pas_capturees = ''
            e = self.echiquier
            for j in e:
                for i in e[j]:
                    case = e[j][i][0]
                    if case != '_' and case != '.':
                        if case.isupper() == x:
                            pas_capturees += case
            pas_capturees = pas_capturees.lower()
            captures = 'ppppppppttccffdr'
            captures = list(captures)
            for i in pas_capturees:
                try:
                    ind = captures.index(i)
                except:
                    captures.pop(0)
                else:
                    captures.pop(ind)
            captures = ordre_alphabetique(captures)
            return(captures)
        def gdye(self, piece): ################################################# Terminé ##
            tableau = self.echiquier
            for i in tableau:
                for j in tableau[i]:
                    if tableau[i][j][0] == piece:
                        return(i, j)
            return(False)
        def __str__(self) -> str:
            tableau = self.echiquier
            out = '    A  B  C  D  E  F  G  H\n'
            for i in tableau:
                outy = ''
                for j in tableau[i]:
                    smt = tableau[i][j][0] == '.'
                    outy += f'{tableau[i][j] if smt else tableau[i][j][0]}, '
                outy = outy[0:len(outy)-2]
                out += f'{i} : {outy}\n'
            out = out[0:len(out)-1]
            return(out)
        def imprime_tableau(self) -> None: ############################################# Terminé ##
            print(self.__str__())
        def getcase(self): ##################################################### Terminé ##
            coos = self.mouse.pos
            if coos != None:
                case = self.case
                for i in case:
                    if clicked_in(coos, [case[i][0], case[i][-1]]):
                        if self._t:
                            p = self.echiquier[i[1]][i[0]][0]
                            if p != '_' and p != '.' and p.isupper() == self.trait:
                                self.sw = True
                                self.img.rectangle(case[i][0], case[i][-1], vert, self.ep, 0)
                                self._1 = i ## Case de sortie ##
                                self._t = False
                                return(None)
                        else: ## Case d'arrivée ##
                            p = self.echiquier[i[1]][i[0]][0]
                            if p != '_' and p != '.' and p.isupper() == self.trait:
                                self.sw = True
                                self._1 = i
                                self._t = False
                                self.image()
                                self.img.rectangle(case[i][0], case[i][-1], vert, self.ep, 0)
                                return(None)
                            else:
                                self._2 = i
                                self._t = True
                                return(None)
    if oui: ## Légalité des pièces ## ### Terminé ##
        def promeut(self, ou): ################################################# Terminé ##
            self.image()
            stop = False
            img = self.img
            nomFenetre = self.nom
            a, b = 10, 6
            cl1, cl2, cl3, cl4 = self.c1, self.c2, self.c3, self.c4
            ct1, ct3 = pt_sg(cl1, cl3, a, b), pt_sg(cl1, cl3, b, a)
            ct2, ct4 = pt_sg(cl2, cl4, a, b), pt_sg(cl2, cl4, b, a)
            ptsh = [ct1, ct_sg(ct1, ct_sg(ct1, ct2)), ct_sg(ct1, ct2), ct_sg(ct2, ct_sg(ct1, ct2)), ct2]
            ptsb = [ct3, ct_sg(ct3, ct_sg(ct3, ct4)), ct_sg(ct3, ct4), ct_sg(ct4, ct_sg(ct3, ct4)), ct4]
            while True:
                self.image()
                if oui: ## Table de choix ##
                    img.rectangle(ct1, ct4, self.bois_noir, -1)
                    for i in range(len(ptsh)-1):
                        img.rectangle(ptsh[i], ptsb[i+1], self.bord_bois_noir, 5)
                    if self.trait:
                        col1 = [255, 255, 255]
                        col2 = [0, 0, 0]
                    else:
                        col1 = [0, 0, 0]
                        col2 = [255, 255, 255]
                    if oui: ## Dame ##
                        i = 0
                        pt1, pt2, pt3, pt4 = ptsh[i], ptsh[i+1], ptsb[i], ptsb[i+1]
                        self.dessine_dame(img, pt1, pt2, pt3, pt4, col1, col2)
                    if oui: ## Tour ##
                        i = 1
                        pt1, pt2, pt3, pt4 = ptsh[i], ptsh[i+1], ptsb[i], ptsb[i+1]
                        self.dessine_tour(img, pt1, pt2, pt3, pt4, col1, col2)
                    if oui: ## Fou ##
                        i = 2
                        pt1, pt2, pt3, pt4 = ptsh[i], ptsh[i+1], ptsb[i], ptsb[i+1]
                        self.dessine_fou(img, pt1, pt2, pt3, pt4, col1, col2)
                    if oui: ## Cavalier ##
                        i = 3
                        pt1, pt2, pt3, pt4 = ptsh[i], ptsh[i+1], ptsb[i], ptsb[i+1]
                        self.dessine_cavalier(img, pt1, pt2, pt3, pt4, col1, col2)
                img.setMouseCallback(echecs.getmouse)
                wk = img.show()
                if wk == 27: raise InterruptedError
                pos = self.mouse.pos
                if pos != None:
                    if pos[1] >= ptsh[0][1] and pos[1] <= ptsb[1][1]:
                        if pos[0] >= ct1[0] and pos[0] <= ct4[0]:
                            if pos[0] <= ptsb[1][0]:
                                self.save_echiquier[ou[1]][ou[0]] = 'D' if self.trait else 'd'
                            elif pos[0] <= ptsb[2][0]:
                                self.save_echiquier[ou[1]][ou[0]] = 'T' if self.trait else 't'
                            elif pos[0] <= ptsb[3][0]:
                                self.save_echiquier[ou[1]][ou[0]] = 'F' if self.trait else 'f'
                            else:
                                self.save_echiquier[ou[1]][ou[0]] = 'C' if self.trait else 'c'
                            stop = True
                            self.mouse.pos = None
                            self.waitkey.wk = 0
                if stop: break
        def leg_p(self, p1, p2): ############################################### Terminé ##
            x1, y1 = self.num[p1[0]], int(p1[1])
            x2, y2 = self.num[p2[0]], int(p2[1])
            piece = self.echiquier[p1[1]][p1[0]].lower() == 'p.'
            leg = False
            arv = self.echiquier[p2[1]][p2[0]]
            if self.echiquier[p1[1]][p1[0]][0].isupper():
                if x1 == x2:
                    if y2 - y1 == 1:
                        if arv == '_' or arv == '.':
                            leg = True
                    elif y2 - y1 == 2 and piece:
                        if self.echiquier[str(y1 + 1)][p1[0]] == '_' or self.echiquier[str(y1 + 1)][p1[0]] == '.':
                            if arv == '_' or arv == '.':
                                if not self.cherchant_echecs:
                                    self.save_echiquier[str((int(p1[1]) + int(p2[1]))//2)][p1[0]] = '..1'
                                leg = True
                elif abs(x1 - x2) == 1 and (y1 - y2) == -1:
                    if self.echiquier[p2[1]][p2[0]][-1] == '2':
                        if not self.imageant_m:
                            self.save_echiquier[p1[1]][p2[0]] = '_'
                        leg = True
                    elif self.echiquier[p2[1]][p2[0]] != '_' and self.echiquier[p2[1]][p2[0]][-1] != '1' and self.echiquier[p2[1]][p2[0]][-1] != '2':
                        leg = True
            else:
                if x1 == x2:
                    if y1 - y2 == 1:
                        if arv == '_' or arv == '.':
                            leg = True
                    elif y1 - y2 == 2 and piece:
                        if self.echiquier[str(y1 - 1)][p1[0]] == '_' or self.echiquier[str(y1 - 1)][p1[0]] == '.':
                            if arv == '_' or arv == '.':
                                if not self.cherchant_echecs:
                                    self.save_echiquier[str((int(p1[1]) + int(p2[1]))//2)][p1[0]] = '..2'
                                leg = True
                elif abs(x1 - x2) == 1 and (y1 - y2) == 1:
                    if self.echiquier[p2[1]][p2[0]][-1] == '1':
                        if not self.imageant_m:
                            self.save_echiquier[p1[1]][p2[0]] = '_'
                        leg = True
                    elif self.echiquier[p2[1]][p2[0]] != '_' and self.echiquier[p2[1]][p2[0]][-1] != '1' and self.echiquier[p2[1]][p2[0]][-1] != '2':
                        leg = True                        
            if not self.imageant_m:
                if leg and not self.cherchant_echecs:
                    if p2[1] == '1' or p2[1] == '8':
                        self.promeut(p1)
            return(leg)
        def leg_r(self, p1, p2): ############################################### Terminé ##
            x1, y1 = self.num[p1[0]], int(p1[1])
            x2, y2 = self.num[p2[0]], int(p2[1])
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                return(True)
            elif self.echiquier[p1[1]][p1[0]].lower() == 'r.':
                if y1 == y2 and abs(x1 - x2) == 2:
                    echec = self.echec('R' if self.trait else 'r')
                    if echec: return(False)
                    else:
                        if p2[0] == 'g':
                            if self.echiquier[str(y1)]['f'] == '_':
                                if self.echiquier[str(y1)]['g'] == '_':
                                    if self.echiquier[str(y1)]['h'].lower() == 't.':
                                        '''self.echiquier[str(y1)]['e'] = '_'
                                        self.echiquier[str(y1)]['f'] = 'R' if self.trait else 'r' '''
                                        echec = self.echec('R' if self.trait else 'r', 'f1' if self.trait else 'f8', 'R' if self.trait else 'r')
                                        if not echec:
                                            self.save_echiquier[str(y1)]['f'] = 'T' if self.trait else 't'
                                            self.save_echiquier[str(y1)]['h'] = '_'
                                            return(True)
                                        else:
                                            return(False)
                        if p2[0] == 'c':
                            if self.echiquier[str(y1)]['d'] == '_':
                                if self.echiquier[str(y1)]['c'] == '_':
                                    if self.echiquier[str(y1)]['b'] == '_':
                                        if self.echiquier[str(y1)]['a'].lower() == 't.':
                                            '''self.echiquier[str(y1)]['e'] = '_'
                                            self.echiquier[str(y1)]['d'] = 'R' if self.trait else 'r' '''
                                            echec = self.echec('R' if self.trait else 'r', 'd1' if self.trait else 'd8', 'R' if self.trait else 'r')
                                            if not echec:
                                                self.save_echiquier[str(y1)]['d'] = 'T' if self.trait else 't'
                                                self.save_echiquier[str(y1)]['a'] = '_'
                                                return(True)
                                            else:
                                                return(False)
            return(False)
        def leg_f(self, p1, p2): ############################################### Terminé ##
            x1, y1 = self.num[p1[0]], int(p1[1])
            x2, y2 = self.num[p2[0]], int(p2[1])
            vide = []
            if x1 == x2:
                pass
            if abs(x1 - x2) == abs(y1 - y2):
                if x1 > x2:
                    xs = [self.let[i] for i in range(x2-1, x1)][::-1]
                else:
                    xs = [self.let[i] for i in range(x1-1, x2)]
                if y1 > y2:
                    ys = [str(i) for i in range(y2, y1+1)][::-1]
                else:
                    ys = [str(i) for i in range(y1, y2+1)]
                xs.pop(0)
                ys.pop(0)
                xs.pop(-1)
                ys.pop(-1)
                for i in range(len(xs)):
                    case = self.echiquier[ys[i]][xs[i]][0]
                    if case == '_':
                        vide.append(True)
                    elif case == '.':
                        vide.append(True)
                    else:
                        vide.append(False)
            else:
                return(False)
            for i in vide:
                if i == False:
                    return(False)
            return(True)
        def leg_t(self, p1, p2): ############################################### Terminé ##
            x1, y1 = self.num[p1[0]], int(p1[1])
            x2, y2 = self.num[p2[0]], int(p2[1])
            if x1 == x2:
                vide = []
                if y1 > y2:
                    ys = [str(i) for i in range(y2, y1+1)][::-1]
                else:
                    ys = [str(i) for i in range(y1, y2+1)]
                ys.pop(0)
                ys.pop(-1)
                for i in ys:
                    case = self.echiquier[i][self.let[x1-1]][0]
                    if case == '_':
                        vide.append(True)
                    elif case == '.':
                        vide.append(True)
                    else:
                        vide.append(False)
            elif y1 == y2:
                vide = []
                if x1 > x2:
                    xs = [self.let[i] for i in range(x2-1, x1)][::-1]
                else:
                    xs = [self.let[i] for i in range(x1-1, x2)]
                xs.pop(0)
                xs.pop(-1)
                for i in xs:
                    case = self.echiquier[str(y1)][i][0]
                    if case == '_' or case == '.':
                        vide.append(True)
                    else:
                        vide.append(False)
            else:
                return(False)
            for i in vide:
                if i == False:
                    return(False)
            return(True)
        def leg_d(self, p1, p2): ############################################### Terminé ##
            if self.leg_f(p1, p2):
                return(True)
            else:
                return(self.leg_t(p1, p2))
        def leg_c(self, p1, p2): ############################################### Terminé ##
            x1, y1 = self.num[p1[0]], int(p1[1])
            x2, y2 = self.num[p2[0]], int(p2[1])
            if abs(x1 - x2) == 1 and abs(y1 - y2) == 2:
                return(True)
            elif abs(x1 - x2) == 2 and abs(y1 - y2) == 1:
                return(True)
            return(False)
        def echec(self, roi, q=s, r=''): ####################################### Terminé ##
            self.cherchant_echecs = True
            tableau = self.echiquier
            self.save_trait = self.trait
            detect_echecs = []
            if q == self.s:
                gde = self.gdye(roi)
                pt2 = gde[1]+gde[0]
            else:
                pt2 = q
                roi = r if r != '' else tableau[q[1]][q[0]][0]
            self.trait = roi.islower()
            for j in tableau:
                for i in tableau[j]:
                    piece = tableau[j][i][0]
                    if piece != '_' and piece != '.':
                        if piece.islower() == roi.isupper():
                            pt1 = i+j
                            detect_echecs.append(self.legaly(pt1, pt2))
            self.cherchant_echecs = False
            self.trait = self.save_trait
            for i in detect_echecs:
                if i:
                    return(True)
            return(False)
        def legal(self, p1, p2, y=False): ###################################### Terminé ##
            self.save = copy.deepcopy(self.echiquier) ## Crée une sauvegarde ##
            self.save_echiquier = copy.deepcopy(self.echiquier) ## Duplique l'échiquier ##
            self.legalite.append(self.legaly(p1, p2)) ## Vérifie la légalité du coup ##
            if self.legalite[-1]: ## Si le coup est légal ##
                self.echiquier[p2[1]][p2[0]] = self.echiquier[p1[1]][p1[0]][0] ## Mouve pièce ##
                self.echiquier[p1[1]][p1[0]] = '_' ## Vide la case d'où la pièce part ##
                if self.echec('R' if self.trait else 'r'): ## Si le roi a qui est le tour est échec ##
                    self.legalite[-1] = False ## Mouvement déclaré illégal ##
                    self.tableau = self.save ## Le tableau est rétabli ##
                    self.echiquier = self.save ## Le tableau est rétabli ##
                    self.image() ## L'image est régénérée ##
                else:
                    self.echiquier = self.save_echiquier ## L'échiquier dupliqué devient le principal ##
            if y:
                self.tableau = self.save
        def legaly(self, p1, p2): ############################################## Terminé ##
            leg = False
            if p1 == p2:
                return(False)
            else:
                piece = self.echiquier[p1[1]][p1[0]]
                if piece == '_':
                    return(False)
                elif piece[0] == '.':
                    return(False)
                elif piece[0] == ' ':
                    return(False)
                else:
                    if piece.islower() != self.echiquier[p2[1]][p2[0]][0].islower() or self.echiquier[p2[1]][p2[0]] == '_' or self.echiquier[p2[1]][p2[0]][0] == '.':
                        if piece.isupper() == self.trait:
                            piece = piece.lower()[0]
                            if piece == 'p':
                                leg = self.leg_p(p1, p2)
                            elif piece == 'r':
                                leg = self.leg_r(p1, p2)
                            elif piece == 't':
                                leg = self.leg_t(p1, p2)
                            elif piece == 'f':
                                leg = self.leg_f(p1, p2)
                            elif piece == 'c':
                                leg = self.leg_c(p1, p2)
                            elif piece == 'd':
                                leg = self.leg_d(p1, p2)
                            else:
                                return(False)
                            self.piece = piece
                            return(leg)
                        else:
                            return(False)
                    else:
                        return(False)
    if oui: ## Légalité d'la partie ## ## Terminé ##
        def detecte_maty(self): ################################################ Terminé ##
            echiquier = self.echiquier
            for j in echiquier:
                for i in echiquier[j]:
                    piece = echiquier[j][i]
                    if piece != '_' and piece != '.' and piece.isupper() == self.trait:
                        p1 = i + j
                        for jj in echiquier:
                            for ii in echiquier[jj]: ## Bouge toutes les pieces pour savoir si un roi est mat ##
                                p2 = ii + jj
                                self.cherchant_echecs = True
                                self.legal(p1, p2)
                                leg = self.legalite[-1]
                                self.legalite.pop(-1)
                                self.cherchant_echecs = False
                                if leg:
                                    return(True)
            if self.echec('R' if self.trait else 'r'): ## Mat ##
                self.cause_fin = 'blancs_m' if not self.trait else 'noirs_m'
                return(False)
            else: ## Pat ##
                self.cause_fin = 'nulle'
                self.nulle = 'pat'
                return(False)
        def detecte_mat(self): ################################################# TODO ##
            self.jouable = self.detecte_maty() ## Redirection, why ??? TODO ##
        def mat_au_pas(self): ################################################## Terminé ##
            ## Géstion pour permettre le mat au pas ##
            e = self.echiquier
            for j in e:
                for i in e[j]:
                    c = e[j][i]
                    if c == '..1':
                        e[j][i] = '.1'
                    elif c == '..2':
                        e[j][i] = '.2'
                    elif c == '.1':
                        e[j][i] = '_'
                    elif c == '.2':
                        e[j][i] = '_'
        def detecte_nulle_par_rep(self): ####################################### Terminé ? ##
            tableaux = []
            for i in self.historique:
                tableaux.append(str(i))
            for i in tableaux:
                cnt = -1
                for j in tableaux:
                    if j == i:
                        cnt += 1
            if cnt >= 5:
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = '5repetition'
                return(None)
            if cnt >= 3:
                self.rep5 = True
        def detecte_nulle_par_materiel(self): ################################## Terminé ##
            if oui: ## Vars ##
                blancs = []
                noirs = []
                for i in self.echiquier:
                    for j in self.echiquier[i]:
                        p = self.echiquier[i][j][0]
                        if p != '_' and p != '.':
                            if p.isupper():
                                blancs.append(p.lower())
                            else:
                                noirs.append(p)
                blancs.sort()
                noirs.sort()
            if blancs == ['r'] and noirs == ['r']: ## Seulement les rois ##
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = 'materiel'
                return(None)
            if blancs == ['f', 'r'] and noirs == ['r']: ## Seulement les rois et un fou ##
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = 'materiel'
                return(None)
            if blancs == ['r'] and noirs == ['f', 'r']: ## Seulement les rois et un fou ##
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = 'materiel'
                return(None)
            if blancs == ['c', 'r'] and noirs == ['r']: ## Seulement les rois et un cavalier ##
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = 'materiel'
                return(None)
            if blancs == ['r'] and noirs == ['c', 'r']: ## Seulement les rois et un cavalier ##
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = 'materiel'
                return(None)
            if blancs == ['f', 'r'] and noirs == ['f', 'r']: ## Seulement les rois et un fou chaqu'un s'ils sont sur la même couleur ##
                f1 = self.gdye('F')
                f2 = self.gdye('f')
                x1, y1 = int(f1[1]), self.num[f1[0]]
                x2, y2 = int(f2[1]), self.num[f2[0]]
                if x1%2 == x2%2 and y1%2 == y2%2:
                    self.jouable = False
                    self.cause_fin = 'nulle'
                    self.nulle = 'materiel'
                    return(None)
        def detecte_nulle_50_moves(self): ###################################### Terminé ##
            if self.regle50mov >= 150:
                self.jouable = False
                self.cause_fin = 'nulle'
                self.nulle = '75'
                return(None)
            elif self.regle50mov >= 100:
                self.reg50mov = True
        def detecte_nulle(self): ############################################### en cours (bogues ?) ##
            self.detecte_nulle_par_rep()
            self.detecte_nulle_50_moves()
            self.detecte_nulle_par_materiel()
    if oui: ## Trucs sur la classe ## ### Terminé ##
        def __init__(self, nom=nom.nom, j1=j1, j2=j2, langue='eo', tourne=non, help=non, dev=non): ## Terminé ##
            if oui: ## Vars ##
                self.begin_playing = False
                self.result = [0, 0]
                if j1 != self.j1.lower() and j2 != self.j2.lower():
                    tirage = [j1, j2]
                    rd.shuffle(tirage)
                    j1, j2 = tirage[0], tirage[1]
                self.dev = dev
                self.sw = False
                self.imageant = False
                self.imageant_m = True
                self.dernier_mouve = 0
                self.p1 = self.p2
                self.p2 = hd
                self.p3 = self.p4
                self.p4 = bd
                self.nom = nom
                self.j1 = self.joueur(j1)
                self.j2 = self.joueur(j2)
                self.tourne = tourne
                self.echiquier = {
                    '8':{'a':'t.','b':'c', 'c':'f', 'd':'d', 'e':'r.','f':'f', 'g':'c', 'h':'t.'}, 
                    '7':{'a':'p.','b':'p.','c':'p.','d':'p.','e':'p.','f':'p.','g':'p.','h':'p.'}, 
                    '6':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '5':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '4':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '3':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '2':{'a':'P.','b':'P.','c':'P.','d':'P.','e':'P.','f':'P.','g':'P.','h':'P.'}, 
                    '1':{'a':'T.','b':'C', 'c':'F', 'd':'D', 'e':'R.','f':'F', 'g':'C', 'h':'T.'}
                }
                self.historique = [copy.deepcopy(self.echiquier)]
            if oui: ## Langues ##
                self.langue = 'eo'
                for i in self.langues:
                    if langue == i:
                        self.langue = langue
                        break
                if self.langue == self.francais:
                    self.player = 'Jouer !'
                    self.charger = 'Charger !'
                    self.illegal_move = 'Mouvement illégal !'
                    self.fin_partie = 'Partie finie !'
                    self.replay = 'Rejouer ?'
                    self.causes_fin_partie = {
                        'blancs_m':'Les blancs gagnent\npar ´echec et mat !',
                        'noirs_m':'Les noirs gagnent\npar ´echec et mat !',
                        'blancs_a':'Les blancs gagnent\npar abandon !',
                        'noirs_a':'Les noirs gagnent\npar abandon !',
                        'nulle':{
                            'pat':'Pat !',
                            'accordee':'Nulle par\naccord mutuel.',
                            'materiel':'Nulle par\nmanque de materiel.', 
                            '50':'Nulle par la\nr`egle des 50 coups.',
                            '75':'Nulle par la\nr`egle des 75 coups',
                            '3repetition':'Nulle par\nr´ep´etition.',
                            '5repetition':'Nulle par\nr´ep´etition.'
                            },
                        'interomp':'Partie interrompue.'
                        }
                elif self.langue == self.esperanto:
                    self.player = 'Ludi!'
                    self.charger = '^Car^gi!'
                    self.fin_partie = 'Fini^gita ludo!'
                    self.illegal_move = 'Kontrala˘uregula movado!'
                    self.replay = 'Reludi ?'
                    self.causes_fin_partie = {
                        'blancs_m':'La blankoj venkis\nper ^sakmato!',
                        'noirs_m':'La nigroj venkis\nper ^sakmato!',
                        'blancs_a':'La blankoj venkis\nper kapitulacio!',
                        'noirs_a':'La nigroj venkis\nper kapitulacio!',
                        'nulle':{
                            'pat':'Senmovi^gio!',
                            'accordee':'Sendecido per\ninterkonsento.',
                            'materiel':'Sendecido per\ninsufi^can\nmaterialon.', 
                            '50':'Sendecido per\nla la˘uregula de\nla 50 movoj.',
                            '75':'Sendecido per\nla la˘uregula de\nla 75 movoj.',
                            '3repetition':'Sendecido\nper ripeto.',
                            '5repetition':'Sendecido\nper ripeto.'
                            },
                        'interomp':'Interrompita ludo .'
                        }
                elif self.langue == self.english:
                    self.player = 'Play!'
                    self.charger = 'Load!'
                    self.illegal_move = 'Illegal move!'
                    self.fin_partie = 'Game over!'
                    self.replay = 'Replay?'
                    self.causes_fin_partie = {
                        'blancs_m':'Whites won\nby checkmate!',
                        'noirs_m':'Blacks won\nby checkmate!',
                        'blancs_a':'Whites won\nby Blaks\' resign!',
                        'noirs_a':'Blacks won\nby Whithes\' resign!',
                        'nulle':{
                            'pat':'Stalemate!',
                            'accordee':'Draw by\nagreement.',
                            'materiel':'Dead position.', 
                            '50':'Draw by\n50\'s rule',
                            '75':'Draw by\n75\'s rule',
                            '3repetition':'Threefold\nrepetition.',
                            '5repetition':'Fivefold\nrepetition.'
                            },
                        'interomp':'Interromped game.'
                        }
                elif self.langue == self.catala:
                    self.player = 'Jugar!'
                    self.charger = 'Carregar'
                    self.illegal_move = 'Moviment il.legal!'
                    self.fin_partie = 'Partida acabada!'
                    self.replay = 'Tornar a jugar'
                    self.causes_fin_partie = {
                        'blancs_m':'Les blanques guanyen\nper escac i mat!',
                        'noirs_m':'Les negres guanyen\nper escac i mat!',
                        'blancs_a':'Les blanques guanyen\nper aband´o!',
                        'noirs_a':'Les negres guanyen\nper aband´o!',
                        'nulle':{
                            'pat':'Ofegat!',
                            'accordee':'Taules pactades.',
                            'materiel':'Nul.la per manca\nde material.', 
                            '50':'Taules per la\nnorma dels\n50 moviments.',
                            '75':'Taules per la\nnorma dels\n75 moviments.',
                            '3repetition':'Taules per\nrepetici´o.',
                            '5repetition':'Taules per\nrepetici´o.'
                            },
                        'interomp':'Partida interrompuda'
                        }
                elif self.langue == self.espanol:
                    self.player = '!Jugar!'
                    self.charger = '!Cargar!'
                    self.illegal_move = '!Movimiento ilegal!'
                    self.fin_partie = '!Partida terminada!'
                    self.replay = '?Volver a jugar?'
                    self.causes_fin_partie = {
                        'blancs_m':'!Las blancas ganan\npor jaque mate!',
                        'noirs_m':'!Las negras ganan\npor jaque mate!',
                        'blancs_a':'!Las blancas ganan\npor abandono!',
                        'noirs_a':'!Las negras ganan\npor abandono!',
                        'nulle':{
                            'pat':'Pat !',
                            'accordee':'Tablas pactadas.',
                            'materiel':'Tablas por\nfalta de material.', 
                            '50':'Tablas por la\nnorma de los\n50 movimientos.',
                            '75':'Tablas por la\nnorma de los\n75 movimientos.',
                            '3repetition':'Tablas por\nrepetici´on.',
                            '5repetition':'Tablas por\nrepetici´on.'
                            },
                        'interomp':'Partida interrompuda.'
                        }
            if oui: ## Autres Vars ##
                self.help = help
                self.rep5 = False
                self.reg50mov = False
                self.wk = 0
                self._t = True
                self._1 = 0
                self._2 = 0
                self.nulle = False
                self.regle50mov = 0
                self.played = 0
                self.trait = True
                self.moves = 0
                self.legalite = [False]
                self.jouable = True
                self.cherchant_echecs = False
                self.piece = '_'
                self.wk = 0
                self.c1 = list(c1).copy()
                self.c2 = list(c2).copy()
                self.c3 = list(c3).copy()
                self.c4 = list(c4).copy()
                self.image()
        def __str__(self): ##################################################### Terminé ##
            return(self.nom)
        def rejouer(self): ##################################################### Terminé ##
            if oui: ## Vars ##
                self.sw = False
                self.rep5 = False
                self.mouse.pos = None
                self.waitkey.wk = 0
                self.imageant = False
                self.imageant_m = True
                self.dernier_mouve = 0
                self.j1, self.j2 = self.j2, self.j1
                self.echiquier = {
                    '8':{'a':'t.','b':'c', 'c':'f', 'd':'d', 'e':'r.','f':'f', 'g':'c', 'h':'t.'}, 
                    '7':{'a':'p.','b':'p.','c':'p.','d':'p.','e':'p.','f':'p.','g':'p.','h':'p.'}, 
                    '6':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '5':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '4':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '3':{'a':'_', 'b':'_', 'c':'_', 'd':'_', 'e':'_', 'f':'_', 'g':'_', 'h':'_'}, 
                    '2':{'a':'P.','b':'P.','c':'P.','d':'P.','e':'P.','f':'P.','g':'P.','h':'P.'}, 
                    '1':{'a':'T.','b':'C', 'c':'F', 'd':'D', 'e':'R.','f':'F', 'g':'C', 'h':'T.'}
                }
                self.historique = [copy.deepcopy(self.echiquier)]
            if oui: ## Autres Vars ##
                self.wk = 0
                self._t = True
                self._1 = 0
                self._2 = 0
                self.nulle = False
                self.exit = False
                self.regle50mov = 0
                self.played = 0
                self.trait = True
                self.moves = 0
                self.legalite = [False]
                self.jouable = True
                self.cherchant_echecs = False
                self.piece = '_'
                self.wk = 0
                self.c1 = list(c1).copy()
                self.c2 = list(c2).copy()
                self.c3 = list(c3).copy()
                self.c4 = list(c4).copy()
                self.cause_fin = ''
                self.nulle = ''
                self.reg50mov = False
                self.image()
        def menuy(self): ####################################################### Terminé ##
            if oui: ## Vars ##
                nomFenetre = self.nom
                img = self.img
                p1, p2, p3, p4, ct = echecs.ct1, echecs.ct2, echecs.ct3, echecs.ct4, echecs.ct
                cg, cd, ch, cb = ct_sg(p1, p3), ct_sg(p2, p4), ct_sg(p3, p4), ct_sg(p3, p4)
                dis1 = 50
                dis2 = 125
                cgph, cdpb = [cg[0] + dis1, cg[1]-dis2], [cd[0] - dis1, cd[1]+dis2]
            if oui: ## Dessin boutton jouer ##
                img.rectangle(cgph, cdpb, echecs.marron_clair, 0)
                img.rectangle(cgph, cdpb, echecs.marron_fonce, echecs.ep)
                ecris(img, self.player, cgph, cdpb, 4, noir, echecs.ep)
            player = False
            while True:
                img.setMouseCallback(echecs.getmouse)
                wk = img.show()
                if wk == 27: ## End of program ##
                    self.exit = True
                    break
                coos = self.mouse.pos
                if coos != None:
                    if clicked_in(coos, [cgph, cdpb]): ## Start game = True ##
                        self.image()
                        self.mouse.pos = None
                        player = True
                        break
            return(player)
        def menu(self): ######################################################## Terminé ##
            if not self.begin_playing:
                j = self.menuy()
                if j: ## Play ##
                    rj = self.jouer()
                else: ## Menuy ##
                    rj = False
            else:
                rj = self.jouer()
            while True:
                if self.exit: ## End of program ##
                    break
                if rj: ## Restart a game ##
                    self.rejouer()
                    rj = ex = self.jouer()
                else: ## Go to menu ##
                    self.rejouer()
                    rj = self.menuy()
        def start(self): ####################################################### Terminé ##
            try:
                while True:
                    self.menu()
                    if self.exit: ## End of program ##
                        break
            except InterruptedError:
                pass
            except Exception as ERREUR:
                print(ERREUR)
    if oui: ## Imagaison ## ############# Terminé ##
        def disquette(self, img, c1, c2, c3, c4): ############################## Terminé ##
            img.rectangle(c1, c4, bleu, 0)
            img.rectangle(c1, pt_sg(pt_sg(c1, c3, 5, 2), pt_sg(c2, c4, 5, 2), 2, 5), self.dore, 0)
            img.rectangle(c2, pt_sg(pt_sg(c1, c3, 5, 2), pt_sg(c2, c4, 5, 2), 2, 5), self.argent, 0)
            img.rectangle(c1, c4, self.gris, self.ep)
            img.rectangle(pt_sg(c1, c3, 5, 2), c4, self.gris, self.ep)
            img.rectangle(pt_sg(c1, c2, 2, 5), pt_sg(pt_sg(c1, c3, 5, 2), pt_sg(c2, c4, 5, 2), 5, 2), self.gris, self.ep//2)
            ctht = ct_sg(pt_sg(c1, c3, 5, 2), pt_sg(c2, c4, 5, 2))
            img.line(ct_sg(c1, c2), ctht, self.gris, self.ep//2)
            img.circle(ct_sg(ct_sg(c3, c4), ctht), dist(c1, c2)//6, self.argent, 0)
            img.circle(ct_sg(ct_sg(c3, c4), ctht), dist(c1, c2)//6, self.gris, self.ep//2)
            img.circle(ct_sg(ct_sg(c3, c4), ctht), self.ep//2, self.gris, 0)
            return(img)
        def bords_echiquier(self, img, ptt1, ptt2, ptt3, ptt4, trait=True): #### Terminé ##
            cases = 9
            cf = 0.5
            cmb = 1 if trait or not self.tourne else -1
            marron = [157, 113, 83]
            case = round((ptt2[0] - ptt1[0]) / cases) # Définition de la taille d'une case.
            img.rectangle(ptt1, ptt4, marron, plein)
            # Dessin des lettres et nes nombres sur les bords de l'échequier.
            x = 0.9 if trait or not self.tourne else 7.9
            y = 0.3
            cv2.putText(img.img, 'A', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'B', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'C', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'D', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'E', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'F', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'G', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'H', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            x = 0.9 if trait or not self.tourne  else 7.9
            y = 8.875
            cv2.putText(img.img, 'A', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'B', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'C', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'D', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'E', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'F', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'G', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            cv2.putText(img.img, 'H', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));x += cmb
            x = 0.125
            y = 1.05 if trait or not self.tourne  else 8.05
            cv2.putText(img.img, '8', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '7', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '6', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '5', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '4', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '3', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '2', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '1', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            x = 8.69
            y = 1.05 if trait or not self.tourne  else 8.05
            cv2.putText(img.img, '8', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '7', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '6', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '5', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '4', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '3', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '2', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            cv2.putText(img.img, '1', (round(ptt1[0] + case * x), round(ptt1[1] + case * y)), cv2.FONT_HERSHEY_TRIPLEX, taille, noir, round(taille * 2.5));y += cmb
            # Remplissage des coins de l'échequier.
            coins = [61, 61, 61]
            img.rectangle(ptt1, (round(ptt1[0] + case * cf), round(ptt1[1] + case * cf)), coins, plein)
            img.rectangle(ptt2, (round(ptt2[0] - case * cf), round(ptt2[1] + case * cf)), coins, plein)
            img.rectangle(ptt3, (round(ptt3[0] + case * cf), round(ptt3[1] - case * cf)), coins, plein)
            img.rectangle(ptt4, (round(ptt4[0] - case * cf), round(ptt4[1] - case * cf)), coins, plein)
            # Délimitations des lignes sur les bords de l'échequier.
            a1 = ptt1
            for i in liste_numbs(0, cases):
                i -= 0.5
                img.line((round(a1[0] + case * i), a1[1]), (round(a1[0] + case * i), ptt3[1]), self.gris, epaisseur)
            for i in liste_numbs(0, cases):
                i -= 0.5
                img.line((a1[0], round(a1[1] + case * i)), (ptt2[0], round(a1[1] + case * i)), self.gris, epaisseur)
            self.taiy_caz = case
            return(img)
        def table_joueur(self, img, joueur, p1, p2, p3, p4): ################### Terminé ##
            if oui: ## Séléction des données ##
                cap = self.captures(joueur)
                if joueur == '1':
                    col1, col2 = noir, blanc
                    joueur = self.j1
                    avantage = self.avantage('1')
                else:
                    col1, col2 = blanc, noir
                    joueur = self.j2
                    avantage = self.avantage('2')
                a, b = 5, 2
                if avantage >= 0:
                    avantage = '+' + str(avantage)
                else:
                    avantage = str(avantage)
                nom = joueur.nom
            if oui: ## Représentation des données en strings ##
                jrb = pt_sg(p1, p3, a, b)
                avh = pt_sg(p1, p2, b, a)
                avb = pt_sg(jrb, pt_sg(p2, p4, a, b), b, a)
                img.rectangle(p1, p4, self.marron_clair, 0)
                img.rectangle(p1, p4, self.marron_fonce, 5)
            if oui: ## Cadre ##
                img.line(jrb, pt_sg(p2, p4, a, b), self.marron_fonce, 5)
                img.line(avh, avb, self.marron_fonce, 5)
            if oui: ## Infos ##
                img.write(avantage, ct_sg(avh, pt_sg(p2, p4, a, b)), noir, echecs.ep, 2.25)
                img.write(nom, ct_sg(p1, avb), noir, echecs.ep, 2.25)
            if oui: ## Vars ##
                a, b = p3, pt_sg(p2, p4, a, b)
                points_x = liste_nbs_sg(a[0], b[0], 6)
                points_y = liste_nbs_sg(a[1], b[1], 3)
                ind1 = 0
                cazes = {}
                for j in range(len(points_x)-1):
                    for i in range(len(points_y)-1):
                        cazes[str(j) + str(i)] = [[points_x[j], points_y[i]], [points_x[j+1], points_y[i]], [points_x[j], points_y[i+1]], [points_x[j+1], points_y[i+1]]]
            for index, piece in enumerate(cap): ## Dessine les pièces capturées ##
                ind1 = index%6
                ind2 = index//6
                caze = cazes[str(ind1) + str(ind2)]
                p1, p2, p3, p4 = caze
                if piece == 'p':
                    self.dessine_pion(img, p1, p2, p3, p4, col1, col2)
                elif piece == 'd':
                    self.dessine_dame(img, p1, p2, p3, p4, col1, col2)
                elif piece == 'f':
                    self.dessine_fou(img, p1, p2, p3, p4, col1, col2)
                elif piece == 'c':
                    self.dessine_cavalier(img, p1, p2, p3, p4, col1, col2)
                elif piece == 'r':
                    self.dessine_roi(img, p1, p2, p3, p4, col1, col2)
                elif piece == 't':
                    self.dessine_tour(img, p1, p2, p3, p4, col1, col2)
            return(img)
        def image(self): ####################################################### Terminé ##
            self.imageant = True
            if oui: ## Echiquier ##
                if oui: ## Vars ##
                    p1, p2, p3, p4, ct = echecs.p1, echecs.p2, echecs.p3, echecs.p4, echecs.ct
                    taille_case = (haut - (abs(p1[1] - echecs.ptt1[1]) * 2)) / self.cases
                    img = new_img(background=COL.black)
                    self.bords_echiquier(img, p1, p2, p3, p4, self.trait)
                    case = {}
                    nums = '87654321'
                    lets = 'abcdefgh'
                    if self.trait == False and self.tourne:
                        lets = lets[::-1]
                        nums = nums[::-1]
                    bl, no = self.marron_clair, self.noir2
                    self.col = no
                for i in range(self.cases):
                    for j in range(self.cases):
                        pt1 = [int(self.ptt1[0] + taille_case * i), int(self.ptt1[1] + taille_case * j)]
                        pt2 = [int(self.ptt1[0] + taille_case * (i + 1)), int(self.ptt1[1] + taille_case * (j + 1))]
                        case[f'{lets[i]}{nums[j]}'] = (pt1, [pt2[0], pt1[1]], [pt1[0], pt2[1]], pt2) ## Coos d'une case ##
                        if self.col == bl:
                            img.rectangle(pt1, pt2, self.col, 0)
                            self.col = no
                        else:
                            img.rectangle(pt1, pt2, self.col, 0)
                            self.col = bl
                    if self.col == bl:
                        self.col = no
                    else:
                        self.col = bl
                distancia = self.taiy_caz/5*3
                if oui: ## Cadre ##
                    img.rectangle(coosCircle(p1, distancia, 45), coosCircle(p4, distancia, 225), [30, 30, 30], epaisseur)
                    img.rectangle(p1, p4, [30, 30, 30], epaisseur)
            if oui: ## Pièces ##
                for i in lets:
                    for j in nums:
                        char = self.echiquier[j][i][0] ## Get case content ##
                        if char != '_' and char != '.':
                            if not self.tourne: ## Set case orientation ##
                                if pieces_d_chaque_cote:
                                    if char.isupper():
                                        pt1, pt2, pt3, pt4 = case[i + j]
                                    else:
                                        pt4, pt3, pt2, pt1 = case[i + j]
                                else:
                                    pt1, pt2, pt3, pt4 = case[i + j]
                            else:
                                if self.trait: ## Set case orientation ##
                                    if char.isupper():
                                        pt1, pt2, pt3, pt4 = case[i + j]
                                    else:
                                        pt4, pt3, pt2, pt1 = case[i + j]
                                else:
                                    if char.islower():
                                        pt1, pt2, pt3, pt4 = case[i + j]
                                    else:
                                        pt4, pt3, pt2, pt1 = case[i + j]
                            if char.islower(): ## Set piece color ##
                                col1 = [0, 0, 0]
                                col2 = [255, 255, 255]
                            else: ## Set piece color ##
                                col1 = [255, 255, 255]
                                col2 = [0, 0, 0]
                            char = char.lower()
                            if oui: ## Dessin de la pièce ##
                                if char == 'p':
                                    self.dessine_pion(img, pt1, pt2, pt3, pt4, col1, col2)
                                elif char == 'd':
                                    self.dessine_dame(img, pt1, pt2, pt3, pt4, col1, col2)
                                elif char == 'f':
                                    self.dessine_fou(img, pt1, pt2, pt3, pt4, col1, col2)
                                elif char == 'c':
                                    self.dessine_cavalier(img, pt1, pt2, pt3, pt4, col1, col2)
                                elif char == 'r':
                                    echec = self.echec(self.echiquier[j][i][0])
                                    self.dessine_roi(img, pt1, pt2, pt3, pt4, col1, col2, echec)
                                elif char == 't':
                                    self.dessine_tour(img, pt1, pt2, pt3, pt4, col1, col2)
                for i in lets:
                    for j in nums:
                        case_sel = i+j
                        if self.dernier_mouve != False:
                            if case_sel == self.dernier_mouve[0] or case_sel == self.dernier_mouve[1]: ## Marque les cases du dernier mouvement ##
                                pt1, pt2, pt3, pt4 = case[i + j]
                                img.rectangle(pt1, pt4, COL.cyan, self.ep)
            if oui: ## UI ##
                if oui: ## Vars ##
                    p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
                    cg, cd, ch, cb = ct_sg(p1, p3), ct_sg(p2, p4), ct_sg(p1, p2), ct_sg(p3, p4)
                    ct = ct_cr(p1, p2, p3, p4)
                    cth, ctb, ctg, ctd = ct_sg(ct, ch), ct_sg(ct, cb), ct_sg(ct, cg), ct_sg(ct, cd)
                    a, b = 1, 2
                    cth1, cth2, cth3, cth4 = pt_sg(cth, p1, a, b), pt_sg(cth, p2, a, b), pt_sg(cth, cg, a, b), pt_sg(cth, cd, a, b)
                    ctb1, ctb2, ctb3, ctb4 = pt_sg(ctb, cg, a, b), pt_sg(ctb, cd, a, b), pt_sg(ctb, p3, a, b), pt_sg(ctb, p4, a, b)
                if oui: ## Tables joueurs ##
                    if self.tourne:
                        self.table_joueur(img, '2' if self.trait else '1', cth1, cth2, cth3, cth4)
                        self.table_joueur(img, '1' if self.trait else '2', ctb1, ctb2, ctb3, ctb4)
                    else:
                        self.table_joueur(img, '2', cth1, cth2, cth3, cth4)
                        self.table_joueur(img, '1', ctb1, ctb2, ctb3, ctb4)
                if self.dev:
                    for i in [cg, cd, ch, cb]:
                        point(img, i)
                    for i in [ct]:
                        point(img, i, COL.new('ff00ff'))
                    for i in [cth, ctb, ctg, ctd]:
                        point(img, i, bleu)
                    for i in [p1, p2, p3, p4]:
                        point(img, i, vert)
                self.ct, self.cg, self.cd, self.ch, self.cb = ct, cg, cd, ch, cb
            if oui: ## Bouttons d'abandon ##
                if oui: ## Vars ##
                    tb = 100
                    dv = 3
                    hg, hd, bg, bd = [p2[0]-tb, p2[1]], p2, [p2[0]-tb, p2[1]+tb], [p2[0], p2[1]+tb]
                    if not self.tourne or self.trait:
                        self.bt_abandonJ2 = [hg, bd]
                    else:
                        self.bt_abandonJ1 = [hg, bd]
                    ct = [p2[0]-tb//2, p2[1]+tb//2]
                    c1, c2, c3, c4 = coosCircle(ct, tb/dv, -135), coosCircle(ct, tb/dv, -45), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                if oui: ## Boutton abandon 1 ##
                    img.rectangle(bg, hd, self.marron_clair, 0)
                    img.rectangle(bg, hd, self.marron_fonce, self.ep)
                    img.line(c1, c4, self.gris, self.ep)
                    img.line(c2, c3, self.gris, self.ep)
                if oui: ## Vars ##
                    tb = 100
                    dv = 3
                    hg, hd, bg, bd = [p4[0]-tb, p4[1]-tb], [p4[0], p4[1]-tb], [p4[0]-tb, p4[1]], p4
                    if not self.tourne or self.trait:
                        self.bt_abandonJ1 = [hg, bd]
                    else:
                        self.bt_abandonJ2 = [hg, bd]
                    ct = [p4[0]-tb//2, p4[1]-tb//2]
                    c1, c2, c3, c4 = coosCircle(ct, tb/dv, -135), coosCircle(ct, tb/dv, -45), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                if oui: ## Boutton abandon 2 ##
                    img.rectangle(bg, hd, self.marron_clair, 0)
                    img.rectangle(bg, hd, self.marron_fonce, self.ep)
                    img.line(c1, c4, self.gris, self.ep)
                    img.line(c2, c3, self.gris, self.ep)
            if oui: ## Bouttons de sauvegarde et de chargement de partie ##
                if oui: ## Boutton sauver ## ## TODO => une flèche vers le bas ##
                    if oui: ## Vars ##
                        hg, hd, bg, bd = [cd[0]-tb, cd[1]-tb//2-tb//2], [cd[0], cd[1]-tb//2-tb//2], [cd[0]-tb, cd[1]+tb//2-tb//2], [cd[0], cd[1]+tb//2-tb//2]
                        ct = ct_sg(ct_sg(hg, bd), ct_sg(hd, bg))
                        c1, c2, c3, c4 = coosCircle(ct, tb/dv, -135), coosCircle(ct, tb/dv, -45), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                    if oui: ## Cadre ##
                        img.rectangle(bg, hd, self.marron_clair, 0)
                        img.rectangle(bg, hd, self.marron_fonce, self.ep)
                    self.disquette(img, c1, c2, c3, c4)
                    if oui: ## Vars ##
                        a, b = 2, 7
                        c, d = 1, 7
                        e, f = 7, 7
                        g, h = 1, 7
                        r1, r4 = pt_sg(pt_sg(c1, c2, a, b), pt_sg(c3, c4, a, b), e, f), pt_sg(pt_sg(c1, c2, c, d), pt_sg(c3, c4, c, d), g, h)
                        r2 = [r4[0], r1[1]]
                        r3 = [r1[0], r4[1]]
                        dst = tb//10
                    if oui: ## Flèche ##
                        img.rectangle(r1, r4, COL.new('00ff00'), 0)
                        img.polygon((coosCircle(r1, dst//2, 180), coosCircle(r2, dst//2, 0), coosCircle(ct_sg(r1, r2), dst, 270)), COL.new('00ff00'), 0)
                    self.bt_sauver = [hg, bd]
                if oui: ## Boutton charger ## ## TODO => une flèche vers le haut ##
                    if oui: ## Vars ##
                        hg, hd, bg, bd = [cd[0]-tb, cd[1]-tb//2+tb//2], [cd[0], cd[1]-tb//2+tb//2], [cd[0]-tb, cd[1]+tb//2+tb//2], [cd[0], cd[1]+tb//2+tb//2]
                        ct = ct_sg(ct_sg(hg, bd), ct_sg(hd, bg))
                        c1, c2, c3, c4 = coosCircle(ct, tb/dv, -135), coosCircle(ct, tb/dv, -45), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                    if oui: ## Cadre ##
                        img.rectangle(bg, hd, self.marron_clair, 0)
                        img.rectangle(bg, hd, self.marron_fonce, self.ep)
                    self.disquette(img, c1, c2, c3, c4)
                    if oui: ## Vars ##
                        a, b = 2, 7
                        c, d = 1, 7
                        e, f = 7, 7
                        g, h = 1, 7
                        r1, r4 = pt_sg(pt_sg(c1, c2, a, b), pt_sg(c3, c4, a, b), e, f), pt_sg(pt_sg(c1, c2, c, d), pt_sg(c3, c4, c, d), g, h)
                        r2 = [r4[0], r1[1]]
                        r3 = [r1[0], r4[1]]
                        dst = tb//10
                    if oui: ## Flèche ##
                        img.rectangle(r1, r4, COL.new('00ff00'), 0)
                        img.polygon((coosCircle(r3, dst//2, 180), coosCircle(r4, dst//2, 0), coosCircle(ct_sg(r3, r4), dst, 90)), COL.new('00ff00'), 0)
                    self.bt_charger = [hg, bd]
            self.img = img
            self.case = case
            self.imageant = False
    if oui: ## Jeu ## ################### Terminé ##
        def jouer(self): ####################################################### Terminé ##
            self.img.build()
            while self.jouable and self.img.is_opened(): ## If not end of game ##
                self.tableau = copy.deepcopy(self.echiquier) ## Creation d'une sauvegarde de la position ##
                if self.legalite[-1]:
                    self.mat_au_pas() ## Vérifications sur le mat au pas ##
                go_menu = self.move() ## If Del or Space => True => menu ##
                if self.jouable and self.legalite[-1]:
                    self.detecte_mat()
                    self.detecte_nulle()
                else:
                    self.echiquier = self.tableau ## Utilise une back-up ##
                if go_menu:
                    return(False)
            if self.exit:
                ferme_all()
                return(False)
            self.image()
            img = self.img
            texte1 = self.fin_partie
            texte2 = str(self.causes_fin_partie[self.cause_fin]) if self.cause_fin != 'nulle' else str(self.causes_fin_partie[self.cause_fin][self.nulle])
            self.result = [1, 0] if self.cause_fin in ['blancs_m', 'blancs_a'] else [0.5, 0.5] if self.cause_fin == 'nulle' else [0, 1]
            raise NotImplementedError()
            p1, p2, p3, p4, ct = echecs.ct1, echecs.ct2, echecs.ct3, echecs.ct4, echecs.ct
            cg, cd, ch, cb = ct_sg(p1, p3), ct_sg(p2, p4), ct_sg(p3, p4), ct_sg(p3, p4)
            cgh = ct_sg(cg, p1)
            cgb = ct_sg(cg, p3)
            cdb = ct_sg(cd, p4)
            cdh = ct_sg(cd, p2)
            if self.help:
                for i in [cg, cd, ch, cb]:
                    point(img, i, rouge)
                for i in [p1, p2, p3, p4]:
                    point(img, i, bleu)
                point(img, ct, vert)
            coul = noir
            img.rectangle(p1, p4, echecs.marron_clair, 0)
            img.rectangle(p1, p4, echecs.marron_fonce, echecs.ep)
            img.rectangle(cgh, cdb, echecs.marron_fonce, echecs.ep)
            img.write(texte1, ct_sg(p1, cdh), coul, echecs.ep, 2)
            img.write(self.replay, ct_sg(cgb, p4), coul, echecs.ep, 2.5)
            try:
                img.write(img, texte2, ct_sg(cgh, cdb), coul, echecs.ep, 2)
            except:
                pass
            if self.gdye('R') == False:
                self.resultat = ''
            elif self.gdye('r') == False:
                self.resultat = ''
            else:
                self.resultat = ''
            nomFenetre = self.nom
            while True:
                img.setMouseCallback(echecs.getmouse)
                self.img.show()
                wk = cv2.waitKey(1)
                if wk == 27:
                    ferme_all()
                    self.exit = True
                    return(False)
                if wk == 8 or wk == 32:
                    return(False)
                coos = self.mouse.pos
                if coos != None:
                    if coos[0] >= cgb[0] and coos[0] <= p4[0] and coos[1] >= cgb[1] and coos[1] <= p4[1]:
                        return(True)
        def move(self): ######################################################## Terminé ##
            if oui: ## Vars ##
                retry = False
                stop = False
                self.exit = False
                nomFenetre = self.nom
            while self.jouable: ## If not end of game ##
                if oui: ## Vars ##
                    img = self.img
                    tb = 100
                    dv = 2
                    p1 = ''
                    p2 = ''
                    p1, p2, p3, p4, ct = echecs.ct1, echecs.ct2, echecs.ct3, echecs.ct4, echecs.ct
                    cg, cd, ch, cb = ct_sg(p1, p3), ct_sg(p2, p4), ct_sg(p3, p4), ct_sg(p3, p4)
                    dis1 = 50
                    dis2 = 125
                    cgph, cdpb = [cg[0] - dis1, cg[1]-dis2], [cd[0] + dis1, cd[1]+dis2]
                    police_vs_input_parties = cv2.FONT_HERSHEY_COMPLEX_SMALL
                    taiy_vs_input_parties = 2.3
                if oui: ## Bouttons ##
                    if self.reg50mov: ## Dessin boutton nulle par 50 mouvements ##
                        ct = ct_sg(self.cd, self.ct)
                        pt50_1, pt50_2, pt50_3, pt50_4 = coosCircle(ct, tb/dv, 225), coosCircle(ct, tb/dv, 315), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                        img.rectangle(pt50_1, pt50_4, self.marron_clair, 0)
                        img.rectangle(pt50_1, pt50_4, self.marron_fonce, self.ep)
                        img.write('50', ct_sg(pt50_1, pt50_4), thickness=self.ep, font=cv2.FONT_HERSHEY_PLAIN, fontSize=3)
                    if self.rep5: ## Dessin boutton nulle par répétition ##
                        ct = ct_sg(self.cg, self.ct)
                        ptrep_1, ptrep_2, ptrep_3, ptrep_4 = coosCircle(ct, tb/dv, 225), coosCircle(ct, tb/dv, 315), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                        img.rectangle(ptrep_1, ptrep_4, self.marron_clair, 0)
                        img.rectangle(ptrep_1, ptrep_4, self.marron_fonce, self.ep)
                        img.write('#', ct_sg(ptrep_1, ptrep_4), thickness=self.ep, font=cv2.FONT_HERSHEY_PLAIN, fontSize=3)
                    if oui: ## Dessin boutton nulle par accord mutuel ##
                        ct = self.ct
                        ptnul_1, ptnul_2, ptnul_3, ptnul_4 = coosCircle(ct, tb/dv, 225), coosCircle(ct, tb/dv, 315), coosCircle(ct, tb/dv, 135), coosCircle(ct, tb/dv, 45)
                        img.rectangle(ptnul_1, ptnul_4, self.marron_clair, 0)
                        img.rectangle(ptnul_1, ptnul_4, self.marron_fonce, self.ep)
                        img.write('-', ct_sg(ptnul_1, ptnul_4), thickness=self.ep, font=cv2.FONT_HERSHEY_PLAIN, fontSize=3)
                        img.write('_', ct_sg(ptnul_1, ptnul_4), thickness=self.ep, font=cv2.FONT_HERSHEY_PLAIN, fontSize=3)
                while True: ## Selectionne une case ou un boutton ##
                    if self.sw:
                        self.sw = non
                        img = self.img
                        case = self.case[self._1]
                        img.rectangle(case[0], case[-1], vert, self.ep)
                    img.setMouseCallback(echecs.getmouse)
                    wk = img.show()
                    if wk == 27: ## Esc pressed => exit ##
                        self.jouable = False
                        stop = True
                        self.exit = True
                        raise InterruptedError
                    elif wk == 8 or wk == 32: ## Del or Space pressed => menu ##
                        img.rectangle(cgph, cdpb, echecs.marron_clair, 0)
                        img.rectangle(cgph, cdpb, echecs.marron_fonce, echecs.ep)
                        nomPartie = visual_input(img, 'Nom de la sauvegarde :\n', '', '\n', nomFenetre, cgph, cdpb, taiy_vs_input_parties, epaisseur=epaisseur/2, police=police_vs_input_parties)
                        if nomPartie == 0:
                            break
                        else:
                            self.sauve_partie(nomPartie)
                            self.charge_partie(nomPartie)
                            return(True)
                    if self.waitkey.wk == 27: ## If clicked => action ##
                        self.getcase()
                        if oui: ## Vars ##
                            coos = self.mouse.pos
                            self.waitkey.wk = 0
                        if coos != None:
                            if clicked_in(coos, self.bt_abandonJ1): ## If cliked => J1 abandone ##
                                self.cause_fin = 'noirs_a'
                                self.jouable = False
                                break
                            elif clicked_in(coos, self.bt_abandonJ2): ## If cliked => J2 abandone ##
                                self.cause_fin = 'blancs_a'
                                self.jouable = False
                                break
                            if self.reg50mov:
                                if clicked_in(coos, [pt50_1, pt50_4]): ## If cliked => Nulle par la règle des 50 coups ##
                                    self.cause_fin = 'nulle'
                                    self.nulle = '50'
                                    self.jouable = False
                                    break
                            if self.rep5:
                                if clicked_in(coos, [ptrep_1, ptrep_4]): ## If cliked => Nulle par répétition ##
                                    self.cause_fin = 'nulle'
                                    self.nulle = '3repetition'
                                    self.jouable = False
                                    break
                            if clicked_in(coos, [ptnul_1, ptnul_4]): ## If cliked => Nulle par accord mutuel ##
                                self.cause_fin = 'nulle'
                                self.nulle = 'accordee'
                                self.jouable = False
                                break
                            if clicked_in(coos, self.bt_sauver): ## If cliked => Sauvegarde la partie ##
                                img.rectangle(cgph, cdpb, echecs.marron_clair, 0)
                                img.rectangle(cgph, cdpb, echecs.marron_fonce, echecs.ep)
                                nomPartie = visual_input(img, 'Sauve\nNom de la sauvegarde :\n', '', '\n', nomFenetre, cgph, cdpb, taiy_vs_input_parties, epaisseur=epaisseur/2, police=police_vs_input_parties)
                                if nomPartie == 0: break
                                self.sauve_partie(nomPartie)
                                self.charge_partie(nomPartie)
                            if clicked_in(coos, self.bt_charger): ## If cliked => Charge la partie ##
                                img.rectangle(cgph, cdpb, echecs.marron_clair, 0)
                                img.rectangle(cgph, cdpb, echecs.marron_fonce, echecs.ep)
                                nomPartie = visual_input(img, 'Charge\nNom de la sauvegarde :\n', '', '\n', nomFenetre, cgph, cdpb, taiy_vs_input_parties, epaisseur=epaisseur/2, police=police_vs_input_parties)
                                if nomPartie == 0: break
                                self.charge_partie(nomPartie)
                    p1, p2 = self._1, self._2
                    if p1 != 0 and p2 != 0:
                        self._1 = 0
                        self._2 = 0
                        break
                    elif p1 != 0:
                        case = self.case[p1]
                        e = self.echiquier
                        for j in e:
                            for i in e[j]:
                                p2 = i+j
                                case = self.case[p2] ## Gets case's coos (p1, p2, p3, p4) ##
                                self.imageant_m = True
                                self.legal(p1, p2, True)
                                self.imageant_m = False
                                if self.legalite[-1]: ## If movement is legal ##
                                    img.circle(ct_sg(ct_sg(case[0], case[3]), ct_sg(case[1], case[2])), self.ep*2, self.col_sel, 0) ## Dessine un cercle sur la case où il a le droit de bouger ##
                                self.legalite.pop(-1)
                                self.echiquier = self.save
                if retry:
                    continue
                if stop:
                    break
                self.imageant_m = False
                self.legal(p1, p2)
                leg = self.legalite[-1]
                if leg: ## If move is legal => move ## 
                    self.dernier_mouve = [p1, p2]
                    p = self.echiquier[p1[1]][p1[0]][0]
                    t = self.echiquier[p2[1]][p2[0]][0].lower()
                    if t == '.':
                        t = 'p' if self.trait else 'P'
                    a = t == '_' or t == '.'
                    b = p.lower()[0] != 'p'
                    if a and b:
                        self.regle50mov += 1
                    else:
                        self.regle50mov = 0
                    if t == '_':
                        move = f'{p}{p1} -> {p2}'
                    else:
                        move = f'{p}{p1} x {t}{p2}'
                    print(move)
                    if t == 'r':
                        jb = False
                    else:
                        jb = True
                    self.echiquier[p2[1]][p2[0]] = self.echiquier[p1[1]][p1[0]][0]
                    self.echiquier[p1[1]][p1[0]] = '_'
                    self.played += 1
                    self.trait = not self.trait
                    self.imageant_m = True
                    self.image()
                    self.jouable = jb
                    self.historique.append(copy.deepcopy(self.echiquier))
                else: ## If move is not legal => illegal move ##
                    if self.help:
                        nemovepas = f'{self.piece} {p1} -> {p2}:\n    {self.illegal_move}'
                        print(nemovepas)
                    self.image()
                break
            return(False)
def starty(j1=echecs.j1, j2=echecs.j2, nom=nom.nom, langue='fr', tourne=non, help=non, dev=non):
    jeu = echecs(nom=nom, j1=j1, j2=j2, langue=langue, tourne=tourne, help=help, dev=dev)
    jeu.begin_playing = True
    try: jeu.start()
    except NotImplementedError: pass
    return(jeu.result)
def start(j1=None, j2=None, nm=None, lg=None, trn=False):
    return(starty(j1=j1, j2=j2, nom=nm, langue=lg, tourne=trn, help=non, dev=non))
if __name__ == '__main__':
    print(start('a', 'b', 'PyChess', 'fr'))