import numpy as np

from settings import *
from audio import Audio
from modules.keyboard import Keyboard
from modules.midi_table import MidiTable
from modules.sine import Sine
from modules.sma_filter import SMAFilter
from modules.rc_filter import RCFilter


class Synth(object):
    """Synthesizer"""

    def __init__(self):
        self.audio = Audio(sample_rate=SAMPLE_RATE, buffer_size=BUFFER_SIZE, volume=.5)

        # modules
        self.keyboard = Keyboard()
        midi_table = MidiTable(input=self.keyboard)

        # frequency modulation
        lfo1 = Sine(frequency=lambda t: 4) * (lambda t: .5)
        out = Sine(frequency=midi_table, fm=lfo1)

        # amplitude modulation
        lfo2 = Sine(frequency=lambda t: 0.5, normalize=False)
        #out = out * lfo2

        # remove clicks with low pass filter
        out = SMAFilter(out, w=42)
        #out = RCFilter(out, alpha=0.1)
        #out = RCFilter(out, alpha=0.1)
        #out = RCFilter(out, alpha=0.1)
        #out = RCFilter(out, alpha=0.1)
        #out = RCFilter(out, alpha=0.1)
        #out = RCFilter(out, alpha=0.1)

        # assign output
        self.out = out

    def done(self, t):
        if self.keyboard.quit: # or t > 2:
            self.keyboard.terminate()
            return True
        return False

    def start(self):
        self.audio.start(self.out, self.done)


if __name__ == '__main__':
    Synth().start()
