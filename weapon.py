import arcade
from animation import Animate
from arcade.hitbox import HitBox
from hitboxes import CustomHitBoxes as Ch
from constance import *


class Weapon(arcade.Sprite):
    """Parent class for all weapons"""
    def __init__(self, game, path, owner, hit_box, dmg, pos_offset=(0, -20), cooldown=20):
        super().__init__(path_or_texture=path, scale=SCALE)

        self.keys = set()

        """Add to group"""
        self.game = game
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)

        self.update_group = self.game.sprite_list
        self.update_group.append(self)

        """Who owns the weapon"""
        self.owner = owner

        """Position"""
        self.pos_offset = pos_offset
        self.position = self.owner.position
        self.hit_box = HitBox(hit_box)

        """Texture"""
        self.original_texture = arcade.load_texture(path)
        self.flipped_texture = self.original_texture.flip_horizontally()

        """Damage"""
        self.dmg = dmg

        self.cooldown = cooldown

        """Weapon state"""
        self.attacking = False
        self.attack_progress = 0
        self.cooldown_time = cooldown  # Total duration for the attack animation
        self.start_angle = 0  # starting rotation
        self.end_angle = 140  # ending rotation
        self.angle = 0  # current angle

    def update_attack_animation(self):
        """Update weapon rotation based on attack progress."""
        if self.attacking:
            print("attack animation")

            # Determine the inversion factor based on owner's horizontal direction.
            # Assume self.owner.dir[0] is "left" or "right"
            if self.owner.dir[0] == "left":
                invert = -1
            else:
                invert = 1

            # Increase progress
            self.attack_progress += 1

            # Normalize progress to a value between 0 and 1
            progress = min(self.attack_progress / self.cooldown_time, 1)

            # Compute current angle based on progress, applying the invert factor
            self.angle = self.start_angle + (progress * (self.end_angle - self.start_angle)) * invert

            # If attack is complete, reset state
            if progress >= 1:
                self.attacking = False
                self.attack_progress = 0
                self.angle = self.start_angle  # Reset to idle rotation

    def adjust_layer_based_on_owner(self):
        draw_group = self.game.layer_adjusted_sprites
        draw_group.remove(self)
        if self.owner.dir[1] == "down":
            draw_group.insert(self.owner.layer_index + 1, self)
        else:
            draw_group.insert(self.owner.layer_index - 1, self)

    def hit(self):
        """Prevents spam attack"""
        if not self.attacking:
            self.attacking = True
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
        """Pos"""
        self.position = (self.owner.position[0] + self.pos_offset[0],
                         self.owner.position[1] + self.pos_offset[1])

        self.update_dir()
        #self.adjust_layer_based_on_owner()

        if arcade.key.SPACE in self.keys:
            self.hit()

        if self.attacking:
            self.update_attack_animation()




class Sword(Weapon):
    def __init__(self, game, owner):
        super().__init__(game=game,
                         path="source/weapon/sword.png",
                         owner=owner,
                         hit_box=Ch().sword,
                         dmg=10)
