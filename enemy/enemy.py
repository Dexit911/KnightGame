import random
import arcade
from constance import *
from animation import *
import math
from entity.moving_entity import *

class Enemy(Animate):
    def __init__(self, game, x, y, hp=50):
        super().__init__(img="source/enemy/slime/Slime.png")
        # Add to enemies
        self.game = game
        self.game.enemy_list.append(self)
        self.collision = arcade.PhysicsEngineSimple(self, self.game.obstacle_list)

        self.sound = arcade.load_sound("sound/hitHurt.wav")

        # Set start pos
        self.center_x = x * TILE_SIZE
        self.center_y = y * TILE_SIZE

        self.knockback_x = 0
        self.knockback_y = 0

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
        self.sound.play()

    def apply_knockback(self, weapon):
        """Applies knockback when hit by a weapon."""

        direction_x = self.center_x - weapon.center_x
        direction_y = self.center_y - weapon.center_y
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length > 0:
            direction_x /= length
            direction_y /= length
        knockback_strength = 5  # Adjust as needed
        self.knockback_x = direction_x * knockback_strength
        self.knockback_y = direction_y * knockback_strength

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
                self.move_vector = (random.randint(-2, 2) * self.speed)/2, (random.randint(-2, 2) * self.speed)/2
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

    def on_update(self):
        super().update()
        self.check_for_player(trigger_d=100)
        self.force = (0, 0)
        self.collision.update()
        self.check_for_damage()

        self.center_y += self.knockback_y
        self.center_x += self.knockback_x

        self.knockback_x *= 0.8  # Slow down over time
        self.knockback_y *= 0.8

        if abs(self.knockback_x) < 0.1:
            self.knockback_x = 0
        if abs(self.knockback_y) < 0.1:
            self.knockback_y = 0
class EEnemy(MovingEntity):
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
        dx = self.center_x - weapon.center_x
        dy = self.center_y - weapon.center_y
        direction = [dx, dy]

        self.get_impulse(20, direction=direction)


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
