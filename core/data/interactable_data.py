from core.utils.path_manager import PathManager as Pm

CHEST = "chest"
NPC = "npc"
DOOR = "door"

NPCS = {
    "blacksmith": {
        "texture_path": Pm.blacksmith_img("idleAni", "IdleAni1.png"),
        "dialogue": {
            "hello": "How you doing buddy?",
            "goodbye": "See you soon!",
            "buy": "Choose wisely!",
        },

    }
}
