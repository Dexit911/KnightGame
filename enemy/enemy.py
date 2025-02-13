import arcade
from animation import Animate


class Enemy(Animate):
    def __init__(self, game, x, y):
        super().__init__(img="source/enemy/slime/Slime.png")
        self.game = game
        self.game.enemy_list.append(self)

        self.center_x = x
        self.center_y = y

        self.states = ["idle", "alert", "attack"]
        self.state = "idle"

    def on_update(self):
        super().update()

    def idle_movement(self):
        

    def check_distance(self, trigger_d):
        distance = self.game.player.get_disctande_to_sprite(self)
        if distance <= 10:
            self.state = "attack"
        elif distance <= trigger_d:
            self.state = "alert"
        else:
            self.state = "idle"

    def state_handler(self):
        if self.state == "idle":

