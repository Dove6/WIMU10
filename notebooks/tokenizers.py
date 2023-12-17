from miditok import REMI
from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from typing import Any

# Creates the tokenizer and list the file paths
tokenizer = REMI()
dataset = 'maestro'
download_muspy_midi(dataset)
midi_paths = list(Path(DATA_RAW_PATH + dataset).glob('**/*.midi'))

# A validation method to discard MIDIs we do not want
# It can also be used for custom pre-processing, for instance if you want to merge
# some tracks before tokenizing a MIDI file
def midi_valid(midi: Any) -> bool:
    return True
    if any(ts.numerator != 4 for ts in midi.time_signature_changes):
        return False  # time signature different from 4/*, 4 beats per bar
    if midi.max_tick < 10 * midi.ticks_per_beat:
        return False  # this MIDI is too short
    return True

# Converts MIDI files to tokens saved as JSON files
tokenizer.tokenize_midi_dataset(  # type: ignore (reportUnknownMemberType)
    midi_paths,
    Path('./data/results/' + tokenizer.__class__.__name__),
    validation_fn=midi_valid,
)
