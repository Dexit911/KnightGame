import arcade
print(arcade.__version__)
import itertools
from core.constance import *
from game.player.player import *
from game.object.object import *
from core.camera import *
from game.enemy.enemy import Enemy
from game.weapon.weapon import Weapon

"""
Problems:
Implements:

 * Drop and pickup other weapon
 
 * slow idle movement enemy 
 * path finding for enemies
 * make that the idle movement only happens in a radius, to prevent chilling around the whole map.
 * Fix pixelart filtering 
 
 * adjust layer, make the bottom hit box y coridnate for layering
 
 * overall enemy AI, and make a good flexible enemy class.
 
 Class Enemy
 construct:
 hp, damage, image, behaviour_mode, x, y, drop, speed.
 
 Methods:
 Path finding
 Behaviour
 Attack
 On
"""


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=TITLE, fullscreen=False)

        self.tile_mapping = {
            "P": Path,
            "E": Enemy,
            "B": Bush,
            "S": BigStone,
            "s": SmallStone,
            "W": HighWall,
            "w": Wall,
            ">": StoneStairs,
            "^": SmallPole,
            "r": RuneStone
        }

    def setup(self):
        print(arcade.__version__)
        """Sprite Lists"""
        self.layer_adjusted_sprites = arcade.SpriteList()

        self.sprite_list = arcade.SpriteList()
        self.moving_entities = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        self.item_list = arcade.SpriteList()

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
                if column != "#":
                    Grass(self, j, i)
                if column in self.tile_mapping:
                    self.tile_mapping[column](self, j, i)

    def on_draw(self):
        """Render every frame"""
        self.clear()  # Clear the screen every frame
        self.camera.use()

        """Draw all elements"""
        self.background_list.draw()
        self.item_list.draw()

        self.sprite_list.draw()
        self.layer_adjusted_sprites.draw()

        """Hitboxes"""

        """self.player.sword.draw_hit_box()
        self.obstacle_list.draw_hit_boxes()
        self.player.draw_hit_box()
        self.item_list.draw_hit_boxes()"""

    def on_update(self, delta_time):
        """Update Camera"""
        self.camera.update()

        """Update Player"""
        self.player.on_update()

        """Update Enemies"""
        for enemy in self.enemy_list:
            enemy.on_update()

        for item in self.item_list:
            item.on_update()

        self.collision_engine.update()

        # for sprite in self.sprite_list:
        # sprite.on_update()

    def on_key_press(self, key, modifiers):
        """Handles key presses"""
        self.player.keys.add(key)
        self.player.weapon.keys.add(key)

    def on_key_release(self, key, modifiers):
        """Handles key releases"""
        if key in self.player.keys:
            self.player.keys.remove(key)
            self.player.weapon.keys.remove(key)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Track mouse position"""
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_pos = [x, y]
        self.player.update_direction_based_on_mouse(x, y)


game = Game()
game.setup()
arcade.run()  # Corrected from game.run()
