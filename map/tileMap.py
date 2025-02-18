import arcade
from object.objects import Object
from main import Game
from player.player import Player


class TileMap:
    def __init__(self, game):
        self.game = game
        self.tile_map = [".......",
                         ".......",
                         ".......",
                         ".......",
                         ".......",
                         ]

    def create_tile_map(self):
        for i, row in enumerate(self.tile_map):
            for j, column in enumerate(row):
                Object(self.game, j, i)
