from game.object.object import ObjectFactory
from core.data.map_data import *

from core.constance import *
from game.object.interactable import Chest
from game.enemy.enemy import Enemy


class TileMap:
    @staticmethod
    def create_tile_map(game, tile_map):
        """Create Objects for different char"""
        turned_map = tile_map[::-1]
        debug = ["E", ".", "C"]
        for i, row in enumerate(turned_map):
            for j, symbol in enumerate(row):
                ObjectFactory.spawn_object(game, (j, i), "ground", "grass")

                if symbol not in debug:
                    walkable_matrix, object_type, object_id = TILE_TYPES[symbol]
                    ObjectFactory.spawn_object(
                        game=game,
                        position=(j, i),
                        object_type=object_type,
                        id=object_id
                    )
                # CUSTOM FOR DEBUG -----------------------------------------
                if symbol == "C":
                    Chest(game).spawn((j * TILE_SIZE, i * TILE_SIZE))

                if symbol == "E":
                    Enemy(game, j, i)

