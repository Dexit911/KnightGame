import arcade
from animation import Animate


class Weapon(Animate):
    def __init__(self, game, owner, dmg, path):
        super().__init__(path)
        self.keys = set()
        self.game = game
        self.game.sprite_list.append(self)


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

    def update_dir(self):
        if self.owner.dir[0] == "left":
            self.texture = self.original_texture
        elif self.owner.dir[0] == "right":
            self.texture = self.flipped_texture

    def animate_attack(self):
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
        if not self.attacking:
            self.attacking = True
            self.attack_progress = 0

    def on_update(self):
        super().update()
        self.position = (self.owner.position[0] + self.pos_offset[0],
                         self.owner.position[1] + self.pos_offset[1])
        self.update_dir()

        if self.attacking:
            self.animate_attack()
        if arcade.key.SPACE in self.keys:
            self.hit()
