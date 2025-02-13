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

        self.impuls = [0, 0]  # Change from tuple to list

    def impulse(self, power: int, direction: list) -> None:
        """
        :param power: How strong the impulse is
        :param direction: What direction it has
        """
        direction_x, direction_y = direction
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if length > 0:
            direction_x /= length
            direction_y /= length
            print("calculated")

        self.impuls[0] += direction_x * power
        self.impuls[1] += direction_y * power

        print("impusle")

    def add_update(self, method_or_list) -> None:
        """Adds one or multiple methods to the update list."""
        if isinstance(method_or_list, list):
            self.update_methods.extend(method_or_list)
        else:
            self.update_methods.append(method_or_list)

    def on_update(self) -> None:
        """Update happens every frame"""
        super().update()
        #self.change_x = 0
        #self.change_y = 0

        # Apply impulse to movement
        self.change_x += self.impuls[0]
        self.change_y += self.impuls[1]

        # Apply impulse decay (smooth stop)
        self.impuls[0] *= 0.8
        self.impuls[1] *= 0.8

        # Stop impulse completely if it's very small
        if abs(self.impuls[0]) < 0.1:
            self.impuls[0] = 0
        if abs(self.impuls[1]) < 0.1:
            self.impuls[1] = 0

        self.adjust_layer()

        for method in self.update_methods:
            if callable(method):
                method()

    def adjust_layer(self) -> None:
        """Adjusting the layer based on sprites y cord"""
        sprite_list = self.game.moving_entities
        sprite_list.remove(self)
        index = 0
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
