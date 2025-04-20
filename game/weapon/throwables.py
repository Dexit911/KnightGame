import arcade
import random
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm
from core.utils.easing import Easing
from core.hitboxes import CustomHitBoxes as Ch
from core.constance import *

from game.weapon import weapon_data


class WeaponTest(arcade.Sprite):

    def __init__(self, game, path, owner, hit_box, dmg, cooldown=20, recoil=5, shake=(0.1, 3)):
        """
        :param game: pass the whole game
        :param path: give path to the texture
        :param owner: apply to an owner
        :param hit_box: give a hit_box
        :param dmg: damage the weapon is dealing
        :param cooldown: how fast the weapon hits
        """
        super().__init__(path_or_texture=path, scale=SCALE)

        """Connect to game, draw and update group"""
        # Update
        self.game = game
        self.update_group = self.game.weapon_list
        self.update_group.append(self)
        # Draw
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)

        """Update Methods"""
        self.update_methods = []

        """Texture"""
        self.original_texture = arcade.load_texture(path)

        """Hit-box"""
        self.hit_box = hit_box

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


class Melee(WeaponTest):
    def __init__(self, game, owner, config: dict):
        super().__init__(
            game=game,  # Connect to game
            owner=owner,  # Connect ot owner
            path=config.get("texture_path"),  # Set texture
            hit_box=Ch().sword,  # Apply hit-box
            dmg=config.get("damage"),  # Set the dmg
            cooldown=config.get("cooldown"),  # Set the cooldown on hit
            recoil=config.get("recoil"),  # Set the recoil
        )
        self.keys = set()

        """Melee exclusive"""
        self.knockback = config.get("knockback")  # How strong knockback the enemy is getting
        self.attack_style = config.get("attack_style")  # Style affects the hit pattern and animation
        self.attack_radius = config.get("attack_radius")  # How far the weapon is reaching
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
            arcade.play_sound(random.choice(self.sounds.get("hit")))
            self.recoil_impulse()
            self.game.camera.start_shake(strength=self.shake)

    def update_dir(self):
        if self.owner.dir[0] == "left":
            self.texture = self.original_texture
        elif self.owner.dir[0] == "right":
            self.texture = self.flipped_texture

    def follow_owner(self):
        self.position = Vm.add_vec2(self.owner.position, self.offset_pos)

    def update_attack_animation(self):
        if self.attacking:
            if self.owner.dir[0] == "left":
                invert = -1
            else:
                invert = 1

            self.attack_progress += 1
            progress = min(self.attack_progress / self.cooldown, 1)

            # Use the custom easing
            eased = Easing.swing_and_return(progress)

            self.angle = self.start_angle + (self.end_angle - self.start_angle) * eased * invert

            if progress >= 1:
                self.attacking = False
                self.attack_progress = 0
                self.angle = self.start_angle

    def update_methods_test(self):

        self.follow_owner()
        print("working")
        self.update_dir()

        if arcade.key.SPACE in self.keys: self.hit()
        if self.attacking: self.update_attack_animation()


class Throwables(WeaponTest):
    def __init__(self, game, path, owner, dmg, cooldown=20, speed=20, recoil=5):
        hit_box = Ch().default
        super().__init__(
            game=game,
            path=path,
            owner=owner,
            hit_box=hit_box,
            # Stats
            dmg=dmg, cooldown=cooldown, recoil=recoil
        )

        """InputKeys"""
        self.keys = set()

        """Collision"""
        self.collision_group = self.game.obstacle_list

        """Sounds"""
        self.sounds = {"throw": [arcade.load_sound(Pm.player_sound("throw", f"Throw{i}.wav")) for i in range(1, 5)],
                       "land": "example"}

        """Stats"""
        self.dmg = dmg
        self.cooldown = cooldown
        self.recoil = recoil
        self.speed = speed

        """UpdateMethods"""
        self.update_methods = [
            self.check_for_collision
        ]

    def launch(self):
        """Launch towards mouse"""
        self.recoil_impulse()
        # Get target position
        target_pos = self.game.mouse_pos

        # Calculate launch and angle direction
        launch_direction = Vm.from_center_to(target_pos)
        angle = Vm.get_angle_from_center_to(target_pos)

        # Apply the changes
        self.velocity = Vm.scale_vec2(launch_direction, self.speed)
        self.angle = angle - 90

    def check_for_collision(self):
        """Destroy it when hitting a wall"""
        collision = arcade.check_for_collision_with_list(
            self, self.collision_group
        )
        if collision:
            self.alive = False


class ThrowingKnife(Throwables):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            path=Pm.weapon_img("throwable", "ThrowingKnife.png"),
            owner=owner,

            # Stats
            dmg=5,
            cooldown=10,
            speed=20,
            recoil=2
        )


class ClassicSword(Melee):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=weapon_data.CLASSIC_SWORD
        )
