import random

import arcade

from game.weapon.throwables import ThrowingKnife
from game.weapon.weapon import *
from core.moving_entity import MovingEntity
from core.hitboxes import CustomHitBoxes as Ch
from core.utils.path_manager import PathManager as Pm
from core.cooldown_manager import CooldownManager
from game.items.item_factory import ItemFactory
from core.constance import *


class Player(MovingEntity):
    def __init__(self, game):
        super().__init__(img=Pm.player_img("idleAni1", "Idle1.1.png"), game=game)
        self.hit_box = Ch().player
        self.keys = set()

        self.sounds = {
            "dash": [arcade.load_sound(Pm.sound("player", f"Dash{i}.wav")) for i in range(1, 3)],
            "weapon_switch": [arcade.load_sound(Pm.sound("player", f"WeaponChange{i}.wav")) for i in range(1, 3)]
        }

        """Weapon"""
        self.weapon_classes = [
            ("sword", "classic_sword"),
            ("sword", "dragon_slayer"),
            ("axe", "double_iron_axe")
        ]

        self.weapon_index = 0
        weapon_type, weapon_id = self.weapon_classes[self.weapon_index]
        self.weapon = ItemFactory.create_weapon(self.game, self, weapon_type, weapon_id)

        self.thrown_classes = [ThrowingKnife]

        """Stats"""
        self.stats_base = {
            "max_hp": 100,
            "hp": 100,
            # Protection--------

            "protection": 0,
            "damage_reduction": 0,
            "evasion": 0,

            # Speed-------------
            "speed": 1,
            "speed_multi": 1,

            # Dash--------------
            "dash_power": 15,
            "dash_cd": 30,
            "dash_cd_multi": 0,

            # Critical damage---
            "critical_chance": 0,
            "critical_mult": 0,

            # Throw-------------
            "throw_cd": 50,
            "throw_cd_multi": 0,  # %

            # Other-------------
            "life_steal": 0,
            "luck": 0,
        }
        self.stats = self.stats_base.copy()

        """Inventory """
        self.inv = {"coin": 0}

        """Cooldown"""
        self.cd = CooldownManager()
        self.cd.add("dash", self.stats["dash_cd"])
        self.cd.add("throw", self.stats["throw_cd"])
        self.cd.add("weapon_switch", 15)

        """Update Methods"""
        self.update_methods = [
            lambda: self.update_animation(delta_time=1),
            self.input,
            self.check_item_picked_up,
            self.cd.tick_all,
        ]

    def setup_textures(self):
        """Setups all the frames for animation"""
        self.idle1_frames = [arcade.load_texture(Pm.player_img("idleAni1", f"Idle1.{i}.png")) for i in range(1, 5)]
        self.idle2_frames = [arcade.load_texture(Pm.player_img("idleAni2", f"Idle2.{i}.png")) for i in range(1, 12)]
        self.idle3_frames = [arcade.load_texture(Pm.player_img("idleAni3", f"Idle3.{i}.png")) for i in range(1, 5)]
        self.idle1_fframes = [tex.flip_horizontally() for tex in self.idle1_frames]
        self.idle2_fframes = [tex.flip_horizontally() for tex in self.idle2_frames]
        self.idle3_fframes = [tex.flip_horizontally() for tex in self.idle3_frames]

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

    def setup(self):
        self.position = (0, 0)
        self.setup_textures()

    def go_direction(self, direction):
        """"""
        change = self.stats["speed"] * self.stats["speed_multi"]
        match direction:
            case "left":
                self.change_x = -change
            case "right":
                self.change_x = change
            case "up":
                self.change_y = change
            case "down":
                self.change_y = -change

    def input(self):
        """Updates all Input"""
        # Input for movement -----------------------------------------------------------
        if arcade.key.A in self.keys:
            self.go_direction("left")
        elif arcade.key.D in self.keys:
            self.go_direction("right")
        if arcade.key.W in self.keys:
            self.go_direction("up")
        elif arcade.key.S in self.keys:
            self.go_direction("down")

        # Input for Dash ---------------------------------------------------------------
        if arcade.key.E in self.keys and self.cd.ready("dash"):
            self.dash()
            self.cd.reset_with_change("dash", self.stats["dash_cd_multi"])

        # Input for Switch weapons -----------------------------------------------------
        if arcade.key.R in self.keys and self.cd.ready("weapon_switch"):
            self.change_weapon()
            arcade.play_sound(random.choice(self.sounds.get("weapon_switch")), volume=1)
            self.cd.reset("weapon_switch")

        # Input for Throwing -----------------------------------------------------------
        if arcade.key.Q in self.keys and self.cd.ready("throw"):
            knife = self.thrown_classes[0]
            knife(self.game, self).launch()
            self.cd.reset_with_change("throw", self.stats["throw_cd_multi"])

    def update_direction_based_on_mouse(self, mouse_x, mouse_y):
        """Turns the sprite base on mouse position"""
        new_horizontal = "right" if mouse_x > SCREEN_WIDTH / 2 else "left"
        new_vertical = "up" if mouse_y > SCREEN_HEIGHT / 2 else "down"
        if self.dir[0] != new_horizontal or self.dir[1] != new_vertical:
            self.dir[0] = new_horizontal
            self.dir[1] = new_vertical
            self.change_texture()

    def dash(self):
        """Makes character dash, by applying impulse"""
        dash_sound = self.sounds.get("dash")
        arcade.play_sound(random.choice(dash_sound), volume=VOLUME)
        mouse_pos = [self.game.mouse_x,
                     self.game.mouse_y]
        start_pos = [SCREEN_WIDTH / 2,
                     SCREEN_HEIGHT / 2]
        # arcade.play_sound(self.sounds["dash"])
        self.get_impulse(self.stats["dash_power"], mouse_pos, start_pos, invert=-1)

    def check_item_picked_up(self):
        """Checks for if you are touching dropped items"""
        hit_list = arcade.check_for_collision_with_list(self, self.game.item_list)
        for item in hit_list:
            item.on_picked_up()
            item.remove_from_sprite_lists()  # Automatically removed from item_list

    # Item management --------------------------------------------------------------------------------------------------
    def set_coin(self, amount):
        self.inv["coin"] += amount

    def heal(self, hp):
        self.stats["hp"] += hp
        if self.stats["hp"] > self.stats["max_hp"]:
            self.stats["hp"] = self.stats["max_hp"]

    def change_weapon(self):
        """Switch to next weapon instance"""
        if not self.weapon.attacking:
            # Safety list check --------------------------------------------------
            if self.weapon in self.game.layer_adjusted_sprites:
                self.game.layer_adjusted_sprites.remove(self.weapon)
            if self.weapon in self.game.sprite_list:
                self.game.sprite_list.remove(self.weapon)
            # Delete the current weapon ------------------------------------------
            self.weapon.kill()
            # Go to next weapon in index -----------------------------------------
            self.weapon_index = (self.weapon_index + 1) % len(self.weapon_classes)
            # Create the next weapon ---------------------------------------------
            weapon_type, weapon_id = self.weapon_classes[self.weapon_index]
            self.weapon = ItemFactory.create_weapon(
                self.game, self, weapon_type, weapon_id
            )

    def __str__(self):
        return f"stats: {self.stats}\n inv: {self.inv}"
