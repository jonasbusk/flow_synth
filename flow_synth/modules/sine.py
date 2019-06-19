import numpy as np

from .base import Module


class Sine(Module):
    """Sinewave module."""

    def __init__(self, frequency, fm=lambda t: 0, hold=False, normalize=False):
        self.frequency = frequency
        self.fm = fm
        self.hold = hold
        self.normalize = normalize
        self.twopi = 2 * np.pi
        self.f = None

    def out(self, t):
        if self.hold:
            self.f = self.frequency(t) or self.f
        else:
            self.f = self.frequency(t)

        if self.f:
            out = np.sin(self.twopi * self.f * t + self.fm(t))
        else:
            out = 0.0
        if self.normalize:
            out = out / 2 + 0.5
        return out
