from miditok import REMI, TokenizerConfig
from pathlib import Path
from setup_dataset import DATA_RAW_PATH, download_muspy_midi

# Creates the tokenizer and list the file paths
config = TokenizerConfig(
    use_chords=True,
    use_rests=True,
    use_tempos=True,
    use_time_signatures=True,
    use_sustain_pedals=True,
    use_pitch_bends=True
)

output = 'results/'  # results for default, results_max for max tokens
tokenizer = REMI()   # change class to change tokenizer, use config as param to override defaults

dataset = 'maestro'
download_muspy_midi(dataset)
midi_paths = list(Path(DATA_RAW_PATH + dataset).glob('**/*.midi'))

# Converts MIDI files to tokens saved as JSON files
tokenizer.tokenize_midi_dataset(  # type: ignore (reportUnknownMemberType)
    midi_paths,
    Path('./data/' + output + tokenizer.__class__.__name__)
)
