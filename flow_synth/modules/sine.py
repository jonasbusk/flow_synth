import numpy as np

from .base import Module


class Sine(Module):
    """Sinewave module"""

    def __init__(self, frequency, fm=lambda t: 0, normalize=False):
        self.frequency = frequency
        self.fm = fm
        self.normalize = normalize
        self.twopi = 2 * np.pi

    def out(self, t):
        f = self.frequency(t)
        if f:
            out = np.sin(self.twopi * f * t + self.fm(t))
        else:
            out = 0.0
        if self.normalize:
            out = out / 2 + 0.5
        return out
