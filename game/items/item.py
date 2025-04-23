import random
import arcade
from core.constance import SCALE
from game.items import item_types as it
from core.utils.easing import Easing
from core.simple_animation import SimpleAnimation as Sm
from core.hitboxes import CustomHitBoxes as Ch
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm

"""Name, is key to texture path"""


class Item(arcade.Sprite):
    def __init__(self, game, name, description, amount, path):
        super().__init__(path_or_texture=path)
        self.game = game

        """Group"""
        self.group = self.game.item_list
        self.group.append(self)

        self.currency_sound = arcade.load_sound(Pm.common_sound("PickupCoin.wav"))
        self.scale = SCALE

        """Values"""
        self.name = name
        self.description = description
        self.item_type = ""
        self.amount = amount

        self.hit_box = Ch(self.center_x, self.center_y).item

        """Animation for dropping, Going to get rework"""
        self.is_dropping = False
        self.drop_progress = 0
        self.max_drop_time = 40
        self.drop_start_y = 0
        self.drop_end_y = 25

    def drop(self, position: tuple):
        offset_position = (random.randint(-5, 5), random.randint(-5, 5))
        self.position = Vm.add_vec2(position, offset_position)
        self.drop_start_y += self.center_y
        self.is_dropping = True

    def update_drop_animation(self):
        if self.is_dropping:
            self.drop_progress += 1
            progress = min(self.drop_progress / self.max_drop_time, 1)
            eased = Easing.bounce_out(progress)
            self.center_y = self.drop_start_y - (eased * self.drop_end_y)

            if progress >= 1:
                self.is_dropping = False

    def on_picked_up(self, owner):
        match self.item_type:
            case it.WEAPON:
                owner.pick_weapon(self)
            case it.ARMOR:
                pass
            case it.CURRENCY:
                arcade.play_sound(self.currency_sound)
                owner.set_coin(self.amount)
                pass

    def on_update(self):
        super().update()
        self.update_drop_animation()


class Coin(Item):
    def __init__(self, game, amount):
        super().__init__(game=game,
                         name="Golden coin",
                         description="It's Shiny",
                         amount=amount,
                         path=Pm.item_img("coin", "Coin1.png"))
        self.item_type = it.CURRENCY
