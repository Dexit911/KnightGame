import arcade
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm
from core.hitboxes import CustomHitBoxes as Ch
from core.constance import *


class WeaponTest(arcade.Sprite):

    def __init__(self, game, path, owner, hit_box, dmg, cooldown=20, power=5, shake=(0.1, 3)):
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
        self.update_group = self.game.sprite_list
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
        self.power = power
        self.shake = shake

        """State"""
        self.alive = True

    def recoil_impulse(self):
        from_x = SCREEN_WIDTH / 2
        from_y = SCREEN_HEIGHT / 2
        self.owner.get_impulse(
            2,
            self.game.mouse_pos,
            invert=-1,
            from_pos=[from_x, from_y])

    def on_update(self):
        for method in self.update_methods:
            if callable(method):
                method()

        if not self.alive:
            self.die()


        self.center_x += self.center_x

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


class Throwables(WeaponTest):
    def __init__(self, game, path, owner, dmg, cooldown=20):
        hit_box = Ch().default
        power = 5
        super().__init__(
            game=game,
            path=path,
            owner=owner,
            hit_box=hit_box,
            # Stats
            dmg=dmg, cooldown=cooldown, power=power
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
        self.power = power
        self.speed = 5

        """UpdateMethods"""
        self.update_methods = [
            self.check_for_collision
        ]

    def launch(self):
        """Launch towards mouse"""
        self.recoil_impulse()
        print("launched")
        launch_direction = Vm.from_center_to(self.game.mouse_x, self.game.mouse_y)
        self.change_x, self.change_y = launch_direction[0] * self.speed, launch_direction[1] * self.speed
        print(f"x: {self.change_x}, y: {self.change_y}")

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
            dmg=5, cooldown=10
        )
