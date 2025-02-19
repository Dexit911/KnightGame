import arcade
from animation import Animate
from arcade.hitbox import HitBox
from hitboxes import CustomHitBoxes as Ch
from constance import *
import random


class Object(Animate):
    """Basic object"""
    def __init__(self, game, x, y, path):
        super().__init__(img=path, scale=2.0)
        self.game = game
        self.center_x = x * TILE_SIZE
        self.center_y = y * TILE_SIZE


class Obstacle(Object):
    """Has hit box, and a specific layer"""
    def __init__(self, game, x, y, path):
        super().__init__(game, x, y, path)
        self.game.obstacle_list.append(self)
        self.hit_boxes = Ch(x * TILE_SIZE, y * TILE_SIZE)


class Ground(Object):
    """Is only for background"""
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


class Bush(Obstacle):
    def __init__(self, game, x, y):
        self.path = "source/terrain/bush/Bush1.png"
        super().__init__(game, x, y, self.path)
        # Set the hit box after the sprite is fully initialized
        self.hit_box = HitBox(self.hit_boxes.default)
