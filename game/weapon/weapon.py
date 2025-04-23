import arcade
import random
from arcade.hitbox import HitBox
from core.utils.hitbox_manager import HitboxManager as Hm
from core.utils.vector_manager import VectorManager as Vm
from core.cooldown_manager import CooldownManager as Cm
from core.simple_animation import SimpleAnimation
from core.utils.easing import Easing
from core.constance import *
from game.weapon.weapon_data import *


class Weapon(arcade.Sprite):

    def __init__(self, game, path, owner, dmg, cooldown=20, recoil=5, shake=(0.1, 3)):
        """
        :param game: pass the whole game
        :param path: give path to the texture
        :param owner: apply to an owner
        :param dmg: damage the weapon is dealing
        :param cooldown: how fast the weapon hits
        """
        super().__init__(path_or_texture=path, scale=2.1)

        """Update group"""
        self.game = game
        self.update_group = self.game.weapon_list
        self.update_group.append(self)
        """Draw group"""
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)
        """Update Methods"""
        self.update_methods = []
        """Texture"""
        self.original_texture = arcade.load_texture(path)
        """Set owner"""
        self.owner = owner
        """Position"""
        self.position = self.owner.position
        """Stats"""
        self.dmg = dmg
        self.cooldown = cooldown
        self.recoil = recoil
        self.shake = shake
        """State"""
        self.alive = True

    def recoil_impulse(self):
        from_x = SCREEN_WIDTH / 2
        from_y = SCREEN_HEIGHT / 2
        self.owner.get_impulse(
            self.recoil,
            self.game.mouse_pos,
            invert=-1,
            from_pos=[from_x, from_y])

    def on_update(self):
        for method in self.update_methods:
            if callable(method):
                method()

        if not self.alive:
            self.die()

        super().update()

    def add_update(self, method_or_list) -> None:
        """Adds one or multiple methods to the update list."""
        if isinstance(method_or_list, list):
            self.update_methods.extend(method_or_list)
        else:
            self.update_methods.append(method_or_list)

    def die(self):
        self.visible = False
        if self in self.draw_group:
            self.draw_group.remove(self)
        if self in self.update_group:
            self.update_group.remove(self)
        self.kill()


class Melee(Weapon):
    def __init__(self, game, owner, config: dict):
        super().__init__(
            game=game,  # Connect to game
            owner=owner,  # Connect ot owner
            path=config.get("texture_path"),  # Set texture
            dmg=config.get("damage"),  # Set the dmg
            cooldown=config.get("cooldown"),  # Set the cooldown on hit
            recoil=config.get("recoil"),  # Set the recoil
        )
        """Set Keys"""
        self.keys = set()
        """Melee exclusive"""
        self.knockback = config.get("knockback")  # How strong knockback the enemy is getting
        self.attack_style = config.get("attack_style")  # Style affects the hit pattern and animation
        self.attack_radius = config.get("attack_radius")  # How far the weapon is reaching
        self.attack_angle = config.get("attack_angle")
        """Texture"""
        self.original_texture = arcade.load_texture(config.get("texture_path"))
        self.flipped_texture = self.original_texture.flip_horizontally()
        """Sounds"""
        self.sounds = {
            "hit": [arcade.load_sound(Pm.common_sound(f"Hit{i}.wav")) for i in range(1, 3)]
        }
        """Pos"""
        self.offset_pos = config.get("offset_pos")
        self.shake = config.get("shake_effect")
        """HitBox"""
        self.cooldowns = Cm()
        self.cooldowns.add("hitbox", 10)
        self.ghost_hitbox = arcade.Sprite(
            path_or_texture=None
        )
        """State"""
        self.attacking = False
        self.attack_progress = 0  # Total duration for the attack animation
        self.start_angle = 0  # starting rotation
        self.end_angle = 140  # ending rotation
        self.angle = 0  # current angle

        self.add_update(self.update_methods_test)

    def hit(self):
        if not self.attacking:
            self.attacking = True
            self.cooldowns.start("hitbox")

            arcade.play_sound(random.choice(self.sounds.get("hit")))
            self.recoil_impulse()
            self.game.camera.start_shake(strength=self.shake)

    def start_attack(self):
        if self.attacking:
            self.update_attack_hitbox()

            """Animation"""
            if self.owner.dir[0] == "left":
                invert = -1
            else:
                invert = 1
            self.attack_progress += 1
            progress = min(self.attack_progress / self.cooldown, 1)
            eased = Easing.swing_and_return(progress)
            self.angle = self.start_angle + (self.end_angle - self.start_angle) * eased * invert

            """Check if enemies in the swing"""
            for enemy in self.game.enemy_list:
                if Hm.check_overlap(self.ghost_hitbox, enemy) and not enemy.took_damage:
                    enemy.get_hit(self)

            if progress >= 1:
                self.end_attack()

    def end_attack(self):
        self.attacking = False
        self.attack_progress = 0
        self.angle = self.start_angle
        # self.ghost_hitbox.hit_box = HitBox([])

    def update_attack_hitbox(self):
        if not self.cooldowns.ready("hitbox"):
            position = self.position
            radius = self.attack_radius  # How big the hit box is going to be
            angle = Vm.get_angle(position, self.game.mouse_world) + 180  # Rotate it towards mouse
            span = self.attack_angle  # How big the pizza slice is going to be
            # Apply the new hitbox
            self.ghost_hitbox.hit_box = HitBox(Hm.sector(position, radius, angle, span))
        else:
            self.ghost_hitbox.hit_box = HitBox([(0, 0)])

    def follow_owner(self):
        self.position = Vm.add_vec2(self.owner.position, self.offset_pos)

    def update_dir(self):
        if self.owner.dir[0] == "left":
            self.texture = self.original_texture
        elif self.owner.dir[0] == "right":
            self.texture = self.flipped_texture

    def update_methods_test(self):
        self.follow_owner()
        self.update_dir()
        self.cooldowns.tick_all()

        if arcade.key.SPACE in self.keys:
            self.hit()
        if self.attacking:
            self.start_attack()


class ClassicSword(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=CLASSIC_SWORD
        )


class IronLongAxe(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=IRON_LONG_AXE
        )


class RedSword(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=RED_SWORD
        )


class IronHammer(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=IRON_HAMMER
        )


class DoubleIronAxe(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=DOUBLE_IRON_AXE
        )



class WoodClub(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=WOOD_CLUB
        )



class DragonSlayer(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=DRAGON_SLAYER
        )




