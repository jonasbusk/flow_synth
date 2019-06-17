from .base import Module


class Counter(Module):
    """Trigger module"""

    def __init__(self, bpm, beats=4, thresh=0.1):
        self.delta = 60.0 / bpm
        self.beats = beats
        self.thresh = thresh
        self.counter = -1
        self.last_trigger = False

    def out(self, t):
        trigger = t % self.delta < self.thresh

        if trigger:
            if trigger != self.last_trigger:
                self.counter += 1
            self.last_trigger = trigger
            return self.counter % self.beats + 1
        else:
            self.last_trigger = trigger
            return 0
