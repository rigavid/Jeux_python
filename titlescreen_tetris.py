from Outils.cvt2 import *

pixelisation = 7

dim_ecran = [i/pixelisation for i in screen]

pt = [i/2 for i in dim_ecran]
sz = 1

def dessine_cathedrale(img, ct=[i/2 for i in dim_ecran], taille=5):
    img = image(img=img.img) ## À suppr, c'est juste pour l'intellisense ##
    img_cathedrale = image()
    img_cathedrale.ouvre_image('imgs_tetris/title_screen.jpg')
    img_cathedrale.agrandis_img(taille)
    offsets = [len(img.img[0])/2+len(img_cathedrale.img[0])/4, len(img.img)/2-len(img_cathedrale.img)/2]
    img.img = fusionImages(img_cathedrale.img, img.img, offsets)
    return img

img = dessine_cathedrale(image(img=image.new_img(dimensions=dim_ecran, fond=col.black)), pt, sz)
#img.ecris('* 1 player game\n* Options       ', ct_sg(ct_sg([0,0],[0,len(img.img)]), ct_sg([0,0], [len(img.img[0]),len(img.img)])), col.white, 1, 0.75)
if __name__ == '__main__': img.montre(fullscreen=True)