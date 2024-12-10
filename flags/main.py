from pyimager import *
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

def openSVG(path):
    img = new_img()
    with open(path, "r") as file:
        img.img = cv2.cvtColor(np.array(Image.open(BytesIO(svg2png(bytestring=file.read()))).convert('RGBA')), cv2.COLOR_RGBA2BGRA)
    return img

COL.DarkModeBG = COL.new("#1e1e1e")
COL.LightModeBG = COL.new("#eeeeee")
class game:
    _infos_ = "{"
    for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/"):
        with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{i}", "r", encoding="utf8") as file:
            _infos_ += f"'{i[:-4:]}':{file.read()},\n"
    flags = [f"{"/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/"}/{i}" for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/")]
    _infos_ = eval((_infos_ + "}").replace("\n", ""))
    def reload_infos(self) -> None:
        self.infos = self._infos_[self.lang]
        self.name = self.infos["title"]
        self.buttons = self.infos["buttons"]
        self.flags_names = self.infos["flags"]
    def load_games(self) -> None:
        try:
            with open("/".join(i for i in __file__.split("/")[:-1:])+"/games.txt", "r", encoding="utf8") as file:
                self.games = eval(file.read())
        except: self.games = []
    def __init__(self, lang="fr"):
        self.lang = lang if lang in self._infos_.keys() else "fr"
        self.reload_infos()
        self.load_games()
        self.mode = True
        self.img = new_img(name=self.name)
        self.round = 0
    def image(self) -> None:
        img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.lightGray)
        coosRound = RES.percentile(80, 10), RES.percentile(90, 15)
        img.rectangle(*coosRound, COL.red, 0)
        img.write_centered(f"Round: {self.round+1}", ct_sg(*coosRound), COL.lime, 1, 1, FONTS[FONT_NAMES[0]])
        self.img.img = img.img
    def guess_img(self, flag, guess):
        self.image()
        drp = openSVG(flag)
        pt_d = [(self.img.size()[0]-self.drp.size()[0])/2, (self.img.size()[1]-self.drp.size()[1])/2]
        pt_f = [pt_d[0]+self.drp.size()[0], pt_d[1]+self.drp.size()[1]]
        self.img.img[pt_d] ## TODO
        self.img.write_centered(guess, RES.percentile(50, 80), COL.lime, 5, 5, FONTS[FONT_NAMES[0]])

    def guess_flag(self, flag):
        guess = ""
        self.flag = openSVG()
        while self.img.is_opened():
            wk = self.img.show()
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.image()
                case a if a in [ord(i) for i in "abcdefghijklmnopqrstuvwxyz"]:
                    guess += chr(wk)
                    self.guess_img(flag, guess)
                case 65535: ## Suppr
                    RES.update()
                    self.guess_img(flag, guess)
                case 8:
                    guess = guess[:-1:]
                    self.guess_img(flag, guess)
    def titlescreen(self):
        self.img.write_centered("Titlescreen", RES.percentile(50, 50), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to start", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.image()
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
                case 27: self.img.close()
                case -1: ...
                case _: print(f"{wk=}")
    def endScreen(self):
        self.img.write_centered("The end", RES.percentile(50, 50), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to restart", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 65473 | 269025139: #f4
                    self.mode = not self.mode
                    self.image()
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
                case 27: self.img.close()
    def start(self):
        img = self.img.build()
        while img.is_opened():
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.titlescreen()
            self.image()
            for flag in self.flags:
                self.guess_flag(flag)
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.endScreen()

def main():
    jeu = game()
    jeu.start()

if __name__ == "__main__":
    main()