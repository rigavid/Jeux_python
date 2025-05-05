from pyimager import *



class chess:
    gris = [30, 30, 30]
    def __init__(self) -> None:
        self.tourne = False
        self.trait = True
        self.epaisseur = 9
    def __str__(self) -> str:
        ...
    def image(self) -> None:
        ...

a = chess()
img = a.new_img().build()
while img.is_opened():
    img.show()