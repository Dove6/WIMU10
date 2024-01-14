"""
A notebook to collect statistical information on a tokenized dataset.
"""

from itertools import chain
import json
from miditok import REMI, REMIPlus, MIDILike, TSD, Structured, CPWord, Octuple, MuMIDI, MMM, MIDITokenizer
from pathlib import Path
from typing import Any, List


def calc_statistics(tokenizer: MIDITokenizer, path: str):
    """Calculate token statistics for each tokenizer."""
    token_lengths: List[int] = []
    name = tokenizer.__class__.__name__
    for file in list(Path('./data/' + path + name).glob('**/*.json')):
        with open(file, 'r') as file:
            # NOTE: Different tokenizers save output as arrays of different shapes.
            # Some are flat, some are nested and thus require flattening.
            tokens: List[Any | List[Any]] = json.load(file)['ids']
            if isinstance(tokens[0], list):
                tokens = list(chain.from_iterable(tokens))
            # Get token count for the file.
            length = len(tokens)
            token_lengths.append(length)
    # Get total token count for all files.
    sum_length = sum(token_lengths)
    # Get average token count for a file.
    avg_length = sum_length / len(token_lengths)
    return name, path, sum_length, avg_length


if __name__ == '__main__':
    tokenizers_bpe = (REMI(), REMIPlus(), MIDILike(), TSD(), Structured(), MMM())
    tokenizers = (*tokenizers_bpe, CPWord(), Octuple(), MuMIDI())
    # Calculate statistics for tokenized datasets.
    for tokenizer in tokenizers:
        results = calc_statistics(tokenizer, 'results/')
        print(*results)
        results = calc_statistics(tokenizer, 'results_max/')
        print(*results)
    # Calculate statistics for tokenized datasets with BPE applied.
    # NOTE: Not every miditok tokenizer supports BPE.
    for tokenizer in tokenizers_bpe:
        results = calc_statistics(tokenizer, 'results_bpe/')
        print(*results)
        results = calc_statistics(tokenizer, 'results_max_bpe/')
        print(*results)
