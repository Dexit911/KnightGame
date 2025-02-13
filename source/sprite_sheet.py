import arcade


class Image:
    def __init__(self, path, scale: int = 2):
        self.path = path
        self.scale = scale
        # Load the entire sprite sheet texture using only the file path.
        self.spritesheet_texture = arcade.load_texture(path)
        self.sheet_width = self.spritesheet_texture.width
        self.sheet_height = self.spritesheet_texture.height

    def get_image(self, x, y, width, height):
        """
        Extract a sub-texture from the sprite sheet.
        The (x, y) coordinates are assumed to be from the top-left.
        """
        # Convert y coordinate from top-left (sprite sheet) to bottom-left (pyglet)
        new_y = self.sheet_height - y - height

        # Get the underlying pyglet image
        full_image = self.spritesheet_texture.image

        # Use pyglet's get_region to crop the desired area.
        sub_image = full_image.get_region(x, new_y, width, height)

        # Create a new Arcade texture from the cropped pyglet image.
        texture_name = f"{self.path}_{x}_{y}_{width}_{height}"
        sub_texture = arcade.Texture(name=texture_name, image=sub_image)
        return sub_texture

    def load_texture_pair(self, path):
        normal_texture = arcade.load_texture(path, scale=self.scale)
        flipped_texture = arcade.load_texture(path, scale=self.scale, flipped=True)
        return normal_texture, flipped_texture
