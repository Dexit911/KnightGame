import math
from core.constance import *


class VectorManager:

    @staticmethod
    def normalised_vector(x1: float, y1: float, x2: float, y2: float) -> list:
        """
        :param x1, y1: start cord
        :param x2, y2: to cord
        :return list: normalised vector
        """
        dx = x2 - x1
        dy = y2 - y1

        length = math.sqrt(dx ** 2 + dy ** 2)
        if length != 0:
            dx /= length
            dy /= length

        return [dx, dy]

    @staticmethod
    def from_center_to(x2, y2):
        return VectorManager.normalised_vector(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, x2, y2)

