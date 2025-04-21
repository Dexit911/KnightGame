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
    "damage": 1,
    "cooldown": 100,
    "knockback": 5,
    "recoil": 1,
    "attack_style": "arc",
    "attack_radius": 50,
    "attack_angle": 60

}

IRON_LONG_AXE = {
    "texture_path": Pm.weapon_img("axe", "IronLongAxe.png"),
    "offset_pos": (0, -20),
    "shake_effect": 3,
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
