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

    "damage": 5,
    "cooldown": 100,
    "knockback": 5,
    "recoil": 1,

    "attack_style": "arc",
    "attack_radius": 30,
    "attack_angle": 45

}
