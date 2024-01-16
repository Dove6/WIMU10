from pathlib import Path
from .midi_to_abc import main as convert_midi_to_abc
from .model.clamp import main as convert_abc_to_embeddings

if __name__ == '__main__':
    convert_midi_to_abc(Path('data/raw/maestro/maestro-v3.0.0'), Path('data/raw/maestro/maestro-v3.0.0-abc'))
    input('Do you like this table? (Press ENTER for "YES") (Press ENTER to continue)')  # :^)
    convert_abc_to_embeddings(Path('data/raw/maestro/maestro-v3.0.0-abc'), Path('data/raw/maestro/maestro-v3.0.0-embeddings'), 64)
