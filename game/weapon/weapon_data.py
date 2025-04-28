from core.utils.path_manager import PathManager as Pm

"""
FORMAT
texture_path:
pos_offset:

damage:
cooldown:
knockback:
attack_style:
attack

"""

WEAPONS = {
    "sword": {
        "classic_sword": {
            "texture_path": Pm.weapon_img("sword", "ClassicSword.png"),
            "offset_pos": (0, -20),
            "shake_effect": 3,
            "damage": 5,
            "cooldown": 30,
            "knockback": 5,
            "recoil": 5,
            "attack_style": "arc",
            "attack_radius": 50,
            "attack_angle": 60
        },
        "red_sword": {
            "texture_path": Pm.weapon_img("sword", "RedSword.png"),
            "offset_pos": (0, -20),
            "shake_effect": 5,
            "damage": 1,
            "cooldown": 20,
            "knockback": 30,
            "recoil": 30,
            "attack_style": "arc",
            "attack_radius": 50,
            "attack_angle": 100
        },
        "dragon_slayer": {
            "texture_path": Pm.weapon_img("sword", "DragonSlayer.png"),
            "offset_pos": (0, -20),
            "shake_effect": 30,
            "damage": 3,
            "cooldown": 30,
            "knockback": 20,
            "recoil": -10,
            "attack_style": "arc",
            "attack_radius": 100,
            "attack_angle": 100
        }
    },
    "axe": {
        "iron_long_axe": {
            "texture_path": Pm.weapon_img("axe", "IronLongAxe.png"),
            "offset_pos": (0, -20),
            "shake_effect": 7,
            "damage": 3,
            "cooldown": 40,
            "knockback": 10,
            "recoil": 2,
            "attack_style": "arc",
            "attack_radius": 50,
            "attack_angle": 100
        },
        "double_iron_axe": {
            "texture_path": Pm.weapon_img("axe", "DoubleBigIronAxe.png"),
            "offset_pos": (0, -20),
            "shake_effect": 50,
            "damage": 1,
            "cooldown": 30,
            "knockback": 20,
            "recoil": -10,
            "attack_style": "arc",
            "attack_radius": 100,
            "attack_angle": 100
        },
    },
    "blunt": {
        "wood_club": {
            "texture_path": Pm.weapon_img("blunt", "WoodClub.png"),
            "offset_pos": (0, -20),
            "shake_effect": 30,
            "damage": 2,
            "cooldown": 40,
            "knockback": 20,
            "recoil": -10,
            "attack_style": "arc",
            "attack_radius": 100,
            "attack_angle": 100
        }
    },
    "dagger": {},
    "throwable": {
        "small_knife": {
            "texture_path": Pm.weapon_img("throwable", "ThrowingKnife.png"),
            "shake_effect": 4,
            "damage": 4,
            "knockback": 5,
            "recoil": -2,
            "speed": 20
        }
    },
}

