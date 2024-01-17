"""
A notebook to apply all available miditok tokenizers on MAESTRO dataset.
"""

from miditok import REMI, REMIPlus, MIDILike, TSD, Structured, CPWord, Octuple, MuMIDI, MMM, TokenizerConfig, MIDITokenizer
from pathlib import Path
from typing import List

from setup_dataset import DATA_RAW_PATH, download_muspy_midi


# A TokenizerConfig with most extra token types enabled.
config = TokenizerConfig(
    use_chords=True,
    use_rests=True,
    use_tempos=True,
    use_time_signatures=True,
    use_sustain_pedals=True,
    use_pitch_bends=True,
)


def tokenize(tokenizer: MIDITokenizer, midi_paths: List[Path], out_dir: str):
    """Convert MIDI files to token sequences saved as JSON files."""
    tokenizer.tokenize_midi_dataset(  # type: ignore (reportUnknownMemberType)
        midi_paths, Path('./data/' + out_dir + tokenizer.__class__.__name__)
    )


if __name__ == '__main__':
    # Ensure that the MAESTRO dataset is downloaded.
    dataset = 'maestro'
    download_muspy_midi(dataset)
    # Glob all MIDI files in the dataset.
    midi_paths = list(Path(DATA_RAW_PATH + dataset).glob('**/*.midi'))
    # Process the dataset with each tokenizer.
    for tokenizer_class in (REMI, REMIPlus, MIDILike, TSD, Structured, CPWord, Octuple, MuMIDI, MMM):
        tokenize(tokenizer_class(), midi_paths, 'results/')
        tokenize(tokenizer_class(config), midi_paths, 'results_max/')
