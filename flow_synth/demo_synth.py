import numpy as np

from .settings import *
from .audio import Audio
from .modules.keyboard import Keyboard
from .modules.midi_table import MidiTable
from .modules.sine import Sine
from .modules.sma_filter import SMAFilter
from .modules.rc_filter import RCFilter
from .modules.ar_envelope import AREnvelope


class DemoSynth(object):
    """Synthesizer demo class.

    A modular synthesizer that takes input from the computer keyboard and generates audio.
    """

    def __init__(self):
        """Setup a modular synthesizer."""
        # audio device
        self.audio = Audio(sample_rate=SAMPLE_RATE, buffer_size=BUFFER_SIZE, volume=.5)

        # modules
        self.keyboard = Keyboard()
        midi_table = MidiTable(input=self.keyboard)

        # frequency modulation
        lfo1 = Sine(frequency=lambda t: 4) * (lambda t: .5)
        out = Sine(frequency=midi_table, fm=lfo1, hold=True)

        # amplitude modulation
        #lfo2 = Sine(frequency=lambda t: 0.5, normalize=False)
        #out = out * lfo2

        # envelope
        out = AREnvelope(out, trigger=self.keyboard.trigger, attack=0.0, release=0.5)

        # remove clicks with low pass filter
        out = SMAFilter(out, w=int(SAMPLE_RATE/1000))
        #out = RCFilter(out, alpha=0.1)

        # assign output function
        self.out = out

    def done(self, t):
        """Check if done.

        The synth will stop when done returns True.

        :param t float: The current time.
        :rtype: bool
        """
        if self.keyboard.quit:
            self.keyboard.terminate()
            return True
        return False

    def start(self):
        """Start the synth.

        It will run until done returns True.
        """
        # start the audio stream with callback functions
        self.audio.start_stream(callback=self.out, done=self.done)


if __name__ == '__main__':
    DemoSynth().start()
