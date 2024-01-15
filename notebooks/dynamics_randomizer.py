from random import randint
import sys

import muspy as mp
from muspy.inputs import read_midi
from muspy.outputs import write_midi


def randomize_dynamics(piece: mp.Music) -> mp.Music:
    piece = piece.deepcopy()
    for track in piece.tracks:
        for note in track.notes:
            note.velocity = randint(1, 127)
    return piece


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python dynamics_randomizer.py path_to_MIDI_file', file=sys.stderr)
    filename = sys.argv[1]
    midi = read_midi(filename)
    processed = randomize_dynamics(midi)
    write_midi(filename + '.rand.mid', processed)
