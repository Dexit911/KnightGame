import arcade
import random


class Camera:
    def __init__(self, game, smooth_speed=0.2):
        self.game = game
        self.camera = arcade.Camera2D()
        self.smooth_speed = smooth_speed
        self.shake_timer = 0
        self.shake_strength = 0

    def update(self):
        player_x, player_y = self.game.player.center_x, self.game.player.center_y
        camera_x, camera_y = self.camera.position
        target_x, target_y = player_x, player_y
        new_x = arcade.math.lerp(camera_x, target_x, self.smooth_speed)
        new_y = arcade.math.lerp(camera_y, target_y, self.smooth_speed)
        if self.shake_timer > 0:
            new_x += random.uniform(-self.shake_strength, self.shake_strength)
            new_y += random.uniform(-self.shake_strength, self.shake_strength)
            self.shake_timer -= 1 / 60
            if self.shake_timer < 0:
                self.shake_timer = 0
        self.camera.position = arcade.math.Vec2(new_x, new_y)

    def use(self):
        self.camera.use()

    def start_shake(self, duration, strength):
        self.shake_timer = duration
        self.shake_strength = strength
