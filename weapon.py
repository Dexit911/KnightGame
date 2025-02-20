import arcade
from animation import Animate
from arcade.hitbox import HitBox
from hitboxes import CustomHitBoxes as Ch


class Weapon(Animate):
    def __init__(self, game, owner, dmg, path):
        super().__init__(path)
        self.keys = set()
        self.game = game
        self.game.layer_adjusted_sprites.append(self)

        """Who carries the weapon"""
        self.owner = owner

        """Pos and individual offset"""
        self.position = self.owner.position
        self.pos_offset = (0, -20)

        """Damage"""
        self.dmg = dmg

        """Textures"""
        self.original_texture = arcade.load_texture(path)
        self.flipped_texture = arcade.load_texture(path).flip_horizontally()

        "Weapon state"
        self.attacking = False

        "Settings for animation"
        self.attack_progress = 0
        self.max_attack_progress = 20
        self.start_angle = None

        """CustomHitbox"""
        self.hit_box = HitBox(Ch().sword)

    def update_dir(self):
        """Turn the weapon if player turns, DOES NOT TURN HIT BOX WIWEIFWIEFHWEIOFHWEIFOQJWEJIFO"""
        if self.owner.dir[0] == "left":
            self.texture = self.original_texture
        elif self.owner.dir[0] == "right":
            self.texture = self.flipped_texture

    def animate_attack(self):
        """Basic animation for hitting with sword"""
        if self.owner.dir[0] == "left":
            if self.attack_progress < self.max_attack_progress:
                self.angle -= 15
                self.attack_progress += 1
            else:
                self.attacking = False
                self.angle = 0
        elif self.owner.dir[0] == "right":
            if self.attack_progress < self.max_attack_progress:
                self.angle += 15
                self.attack_progress += 1
            else:
                self.attacking = False
                self.angle = 0

    def hit(self):
        """Prevents spam attack"""
        if not self.attacking:
            self.attacking = True
            self.attack_progress = 0

    def weapon_push(self):
        pass

    def adjust_layer_based_on_owner(self):
        draw_group = self.game.layer_adjusted_sprites
        draw_group.remove(self)
        if self.owner.dir[1] == "down":
            draw_group.insert(self.owner.layer_index + 1, self)
        else:
            draw_group.insert(self.owner.layer_index - 1, self)

    def on_update(self):
        super().update()
        self.position = (self.owner.position[0] + self.pos_offset[0],
                         self.owner.position[1] + self.pos_offset[1])
        self.update_dir()

        # self.adjust_layer_based_on_owner()

        if self.attacking:
            self.animate_attack()
        if arcade.key.SPACE in self.keys:
            self.hit()


class WWeapon(arcade.Sprite):
    def __init__(self, game, path, owner, pos_offset, hit_box, dmg):
        super().__init__(path_or_texture=path)
        """Add to group"""
        self.game = game
        self.draw_group = self.game.layer_adjusted_sprites
        self.update_group = None

        """Who owns the weapon"""
        self.owner = owner

        """Position"""
        self.pos_offset = pos_offset
        self.position = self.owner.position
        self.hit_box = HitBox(hit_box)

        """Damage"""
        self.dmg = dmg

        """Texture"""
        self.original_image = arcade.load_texture(path)
        self.flipped_image = self.original_image.flip_horizontally()

        """Weapon state"""
        self.attacking = False

    def on_update(self):
        super().update()

        self.position = (self.owner.position[0] + self.pos_offset[0],
                         self.owner.position[1] + self.pos_offset[1])






