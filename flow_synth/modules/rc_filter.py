import numpy as np

from .base import Module


class RCFilter(Module):
    """RC filter module"""

    def __init__(self, input, alpha=0.1):
        self.input = input
        self.alpha = alpha
        self.y = 0

    def out(self, t):
        self.y = self.y + self.alpha * (self.input(t) - self.y)
        return self.y
