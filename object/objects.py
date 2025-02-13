import arcade
from animation import Animate
from constance import *
import random


class Object(Animate):
    def __init__(self, game, x, y, path):
        super().__init__(img=path, scale=2.0)
        self.game = game
        self.center_x = x * TILE_SIZE
        self.center_y = y * TILE_SIZE


class Obstacle(Object):
    def __init__(self, game, x, y, path):
        super().__init__(game, x, y, path)
        self.game.obstacle_list.append(self)


class Ground(Object):
    def __init__(self, game, x, y, path):
        super().__init__(game, x, y, path)
        self.game.background_list.append(self)


class Grass(Ground):
    def __init__(self, game, x, y):
        self.i = random.randint(1, 5)
        self.path = f"source/terrain/grass/GrassTile{self.i}.png"
        super().__init__(game, x, y, self.path)


class Path(Ground):
    def __init__(self, game, x, y):
        self.i = random.randint(1, 5)
        self.path = f"source/terrain/path/PathTile{self.i}.png"
        super().__init__(game, x, y, self.path)


class Wall(Obstacle):
    def __init__(self, game, x, y):
        self.path = "source/terrain/WallTile.png"
        super().__init__(game, x, y, self.path)
