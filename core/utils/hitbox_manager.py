import math
import arcade


class HitboxManager:
    """
    Handles hard types of hit-boxes.
    Adds some of mine collision logic.
    """

    @staticmethod
    def circle(center: tuple, radius: float, resolution: int = 16) -> list:
        cx, cy = center
        return [
            (cx + math.cos(math.radians(i)) * radius,
             cy + math.sin(math.radians(i)) * radius)
            for i in range(0, 360, 360 // resolution)
        ]

    @staticmethod
    def sector(center: tuple, radius: float, angle_deg: float, span_deg: float, resolution: int = 8) -> list:
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

    @staticmethod
    def is_point_in_polygon(x, y, polygon_points):
        inside = False
        n = len(polygon_points)
        px, py = polygon_points[0]
        for i in range(1, n + 1):
            sx, sy = polygon_points[i % n]
            if ((sy > y) != (py > y)) and \
                    (x < (px - sx) * (y - sy) / (py - sy + 1e-10) + sx):
                inside = not inside
            px, py = sx, sy
        return inside

    @staticmethod
    def check_overlap(polygon_sprite, target_sprite) -> bool:
        """Checks if any point from the target's hitbox overlaps with the polygon-shaped hitbox of the weapon sprite."""
        poly = polygon_sprite.hit_box.get_adjusted_points()
        for point in target_sprite.hit_box.get_adjusted_points():
            if HitboxManager.is_point_in_polygon(point[0], point[1], poly):
                return True
        return False

    @staticmethod
    def raycast(origin, direction, max_distance, obstacles, step=4):
        """
        Casts a ray from origin in a direction until it hits an obstacle or reaches max_distance.

        origin: (x, y)
        direction: (dx, dy) — should be normalized
        max_distance: float
        obstacles: arcade.SpriteList
        step: how much to advance per check (smaller = more precise)
        """
        x, y = origin
        dx, dy = direction
        distance = 0

        while distance < max_distance:
            point = (x + dx * distance, y + dy * distance)

            if arcade.get_sprites_at_point(point, obstacles):
                return False  # blocked
            distance += step

        return True  # line of sight clear