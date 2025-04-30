from game.items.trinket import Trinket
from game.weapon.weapon import Melee
from core.data import weapon_data, item_data as data


class ItemFactory:
    """Instantiating weapon, items, soon other stuff from configs """
    @staticmethod
    def create_trinket(game, trinket_id) -> Trinket:
        return Trinket(game, data.TRINKETS[trinket_id])

    @staticmethod
    def create_weapon(game, owner, weapon_type, weapon_id) -> Melee:
        return Melee(game, owner, weapon_data.WEAPONS[weapon_type][weapon_id])


