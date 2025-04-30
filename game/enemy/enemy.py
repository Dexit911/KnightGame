import random
import arcade
from core.constance import *
from core.moving_entity import *
from core.utils.path_manager import PathManager as Pm
from game.weapon.throwables import Throwables
from game.weapon.weapon import Weapon
from game.items.item_factory import ItemFactory
import time

from game.items.item import Coin


class Enemy(MovingEntity):
    def __init__(self, game, x, y, hp=20):
        super().__init__(img=Pm.img("enemy", "slime", "Slime.png"), game=game)
        # Add to enemies
        self.game.enemy_list.append(self)

        # have collision with obstacles
        self.obstacle_group = self.game.obstacle_list
        self.collision = arcade.PhysicsEngineSimple(self, self.obstacle_group)

        # just a random sound fot hit
        # self.sounds = {"hurt": [arcade.load_sound(Pm.common_sound(f"Hurt{i}.wav")) for i in range(1, 5)]}

        # Set start pos, based on tile
        self.center_x = x * TILE_SIZE
        self.center_y = y * TILE_SIZE
        # sets up the speed
        self.speed = 0.5
        self.hp = hp
        self.took_damage = False

        # storing directions
        self.idle_movement_state = "resting"
        self.current_stalling_time = 0
        self.stalling_time = 0
        self.max_steps = 0
        self.current_steps = 0

        self.move_vector = None
        # Update Methods
        self.update_methods = [lambda: self.check_for_player(trigger_d=50),
                               self.collision.update,
                               self.check_for_damage]

        self.damage_sources = []

        """Sounds"""
        self.sounds = {
            "hurt": [arcade.load_sound(Pm.sound("enemy", "slime", f"SlimeHurt{i}.wav")) for i in range(1, 4)]}

    def check_for_damage(self):
        new_sources = []

        for damage_source in self.damage_sources:
            if isinstance(damage_source, Throwables):
                continue  # handle this separately if needed

            if isinstance(damage_source, Weapon):
                if damage_source.attacking:
                    new_sources.append(damage_source)

        # Allow damage again only if list is now empty
        if not new_sources:
            self.took_damage = False

        self.damage_sources = new_sources

    def drop_loot(self):
        position = self.position
        game = self.game
        trinket_haste = ItemFactory.create_trinket(game, "haste_amulet")
        trinket_haste.drop(position)
        trinket_dash = ItemFactory.create_trinket(game, "dash_feather")
        trinket_dash.drop(position)
        trinket_throw = ItemFactory.create_trinket(game, "kunai_charm")
        trinket_throw.drop(position)

    def get_hit(self, weapon):
        """When enemy get hit"""
        if weapon.attacking and not self.took_damage:
            # Play sound
            arcade.play_sound(random.choice(self.sounds["hurt"]), volume=2)
            self.hp -= weapon.dmg  # Reduce
            self.took_damage = True

            self.damage_sources.append(weapon)
            if self.hp <= 0:
                self.die()
                self.drop_loot()

            self.get_impulse(weapon.knockback, [weapon.center_x, weapon.center_y])  # Get knockback

    """Stopped working after migrating to MovingEntity parent class"""

    def idle_movement(self):
        # If you are moving
        if self.idle_movement_state == "moving":
            # Check if you have walked enough
            if self.current_steps < self.max_steps:
                # If not, add a step
                self.current_steps += 1
            # If you have walked enough
            else:
                # Stop, and go in the "resting" state
                self.current_steps = 0
                self.max_steps = random.randint(100, 150)
                self.change_x, self.change_y = 0, 0
                self.idle_movement_state = "resting"

        # If you are resting
        elif self.idle_movement_state == "resting":
            # Check if you have rested enough
            if self.current_stalling_time < self.stalling_time:
                # If not, add time to current rest timer
                self.current_stalling_time += 1
            else:
                # If you rested enough
                self.current_stalling_time = 0
                self.stalling_time = random.randint(100, 200)
                self.move_vector = (random.randint(-2, 2) * self.speed), (random.randint(-2, 2) * self.speed)
                self.change_x, self.change_y = self.move_vector
                self.idle_movement_state = "moving"

    def alert_movement(self):
        """Makes enemy run to player"""
        player_x, player_y = self.game.player.center_x, self.game.player.center_y
        dx = player_x - self.center_x
        dy = player_y - self.center_y

        # Normalize the vector
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length

        # Apply speed
        self.change_x = dx * self.speed
        self.change_y = dy * self.speed

    def check_for_player(self, trigger_d):
        """Change enemy behaviour based on the distance from player"""
        distance = arcade.get_distance_between_sprites(self.game.player, self)
        if distance <= 10:
            pass
        elif distance <= trigger_d:
            self.alert_movement()
        else:
            self.idle_movement()


class EnemyTest(MovingEntity):
    pass


class EnemyAi(MovingEntity):
    pass


class PathfindingManager:
    def __init__(self, game):
        self.game = game
        self.grid = self.create_grid()

    def create_grid(self):
        # Build the walkable/non-walkable grid from the map
        pass

    def is_walkable(self, x, y):
        # Return True if tile (x,y) can be walked
        pass

    def neighbors(self, x, y):
        # Return valid neighbor tiles
        pass

    def find_path(self, start, goal):
        # Launch A* search (maybe in multiprocessing)
        pass

    def update_grid(self):
        # If the world changes, update the walkability map
        pass
