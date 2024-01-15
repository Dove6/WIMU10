"""
A notebook to test impact of vocabulary size on Byte Pair Encoding.
This notebook assumes that tokenized datasets already exist, i.e. because `tokenize.py` notebook was run.
"""

from miditok import REMI, TokenizerConfig, MIDITokenizer
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
        Path('./data/' + input_path[:-1] + '_bpe_var/' + tokenizer.__class__.__name__ + '/' + str(vocab_size)),
    )


if __name__ == '__main__':
    # Learn and apply BPE on tokenized datasets.
    # NOTE: Not every miditok tokenizer supports BPE.
    for vocab_size in (500, 1000, 1500, 2000, 3000):
        print('BPE on default REMI with vocabulary size of', vocab_size)
        learn_and_apply_bpe(REMI(), 'results/', vocab_size)
        print('BPE on max REMI with vocabulary size of', vocab_size)
        learn_and_apply_bpe(REMI(config), 'results_max/', vocab_size)
