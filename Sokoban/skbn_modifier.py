import os
levs = os.listdir('./Sokoban_levels')
for nom in levs:
    with open(f'./Sokoban_levels/{nom}', 'r', encoding='utf8') as file:
        print(nom)
        txt = file.read()
    with open(f'./Sokoban_levels/{nom}', 'w', encoding='utf8') as file:
        file.write(txt.replace(' ', '!'))