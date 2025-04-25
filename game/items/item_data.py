from core.utils.path_manager import PathManager as Pm

WEAPON = "weapon"
ARMOR = "armor"
CURRENCY = "currency"
HEAL = "heal"
TRINKET = "trinket"

COIN = {
    "path": Pm.item_img("coin", "Coin1.png"),
    "name": "Coin",
    "description": "Very shiny, probably valuable.",
}

TRINKETS = {
    "haste_amulet": {
        "path": Pm.trinket_img("HasteAmulet.png"),
        "name": "Haste Amulet",
        "description": "WHY ARE YOU BLUE?",
        "stat": "speed_multi",
        "value": 0.02,
    },
    "health_amulet": {
        "path": Pm.trinket_img("HealthAmulet.png"),
        "name": "Health Amulet",
        "description": "Give me love.",
        "stat": "hp",
        "value": 10,
    },
    "protection_amulet": {
        "path": Pm.trinket_img("ProtectionAmulet.png"),
        "name": "Shield Amulet",
        "description": "Always remember about protection",
        "stat": "protection",
        "value": 2,
    },
    "dash_feather": {
        "path": Pm.trinket_img("SwiftnessFeather.png"),
        "name": "Feather of Swiftness",
        "description": "Light as a feather, well no shit.",
        "stat": "dash_cd_multi",
        "value": 0.02,
    },
    "kunai_charm": {
        "path": Pm.trinket_img("KunaiCharm.png"),
        "name": "Charm of Kunai",
        "description": "Reduces throwing cooldown",
        "stat": "throw_cd_multi",
        "value": 0.03,
    }

}
HEALS = {
    "big_heal_potion": {
        "path": Pm.heal_img("HealPotionBig.png"),
        "name": "Big health Potion",
        "description": "Tastes like.. a heal potion.",
        "hp": 30,
    },
}

