from .base import Module


class MidiTable(Module):
    """MIDI table module"""

    def __init__(self, input):
        self.input = input

        # create midi table
        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}

    def out(self, t):
        note = self.input(t)
        return self.midi_table.get(note, 0.0)
