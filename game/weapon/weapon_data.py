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

CLASSIC_SWORD = {
    "texture_path": Pm.weapon_img("sword", "ClassicSword.png"),
    "offset_pos": (0, -20),
    "shake_effect": 3,
    "damage": 10,
    "cooldown": 100,
    "knockback": 5,
    "recoil": 5,
    "attack_style": "arc",
    "attack_radius": 50,
    "attack_angle": 60

}

IRON_LONG_AXE = {
    "texture_path": Pm.weapon_img("axe", "IronLongAxe.png"),
    "offset_pos": (0, -20),
    "shake_effect": 7,
    "damage": 3,
    "cooldown": 100,
    "knockback": 10,
    "recoil": 2,
    "attack_style": "arc",
    "attack_radius": 50,
    "attack_angle": 100

}

RED_SWORD = {
    "texture_path": Pm.weapon_img("sword", "RedSword.png"),
    "offset_pos": (0, -20),
    "shake_effect": 5,
    "damage": 1,
    "cooldown": 30,
    "knockback": 30,
    "recoil": 30,
    "attack_style": "arc",
    "attack_radius": 50,
    "attack_angle": 100
}

IRON_HAMMER = {
    "texture_path": Pm.weapon_img("hammer", "IronHammer.png"),
    "offset_pos": (0, -20),
    "shake_effect": 10,
    "damage": 5,
    "cooldown": 50,
    "knockback": 15,
    "recoil": -5,
    "attack_style": "arc",
    "attack_radius": 80,
    "attack_angle": 100
}

DOUBLE_IRON_AXE = {
    "texture_path": Pm.weapon_img("axe", "DoubleBigIronAxe.png"),
    "offset_pos": (0, -20),
    "shake_effect": 50,
    "damage": 1,
    "cooldown": 70,
    "knockback": 20,
    "recoil": -10,
    "attack_style": "arc",
    "attack_radius": 100,
    "attack_angle": 100
}

WOOD_CLUB = {
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

DRAGON_SLAYER = {
    "texture_path": Pm.weapon_img("sword", "DragonSlayer.png"),
    "offset_pos": (0, -20),
    "shake_effect": 30,
    "damage": 3,
    "cooldown": 100,
    "knockback": 20,
    "recoil": -10,
    "attack_style": "arc",
    "attack_radius": 100,
    "attack_angle": 100
}

