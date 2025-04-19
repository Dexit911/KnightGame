class Cooldown:
    def __init__(self, duration_frames):
        self.max = duration_frames
        self.timer = 0

    def reset(self):
        self.timer = self.max

    def tick(self):
        if self.timer > 0:
            self.timer -= 1

    def ready(self):
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

    def add(self, name: str, duration_frames: int):
        self.cooldowns[name] = Cooldown(duration_frames)

    def reset(self, name: str):
        if name in self.cooldowns:
            self.cooldowns[name].reset()

    def ready(self, name: str) -> bool:
        return self.cooldowns.get(name, Cooldown(0)).ready()

    def trigger_once(self, name: str) -> bool:
        return self.cooldowns.get(name, Cooldown(0)).trigger_once()

    def tick_all(self):
        for cooldown in self.cooldowns.values():
            cooldown.tick()

    def with_reduction(self, name: str, reduction_percent: float):
        if name in self.cooldowns:
            base = self.cooldowns[name].max
            self.cooldowns[name] = Cooldown.with_reduction(base, reduction_percent)

    def __getitem__(self, name: str) -> Cooldown:
        return self.cooldowns[name]  # direct access if needed
