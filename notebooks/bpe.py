from miditok import MMM, TokenizerConfig
from pathlib import Path

# Creates the tokenizer and list the file paths
config = TokenizerConfig(
    use_chords=True,
    use_rests=True,
    use_tempos=True,
    use_time_signatures=True,
    use_sustain_pedals=True,
    use_pitch_bends=True
)

input_path = 'results/'  # results for default, results_max for max tokens
vocab_size = 500         # 500 for default, 1500 for max tokens
tokenizer = MMM(config)  # change class to change tokenizer, use config as param to override defaults

tokens_no_bpe_paths = list(Path('./data/' + input_path + tokenizer.__class__.__name__).glob('**/*.json'))

# Learns the vocabulary with BPE
tokenizer.learn_bpe(  # type: ignore (reportUnknownMemberType)
    vocab_size=vocab_size,
    tokens_paths=tokens_no_bpe_paths,  # type: ignore (reportGeneralTypeIssues)
)

# Converts the tokenized musics into tokens with BPE
tokenizer.apply_bpe_to_dataset(
    Path('./data/' + input_path + tokenizer.__class__.__name__),
    Path('./data/' + input_path[:-1] + 'bpe/' + tokenizer.__class__.__name__)
)
