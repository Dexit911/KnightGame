from game.items.item import Item


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