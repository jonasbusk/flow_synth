from .base import Module


class Trigger(Module):
    """Trigger module"""

    def __init__(self, bpm, thresh=0.1):
        self.delta = 60.0 / bpm
        self.thresh = thresh

    def out(self, t):
        return t % self.delta < self.thresh
