from cvt2 import *

img = image()
img.ouvre_image('imgs_tetris/Amstrad_CPC_Full_AMSDOS_Character_Set.png')

img.montre(fullscreen=True)

pw = 2

xc, yc = 8*pw, 8*pw

for y in range(16):
    for x in range(16):
        im = img.img
        im = image(img=im[(y*yc):(y*yc)+yc, (x*xc):(x*xc)+xc])
        if im.montre(fullscreen=True) == 27: raise SystemExit