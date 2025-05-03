from game.object.object import ObjectFactory
from core.data.map_data import *
from core.data import enemy_data

from core.constance import *
from game.object.interactable import Chest
from game.enemy.enemy import Enemy


class TileMap:
    @staticmethod
    def create_tile_map(game, tile_map):
        """Create Objects for different char"""
        debug = ["C"]

        # Matrix for pathfinding algorithm
        final_matrix = []

        # DEFINE MAP HEIGHT AND LEN
        map_height = len(tile_map)

        for i, row in enumerate(tile_map):
            # Each tile_matrix in 2x2, maybe more later
            matrix_row_top = []
            matrix_row_bottom = []

            for j, symbol in enumerate(row):
                spawn_x = j
                spawn_y = map_height - 1 - i

                # Always create grass on every tile, going to be changed soon
                ObjectFactory.spawn_object(game, (j, i), "ground", "grass")

                if symbol not in debug:
                    # Parse the symbol if not in debug, and create the tile
                    matrix_type, object_type, object_id = TILE_TYPES[symbol]
                    ObjectFactory.spawn_object(
                        game=game,
                        position=(spawn_x, spawn_y),
                        object_type=object_type,
                        id=object_id
                    )
                    # Get the tile properties
                    matrix = TILE_WALK_PROPERTIES[matrix_type]

                    # Extend the top and bottom rows
                    matrix_row_top.extend(matrix[0])
                    matrix_row_bottom.extend(matrix[1])

                # Add both rows to the final matrix
            final_matrix.append(matrix_row_top)
            final_matrix.append(matrix_row_bottom)
            # Turning it one more, because, why not

            for row in final_matrix:
                print(row)

        game.matrix_map = final_matrix
