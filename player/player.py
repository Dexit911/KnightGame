import arcade
import math
from constance import *
from animation import Animate
from weapon import *
from entity.moving_entity import MovingEntity
from hitboxes import CustomHitBoxes as Ch
from arcade.hitbox import HitBox


class Player(MovingEntity):
    def __init__(self, game):
        super().__init__(img="source/player/idleAni1/Idle1.1.png", game=game)
        self.hit_box = HitBox(Ch().player)

        self.speed = 1
        self.keys = set()

        """Needs improvement, better storing"""
        self.idle1_frames = []
        self.idle1_fframes = []
        self.idle2_frames = []
        self.idle2_fframes = []
        self.idle3_frames = []
        self.idle3_fframes = []

        # Set the right textures
        self.change_texture()

        # Apply weapon
        #self.sword = Weapon(self.game, self, dmg=10, path="source/weapon/sword.png")
        self.sword = Sword(self.game, self)


        # Add all update methods to the list
        self.update_methods = [self.movement,
                               lambda: self.update_animation(delta_time=1),
                               self.sword.on_update,
                            ]

    def setup_textures(self):
        """Setups all the frames for animation"""
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

    def go_right(self):
        self.change_x = self.speed

    def go_up(self):
        self.change_y = self.speed

    def go_down(self):
        self.change_y = -self.speed

    def setup(self):
        self.center_x = 100
        self.center_y = 100
        self.setup_textures()

    def change_texture(self):
        """Change frames based in what direction you move"""
        if self.dir == ["left", "down"]:
            self.textures = self.idle1_frames
        elif self.dir == ["right", "down"]:
            self.textures = self.idle1_fframes
        elif self.dir == ["left", "up"]:
            self.textures = self.idle3_frames
        elif self.dir == ["right", "up"]:
            self.textures = self.idle3_fframes

    def movement(self):
        """Input for movement"""
        if arcade.key.A in self.keys:
            self.go_left()
        elif arcade.key.D in self.keys:
            self.go_right()

        if arcade.key.W in self.keys:
            self.go_up()
        elif arcade.key.S in self.keys:
            self.go_down()

        if arcade.key.E in self.keys:
            self.dash()

    def update_direction_based_on_mouse(self, mouse_x, mouse_y):
        new_horizontal = "right" if mouse_x > SCREEN_WIDTH / 2 else "left"
        new_vertical = "up" if mouse_y > SCREEN_HEIGHT / 2 else "down"

        if self.dir[0] != new_horizontal or self.dir[1] != new_vertical:
            self.dir[0] = new_horizontal
            self.dir[1] = new_vertical
            self.change_texture()

    def dash(self):
        """Makes character dash, by applying impulse"""
        mouse_pos = [self.game.mouse_x,
                     self.game.mouse_y]

        start_pos = [SCREEN_WIDTH / 2,
                     SCREEN_HEIGHT / 2]

        self.get_impulse(10, mouse_pos, start_pos, invert=-1)
