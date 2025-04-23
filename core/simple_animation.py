class SimpleAnimation:
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration
        self.progress = 0
        self.active = False

    def start_anim(self):
        self.progress = 0
        self.active = True

    def update(self):
        if not self.active:
            return self.current_value()

        self.progress += 1
        if self.progress >= self.duration:
            self.progress = self.duration
            self.active = False

    def current_value(self, easing_func=lambda x: x):
        progress = min(self.progress / self.duration, 1)
        eased = easing_func(progress)
        return self.start + (self.end - self.start) * eased

    def is_done(self):
        return not self.active

    def progress_ratio(self):
        return self.progress / self.duration if self.duration > 0 else 1

