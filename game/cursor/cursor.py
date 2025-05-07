import arcade
from core.utils.path_manager import PathManager as Pm
from core.utils.vector_manager import VectorManager as Vm
from core.cooldown_manager import CooldownManager
from core.constance import *


class Cursor(arcade.Sprite):
    def __init__(self, game):
        super().__init__(
            path_or_texture=Pm.cursor_img("Target.png"),
            scale=SCALE
        )
        """Keys"""
        self.keys = set()

        """Connect to game, player"""
        self.game = game
        self.player = self.game.player
        """Textures"""
        self.textures = [
            arcade.load_texture(Pm.cursor_img("Target.png")),
            # arcade.load_texture(Pm.cursor_img("HandPointer.png")),
            arcade.load_texture(Pm.cursor_img("Interact.png"))
        ]
        """Sounds"""

        """State"""
        self.state = "targeting"

        self.interact_radius = 50
        self.nearby_interactables = []


        """Cooldowns"""
        self.cd = CooldownManager()
        self.cd.add("tick", 0.1)

    def on_update(self, dt):
        """Events that happens every frame"""
        self.follow_mouse()
        self.update_state()
        self.update_input()

        self.cd.tick_all(dt)

    def follow_mouse(self):
        """Always follow mouse position"""
        self.position = self.game.mouse_world

    def change_texture(self):
        """Change texture based on state"""
        match self.state:
            case "targeting":
                self.texture = self.textures[0]
            case "pointing":
                self.texture = self.textures[2]
            case "interacting":
                self.texture = self.textures[1]

    def update_input(self):
        if arcade.key.F in self.keys:
            if self.nearby_interactables:
                obj = self.nearby_interactables[0]
                obj.interact()

    def update_state(self):
        if self.cd.ready("tick"):
            self.cd.reset("tick")

            print("tick")

            """Update state based on what the cursor is touching"""
            interactables = self.game.interactable_list
            self.nearby_interactables = []

            for obj in interactables:
                if abs(self.player.center_x - obj.center_x) > self.interact_radius:
                    continue
                if abs(self.player.center_y - obj.center_y) > self.interact_radius:
                    continue

                distance = arcade.get_distance_between_sprites(self, obj)
                if distance <= self.interact_radius:
                    self.nearby_interactables.append(obj)

            # After the loop
            if self.nearby_interactables:
                self.state = "interacting"
            else:
                self.state = "targeting"

            self.change_texture()
