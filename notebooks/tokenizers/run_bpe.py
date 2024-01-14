"""
A notebook to apply Byte Pair Encoding to tokenized datasets.
This notebook assumes that tokenized datasets already exist, i.e. because `run_tokenizers.py` notebook was run.
"""

from miditok import REMI, REMIPlus, MIDILike, TSD, Structured, MMM, TokenizerConfig, MIDITokenizer
from pathlib import Path
from typing import List


# A TokenizerConfig with most extra token types enabled.
config = TokenizerConfig(
    use_chords=True,
    use_rests=True,
    use_tempos=True,
    use_time_signatures=True,
    use_sustain_pedals=True,
    use_pitch_bends=True,
)


def learn_and_apply_bpe(tokenizer: MIDITokenizer, input_path: str, vocab_size: int):
    """Learn the dataset vocabulary with BPE, then apply it and save to a separate directory."""
    # Glob all tokenized files.
    tokens_no_bpe_paths: List[Path | str] = list(Path('./data/' + input_path + tokenizer.__class__.__name__).glob('**/*.json'))
    # Learn BPE on the entire dataset.
    tokenizer.learn_bpe(  # type: ignore (reportUnknownMemberType)
        vocab_size=vocab_size,
        tokens_paths=tokens_no_bpe_paths,
    )
    # Convert the tokenized music data into tokens with BPE.
    tokenizer.apply_bpe_to_dataset(
        Path('./data/' + input_path + tokenizer.__class__.__name__),
        Path('./data/' + input_path[:-1] + 'bpe/' + tokenizer.__class__.__name__),
    )


if __name__ == '__main__':
    # Learn and apply BPE on tokenized datasets.
    # Vocabulary size was roughly based on tokenized dataset vocabulary.
    # NOTE: Not every miditok tokenizer supports BPE.
    for tokenizer_class in (REMI, REMIPlus, MIDILike, TSD, Structured, MMM):
        learn_and_apply_bpe(tokenizer_class(), 'results/', 500)
        learn_and_apply_bpe(tokenizer_class(config), 'results_max/', 1500)
