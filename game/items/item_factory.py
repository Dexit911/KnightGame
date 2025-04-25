from game.items import item_data as data
from game.items.trinket import Trinket
from game.weapon.weapon import Weapon


class ItemFactory:
    @staticmethod
    def create_trinket(game, trinket_id):
        return Trinket(game, data.TRINKETS[trinket_id])

    @staticmethod
    def create_weapon(game, weapon_type, weapon_id):
        pass
