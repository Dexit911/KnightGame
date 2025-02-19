import arcade


class Camera:
    def __init__(self, game, dead_zone_width=10, dead_zone_height=10, smooth_speed=0.2):
        """
        Initialize the Camera.

        :param game: Reference to the main game instance.
        :param dead_zone_width: work in progress
        :param dead_zone_height: word in progress
        :param smooth_speed: Speed of camera movement (lower = smoother).
        """
        self.game = game
        self.camera = arcade.Camera2D()
        self.dead_zone_width = dead_zone_width
        self.dead_zone_height = dead_zone_height
        self.smooth_speed = smooth_speed

    def update(self):
        """
        Moves the camera smoothly if the player exits the dead zone.
        """
        player_x, player_y = self.game.player.center_x, self.game.player.center_y
        camera_x, camera_y = self.camera.position

        left_bound = camera_x + (self.game.width / 2) - (self.dead_zone_width / 2)
        right_bound = camera_x + (self.game.width / 2) + (self.dead_zone_width / 2)
        bottom_bound = camera_y + (self.game.height / 2) - (self.dead_zone_height / 2)
        top_bound = camera_y + (self.game.height / 2) + (self.dead_zone_height / 2)

        target_x, target_y = camera_x, camera_y

        if player_x < left_bound:
            target_x = player_x - (self.dead_zone_width / 2)
        elif player_x > right_bound:
            target_x = player_x + (self.dead_zone_width / 2)

        if player_y < bottom_bound:
            target_y = player_y - (self.dead_zone_height / 2)
        elif player_y > top_bound:
            target_y = player_y + (self.dead_zone_height / 2)

        # Smooth transition using lerp
        new_x = arcade.math.lerp(camera_x, target_x, self.smooth_speed)
        new_y = arcade.math.lerp(camera_y, target_y, self.smooth_speed)

        self.camera.position = arcade.math.Vec2(new_x, new_y) # Apply the pos for camera

    def use(self):
        """Builtin camera method, used for rendering"""
        self.camera.use()
