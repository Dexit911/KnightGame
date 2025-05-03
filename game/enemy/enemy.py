import random
import arcade
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from core.cooldown_manager import CooldownManager
from core.constance import *
from core.moving_entity import *
from core.utils.path_manager import PathManager as Pm
from game.weapon.throwables import Throwables
from game.weapon.weapon import Weapon
from core.utils.vector_manager import VectorManager as Vm
from core.utils.hitbox_manager import HitboxManager as Hm
from arcade.hitbox import HitBox
from game.items.item_factory import ItemFactory
import time

from game.items.item import Coin


class Enemy(MovingEntity):
    def __init__(self, game, config):
        super().__init__(
            game=game,
            img=config["texture_path"]
        )

        # CONNECT TO GAME AND GROUPS
        self.game = game
        self.update_group = self.game.enemy_list
        self.update_group.append(self)
        self.obstacle_group = self.game.obstacle_list
        # COLLISION
        self.collision = arcade.PhysicsEngineSimple(self, self.obstacle_group)
        # AI
        self.ai = EnemyAi(self)
        # UPDATE METHODS
        # STATS
        self.stats = {
            "hp": config["hp"],
            "dmg": config["dmg"],
            "speed": config["speed"],
        }
        # STATES
        self.took_damage = False
        # SOUNDS
        self.sounds = {
            "hurt": [arcade.load_sound(Pm.sound("enemy", "slime", f"SlimeHurt{i}.wav")) for i in range(1, 4)]}
        # OTHER
        self.damage_sources = []
        # UPDATE
        self.update_methods = [
            self.ai.update,
            self.ai.cd.tick_all,
            self.check_for_damage
        ]

        self.hit_box = HitBox([(0, 0)])

    def spawn(self, position):
        """Spawn on map"""
        x, y = position
        self.position = (x * TILE_SIZE, y * TILE_SIZE)
        self.ai.matrix = self.game.matrix_map
        self.ai.start_m_pos = PathfindingManager.world_to_matrix(self.position)

        print(PathfindingManager.world_to_matrix((100, 100)))

    def drop_loot(self):
        pass

    def get_hit(self, weapon):
        """When enemy get hit"""
        if weapon.attacking and not self.took_damage:
            # Play sound
            arcade.play_sound(random.choice(self.sounds["hurt"]), volume=2)
            self.stats["hp"] -= weapon.dmg  # Reduce
            self.took_damage = True

            self.damage_sources.append(weapon)
            if self.stats["hp"] <= 0:
                self.die()
                self.drop_loot()

            self.get_impulse(weapon.knockback, [weapon.center_x, weapon.center_y])  # Get knockback

    def check_for_damage(self):
        """Check for if something hit you"""
        new_sources = []
        for damage_source in self.damage_sources:
            if isinstance(damage_source, Throwables):
                continue  # handle this separately if needed
            if isinstance(damage_source, Weapon):
                if damage_source.attacking:
                    new_sources.append(damage_source)
        # Allow damage again only if list is now empty
        if not new_sources:
            self.took_damage = False

        self.damage_sources = new_sources


