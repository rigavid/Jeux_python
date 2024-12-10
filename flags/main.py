from pyimager import *
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

def openflag(path):
    img = new_img(name=path.split("/")[-1])
    with open(path, "r") as file:
        img.img = cv2.cvtColor(np.array(Image.open(BytesIO(svg2png(bytestring=file.read(), output_height=RES.resolution[1]*60//100))).convert('RGB')), cv2.COLOR_RGB2BGR)
    return img

COL.DarkModeBG = COL.new("#1e1e1e")
COL.LightModeBG = COL.new("#eeeeee")
class game:
    _infos_ = "{"
    for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/"):
        with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{i}", "r", encoding="utf8") as file:
            _infos_ += f"'{i[:-4:]}':{file.read()},\n"
    flags = [f"{"/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux"}/{i}" for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/")]
    _infos_ = eval((_infos_ + "}").replace("\n", ""))
    def reload_infos(self) -> None:
        self.infos = self._infos_[self.lang]
        self.name = self.infos["title"]
        self.buttons = self.infos["buttons"]
        self.flags_names = self.infos["flags"]
    def __init__(self, lang="fr"):
        self.lang = lang if lang in self._infos_.keys() else "fr"
        self.reload_infos()
        self.mode = True
        self.img = new_img(name=self.name)
        self.round = 0
        self.random = False
    def image(self, UI=True) -> None:
        img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.lightGray)
        if UI: ## Draws UI
            coosRound = RES.percentile(80, 10), RES.percentile(90, 15)
            img.rectangle(*coosRound, COL.red, 0)
            img.write_centered(f"Round: {self.round+1}", ct_sg(*coosRound), COL.lime, 1, 1, FONTS[FONT_NAMES[0]])
        self.img.img = img.img
    def guess_img(self, guess):
        self.image()
        pt_d = [(self.img.size()[0]-self.flag.size()[0])//2, (self.img.size()[1]-self.flag.size()[1])//2]
        pt_f = [pt_d[0]+self.flag.size()[0], pt_d[1]+self.flag.size()[1]]
        self.img.img[pt_d[1]:pt_f[1], pt_d[0]:pt_f[0]] = self.flag.img
        self.img.write_centered(guess, RES.percentile(50, 80), COL.lime, 5, 5, FONTS[FONT_NAMES[0]])
        if self.show_an:
            self.img.write_centered(self.show_an, RES.percentile(50, 15), COL.red, 4, 4, FONTS[FONT_NAMES[0]])
    def guess_flag(self, flag):
        guess = ""
        self.flag = openflag(flag)
        self.show_an = None
        self.guess_img(guess)
        try: country_names = [i.replace(" ", "").replace("-", "").replace("\n", "").lower() for i in eval(self.infos["flags"][self.flag.name.split(".")[0]])]
        except KeyError: return print(f"{self.flag.name.split(".")[0]} has no names defined yet!")
        while self.img.is_opened():
            wk = self.img.show()
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.guess_img(guess)
                case 65474: #f5
                    self.show_an = None if self.show_an else eval(self.infos["flags"][self.flag.name.split(".")[0]])[0]
                    self.guess_img(guess)
                case a if a in [ord(i) for i in "abcdefghijklmnopqrstuvwxyz"]:
                    guess += chr(wk)
                    self.guess_img(guess)
                    if guess in country_names:
                        self.round += 1
                        return
                case 65535: ## Suppr
                    RES.update()
                    self.guess_img(guess)
                case 8:
                    guess = guess[:-1:]
                    self.guess_img(guess)
                case 27: return self.img.close()
    def titleImg(self):
        self.image(False)
        self.img.write_centered("Titlescreen", RES.percentile(50, 30), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to start", RES.percentile(50, 50), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        self.img.write_centered(f"Mode: {"aleatoire" if self.random else "ordre"}\n'c' pour changer de mode", RES.percentile(50, 80), COL.red, 3, 3, FONTS[FONT_NAMES[1]])
    def endImg(self):
        self.image(False)
        self.img.write_centered("The end", RES.percentile(50, 50), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to restart", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
    def titlescreen(self):
        self.titleImg()
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.titleImg()
                case 99:
                    self.random = not self.random
                    self.titleImg()
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
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
    def start(self):
        img = self.img.build()
        while img.is_opened():
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.titlescreen()
            self.image()
            if self.random:
                np.random.shuffle(game.flags)
            for flag in game.flags:
                if flag.split("/")[-1].split(".")[0] in self.flags_names.keys():
                    self.guess_flag(flag)
                    if img.is_closed(): break
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.endScreen()

def main():
    jeu = game()
    jeu.img.fullscreen = True
    jeu.start()

if __name__ == "__main__":
    main()