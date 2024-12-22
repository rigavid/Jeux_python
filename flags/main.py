from pyimager import *
from PIL import Image
from cairosvg import svg2png
from io import BytesIO
import time

def openflag(path, bg=COL.black):
    try:
        img = new_img(name=path.split("/")[-1])
        with open(path, "r") as file:
            im = np.array(Image.open(BytesIO(svg2png(bytestring=file.read(), output_height=RES.resolution[1]*60//100))).convert('RGBA'))
        im[im[:,:,3] < 200] = [*bg, 255]
        img.img = cv2.cvtColor(im, cv2.COLOR_RGBA2BGR)
        return img
    except KeyboardInterrupt as e:
        raise ValueError(path)
    except Exception:
        raise ValueError(path)

COL.DarkModeBG = COL.new("#1e1e1e")
COL.LightModeBG = COL.new("#eeeeee")

class flags:
    flags = []
    count = 0

    def get_flags(path):
        try:
            for flag in os.listdir(path):
                if os.path.isdir(f"{path}/{flag}"): flags.get_flags(f"{path}/{flag}")
                else:
                    flags.flags.append(f"{path}/{flag}")
        except Exception as e:
            print(f"Couldn't load {path} because of {e} at {e.__traceback__.tb_lineno}")
    def reset_flags():
        flags.flags = []
        flags.count = 0

class chronometre:
    def __init__(self): self.start_time = self.stop_time = None
    def start(self):
        if self.stop_time == None: self.start_time = time.time()
        else:
            self.start_time += diff(self.stop_time, time.time())
            self.stop_time = None
    def stop(self): self.stop_time = time.time()
    def reset(self): self.__init__()
    def elapsed(self):
        t = time.time()
        if self.start_time == None: return 0
        elif self.stop_time == None: return diff(self.start_time, t)
        else: return diff(self.start_time, t)-diff(self.stop_time, t)
class game:
    _infos_ = "{"
    for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/"):
        with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{i}", "r", encoding="utf8") as file:
            _infos_ += f"'{i[:-4:]}':{file.read()},\n"
    _infos_ = eval((_infos_ + "}").replace("\n", ""))
    def reload_infos(self) -> None:
        self.infos = self._infos_[self.lang]
        self.name = self.infos["title"]
        self.buttons = self.infos["buttons"]
        self.flags_names = self.infos["flags"]
    def __init__(self, lang="fr"):
        self.flags = copy.deepcopy(flags.flags)
        self.lang = lang if lang in self._infos_.keys() else "fr"
        self.reload_infos()
        self.mode = True
        self.img = new_img(name=self.name)
        self.round = 0
        self.random = True
        self.chrono = chronometre()
        self.flgs = False
    def image(self, UI=True) -> None:
        img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.lightGray)
        if UI: ## Draws UI ## TODO ## Prendre les variables de bouttons dans game._infos_ pour écrire pour avoir plusieurs langues
            coosRound = RES.percentile(70, 10), RES.percentile(90, 15)
            img.rectangle(*coosRound, COL.red, 0)
            img.write_centered(f"Round: {self.round+1}/{len(flags.flags)}", ct_sg(*coosRound), COL.lime, 1, 1, FONTS[FONT_NAMES[0]])
            coosTimer = RES.percentile(10, 10), RES.percentile(30, 15)
            img.rectangle(*coosTimer, COL.red, 0)
            t = round(self.chrono.elapsed())
            img.write_centered(f"Time: {t//3600:0>2}:{t%3600//60:0>2}:{t%60:0>2}", ct_sg(*coosTimer), COL.lime, 1, 1, FONTS[FONT_NAMES[0]])
        self.img.img = img.img
    def guess_img(self, guess):
        self.image()
        pt_d = [(self.img.size()[0]-self.flag.size()[0])//2, (self.img.size()[1]-self.flag.size()[1])//2]
        pt_f = [pt_d[0]+self.flag.size()[0], pt_d[1]+self.flag.size()[1]]
        self.img.img[pt_d[1]:pt_f[1], pt_d[0]:pt_f[0]] = self.flag.img
        self.img.write_centered(guess, RES.percentile(50, 80), COL.lime, 5, 5, FONTS[FONT_NAMES[0]])
        if self.show_an: self.img.write_centered(self.show_an, RES.percentile(50, 15), COL.red, 4, 4, FONTS[FONT_NAMES[0]])
    def pause(self) -> bool: ## TODO ## Boutton pour revenir à l'écran titre
        self.image(False)
        coosText1, coosText2 = RES.percentile(50, 50), RES.percentile(50, 70)
        self.img.write_centered(f"Game paused", coosText1, COL.red, 5, 5, FONTS[FONT_NAMES[0]])
        self.img.write_centered(f"Wanna exit [y/N]?", coosText2, COL.red, 3, 3, FONTS[FONT_NAMES[0]])
        return self.img.show_(0, built_in_functs=False) in [27, ord("y")]
    def guess_flag(self, flag):
        guess = ""
        self.flag = openflag(flag, COL.DarkModeBG if self.mode else COL.LightModeBG)
        self.show_an = None
        self.guess_img(guess)
        try: country_names = [i.replace(" ", "").replace("-", "").replace("\n", "").lower() for i in eval(self.infos["flags"][self.flag.name.split(".")[0]])]
        except KeyError: return print(f"{self.flag.name.split(".")[0]} has no names defined yet!")
        while self.img.is_opened():
            wk = self.img.show(built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.guess_img(guess)
                case 65474: #f5
                    self.show_an = None if self.show_an else eval(self.infos["flags"][self.flag.name.split(".")[0]])[0]
                    self.guess_img(guess)
                case a if a in [ord(i) for i in " -abcdefghijklmnopqrstuvwxyz"]:
                    guess += chr(wk)
                    self.guess_img(guess)
                    if guess.replace(" ", "") in country_names:
                        self.round += 1
                        return True
                case 13:
                    guess = ""
                    self.guess_img(guess)
                case 65535: ## Suppr
                    self.img.fullscreen = not self.img.fullscreen
                case 8:
                    guess = guess[:-1:]
                    self.guess_img(guess)
                case 27:
                    self.chrono.stop()
                    if self.pause():
                        return False
                    self.guess_img(guess)
                    self.chrono.start()
            if diff(self.chrono.elapsed()%1,0)<0.1: self.guess_img(guess)
    def titleImg(self): ## TODO Styliser cette image
        self.image(False)
        self.img.write_centered("Titlescreen", RES.percentile(50, 20), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to start", RES.percentile(50, 40), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        self.img.write_centered(f"Drapeaux: {"tous" if self.flgs else "pays et territoires"}\n'd' pour modifier", RES.percentile(50, 60), COL.red, 3, 3, FONTS[FONT_NAMES[1]])
        self.img.write_centered(f"Mode: {"aleatoire" if self.random else "ordre"}\n'c' pour changer de mode", RES.percentile(50, 80), COL.red, 3, 3, FONTS[FONT_NAMES[1]])
    def endImg(self): ## TODO Styliser cette image
        self.image(False)
        self.img.write_centered("The end", RES.percentile(50, 20), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        t = self.chrono.elapsed()
        self.img.write_centered(f"You made it in\n{int(t//3600):0>2}:{int(t%3600//60):0>2}:{int(t%60):0>2}", RES.percentile(50, 45), COL.red, 6, 6, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to restart", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
    def titlescreen(self): ## TODO ## Option nº de questions / quantité de temps à disposition
        ## TODO ## Changer de langue depuis le titlescreen (pas possible pendant la partie)
        self.titleImg()
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.titleImg()
                case 99: ## "c"
                    self.random = not self.random
                    self.titleImg()
                case 100: ## "d"
                    self.flgs = not self.flgs
                    self.titleImg()
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13:
                    flags.reset_flags()
                    flags.get_flags("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux")
                    if self.flgs: flags.get_flags("/".join(i for i in __file__.split("/")[:-1:])+"/drapeauxAutres")
                    return flags.flags
                case 27: self.img.close()
                case -1: ...
                case _: print(f"{wk=}")
    def endScreen(self):
        self.endImg()
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.endImg()
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
                case 27: self.img.close()
    def start_game(self, flgs) -> bool:
        if self.random: np.random.shuffle(flgs)
        self.chrono.start()
        self.image()
        for flag in flgs:
            if flag.split("/")[-1].split(".")[0] in self.flags_names.keys():
                if not self.guess_flag(flag): return False
            else: print(f"{flag} is not defined for language: {self.lang}!")
        self.chrono.stop()
        return True
    def start(self):
        img = self.img.build()
        while img.is_opened():
            flgs = self.titlescreen()
            if img.is_opened():
                if self.start_game(flgs):
                    self.endScreen()
            self.chrono.reset()

def main():
    jeu = game()
    jeu.img.fullscreen = True
    try: jeu.start()
    except KeyboardInterrupt: ...

if __name__ == "__main__":
    main()