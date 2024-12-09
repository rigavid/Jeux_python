from pyimager import *

COL.DarkModeBG = COL.new("#1e1e1e")
COL.LightModeBG = COL.new("#eeeeee")
class game:
    _infos_ = "{"
    for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/"):
        with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{i}", "r", encoding="utf8") as file:
            _infos_ += f"'{i[:-4:]}':{file.read()},\n"
    flags = {i[:-4:]: image(i).open_img("/".join(i for i in __file__.split("/")[:-1:])+f"/drapeaux/{i}") for i in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/")}
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
    def ecris(self, guess):
        self.img.write_centered(guess, RES.percentile(50, 80), COL.lime, 5, 5, FONTS[FONT_NAMES[0]])
    def guess_flag(self, flag):
        guess = ""
        while self.img.is_opened():
            wk = self.img.show()
            match wk:
                case 65473: #f4
                    self.mode = not self.mode
                    self.image()
                case a if a in [ord(i) for i in "abcdefghijklmnopqrstuvwxyz"]:
                    guess += chr(wk)
                    self.image()
                    self.ecris(guess)
                case 65535: ## Suppr
                    RES.update()
                    self.image()
                case 8:
                    guess = guess[:-1:]
                    self.image()
                    self.ecris(guess)
    def titlescreen(self):
        self.img.write_centered("Titlescreen", RES.percentile(50, 50), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to start", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
                case 27: self.img.close()
    def endScreen(self):
        self.img.write_centered("The end", RES.percentile(50, 50), COL.red, 10, 10, FONTS[FONT_NAMES[1]])
        self.img.write_centered("Press enter to restart", RES.percentile(50, 70), COL.red, 5, 5, FONTS[FONT_NAMES[1]])
        while self.img.is_opened():
            wk = self.img.show_(0, built_in_functs=False)
            match wk:
                case 32: self.img.fullscreen = not self.img.fullscreen
                case 13: return
                case 27: self.img.close()
    def start(self):
        img = self.img.build()
        while True:
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.titlescreen()
            self.image()
            for flag in self.flags:
                self.guess_flag(flag)
                match wk:
                    case 65473: #f4
                        self.mode = not self.mode
                        self.image()
                    case 65535: ## Suppr
                        RES.update()
                        self.image()
                    case -1: ...
                    case _: print(wk)
            self.img.img = new_img(RES.resolution, COL.DarkModeBG if self.mode else COL.LightModeBG).img
            self.endScreen()

def main():
    jeu = game()
    jeu.start()

if __name__ == "__main__":
    main()