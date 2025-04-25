from game.items.item import Item
from game.items import item_data as data


class Trinket(Item):
    def __init__(self, game, config):
        super().__init__(
            game=game,
            config=config
        )
        self.item_type = data.TRINKET
        self.stat = config["stat"]
        self.value = config["value"]

    def use(self):
        """Applies effects to player"""
        self.player.stats[self.stat] += self.value
        print(self.player)
        self.kill()
