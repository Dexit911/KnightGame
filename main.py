import arcade.color

from game.player.player import *
from game.object.object import *
from game.object.interactable import Chest
from core.data.map_data import *
from game.object.npc.npc import BlackSmith
from core.camera import *
from core.utils.path_manager import PathManager as Pm
from game.cursor.cursor import Cursor
from game.map.tile_map import TileMap
from core.constance import *
import time

"""
TODOLIST
Fixes: 
- Change_layer for weapon class
- Optimize the scripts (update). Cache, multithreading for loading assets.
- Make the adjust layer that is used once a staticmethod 

Implements to do:
- Make text appear with name of the cursor is over
- Make a custom font for the game
- Make a Npc class
- Setup drop loot settings/ loot table

Future Plans: 
- Make map generation 
- Make custom map editor (In progress) maybe +-
"""


class Game(arcade.Window):
    def __init__(self):
        super().__init__(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            title=TITLE,
            fullscreen=False,
        )

    def setup(self):
        print(arcade.__version__)
        #self.set_mouse_visible(False)

        """Sprite Lists"""
        # Draw -----------------------------------------
        self.layer_adjusted_sprites = arcade.SpriteList()
        # ----------------------------------------------
        self.sprite_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        """Background, obstacles"""
        self.obstacle_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        """Items, Weapons, interactable"""
        self.item_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.throwable_list = arcade.SpriteList()
        self.interactable_list = arcade.SpriteList()

        self.cursor_list = arcade.SpriteList()

        """Map"""
        self.matrix_map = []
        TileMap.create_tile_map(self, TILE_MAPS["start_level"]["object"])

        """Camera"""
        self.camera = Camera(self)

        """Player"""
        self.player = Player(self)
        self.player.setup()
        self.sprite_list.append(self.player)

        """Physics"""
        self.collision_engine = arcade.PhysicsEngineSimple(self.player, self.obstacle_list)

        """Mouse"""
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pos = (self.mouse_x, self.mouse_y)
        self.mouse_world = self.camera.get_mouse_world(self.mouse_pos)

        """Cursor"""
        self.cursor = Cursor(self)
        self.cursor_list.append(self.cursor)

        """Debug Spawn"""
        Chest(self).spawn((50, 150))
        BlackSmith(self).spawn((50, 100))

        """Sound"""
        self.song = arcade.load_sound(Pm.sound("main_theme.mp3"))
        arcade.play_sound(self.song, volume=0.2, loop=True)

    def on_draw(self):
        start = time.time()
        """Render every frame"""
        self.clear()  # Clear the screen every frame
        self.camera.use()

        """Draw all elements"""
        self.background_list.draw()
        self.item_list.draw()
        self.sprite_list.draw()
        self.layer_adjusted_sprites.draw()

        self.cursor_list.draw()

        """Hitboxes"""

        """for weapon in self.weapon_list:
            weapon.ghost_hitbox.draw_hit_box(color=arcade.color.RED)"""
        stop = time.time()
        # print(f"draw time: {stop - start}")


    def on_update(self, delta_time):
        """Update Camera"""
        self.camera.update()
        """Update Mouse cord"""
        self.mouse_world = self.camera.get_mouse_world(self.mouse_pos)
        """Update Player"""
        self.player.on_update(delta_time)
        """Update Cursor"""
        self.cursor.on_update(delta_time)
        """Update all groups"""
        for enemy in self.enemy_list: enemy.on_update(delta_time)
        for item in self.item_list: item.on_update()
        for weapon in self.weapon_list: weapon.on_update(delta_time)
        for throwable in self.throwable_list: throwable.on_update()
        for interactable in self.interactable_list: interactable.on_update()

        self.collision_engine.update()
        stop = time.time()
        self.update_debug(False)

    def on_key_press(self, key, modifiers):
        """Handles key presses"""
        self.player.keys.add(key)
        self.player.weapon.keys.add(key)
        self.cursor.keys.add(key)

    def on_key_release(self, key, modifiers):
        """Handles key releases"""
        if key in self.player.keys:
            self.player.keys.remove(key)
            self.player.weapon.keys.discard(key)
            self.cursor.keys.discard(key)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """Track mouse position"""
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_pos = (x, y)

        self.player.update_direction_based_on_mouse(x, y)

    # DEBUG

    def draw_subgrid_lines(self, matrix, sub_tile_size, offset_x=1, offset_y=1):
        """Draw grid lines for a matrix of sub-tiles with optional offset.

        Args:
            matrix: 2D matrix representing the grid
            sub_tile_size: Size of each sub-tile in pixels
            offset_x: Horizontal offset (negative = left, positive = right)
            offset_y: Vertical offset (negative = down, positive = up)
        """
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        # Apply offsets (negative for left/down)
        x_offset = -offset_x * sub_tile_size
        y_offset = -offset_y * sub_tile_size

        # Draw horizontal lines (Y changes, X runs full width)
        for row in range(rows + 1):
            y = row * sub_tile_size + y_offset
            arcade.draw_line(
                start_x=0 + x_offset,
                start_y=y,
                end_x=cols * sub_tile_size + x_offset,
                end_y=y,
                color=arcade.color.GRAY,
                line_width=1
            )

        # Draw vertical lines (X changes, Y runs full height)
        for col in range(cols + 1):
            x = col * sub_tile_size + x_offset
            arcade.draw_line(
                start_x=x,
                start_y=0 + y_offset,
                end_x=x,
                end_y=rows * sub_tile_size + y_offset,
                color=arcade.color.GRAY,
                line_width=1
            )

    def update_debug(self, on=False):
        if on:
            self.obstacle_list.draw_hit_boxes()
            self.player.draw_hit_box()
            self.item_list.draw_hit_boxes()
            self.enemy_list.draw_hit_boxes()
            self.draw_subgrid_lines(self.matrix_map, SUB_TILE_SIZE)

            """for weapon in self.weapon_list:
                weapon.ghost_hitbox.draw_hit_box(color=arcade.color.RED)"""




game = Game()
game.setup()
arcade.run()  # Corrected from game.run()
