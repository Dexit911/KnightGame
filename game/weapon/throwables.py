import arcade
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm
from core.hitboxes import CustomHitBoxes as Ch
from game.weapon import weapon_data as data

from game.weapon.weapon import Weapon


class Throwables(Weapon):
    def __init__(self, game, owner, config):
        super().__init__(
            game=game,
            owner=owner,
            config=config
        )

        """InputKeys"""
        self.keys = set()

        """Hitbox"""


        """Group"""
        self.collision_group = self.game.obstacle_list
        self.update_group = self.game.throwable_list

        """Sounds"""
        self.sounds = {"throw": [arcade.load_sound(Pm.player_sound("throw", f"Throw{i}.wav")) for i in range(1, 5)],
                       "land": "example"}

        """Stats"""
        self.speed = config["speed"]

        """UpdateMethods"""
        self.update_methods = [
            self.check_for_collision,
            self.update_fly
        ]

    def launch(self):
        """Launch towards mouse"""
        self.recoil_impulse()
        # Get target position
        target_pos = self.game.mouse_pos
        # Calculate launch and angle direction
        launch_direction = Vm.from_center_to(target_pos)
        angle = Vm.get_angle_from_center_to(target_pos) * -1
        # Apply the changes
        self.velocity = Vm.scale_vec2(launch_direction, self.speed)
        self.angle = angle - 90

        self.alive = True
        self.attacking = True

    def check_for_collision(self):
        """Destroy it when hitting a wall"""
        collision = arcade.check_for_collision_with_list(
            self, self.collision_group
        )
        if collision:
            self.alive = False

    def update_fly(self):
        if self.alive:
            self.check_for_collision()
            self.check_for_enemy(self)


class ThrowingKnife(Throwables):
    def __init__(self, game, owner):
        super().__init__(
            game=game,
            owner=owner,
            config=data.WEAPONS["throwable"]["small_knife"]
        )
