from core.utils.path_manager import PathManager as Pm

ENEMIES = {
    "slime": {
        "texture_path": Pm.img("enemy", "slime", "Slime.png"),
        "hp": 20,
        "dmg": 2,
        "speed": 0.1
    }
}