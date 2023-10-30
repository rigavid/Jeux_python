from cvt2 import *

noir = col.new('0'*6)
pourpre = col.new('800080')
turquoise = col.new('808000')
a = b = None
a = np.array([[noir, pourpre, pourpre, noir], [noir, pourpre, pourpre, noir], [noir, noir, noir, turquoise]], np.uint8)

img = image(img=a)
img2= image(img=image.new_img(dimensions=[50, 50]))
for i in [img, img2]: i.imprime()