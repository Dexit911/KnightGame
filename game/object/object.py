from core.animation import Animate
from arcade.hitbox import HitBox
from core.hitboxes import CustomHitBoxes as Ch
from core.constance import *
from core.utils.path_manager import PathManager as Pm
import random


class Object(Animate):
    """Basic object"""

    def __init__(self, game, x, y, path):
        super().__init__(img=path, scale=SCALE)
        self.game = game
        self.center_x = x * TILE_SIZE
        self.center_y = y * TILE_SIZE


class Obstacle(Object):
    """Has hit box, and a specific layer"""

    def __init__(self, game, x, y, path, offset: int = 0):
        super().__init__(game, x, y, path)
        self.draw_group = self.game.layer_adjusted_sprites
        self.update_group = self.game.obstacle_list

        self.update_group.append(self)
        self.draw_group.append(self)

        self.hit_boxes = Ch(x * TILE_SIZE, y * TILE_SIZE)

        self.offset = offset
        self.adjust_layer(self.offset)

    def adjust_layer(self, offset: int = 0) -> None:
        """
        Adjusting the layer based on sprites y cord,
        Apply offset to manually adjust layering,
        """
        sprite_list = self.draw_group
        sprite_list.remove(self)
        for i, sprite in enumerate(sprite_list):
            if self.center_y + offset > sprite.center_y:
                index = i
                break
        else:
            index = len(sprite_list)  # If not found, put at the end
        sprite_list.insert(index, self)  # Insert at correct layer position


"""BACKGROUND"""


class Ground(Object):
    """Is only for background"""

    def __init__(self, game, x, y, path):
        super().__init__(game, x, y, path)
        self.game.background_list.append(self)


class Grass(Ground):
    def __init__(self, game, x, y):
        self.i = random.randint(1, 5)
        self.path = Pm.tile_img("grass", f"GrassTile{self.i}.png")
        super().__init__(game, x, y, self.path)


class Path(Ground):
    def __init__(self, game, x, y):
        self.i = random.randint(1, 5)
        self.path = Pm.tile_img("path", f"PathTile{self.i}.png")
        super().__init__(game, x, y, self.path)


class SmallStone(Ground):
    def __init__(self, game, x, y):
        self.path = Pm.object_img("stone", "SmallStone1.png")
        super().__init__(game, x, y, self.path)


class StoneStairs(Ground):
    def __init__(self, game, x, y):
        self.path = Pm.structure_img("StoneStairs1.png")
        super().__init__(game, x, y, self.path)


"""OBSTACLES"""


class Bush(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.object_img("bush", "Bush1.png")
        super().__init__(game, x, y, self.path)

        self.hit_box = self.hit_boxes.default


class BigStone(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.object_img("stone", "BigStone1.png")
        super().__init__(game, x, y, self.path, offset=40)

        self.hit_box = self.hit_boxes.big_stone


class Wall(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.structure_img("WallTile.png")
        super().__init__(game, x, y, self.path)


class HighWall(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.structure_img("HighWall.png")
        super().__init__(game, x, y, self.path)


class SmallPole(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.structure_img("SmallPole.png")
        super().__init__(game, x, y, self.path, offset=40)
        self.hit_box = self.hit_boxes.stone_small_pole


class RuneStone(Obstacle):
    def __init__(self, game, x, y):
        self.path = Pm.structure_img("RuneStone1.png")
        super().__init__(game, x, y, self.path)
        self.hit_box = self.hit_boxes.rune_stone
