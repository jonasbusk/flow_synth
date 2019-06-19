import numpy as np

from ..settings import *
from .base import Module


class AREnvelope(Module):
    """Attack-release envelope."""

    def __init__(self, input, trigger, attack=0.0, release=0.0):
        """Create envelope.

        :param input callable: Input signal.
        :param trigger callable: Device that triggers the envelope.
        :param attack float: Attack time.
        :param release float: Release time.
        """
        assert attack >= 0 and release >= 0
        self.input = input
        self.trigger = trigger
        #self.attack = attack
        #self.release = release

        self.attack_incr = (1 / (attack * SAMPLE_RATE)) if attack>0 else 1.0
        self.release_incr = (1 / (release * SAMPLE_RATE)) if release>0 else 1.0

        self.volume = 0.0 # current amplitude of the envelope

    def out(self, t):
        # adjust volume
        if self.trigger(t):
            if self.volume < 1.0: # attack
                self.volume = min(self.volume + self.attack_incr, 1.0)
        else: # release
            self.volume = max(self.volume - self.release_incr, 0.0)
        # output
        return self.input(t) * self.volume
