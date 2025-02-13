import arcade


class Animate(arcade.Sprite):
    def __init__(self, img, scale: float = 2.0, animate_time: float = 10.0):
        """
        :param img:
        :param scale:
        :param animate_time:
        """

        texture = arcade.load_texture(img)
        super().__init__(texture, scale)
        self.i = 0
        self.time = 0
        self.animate_time = animate_time

    def update_animation(self, delta_time):
        self.time += delta_time
        if self.time >= self.animate_time:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)
