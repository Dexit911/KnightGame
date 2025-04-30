class Cooldown:
    def __init__(self, duration_seconds: float):
        self.max = duration_seconds
        self.base_max = duration_seconds
        self.timer = 0

    def reset(self):
        self.timer = self.max

    def reset_with_change(self, multi_percent):
        self.max = self.base_max * (1 - multi_percent)
        self.reset()

    def tick(self, dt):
        if self.timer > 0:
            self.timer -= dt
            self.timer = round(self.timer, 4)

    def ready(self) -> bool:
        return self.timer <= 0

    def trigger_once(self):
        if self.ready():
            self.reset()
            return True
        return False

    @staticmethod
    def with_reduction(base_duration, reduction_percent):
        reduced = int(base_duration * (1 - reduction_percent))
        return Cooldown(reduced)


class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def add(self, name: str, duration_second: float):
        self.cooldowns[name] = Cooldown(duration_second)

    def reset(self, name: str):
        if name in self.cooldowns:
            self.cooldowns[name].reset()

    def start(self, name: str):
        self.reset(name)

    def ready(self, name: str) -> bool:
        return self.cooldowns.get(name, Cooldown(0)).ready()

    def trigger_once(self, name: str) -> bool:
        return self.cooldowns.get(name, Cooldown(0)).trigger_once()

    def tick_all(self, dt: float):
        for cooldown in self.cooldowns.values():
            cooldown.tick(dt)

    def reset_with_change(self, name: str, multi_percent):
        return self.cooldowns.get(name).reset_with_change(multi_percent)

    def __getitem__(self, name: str) -> Cooldown:
        return self.cooldowns[name]  # direct access if needed
