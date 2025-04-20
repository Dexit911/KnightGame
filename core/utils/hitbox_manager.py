import math


class HitboxManager:
    @staticmethod
    def circle(center: tuple, radius: float, resolution: int = 16) -> list:
        cx, cy = center
        return [
            (cx + math.cos(math.radians(i)) * radius,
             cy + math.sin(math.radians(i)) * radius)
            for i in range(0, 360, 360 // resolution)
        ]

    @staticmethod
    def sector(center: tuple, radius: float, angle_deg: float, span_deg: float, resolution: int = 16) -> list:
        cx, cy = center
        start_angle = angle_deg - span_deg / 2
        step = span_deg / resolution

        points = [center]
        for i in range(resolution + 1):
            angle = math.radians(start_angle + i * step)
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            points.append((x, y))

        return points
