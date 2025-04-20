import random

import arcade

from game.weapon.throwables import ThrowingKnife
from game.weapon.throwables import ClassicSword
from core.moving_entity import MovingEntity
from core.hitboxes import CustomHitBoxes as Ch
from core.utils.path_manager import PathManager as Pm
from core.cooldown_manager import CooldownManager
from core.constance import *


class Player(MovingEntity):
    def __init__(self, game):
        super().__init__(img=Pm.player_img("idleAni1", "Idle1.1.png"), game=game)
        self.hit_box = Ch().player

        self.speed = 1
        self.keys = set()

        """Texture and sound"""
        self.idle1_frames = []
        self.idle1_fframes = []
        self.idle2_frames = []
        self.idle2_fframes = []
        self.idle3_frames = []
        self.idle3_fframes = []
        self.change_texture()

        self.sounds = {
            "dash": [arcade.load_sound(Pm.sound("player", f"Dash{i}.wav")) for i in range(1, 3)],
            "weapon_switch": [arcade.load_sound(Pm.sound("player", f"WeaponChange{i}.wav")) for i in range(1, 3)]
        }

        """Weapon"""
        self.weapon_classes = [ClassicSword]
        self.weapon_index = 0
        self.weapon = self.weapon_classes[self.weapon_index](self.game, self)

        self.thrown_classes = [ThrowingKnife]


        """Inventory """
        self.inv = {"coin": 0}

        """Cooldown"""
        self.cooldowns = CooldownManager()
        self.cooldowns.add("dash", 30)
        self.cooldowns.add("weapon_switch", 15)
        self.cooldowns.add("throw", 50)

        """Update Methods"""
        self.update_methods = [
            lambda: self.update_animation(delta_time=1),
            self.movement,
            self.weapon_update,
            self.check_item_picked_up,
            self.cooldowns.tick_all,

        ]

    def setup_textures(self):
        """Setups all the frames for animation"""

        self.idle1_frames = [
            arcade.load_texture(Pm.player_img("idleAni1", f"Idle1.{i}.png")) for i in range(1, 5)
        ]
        self.idle2_frames = [
            arcade.load_texture(Pm.player_img("idleAni2", f"Idle2.{i}.png")) for i in range(1, 12)
        ]
        self.idle3_frames = [
            arcade.load_texture(Pm.player_img("idleAni3", f"Idle3.{i}.png")) for i in range(1, 5)
        ]

        self.idle1_fframes = [tex.flip_horizontally() for tex in self.idle1_frames]
        self.idle2_fframes = [tex.flip_horizontally() for tex in self.idle2_frames]
        self.idle3_fframes = [tex.flip_horizontally() for tex in self.idle3_frames]

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

        if arcade.key.E in self.keys and self.cooldowns.ready("dash"):
            self.dash()
            self.cooldowns.reset("dash")

        if arcade.key.R in self.keys and self.cooldowns.ready("weapon_switch"):
            self.change_weapon()
            arcade.play_sound(random.choice(self.sounds.get("weapon_switch")), volume=1)
            self.cooldowns.reset("weapon_switch")

        if arcade.key.Q in self.keys and self.cooldowns.ready("throw"):
            knife = self.thrown_classes[0]
            knife(self.game, self).launch()
            self.cooldowns.reset("throw")



    def update_direction_based_on_mouse(self, mouse_x, mouse_y):
        new_horizontal = "right" if mouse_x > SCREEN_WIDTH / 2 else "left"
        new_vertical = "up" if mouse_y > SCREEN_HEIGHT / 2 else "down"

        if self.dir[0] != new_horizontal or self.dir[1] != new_vertical:
            self.dir[0] = new_horizontal
            self.dir[1] = new_vertical
            self.change_texture()

    def dash(self):
        """Makes character dash, by applying impulse"""

        dash_sound = self.sounds.get("dash")

        arcade.play_sound(random.choice(dash_sound), volume=0.7)

        mouse_pos = [self.game.mouse_x,
                     self.game.mouse_y]
        start_pos = [SCREEN_WIDTH / 2,
                     SCREEN_HEIGHT / 2]

        # arcade.play_sound(self.sounds["dash"])
        self.get_impulse(10, mouse_pos, start_pos, invert=-1)

    def check_item_picked_up(self):
        hit_list = arcade.check_for_collision_with_list(self, self.game.item_list)

        for item in hit_list:
            item.on_picked_up(self)
            item.remove_from_sprite_lists()  # Automatically removed from item_list

    """Items"""

    def set_coin(self, amount):
        self.inv["coin"] += amount
        print(self.inv["coin"])

    def change_weapon(self):
        # Remove the current weapon from groups
        if self.weapon in self.game.layer_adjusted_sprites:
            self.game.layer_adjusted_sprites.remove(self.weapon)
        if self.weapon in self.game.sprite_list:
            self.game.sprite_list.remove(self.weapon)

        # Kill current weapon
        self.weapon.kill()

        # Go to next weapon in the list
        self.weapon_index = (self.weapon_index + 1) % len(self.weapon_classes)
        self.weapon = self.weapon_classes[self.weapon_index](self.game, self)

    def weapon_update(self):
        if self.weapon:
            self.weapon.on_update()