class EnemyAi:
    def __init__(self, enemy):
        # CONNECT TO ENEMY --------------------------------------------------------------
        self.enemy = enemy
        self.game = self.enemy.game
        # MATRIX for path finding -------------------------------------------------------
        self.matrix = []
        # TRIGGERS ----------------------------------------------------------------------
        self.ray_length = 100  # If ray touches the player, start alert mode
        self.alert_radius = 200  # If the player escapes this radius, return to idle zone
        self.idle_walking_radius = 1  # A limited radius where the Enemy can do random walks
        self.attack_radius = 0  # If player in this radius, start attack mode
        # STATES ------------------------------------------------------------------------
        self.states = ["idle", "alert", "attack"]
        self.state = "alert"
        self.is_moving = False
        # CD:s --------------------------------------------------------------------------
        self.cd = CooldownManager()
        self.cd.add("ai_tick", 0.4)
        # PATH --------------------------------------------------------------------------
        self.path = []
        self.path_index = 0
        self.goal_tile = None
        # START MATRIX POS --------------------------------------------------------------
        self.start_m_pos = []

    def state_handler(self):
        """Update the acting based on state"""
        if self.cd.ready("ai_tick"):
            self.cd.reset("ai_tick")

            print("Should be every two seconds")

            if self.state == "idle":
                self.idle_walk()
            elif self.state == "alert":
                self.chase_player()
            elif self.state == "attack":
                self.attack()

    # MAIN METHODS -----------------------------------------------------------------------------------------------------
    def idle_walk(self):
        """Do so random walks in the idle radius"""

        goal = PathfindingManager.get_random_matrix_target_within_radius(
            self.matrix,
            self.start_m_pos,
            self.idle_walking_radius)

        if goal is not None:
            self.set_destination(self.enemy.position, goal)

    def chase_player(self):
        """Get players matrix position, move to him"""
        player_position = self.game.player.position
        self.set_destination(self.enemy.position, player_position)

    def attack(self):
        """Start attacking player"""
        pass

    # SUB-METHODS ------------------------------------------------------------------------------------------------------
    def can_enemy_see_player(self):
        """Shoots a ray cast towards player, if reaching: chase player"""
        if self.cd.ready("check_player"):  # If cd for check is ready
            self.cd.reset("check_player")
            enemy_position = self.enemy.position
            player_position = self.game.player.position
            direction = Vm.get_direction(player_position, enemy_position)  # Calculate the direction for the ray
            if Hm.raycast(enemy_position, direction, self.ray_length, self.game.obstacle_list):  # If hits the player
                self.state = "alert"  # Turn on the alert mode

    def set_destination(self, start_pos: tuple, goal_pos: tuple):
        """Set a new destination"""
        start_matrix_pos = PathfindingManager.world_to_matrix(start_pos)  # Set start matrix position
        print(start_matrix_pos)
        goal_matrix_pos = PathfindingManager.world_to_matrix(goal_pos)  # Set end matrix position
        print(goal_matrix_pos)
        matrix = self.game.matrix_map
        self.path = PathfindingManager.find_path(matrix, start_matrix_pos, goal_matrix_pos)  # Calculate the path
        print(self.path)

        if self.path:
            self.path_index = 0
        else:
            self.path = []

    def update_movement(self):
        """Update the movement towards the goal (If you have a goal)"""
        if self.path and self.path_index < len(self.path):
            world_position = PathfindingManager.matrix_to_world(self.path[self.path_index])

            # Get move towards the destination, with the right speed
            speed = self.enemy.stats["speed"]
            normalized_vector = Vm.normalised_vector(self.enemy.position, world_position)

            # Distance to the goal
            dist = Vm.get_distance(self.enemy.position, world_position)
            # Snap to the destination if very close, and start moving to the next one
            if dist < speed:
                self.enemy.position = world_position
                self.path_index += 1
            else:
                self.enemy.velocity = Vm.scale_vec2(normalized_vector, speed)
        else:
            self.enemy.velocity = (0, 0)


    def update(self):
        self.state_handler()
        self.update_movement()
        self.can_enemy_see_player()


class PathfindingManager:
    finder = AStarFinder()

    @staticmethod
    def find_path(matrix: list, start: tuple, goal: tuple) -> list:
        if not matrix or not matrix[0]:
            print("Matrix is empty or malformed.")
            return []
        grid = Grid(matrix=matrix)
        start_node = grid.node(*start)
        goal_node = grid.node(*goal)
        path, _ = PathfindingManager.finder.find_path(start_node, goal_node, grid)
        return path

    @staticmethod
    def world_to_matrix(position):
        col = int(position[1] // SUB_TILE_SIZE)
        row = int(position[0] // SUB_TILE_SIZE)
        return row, col  # Reversed to match matrix_to_world

    @staticmethod
    def matrix_to_world(matrix_position: tuple) -> tuple:
        x, y = matrix_position  # x=column, y=row
        world_x = x * SUB_TILE_SIZE + SUB_TILE_SIZE // 2
        world_y = y * SUB_TILE_SIZE + SUB_TILE_SIZE // 2
        return world_x, world_y

    @staticmethod
    def get_random_matrix_target_within_radius(matrix, matrix_pos, radius):
        max_x = len(matrix[0])
        max_y = len(matrix)

        cx, cy = matrix_pos
        candidates = []

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                tx = cx + dx
                ty = cy + dy

                # Stay within bounds
                if 0 <= tx < max_x and 0 <= ty < max_y:
                    # Check distance
                    if math.hypot(dx, dy) <= radius:
                        # Check if walkable (1 means walkable)
                        if matrix[ty][tx] == 1:
                            candidates.append((tx, ty))

        return random.choice(candidates) if candidates else None
