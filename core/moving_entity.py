import math
from core.animation import Animate


class MovingEntity(Animate):
    def __init__(self, game, img, scale=2.0, animate_time=10.0):
        super().__init__(img=img, scale=scale, animate_time=animate_time)
        self.game = game
        # self.game.moving_entities.append(self)  # Ad to entity list that handles the draw
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)
        self.layer_index = self.draw_group.index(self)

        self.dir = ["right", "down"]  # Start pos for Entity
        self.is_moving = False  # If the Entity is moving or not

        self.update_methods = []  # List of methods that need to be updated

        # Impulse atr
        self.impulse_x = 0
        self.impulse_y = 0
        self.in_impulse = False

        # Collision atr
        self.collision_group = None
        self.collision = None

        # Layer atr
        self.old_y = self.center_y
        self.needs_layer_adjust = False

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

        self.in_impulse = True

    def handle_impulse_collision(self, pre_x, pre_y):
        if int(self.center_x) == int(pre_x):
            self.impulse_x = 0
        if int(self.center_y) == int(pre_y):
            self.impulse_y = 0
            self.center_y = pre_y  # prevent bad layer shift

    def update_impulse(self):
        """Updates Impulse - checks: If layer adjust is needed, if you collide and need to stop"""
        if self.in_impulse:
            # Store position before movement
            old_x = self.center_x
            old_y = self.center_y

            # Apply impulse movement
            self.center_x += self.impulse_x
            self.center_y += self.impulse_y

            # Let physics correct illegal movement
            if self.collision:
                self.collision.update()
                self.handle_impulse_collision(old_x, old_y)

            # Check what actually changed
            if int(self.center_y) != int(old_y):
                self.needs_layer_adjust = True
                self.old_y = self.center_y

            # Optional: stop impulse if movement blocked
            if int(self.center_x) == int(old_x):
                self.impulse_x = 0
            if int(self.center_y) == int(old_y):
                self.impulse_y = 0

        # Impulse decay
        self.impulse_x *= 0.9
        self.impulse_y *= 0.9

        if abs(self.impulse_x) < 0.1:
            self.impulse_x = 0
        if abs(self.impulse_y) < 0.1:
            self.impulse_y = 0

        self.in_impulse = bool(self.impulse_x or self.impulse_y)

    def add_update(self, method_or_list) -> None:
        """Adds one or multiple methods to the update list."""
        if isinstance(method_or_list, list):
            self.update_methods.extend(method_or_list)
        else:
            self.update_methods.append(method_or_list)

    def on_update(self) -> None:
        """Update happens every frame"""
        super().update()

        self.update_movement_state()
        self.update_impulse()
        self.update_layer_adjust()

        # Update every method in the list
        for method in self.update_methods:
            if callable(method):
                method()

    def update_movement_state(self):
        self.change_x, self.change_y = 0, 0

    def adjust_layer(self) -> None:
        """Adjusting the layer based on sprites y cord"""
        sprite_list = self.draw_group
        sprite_list.remove(self)
        for i, sprite in enumerate(sprite_list):
            if self.center_y > sprite.center_y:
                index = i
                break
        else:
            index = len(sprite_list)  # If not found, put at the end
        sprite_list.insert(index, self)  # Insert at correct layer position

    def update_layer_adjust(self):
        if self.center_y != self.old_y:
            self.needs_layer_adjust = True

        if self.needs_layer_adjust:
            self.adjust_layer()
            self.layer_index = self.draw_group.index(self)
            self.old_y = self.center_y
            self.needs_layer_adjust = False

    def die(self) -> None:
        """
        Removes entity safely from lists and deletes it.
        Use it instead of builtin kill()
        """
        if self in self.draw_group:
            self.draw_group.remove(self)
        self.kill()  # Remove from the game



