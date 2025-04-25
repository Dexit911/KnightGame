import arcade
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm
from core.hitboxes import CustomHitBoxes as Ch

from game.weapon.weapon import Weapon


class Throwables(Weapon):
    def __init__(self, game, path, owner, dmg, cooldown=20, speed=20, recoil=5):
        super().__init__(
            game=game,
            path=path,
            owner=owner,
            # Stats
            dmg=dmg, cooldown=cooldown, recoil=recoil
        )

        """InputKeys"""
        self.keys = set()

        """Hitbox"""
        self.hit_box = Ch().default

        """Group"""
        self.collision_group = self.game.obstacle_list
        self.update_group = self.game.throwable_list

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
        angle = Vm.get_angle_from_center_to(target_pos) * -1

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
