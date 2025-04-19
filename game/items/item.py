import random
import arcade
from core.constance import SCALE
from game.items import item_types as it
from core.hitboxes import CustomHitBoxes as Ch
from core.utils.path_manager import PathManager as Pm

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


        self.is_dropping = False
        self.drop_progress = 0
        self.max_drop_time = 1

    def drop(self, x, y):
        self.is_dropping = True
        offset_x, offset_y = random.randint(-5, 5), random.randint(-5, 5)
        self.center_x, self.center_y = x + offset_x, y + offset_y

    def update_drop_animation(self):
        pass



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


class Coin(Item):
    def __init__(self, game, amount):
        super().__init__(game=game,
                         name="Golden coin",
                         description="It's Shiny",
                         amount=amount,
                         path=Pm.item_img("coin", "Coin1.png"))
        self.item_type = it.CURRENCY
