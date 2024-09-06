from tsanap import *
os.chdir(__file__[::-1].split("/",1)[1][::-1])
create_dir_if_unexisting("imgs")

resolution = [384, 216]

class color:
    noir = col.new("#000000") 
    blanc = col.new("#FFFFFF") 
    rouge = col.new("#FF0000") 
    jaune = col.new("#FFFF00") 
    vert = col.new("#00FF00") 
    bleu = col.new("#0000FF") 
    cyan = col.new("#00FFFF") 
    magenta = col.new("#FF00FF") 
    orange = col.new("#FFA500") 
    marron = col.new("#A52A2A") 
    roseclair = col.new("#FFB6C1")
    vertfonce = col.new("#008000")
    bleuclair = col.new("#ADD8E6")
    bleufonce = col.new("#00008B")
    grisclair = col.new("#D3D3D3")
    grisfonce = col.new("#A9A9A9")

def image_creation(path, data) -> None:
    cv2.imwrite(path, data)

def image_bg() -> image: ## Image Background
    img = image(img=image.new_img(dimensions=resolution))
    img.ecris("BACKGROUND", ct_sg([0,0], resolution), color.rouge, 1, 1)
    return img

def image_ts() -> image: ## Image Titlescreen
    img = image(img=image.new_img(dimensions=resolution))
    img.ecris("TITLESCREEN", ct_sg([0,0], resolution), color.rouge, 1, 1)
    return img

def icone() -> image:
    img = image(img=image.new_img(dimensions=[11,8], fond=color.noir))
    POINTS = [[2,0],[3,1],[8,0],[7,1]]
    POINTS+= [[3,7],[4,7],[6,7],[7,7]]
    POINTS+= [[x,4] for x in range(11)]
    POINTS+= [[x,2] for x in range(2,9)]
    POINTS+= [[x,5] for x in range(2,9)]
    POINTS+= [[x,6] for x in range(2,9)]
    POINTS+= [[x,3] for x in range(1,10)]
    POINTS+= [[x,y] for x in [0,10] for y in [5,6]]
    for p in POINTS:
        img.img[p[1], p[0]] = color.vert[::-1]
    POINTS = [[3,3],[7,3]]
    POINTS+= [[x,6] for x in range(3,8)]
    for p in POINTS:
        img.img[p[1], p[0]] = color.noir[::-1]
    return img

def images() -> None:
    image_creation("./imgs/bg_img.png", image_bg().img)
    image_creation("./imgs/ts_img.png", image_ts().img)
    image_creation("./imgs/icon.png", icone().img)

if __name__ == "__main__":
    images()