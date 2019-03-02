import numpy as np

from .base import Module


class SMAFilter(Module):
    """Simple moving average filter module"""

    def __init__(self, input, w=2):
        self.input = input
        self.buffer = np.zeros(w)

    def out(self, t):
        self.buffer[:-1] = self.buffer[1:]
        self.buffer[-1] = self.input(t)
        return self.buffer.mean()
