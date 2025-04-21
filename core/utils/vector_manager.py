import math
from core.constance import *


class VectorManager:

    @staticmethod
    def add_vec2(a, b):
        return a[0] + b[0], a[1] + b[1]

    @staticmethod
    def subtract_vec2(a, b):
        return a[0] - b[0], a[1] - b[1]

    @staticmethod
    def scale_vec2(v, scalar):
        return v[0] * scalar, v[1] * scalar

    @staticmethod
    def normalised_vector(a: tuple, b: tuple) -> tuple:
        """
        :param a: From pos
        :param b: To pos
        """
        dv = VectorManager.subtract_vec2(b, a)
        length = math.sqrt(dv[0] ** 2 + dv[1] ** 2)
        if length != 0:
            return dv[0] / length, dv[1] / length
        else:
            return 0, 0

    @staticmethod
    def from_center_to(b: tuple) -> tuple:
        """
        :param b: to pos
        """
        return VectorManager.normalised_vector(SCREEN_CENTER_POS, b)

    @staticmethod
    def get_angle(a: tuple, b: tuple) -> float:
        """
        :param a: from pos
         :param b: to pos
        """
        dv = (a[0] - b[0], a[1] - b[1])
        return math.degrees(math.atan2(dv[1], dv[0]))

    @staticmethod
    def get_angle_from_center_to(b: tuple) -> float:
        """
        :param b: to pos
        """
        return VectorManager.get_angle(SCREEN_CENTER_POS, b)
