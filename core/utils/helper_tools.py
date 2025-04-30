class HelperTools:
    """Some random methods that is use here and there"""
    @staticmethod
    def adjust_layer(self, offset=0):
        """Adjusting the layer based on sprites y cord"""
        sprite_list = self.draw_group
        sprite_list.remove(self)
        for i, sprite in enumerate(sprite_list):
            if self.center_y > sprite.center_y:
                index = i
                break
        else:
            index = len(sprite_list)
        sprite_list.insert(index, self)
