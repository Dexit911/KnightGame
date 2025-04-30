import arcade.hitbox
import random
from core.animation import Animate
from core.constance import *
from core.utils.helper_tools import HelperTools
from core.data import map_data
from core.hitboxes import CustomHitBoxes as Ch


class Object(Animate):
    """Basic object"""

    def __init__(self, game, position, path):
        super().__init__(img=path, scale=SCALE)
        self.game = game
        self.center_x = position[0] * TILE_SIZE
        self.center_y = position[1] * TILE_SIZE


class Obstacle(Object):
    """Has hit box, and a specific layer"""

    def __init__(self, game, position, path, hitbox, offset):
        super().__init__(game, position, path)
        # UPDATE GROUPS ------------------------------------------
        self.draw_group = self.game.layer_adjusted_sprites
        self.update_group = self.game.obstacle_list
        self.draw_group.append(self)
        self.update_group.append(self)
        # HIT BOX, OFFSET ----------------------------------------
        if hitbox is None:
            self.hit_box = Ch(self.center_x, self.center_y).default
        else:
            self.hit_box = Ch().get_hitbox(hitbox, self.position)
        if offset is None:
            self.offset = 0
        else:
            self.offset = offset
        # ADJUST LAYER -------------------------------------------
        HelperTools.adjust_layer(self, self.offset)


class Ground(Object):
    """Is only for background"""

    def __init__(self, game, position, path):
        super().__init__(game, position, path)
        self.game.background_list.append(self)


class ObjectFactory:
    """Create Object"""
    @staticmethod
    def spawn_object(game, position, object_type, id):
        data = map_data.TILE_DATA[object_type][id]
        texture_path = data["texture_path"]
        # If texture is a list, take random path from it
        if isinstance(texture_path, list):
            texture_path = random.choice(texture_path)
        hit_box = data.get("hitbox")
        offset = data.get("offset")
        match object_type:
            case "ground":
                return Ground(game, position, texture_path)
            case "obstacle":
                return Obstacle(game, position, texture_path, hit_box, offset)
            case "interactable":
                pass
