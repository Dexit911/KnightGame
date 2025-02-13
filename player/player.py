import arcade
import math
from animation import Animate
from weapon import Weapon
from entity.moving_entity import MovingEntity

class Player(Animate):
    def __init__(self, game):
        super().__init__(img="source/player/idleAni1/Idle1.1.png", animate_time=10, scale=2)
        self.game = game
        self.game.moving_entities.append(self)

        self.speed = 1.5
        self.diagonal_speed = self.speed / 2
        self.change_x = 0
        self.change_y = 0

        self.keys = set()
        self.idle1_frames = []
        self.idle1_fframes = []
        self.idle2_frames = []
        self.idle2_fframes = []
        self.idle3_frames = []
        self.idle3_fframes = []

        self.dir = ["right", "down"]
        self.change_texture()

        self.mouse_x = 0
        self.mouse_y = 0

        self.sword = Weapon(self.game, self, dmg=10, path="source/weapon/sword.png")

    def setup_textures(self):
        self.idle1_frames = [arcade.load_texture(f"source/player/idleAni1/Idle1.{i}.png") for i in range(1, 5)]
        self.idle2_frames = [arcade.load_texture(f"source/player/idleAni2/Idle2.{i}.png") for i in range(1, 12)]
        self.idle3_frames = [arcade.load_texture(f"source/player/idleAni3/Idle3.{i}.png") for i in range(1, 5)]
        for i in range(1, 5):
            self.idle1_fframes.append(arcade.load_texture(f"source/player/idleAni1/Idle1.{i}.png").flip_horizontally())
        for i in range(1, 12):
            self.idle2_fframes.append(arcade.load_texture(f"source/player/idleAni2/Idle2.{i}.png").flip_horizontally())
        for i in range(1, 5):
            self.idle3_fframes.append(arcade.load_texture(f"source/player/idleAni3/Idle3.{i}.png").flip_horizontally())

    def go_left(self):
        self.textures = self.idle1_frames
        self.change_x = -self.speed
        self.dir[0] = "left"
        self.change_texture()

    def go_right(self):
        self.textures = self.idle1_fframes
        self.change_x = self.speed
        self.dir[0] = "right"
        self.change_texture()

    def go_up(self):
        self.change_y = self.speed
        self.dir[1] = "up"
        self.change_texture()

    def go_down(self):
        self.change_y = -self.speed
        self.dir[1] = "down"
        self.change_texture()

    def setup(self):
        self.center_x = 100
        self.center_y = 100
        self.setup_textures()

    def change_texture(self):
        if self.dir == ["left", "down"]:
            self.textures = self.idle1_frames
        elif self.dir == ["right", "down"]:
            self.textures = self.idle1_fframes
        elif self.dir == ["left", "up"]:
            self.textures = self.idle3_frames
        elif self.dir == ["right", "up"]:
            self.textures = self.idle3_fframes

    def movement(self):
        self.change_x = 0
        self.change_y = 0

        if arcade.key.A in self.keys:
            self.go_left()
        elif arcade.key.D in self.keys:
            self.go_right()

        if arcade.key.W in self.keys:
            self.go_up()
        elif arcade.key.S in self.keys:
            self.go_down()

    def on_update(self):
        super().update()
        self.movement()
        self.update_animation(delta_time=1)

        self.sword.on_update()

    def adjust_layer(self):
        sprite_list = self.game.moving_entities
        if self in sprite_list: a
        sprite_list.remove(self)
        index = 0
        for i, sprite in enumerate(sprite_list):
            if self.center_y > sprite.center_y:
                index = i
                break
        else:
            index = len(sprite_list)  # If not found, put at the end
        sprite_list.insert(index, self)  # Insert at correct layer position
class FPlayer(MovingEntity):
    def __init__(self, game):
        super().__init__(img="source/player/idleAni1/Idle1.1.png", game=game)

        self.speed = 1.5

        self.keys = set()
        self.idle1_frames = []
        self.idle1_fframes = []
        self.idle2_frames = []
        self.idle2_fframes = []
        self.idle3_frames = []
        self.idle3_fframes = []

        self.setup()
        self.sword = Weapon(self.game, self, dmg=10, path="source/weapon/sword.png")

        self.update_methods = [self.movement,
                               lambda: self.update_animation(delta_time=1.0),
                               self.sword.on_update,
                               lambda: print(self.dir)]

    def setup_textures(self):
        self.idle1_frames = [arcade.load_texture(f"source/player/idleAni1/Idle1.{i}.png") for i in range(1, 5)]
        self.idle2_frames = [arcade.load_texture(f"source/player/idleAni2/Idle2.{i}.png") for i in range(1, 12)]
        self.idle3_frames = [arcade.load_texture(f"source/player/idleAni3/Idle3.{i}.png") for i in range(1, 5)]
        for i in range(1, 5):
            self.idle1_fframes.append(arcade.load_texture(f"source/player/idleAni1/Idle1.{i}.png").flip_horizontally())
        for i in range(1, 12):
            self.idle2_fframes.append(arcade.load_texture(f"source/player/idleAni2/Idle2.{i}.png").flip_horizontally())
        for i in range(1, 5):
            self.idle3_fframes.append(arcade.load_texture(f"source/player/idleAni3/Idle3.{i}.png").flip_horizontally())

    def go_left(self):
        self.change_x = -self.speed
        self.dir[0] = "left"
        self.change_texture()

    def go_right(self):
        self.change_x = self.speed
        self.dir[0] = "right"
        self.change_texture()

    def go_up(self):
        self.change_y = self.speed
        self.dir[1] = "up"
        self.change_texture()

    def go_down(self):
        self.change_y = -self.speed
        self.dir[1] = "down"
        self.change_texture()

    def setup(self):
        self.center_x = 100
        self.center_y = 100
        self.setup_textures()

    def change_texture(self):
        if self.dir == ["left", "down"]:
            self.textures = self.idle1_frames
        elif self.dir == ["right", "down"]:
            self.textures = self.idle1_fframes
        elif self.dir == ["left", "up"]:
            self.textures = self.idle3_frames
        elif self.dir == ["right", "up"]:
            self.textures = self.idle3_fframes

    def movement(self):
        if arcade.key.A in self.keys:
            self.go_left()
        elif arcade.key.D in self.keys:
            self.go_right()

        if arcade.key.W in self.keys:
            self.go_up()
        elif arcade.key.S in self.keys:
            self.go_down()
