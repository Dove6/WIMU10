from miditok import REMI, REMIPlus, MIDILike, TSD, Structured, MMM, TokenizerConfig
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


# Learns the vocabulary with BPE
def calc(tokenizer, input_path, vocab_size):
    tokens_no_bpe_paths = list(Path('./data/' + input_path + tokenizer.__class__.__name__).glob('**/*.json'))
    tokenizer.learn_bpe(  # type: ignore (reportUnknownMemberType)
        vocab_size=vocab_size,
        tokens_paths=tokens_no_bpe_paths,  # type: ignore (reportGeneralTypeIssues)
    )
    # Converts the tokenized musics into tokens with BPE
    tokenizer.apply_bpe_to_dataset(
        Path('./data/' + input_path + tokenizer.__class__.__name__),
        Path('./data/' + input_path[:-1] + 'bpe/' + tokenizer.__class__.__name__)
    )


for tokenizer_class in (REMI, REMIPlus, MIDILike, TSD, Structured, MMM):
    calc(tokenizer_class(), 'results/', 500)
    calc(tokenizer_class(config), 'results_max/', 1500)
