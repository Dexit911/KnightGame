class CustomHitBoxes:
    def __init__(self, x=0, y=0):
        """Obstacles that are connected to grid cords"""

        self.default = [
            (-10 + x, -22 + y),  # Down left corner
            (10 + x, -22 + y),  # Down right corner
            (10 + x, -17 + y),  # Upper left corner
            (-10 + x, -17 + y)  # Upper right corner
        ]

        self.big_stone = [
            (-10 + x, -20 + y),
            (10 + x, -20 + y),
            (30 + x, 0 + y),
            (-30 + x, 0 + y)
        ]

        """Static hit boxes that in middle of the screen"""
        self.sword = [
            (-20, -10),
            (20, -10),
            (20, 40),
            (-20, 40)
        ]

        self.player = [
            (-12, -32),
            (12, -32),
            (10, -15),
            (-10, -15)

        ]

    # going to use soon to optimize and make my life easy
    def setup_cords(self, x, y, hit_box: list):
        return [(point[0] * x, point[1] * y) for point in hit_box]
