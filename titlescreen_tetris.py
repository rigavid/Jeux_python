from cvt2 import *

pixelisation = 10

dim_ecran = [i/pixelisation for i in screen]

pt = [i/2 for i in dim_ecran]
sz = 1

def dessine_cathedrale(img, ct=[i/2 for i in dim_ecran], taille=5):
    img = image(img=img.img) ## À suppr, c'est juste pour l'intellisense ##
    img_cathedrale = image()
    img_cathedrale.ouvre_image('imgs_tetris/title_screen.jpg')
    img_cathedrale.agrandis_img(taille)
    img.img = fusionImages(img_cathedrale.img, img.img)
    return img

img = dessine_cathedrale(image(img=image.new_img(dimensions=dim_ecran, fond=col.black)), pt, sz)

if __name__ == '__main__': img.montre(fullscreen=True)