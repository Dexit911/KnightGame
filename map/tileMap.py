import arcade
from object.objects import *
from player.player import *
from enemy.enemy import *

"""WORK IN PROGRESS"""
class TileMap:
    def __init__(self, game):
        self.game = game
        self.tile_map = [".......",
                         ".......",
                         ".......",
                         ".......",
                         "......."]

    def create_tile_map(self):
        for i, row in enumerate(self.tile_map):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "W":
                    Wall(self, j, i)
                if column == "p":
                    Path(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
