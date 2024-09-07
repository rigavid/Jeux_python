from tsanap import *
from Asteroids.maelstrom import main as maelstrom
from Shogi.shogi import main as shogi
from _2048._2048 import main as _2048
from Tetris.tetris import main as tetris
from Sokoban.sokoban import main as sokoban

jeux = [{'maelstrom':maelstrom, 'shogi':shogi, '_2048':_2048}, {'sokoban':sokoban, 'tetris':tetris}]
img = image()
y = screen[1]/len(jeux)
x = screen[0]/max(len(jeux[i]) for i in range(len(jeux)))

for row in jeux:
    for jeu in row:
        row[jeu]()
