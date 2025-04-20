import arcade
import random
from core.utils.easing import Easing
from core.utils.path_manager import PathManager as Pm
from core.hitboxes import CustomHitBoxes as Ch
from core.constance import *


class Weapon(arcade.Sprite):
    """Parent class for all weapons"""

    def __init__(self, game, path, owner, hit_box, dmg, pos_offset=(0, -20), cooldown=20, power=5):
        """
        :param game: pass the whole game
        :param path: give path to the texture
        :param owner: apply to an owner
        :param hit_box: give a hit_box
        :param dmg: damage the weapon is dealing
        :param pos_offset: setup individual offset to make weapon look good
        :param cooldown: how fast the weapon hits
        """
        super().__init__(path_or_texture=path, scale=SCALE)

        """Input key list"""
        self.keys = set()

        """Add to group"""
        self.game = game
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)

        self.update_group = self.game.sprite_list
        self.update_group.append(self)

        """Sounds"""
        self.sounds = {"hit": [arcade.load_sound(Pm.common_sound(f"hit{i}.wav")) for i in range(1, 3)]}

        """Who owns the weapon"""
        self.owner = owner

        """Position"""
        self.pos_offset = pos_offset
        self.position = self.owner.position
        self.hit_box = hit_box

        """Texture"""
        self.original_texture = arcade.load_texture(path)
        self.flipped_texture = self.original_texture.flip_horizontally()

        """Stats"""
        self.dmg = dmg
        self.cooldown = cooldown
        self.power = power

        """Weapon state"""
        self.attacking = False
        self.attack_progress = 0
        self.cooldown_time = cooldown  # Total duration for the attack animation
        self.start_angle = 0  # starting rotation
        self.end_angle = 140  # ending rotation
        self.angle = 0  # current angle

    def update_attack_animation(self):
        if self.attacking:
            if self.owner.dir[0] == "left":
                invert = -1
            else:
                invert = 1

            self.attack_progress += 1
            progress = min(self.attack_progress / self.cooldown_time, 1)

            # Use the custom easing
            eased = Easing.swing_and_return(progress)

            self.angle = self.start_angle + (self.end_angle - self.start_angle) * eased * invert

            if progress >= 1:
                self.attacking = False
                self.attack_progress = 0
                self.angle = self.start_angle

    """def adjust_layer_based_on_owner(self):
        draw_group = self.draw_group
        if self in draw_group:
            draw_group.remove(self)

        owner_index = draw_group.index(self.owner)

        if self.owner.dir[1] == "down":
            draw_group.insert(owner_index + 1, self)  # Weapon in front
        else:
            draw_group.insert(owner_index - 1, self)  # Weapon behind or at same level"""

    def hit(self):
        """Prevents spam attack"""
        if not self.attacking:
            self.attacking = True

            # Play sound
            arcade.play_sound(random.choice(self.sounds.get("hit")))

            self.recoil_impulse()
            self.game.camera.start_shake(0.1, 3)
            self.attack_progress = 0

    def update_dir(self):
        """Turn the weapon if player turns"""
        if self.owner.dir[0] == "left":
            self.texture = self.original_texture
        elif self.owner.dir[0] == "right":
            self.texture = self.flipped_texture

    def recoil_impulse(self):
        from_x = SCREEN_WIDTH / 2
        from_y = SCREEN_HEIGHT / 2
        self.owner.get_impulse(2, self.game.mouse_pos, invert=-1, from_pos=[from_x, from_y])

    def on_update(self):
        super().update()
        # Update weapon position relative to owner
        self.position = (self.owner.position[0] + self.pos_offset[0],
                         self.owner.position[1] + self.pos_offset[1])

        self.update_dir()
        # self.adjust_layer_based_on_owner()

        if arcade.key.SPACE in self.keys:
            self.hit()

        if self.attacking:
            self.update_attack_animation()


"""Sword"""


class ClassicSword(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("sword", "ClassicSword.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=10,
                         cooldown=25,
                         power=5)


class BrokenSword(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("sword", "BrokenSword.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=2,
                         cooldown=60,
                         power=2)


class IronSword(Weapon):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            path=Pm.weapon_img("sword", "IronSword.png"),
            owner=owner,
            hit_box=Ch().sword,

            dmg=5, cooldown=50, power=3
        )


class RedSword(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("sword", "RedSword.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=4,
                         cooldown=20,
                         power=2)


"""AXES"""


class DoubleBigIronAxe(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("axe", "DoubleBigIronAxe.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=15,
                         cooldown=80,
                         power=6)


class IronLongAxe(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("axe", "IronLongAxe.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=10,
                         cooldown=70,
                         power=3)


"""Blunt"""


class WoodClub(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("blunt", "WoodClub.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=2,
                         cooldown=60,
                         power=10)


class ShortStick(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("blunt", "ShortStick.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=1,
                         cooldown=60,
                         power=2)


"""Dagger"""


class Dagger(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path=Pm.weapon_img("dagger", "Dagger.png"),
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=1,
                         cooldown=10,
                         power=1)
