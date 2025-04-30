from arcade.hitbox import HitBox as HB
from core.utils.hitbox_manager import HitboxManager
from core.constance import *


class CustomHitBoxes:
    def __init__(self, x=0, y=0):
        """Obstacles that are connected to grid cords"""
        self.scale = TILE_SIZE / 2

        self.default = HB([
            (-self.scale + x, -self.scale + y),  # Bottom-left
            (self.scale + x, -self.scale + y),  # Bottom-right
            (self.scale + x, self.scale + y),  # Top-right
            (-self.scale + x, self.scale + y)  # Top-left
        ])

        self.big_stone = HB([
            (-10 + x, -20 + y),
            (10 + x, -20 + y),
            (30 + x, 0 + y),
            (-30 + x, 0 + y)
        ])

        self.stone_small_pole = HB([
            (-23 + x, -22 + y),  # Down left corner
            (23 + x, -22 + y),  # Down right corner
            (23 + x, 10 + y),  # Upper left corner
            (-23 + x, 10 + y)  # Upper right corner
        ])

        self.rune_stone = HB([
            (-10 + x, -22 + y),  # Down left corner
            (10 + x, -22 + y),  # Down right corner
            (10 + x, -17 + y),  # Upper left corner
            (-10 + x, -17 + y)  #
        ])

        """Static hit boxes that in middle of the screen"""
        self.sword = HB([
            (-20, -10),
            (20, -10),
            (20, 40),
            (-20, 40)
        ])

        self.player = HB([
            (-12, -32),
            (12, -32),
            (10, -15),
            (-10, -15)
        ])

        self.item = HB([
            (-10 + x, -10 + y),  # Down left corner
            (10 + x, -10 + y),  # Down right corner
            (10 + x, 10 + y),  # Upper left corner
            (-10 + x, 10 + y)  # Upper right corner
        ])

        self.point_list = {
            "big_stone": [(-10, -20),
                          (10, -20),
                          (30, 0),
                          (-30, 0)],

            "rune_stone": [(-10, -22),
                           (10, -22),
                           (10, -17),
                           (-10, -17)],

            "bush": [(-32, -32),
                     (32, -32),
                     (32, 32),
                     (-32, 32)],

            "small_pole": [(-23, -22),
                           (23, -22),
                           (23, 10),
                           (-23, 10)]

        }

    def get_hitbox(self, name, position: tuple) -> HB:
        """Gets hit-box based on position"""
        x, y = position
        point_list = self.point_list[name]
        new_point_list = []
        for row in point_list:
            new_tuple = (row[0] + x, row[1] + y)
            new_point_list.append(new_tuple)
        return HB(new_point_list)

    def get_static_hitbox(self, name: str) -> HB:
        """Used for Sprites in the middle of screen"""
        return HB(self.point_list[name])
