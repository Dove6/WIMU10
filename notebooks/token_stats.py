from miditok import REMI, REMIPlus, MIDILike, TSD, Structured, CPWord, Octuple, MuMIDI, MMM
from pathlib import Path
import json
from itertools import chain


def calc(tokenizer, path):
    token_lengths = []
    name = tokenizer.__class__.__name__
    for file in list(Path('./data/' + path + name).glob('**/*.json')):
        with open(file, "r") as file:
            tokens = json.load(file)['ids']
            if isinstance(tokens[0], list):
                tokens = list(chain.from_iterable(tokens))
            length = len(tokens)
            token_lengths.append(length)
    sum_length = sum(token_lengths)
    avg_length = sum_length / len(token_lengths)
    print(name, path, sum_length, avg_length)


for tokenizer in (REMI(), REMIPlus(), MIDILike(), TSD(), Structured(), CPWord(), Octuple(), MuMIDI(), MMM()):
    calc(tokenizer, 'results/')
    calc(tokenizer, 'results_max/')

for tokenizer in (REMI(), REMIPlus(), MIDILike(), TSD(), Structured(), MMM()):
    calc(tokenizer, 'results_bpe/')
    calc(tokenizer, 'results_max_bpe/')
