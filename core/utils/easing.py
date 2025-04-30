class Easing:
    """CSS ctrl-c, ctrl-v. Methods used for animation"""

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

    @staticmethod
    def ease_swing_linear_return(t: float) -> float:
        """Ease out, hold a bit, then return linearly to 0."""
        if t < 0.4:
            # Ease out for the first 40% of time
            return Easing.ease_out(t / 0.4)
        elif t < 0.6:
            # Hold at the peak (like a plateau)
            return 1.0
        else:
            # Linearly return to 0
            return max(0.0, 1.0 - ((t - 0.6) / 0.4))

    @staticmethod
    def swing_up_fast_down_soft_return(t):
        """Small rise, fast drop, then slow recovery to end"""
        if t < 0.15:
            return -0.1 * Easing.ease_out(t / 0.15)  # tiny dip
        elif t < 0.4:
            return -0.1 + 1.2 * Easing.ease_in_out((t - 0.15) / 0.25)  # steep climb
        elif t < 0.85:
            return 1.1 - 0.6 * Easing.ease_out((t - 0.4) / 0.45)  # quick fall
        else:
            return 0.5 + 0.5 * Easing.ease_in((t - 0.85) / 0.15)  # slow glide back to end

    @staticmethod
    def swing_and_return(t):
        # Goes to 1 at t=0.5, then returns to 0 at t=1.0
        if t < 0.5:
            return Easing.ease_out(t * 2)
        else:
            return Easing.ease_out(2 - t * 2)
