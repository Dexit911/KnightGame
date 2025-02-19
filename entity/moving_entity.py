import arcade
import math
from animation import Animate


class MovingEntity(Animate):
    def __init__(self, game, img, scale=2.0, animate_time=10.0):
        super().__init__(img=img, scale=scale, animate_time=animate_time)
        self.game = game
        self.game.moving_entities.append(self)  # Ad to entity list that handles the draw

        self.dir = ["right", "down"]  # Start pos for Entity
        self.moving = False  # If the Entity is moving or not

        self.update_methods = []  # List of methods that need to be updated

        self.impulse_x = 0
        self.impulse_y = 0

    def get_impulse(self, power: int, direction: list, from_pos: list = None, invert: int = 1) -> None:
        """
        :param power: How strong the impulse is
        :param direction: What direction it goes from
        :param from_pos: Instead of Calculating from self.center_pos you can apply custom
        :param invert: If you want to invert the impulse, 1 is from, -1 is to
        """
        if from_pos is None:
            start_pos_x = self.center_x
            start_pos_y = self.center_y
        else:
            start_pos_x = from_pos[0]
            start_pos_y = from_pos[1]

        direction_x = start_pos_x - direction[0]
        direction_y = start_pos_y - direction[1]
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if length > 0:
            direction_x /= length
            direction_y /= length
        impulse_power = power
        self.impulse_x = direction_x * impulse_power * invert
        self.impulse_y = direction_y * impulse_power * invert

    def add_update(self, method_or_list) -> None:
        """Adds one or multiple methods to the update list."""
        if isinstance(method_or_list, list):
            self.update_methods.extend(method_or_list)
        else:
            self.update_methods.append(method_or_list)

    def on_update(self) -> None:
        """Update happens every frame"""
        super().update()
        self.change_x = 0
        self.change_y = 0

        # Apply impulse to movement
        self.center_x += self.impulse_x
        self.center_y += self.impulse_y

        # Apply impulse decay (smooth stop)
        self.impulse_x *= 0.9
        self.impulse_y *= 0.9

        # Stop impulse completely if it's very small
        if abs(self.impulse_x) < 0.1:
            self.impulse_x = 0
        if abs(self.impulse_y) < 0.1:
            self.impulse_y = 0

        self.adjust_layer()

        # Update every method in the list
        for method in self.update_methods:
            if callable(method):
                method()

    def adjust_layer(self) -> None:
        """Adjusting the layer based on sprites y cord"""
        sprite_list = self.game.moving_entities
        sprite_list.remove(self)
        for i, sprite in enumerate(sprite_list):
            if self.center_y > sprite.center_y:
                index = i
                break
        else:
            index = len(sprite_list)  # If not found, put at the end
        sprite_list.insert(index, self)  # Insert at correct layer position

    def die(self) -> None:
        """
        Removes entity safely from lists and deletes it.
        Use it instead of builtin kill()
        """
        if self in self.game.moving_entities:
            self.game.moving_entities.remove(self)
        self.kill()  # Remove from the game
