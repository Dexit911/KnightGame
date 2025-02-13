import random
import arcade
from constance import *
from animation import *
import math
from entity.moving_entity import *


class Enemy(MovingEntity):
    def __init__(self, game, x, y, hp=1000):
        super().__init__(img="source/enemy/slime/Slime.png", game=game)
        # Add to enemies
        self.game.enemy_list.append(self)
        self.collision = arcade.PhysicsEngineSimple(self, self.game.obstacle_list)

        self.sound = arcade.load_sound("sound/hitHurt.wav")

        # Set start pos
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
        self.max_steps = 20
        self.current_steps = 0

        self.move_vector = None

        self.update_methods = [lambda: self.check_for_player(trigger_d=100),
                               self.collision.update,
                               self.check_for_damage]

    def check_for_damage(self):
        weapon = self.game.player.sword
        if weapon.attacking:
            collide = arcade.check_for_collision(self, weapon)  # FIX: Check against weapon, not player
            if collide and not self.took_damage:  # FIX: Don't reset it every frame

                self.get_hit(weapon)
                self.took_damage = True  # Mark that this enemy was hit this attack

        if not weapon.attacking:  # Reset when attack is over
            self.took_damage = False

        if self.hp <= 0:
            self.kill()

    def get_hit(self, weapon):
        self.color = (255, 255, 255)
        self.hp -= weapon.dmg
        self.apply_knockback(weapon)
        arcade.play_sound(self.sound)

    def apply_knockback(self, weapon):
        """Applies consistent knockback away from the weapon on hit."""

        # Step 1: Get direction from weapon to enemy (opposite of impact)
        direction_x = self.center_x - weapon.center_x
        direction_y = self.center_y - weapon.center_y

        # Step 2: Normalize the direction so knockback is always the same strength
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length > 0:
            direction_x /= length
            direction_y /= length

        # Step 3: Apply a FIXED knockback strength (independent of distance)
        knockback_strength = 20  # Adjust this value to control knockback force
        self.impulse(knockback_strength, [direction_x, direction_y])

        print(f"Knockback applied! Direction: ({direction_x}, {direction_y}), Strength: {knockback_strength}")

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
                self.max_steps = random.randint(50, 60)
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
                self.move_vector = (random.randint(-2, 2) * self.speed) / 2, (random.randint(-2, 2) * self.speed) / 2
                self.change_x, self.change_y = self.move_vector
                self.idle_movement_state = "moving"

    def alert_movement(self):
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
        distance = arcade.get_distance_between_sprites(self.game.player, self)
        if distance <= 10:
            pass
        elif distance <= trigger_d:
            self.alert_movement()
        else:
            self.idle_movement()
