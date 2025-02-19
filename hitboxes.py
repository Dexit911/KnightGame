class CustomHitBoxes:
    def __init__(self, x=0, y=0):
        self.default = [
            (-10 + x, -22 + y), # Down left corner
            (10 + x, -22 + y),  # Down right corner
            (10 + x, -17 + y),  # Upper left corner
            (-10 + x, -17 + y)  # Upper right corner
        ]

        self.sword = [
            (-40, -10),
            (0, -10),
            (0, 40),
            (-40, 40)
        ]

        self.player = [
            (-12, -32),
            (12, -32),
            (10, 0),
            (-10, 0)

        ]
