from argparse import ArgumentParser
from pathlib import Path
from random import randint, random
from typing import Optional

import muspy as mp
from muspy.inputs import read_midi
from muspy.outputs import write_midi


# source: https://docs.python.org/3/library/random.html#random.binomialvariate
def _binomialvariate(n: int, p: float) -> int:
    return sum(random() < p for _ in range(n))


def randomize_dynamics(piece: mp.Music, lower_bound: int, upper_bound: int, binomial_p: Optional[float]) -> mp.Music:
    piece = piece.deepcopy()
    if lower_bound <= upper_bound:
        possible_values = list(range(lower_bound, upper_bound + 1))
    else:
        possible_values = list(range(1, upper_bound + 1)) + list(range(lower_bound, 128))
    for track in piece.tracks:
        for note in track.notes:
            note.velocity = possible_values[
                randint(0, len(possible_values) - 1)
                if binomial_p is None
                else _binomialvariate(len(possible_values) - 1, binomial_p)
            ]
    return piece


if __name__ == '__main__':
    parser = ArgumentParser(
        description='The program randomizes the velocity of notes in a MIDI file using uniform or binomial distribution.'
    )
    parser.add_argument('input_path', type=Path, help='Input MIDI path')
    parser.add_argument('output_path', type=Path, nargs='?', default=None, help='Output MIDI path')
    parser.add_argument(
        '--binomial-p',
        type=lambda p: p and max(0.0, min(1.0, float(p))),
        required=False,
        default=None,
        help='Binomial distribution parameter in range [0; 1] (switches distribution from uniform to polynomial)',
    )
    parser.add_argument(
        '--lower-bound',
        type=int,
        required=False,
        default=1,
        help='Lower bound (inclusive) of generated velocity values',
    )
    parser.add_argument(
        '--upper-bound',
        type=int,
        required=False,
        default=127,
        help='Lower bound (inclusive) of generated velocity values',
    )
    args = parser.parse_args()

    midi = read_midi(args.input_path)
    processed = randomize_dynamics(midi, args.lower_bound, args.upper_bound, args.binomial_p)
    if args.output_path is None:
        args.output_path = args.input_path.with_name(args.input_path.name + '.rand.mid')
    write_midi(args.output_path, processed)
