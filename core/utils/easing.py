class Easing:
    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def ease_in(t):
        return t * t

    @staticmethod
    def ease_out(t):
        return t * (2 - t)

    @staticmethod
    def ease_in_out(t):
        return t * t * (3 - 2 * t)

    @staticmethod
    def bounce_out(t):
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375

    @staticmethod
    def swing_back_ease(t):
        if t < 0.5:
            return Easing.ease_out(t * 2)
        else:
            return 1 - Easing.ease_out((t - 0.5) * 2)

    @staticmethod
    def swing_linear_return(t: float) -> float:
        """
        Ease-out forward swing, then linear return.
        """
        if t < 0.5:
            # Ease out as it swings forward
            return Easing.ease_out(t * 2)
        else:
            # Linear return back to 0
            return 1 - ((t - 0.5) * 2)

