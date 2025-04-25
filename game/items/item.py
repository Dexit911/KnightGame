import random
import arcade
from core.constance import SCALE
from core.utils.easing import Easing
from core.hitboxes import CustomHitBoxes as Ch
from core.utils.vector_manager import VectorManager as Vm
from core.utils.path_manager import PathManager as Pm
from game.items import item_data as data

"""Name, is key to texture path"""


class Item(arcade.Sprite):
    def __init__(self, game, config, amount=1):
        super().__init__(path_or_texture=config.get("path"), scale=SCALE)
        """Connect Game and player"""
        self.game = game
        self.player = self.game.player

        """Group"""
        self.group = self.game.item_list
        self.group.append(self)

        """Sounds"""
        self.currency_sound = arcade.load_sound(Pm.common_sound("PickupCoin.wav"))

        """Values"""
        self.name = config.get("name")
        self.description = config.get("description")
        self.item_type = None
        self.amount = amount

        """Hitbox"""
        self.hit_box = Ch(self.center_x, self.center_y).item

        """Animation for dropping, Going to get rework"""
        self.is_dropping = False
        self.drop_progress = 0
        self.max_drop_time = 40
        self.drop_start_y = 0
        self.drop_end_y = 25

    def drop(self, position: tuple):
        offset_position = (random.randint(-20, 20), random.randint(-5, 5))
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

    def on_picked_up(self):
        match self.item_type:
            case data.WEAPON:
                # Not working
                self.player.pick_weapon(self)
            case data.ARMOR:
                # Not working
                self.player.add_to_inv()
            case data.CURRENCY:
                arcade.play_sound(self.currency_sound)
                self.player.set_coin(self.amount)
            case data.HEAL:
                self.player.add_to_inv()
            case data.TRINKET:
                self.use()

    def on_update(self):
        super().update()
        self.update_drop_animation()

    def use(self):
        pass


class Healing(Item):
    def __init__(self, game, config_dict):
        super().__init__(
            game=game,
            config=config_dict,
        )

    def use(self):
        self.player.heal()
        self.kill()


class Coin(Item):
    def __init__(self, game, amount):
        if amount == 1:
            path_index = 1
        elif 1 < amount <= 10:
            path_index = 2
        else:
            path_index = 3

        super().__init__(
            game=game,
            config=data.COIN,
            amount=amount
        )
        self.item_type = data.CURRENCY


