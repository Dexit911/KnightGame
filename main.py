import arcade
from constance import *
from player.player import *
from object.objects import *
from camera import *


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=TITLE, fullscreen=False)

    def setup(self):

        """Player"""
        self.player = Player()
        self.player.setup()

        """Sprite Lists"""
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.player)

        self.enemy_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        """Map"""
        self.tile_map = TILE_MAP
        self.create_tile_map()

        """Camera"""
        self.camera = Camera(self)

        """Physics"""
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.obstacle_list)

    def create_tile_map(self):
        rows = len(self.tile_map)
        for i, row in enumerate(self.tile_map):
            for j, column in enumerate(row):
                real_y = rows - i - 1
                if column == ".":
                    Grass(self, j, i)
                if column == "W":
                    Wall(self, j, i)
                if column == "p":
                    Path(self, j, i)

    def on_draw(self):
        """Draw all sprite"""
        self.clear()  # Clear screen after every frame
        self.camera.use()  # Use camera
        """Draw all elements"""
        self.background_list.draw()
        self.obstacle_list.draw()
        self.sprite_list.draw()

        """Draw player hit box for debug"""
        #self.player.draw_hit_box()

    def on_update(self, delta_time):
        """Update Camera"""
        self.camera.update()

        """Update Player"""
        self.player.on_update()

        """Update collision"""
        self.collision_engine.update()

    def on_key_press(self, key, modifiers):
        """Handles key presses"""
        self.player.keys.add(key)

    def on_key_release(self, key, modifiers):
        """Handles key releases"""
        if key in self.player.keys:
            self.player.keys.remove(key)


game = Game()
game.setup()
arcade.run()  # Corrected from game.run()
