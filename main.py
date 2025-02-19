import arcade
import itertools
from constance import *
from player.player import *
from object.objects import *
from camera import *
from enemy.enemy import Enemy
from weapon import Weapon

"""
Problems:
 * the Enemy does not have collision. Change the mode to "resting" when collid
Implements:

 * Drop and pickup other weapon
 * Make better hitbox for hitting with sword
 
 * Make system for adjusting layer order for obsatcles and movings sprite for better visuals
 * slow idle movement enemy 
 * path finding for enemies
 * Fix pixelart filtering 
 * MAYBE make individual animation for sword instead of rotating it
 
"""


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=TITLE, fullscreen=False)

    def setup(self):
        print(arcade.__version__)
        """Sprite Lists"""
        self.sprite_list = arcade.SpriteList()
        self.moving_entities = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        """Map"""
        self.tile_map = TILE_MAP
        self.create_tile_map()

        """Camera"""
        self.camera = Camera(self)

        """Player"""
        self.player = Player(self)
        self.player.setup()
        self.sprite_list.append(self.player)

        """Physics"""
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.obstacle_list)

        self.mouse_x = 0
        self.mouse_y = 0

    def create_tile_map(self):
        """Create Objects for different char"""
        for i, row in enumerate(self.tile_map):
            for j, column in enumerate(row):
                Grass(self, j, i)
                if column == "W":
                    Wall(self, j, i)
                if column == "p":
                    Path(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "B":
                    Bush(self, j, i)

    def on_draw(self):
        """Render every frame"""
        self.clear()  # Clear the screen every frame
        self.camera.use()

        """Draw all elements"""
        self.background_list.draw()
        self.sprite_list.draw()
        self.moving_entities.draw()
        self.obstacle_list.draw()

        # self.player.sword.draw_hit_box()
        self.obstacle_list.draw_hit_boxes()
        self.player.draw_hit_box()

    def on_update(self, delta_time):
        """Update Camera"""
        self.camera.update()

        """Update Player"""
        self.player.on_update()

        """Update Enemies"""
        for enemy in self.enemy_list:
            enemy.on_update()

        self.collision_engine.update()

    def on_key_press(self, key, modifiers):
        """Handles key presses"""
        self.player.keys.add(key)
        self.player.sword.keys.add(key)

    def on_key_release(self, key, modifiers):
        """Handles key releases"""
        if key in self.player.keys:
            self.player.keys.remove(key)
            self.player.sword.keys.remove(key)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Track mouse position"""
        self.mouse_x = x
        self.mouse_y = y
        print(f"{self.mouse_x}, {self.mouse_y}")


game = Game()
game.setup()
arcade.run()  # Corrected from game.run()
