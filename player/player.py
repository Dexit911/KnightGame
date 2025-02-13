import arcade
import math
from animation import Animate


class Player(Animate):
    def __init__(self):
        super().__init__(img="source/player/idleAni1/Idle1.1.png", animate_time=10, scale=2)
        self.speed = 1
        self.change_x = 0
        self.change_y = 0


        self.keys = set()
        self.idle1_frames = []
        self.idle2_frames = []

    def setup_textures(self):
        self.idle1_frames = [arcade.load_texture(f"source/player/idleAni1/Idle1.{i}.png") for i in range(1, 5)]
        self.idle2_frames = [arcade.load_texture(f"source/player/idleAni2/Idle2.{i}.png") for i in range(1, 12)]


    def setup(self):
        self.center_x = 100
        self.center_y = 100
        self.setup_textures()

    def movement(self):
        self.change_x = 0
        self.change_y = 0

        if arcade.key.A in self.keys:
            self.change_x = -self.speed
        elif arcade.key.D in self.keys:
            self.change_x = self.speed

        if arcade.key.W in self.keys:
            self.change_y = self.speed
        elif arcade.key.S in self.keys:
            self.change_y = -self.speed

    def on_update(self):
        super().update()
        self.movement()
        self.update_animation(delta_time=1)

