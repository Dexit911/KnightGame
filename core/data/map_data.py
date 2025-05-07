from core.utils.path_manager import PathManager as Pm
from core.hitboxes import CustomHitBoxes as Ch

# DESIGN NEW MAPS AND LEVELS -------------------------------------------------------------------------------------------
TILE_MAPS = {
    "start_level": {
        "base": [
            "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
            "w........................................................PP...s...s.......C.............................w",
            "w.........S....s....CCCCCCCC..................S..........PPP.P.PP..P..Ps....s.r..............S..........w",
            "w...............s.S.s...s.....S..........................PPP..P.PPP.P....r..s..s....C...................w",
            "w...........s.s.....s.s..........E......S...............PPP.S...S.s...s..s.srs....s..S..................w",
            "w...........S.....s.......S.......E..E.E.................PP.....C....S...s...C.s..............S.........w",
            "w.................s............E....E............S.......PP........C....................................w",
            "w..............^B...^B.B.^..B.^....^BB..^.S.B^.B..^.B..^.PPB^.B..^B.S.^.B.B^..B.^..B.^S..B^.S..^BB..^B..w",
            "w.........sPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP..w",
            "w...s..PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP..w",
            "w.....PPPPPP...^.B..^.B.B^.BS.^.Bs.^PP.B^s.B.^..Bs^B.B.^.BB.^.B.S^.sB.^.SBs^.BSB^sBB.^B.B.^.B..^.B..^..Bw",
            "w..s.PPP.s..s..........s.......s....PP...s...s.......s...................s...................s....s.....w",
            "w..s.PP..s.....s....................PP..................s.......BBB.....................................w",
            "w..PPP..s...........................PP.....wwwwwwwwwwwwww.......BBB..E.....E............................w",
            "w...PP..............................PP.....w....E.E.....w.........E...E..E..............................w",
            "w..PP...............................PPP....w...E.E.E....w..............E...E............................w",
            "w..PP................s..............PPPPPPP.PP.P..P.P...w...............................................w",
            "w..PPP....s.....s......................PP..w..C......C..w...............................................w",
            "w..PP...s...s.........s....................w......C.....w...............................................w",
            "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
        ],
        "object": [".........................",
                   "...s.....................",
                   ".S...s.wwwwwww...........",
                   ".PPPPP.P.PP..P.E.........",
                   ".P...s....E..E...........",
                   ".P......................."],

        "spawn": "",
    }
}
# DEFINES THE WALKABLE SUB-GRIDS FOR PATH FINDING ----------------------------------------------------------------------
TILE_WALK_PROPERTIES = {
    "G": [[1, 1],
          [1, 1]],
    "W": [[0, 0],  # Wall
          [0, 0]],
    "A": [[1, 1],  # Half
          [0, 0]],
    "U": [[0, 0],  # Half under
          [1, 1]],
}
# PARSING METHOD -------------------------------------------------------------------------------------------------------
TILE_TYPES = {
    # Ground
    ".": ["G", "ground", "grass"],
    "P": ["G", "ground", "path"],
    "s": ["G", "ground", "small_stone"],
    # Obstacles
    "w": ["W", "obstacle", "stone_wall"],
    "^": ["A", "obstacle", "pole"],
    "S": ["A", "obstacle", "big_stone"],
    "r": ["A", "obstacle", "rune_stone"],
    "B": ["G", "obstacle", "bush"],
    # Enemy
    "E": ["G", "enemy", "slime"],

    # Interactable
    "C": ["G", "interactable", "chest"]
}
# ADD NEW OBJECTS HERE. note: do not give hitbox to obstacle that covers the whole tile --------------------------------
"""
GUIDE
Remember to add a symbol to map parses
------------------------------------------------------------------
GROUND: 
texture_path - if list gets random texture_path
------------------------------------------------------------------
OBSTACLE:
texture_path - same as ground
hitbox - get the name from core.hitboxes CustomHitBoxes.point_list
"""
TILE_DATA = {

    "ground": {
        "grass": {"texture_path": [Pm.tile_img("grass", f"GrassTile{i}.png") for i in range(1, 5)]},
        "path": {"texture_path": Pm.tile_img("path", f"PathTile{i}.png") for i in range(1, 5)},
        "small_stone": {"texture_path": Pm.object_img("stone", "SmallStone1.png")}
    },
    "obstacle": {
        "stone_wall": {
            "texture_path": Pm.structure_img("WallTile.png"),
        },
        "big_stone": {
            "texture_path": Pm.object_img("stone", "BigStone1.png"),
            "hitbox": "big_stone"
        },
        "rune_stone": {
            "texture_path": Pm.structure_img("RuneStone1.png"),
            "hitbox": "rune_stone"
        },
        "bush": {
            "texture_path": Pm.object_img("bush", "Bush1.png"),
            "hitbox": "rune_stone",
        },
        "pole": {
            "texture_path": Pm.structure_img("SmallPole.png"),
            "hitbox": "small_pole",
        }

    },
    "interactable": {
        "chest": Pm.object_img("chest", "CommonChest.png")
    },

    # DEBUG
    "enemy": {
        "slime": {
            "texture_path": Pm.img("enemy", "slime", "Slime.png"),
            "hp": 50,
            "dmg": 2,
            "speed": 2
        }
    },
}
