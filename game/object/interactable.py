from core.utils.path_manager import PathManager as Pm
from game.object import interactable_data as inter_data
from game.items.item_factory import ItemFactory
from core.constance import *
from core.animation import Animate


class Interactable(Animate):
    def __init__(self, game, path):
        super().__init__(
            img=path,
            scale=SCALE
        )
        """Connect to game, draw and update group"""
        self.game = game
        self.draw_group = self.game.layer_adjusted_sprites
        self.draw_group.append(self)
        self.update_group = self.game.interactable_list
        self.update_group.append(self)

        """Type"""
        self.type = None

    def spawn(self, position: tuple):
        self.position = position

    def interact(self):
        match self.type:
            case inter_data.CHEST:
                self.open()
            case inter_data.NPC:
                self.talk()

    def on_update(self):
        if self.textures:
            self.update_animation()


class Chest(Interactable):
    def __init__(self, game):
        super().__init__(
            game=game,
            path=Pm.object_img("chest", "CommonChest.png")
        )
        self.type = inter_data.CHEST

    def open(self):
        game = self.game
        items = [
            ItemFactory.create_trinket(game, "haste_amulet"),
            ItemFactory.create_trinket(game, "dash_feather"),
            ItemFactory.create_trinket(game, "kunai_charm")
        ]
        for item in items: item.drop(self.position)
        # self.kill()
