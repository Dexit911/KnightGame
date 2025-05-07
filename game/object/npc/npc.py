import arcade

from core.data import interactable_data as inter_data
from game.object.interactable import Interactable
from core.utils.path_manager import PathManager as Pm


class Npc(Interactable):
    def __init__(self, game, config):
        super().__init__(
            game=game,
            path=config.get("texture_path"),
        )
        """Connect to game"""
        self.game = game
        self.type = inter_data.NPC

    def talk(self):
        print("suybau")


class BlackSmith(Npc):
    def __init__(self, game):
        super().__init__(game=game, config=inter_data.NPCS["blacksmith"])
        self.setup_textures()

    def setup_textures(self):
        idle_textures = [
            arcade.load_texture(Pm.blacksmith_img("idleAni", f"IdleAni{i}.png")) for i in range(1, 10)]
        self.textures = idle_textures
