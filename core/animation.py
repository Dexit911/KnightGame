import arcade


class Animate(arcade.Sprite):
    def __init__(self, img: str, scale: float = 1.0, animate_time: float = 10.0):
        super().__init__(img, scale=scale)
        self.textures: list[arcade.Texture] = []
        self.i = 0
        self.animate_time = animate_time
        self.counter = 0

    def update_animation(self, delta_time: float = 1/60):
        if not self.textures:
            return  # No textures to animate

        self.counter += 1
        if self.counter >= self.animate_time:
            self.counter = 0
            self.i = (self.i + 1) % len(self.textures)
            self.set_texture(self.i)

    def set_texture_list(self, textures: list[arcade.Texture]):
        self.textures = textures
        if textures:
            self.set_texture(0)
