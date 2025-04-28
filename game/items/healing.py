from game.items.item import Item
import pyglet.gl
from arcade import load_texture
from core.utils.path_manager import PathManager as Pm

texture = load_texture(Pm.trinket_img("HealthAmulet.png"))
gl_texture = texture.t








class Healing(Item):
    def __init__(self, game, config_dict):
        super().__init__(
            game=game,
            config=config_dict,
        )
        self.health = config_dict["hp"]

    def use(self):
        self.player.heal(self.health)
        self.kill()