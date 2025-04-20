import os


class PathManager:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    """Base-path methods"""

    @staticmethod
    def img(*path):
        return os.path.join(PathManager.ASSETS_DIR, "source", *path)

    @staticmethod
    def sound(*path):
        return os.path.join(PathManager.ASSETS_DIR, "sound", *path)

    @staticmethod
    def player_sound(*path):
        return PathManager.sound("player", *path)

    """Sub-path methods, ad more if needed /IMG"""

    @staticmethod
    def weapon_img(*name):
        return PathManager.img("weapon", *name)

    @staticmethod
    def item_img(*name):
        return PathManager.img("item", *name)

    @staticmethod
    def player_img(*name):
        return PathManager.img("player", *name)

    @staticmethod
    def tile_img(*name):
        return PathManager.img("terrain", "tile", *name)

    @staticmethod
    def object_img(*name):
        return PathManager.img("terrain", "object", *name)

    @staticmethod
    def structure_img(*name):
        return PathManager.img("terrain", "object", "structure", *name)

    """Sub-path methods, ad more if needed /SOUND"""

    @staticmethod
    def common_sound(*name):
        return PathManager.sound("common", *name)
