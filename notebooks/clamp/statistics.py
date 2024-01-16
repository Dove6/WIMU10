import pandas as pd
from pathlib import Path
import numpy as np
from numpy.typing import ArrayLike
from json import load
from typing import List, Tuple
from collections import Counter


class MaestroHeaders:
    CANONICAL_COMPOSER = 'canonical_composer'
    CANONICAL_TITLE = 'canonical_title'
    SPLIT = 'split'
    YEAR = 'year'
    MIDI_FILENAME = 'midi_filename'
    AUDIO_FILENAME = 'audio_filename'
    DURATION = 'duration'


def load_maestro_info() -> pd.DataFrame:
    return pd.read_csv('data/raw/maestro/maestro-v3.0.0/maestro-v3.0.0.csv', sep=',', header=0)


def load_maestro_clamp_embeddings() -> Tuple[List[str], ArrayLike]:
    embeddings_dir = Path('data/raw/maestro/maestro-v3.0.0-embeddings')
    embedding_files = list(embeddings_dir.glob('**/*.json'))
    names = list(f'{f.stem}.midi' for f in embedding_files)
    embeddings = np.stack(list(load_json_as_ndarray(f) for f in embedding_files))
    return (names, embeddings)


def load_json_as_ndarray(path: Path) -> ArrayLike:
    data = None
    with open(path, 'r') as f:
        data = load(f, parse_float=float)
    data = np.array(data)
    return data


def normalize_embeddings(data: ArrayLike) -> ArrayLike:
    """
    Normalizing embeddings is closer to cosine distance:
    https://stackoverflow.com/questions/46409846/using-k-means-with-cosine-similarity-python
    """
    length = np.sqrt((data**2).sum(axis=1))[:, None]
    return data / length


def embeddings_sorted_variance(data: ArrayLike) -> ArrayLike:
    return np.sort(np.var(data, axis=0))


def embeddings_sorted_mean(data: ArrayLike) -> ArrayLike:
    return np.sort(np.mean(data, axis=0))


def main():
    info = load_maestro_info()
    (names, embeddings) = load_maestro_clamp_embeddings()
    embeddings = normalize_embeddings(embeddings)
    author_names_and_occurences = list(dict(Counter(info[MaestroHeaders.CANONICAL_COMPOSER].iloc)).items())
    author_names_and_occurences.sort(key=lambda x: x[1])
    name_to_idx = {name: i for i, name in enumerate(names)}

    print('|                  Group or author                   | Songs | Min variance | Max variance |')
    print('|----------------------------------------------------|-------|--------------|--------------|')

    # Variance of embeddings accross entire dataset
    sorted_variance = embeddings_sorted_variance(embeddings)
    print(f'| {"Everyone": ^50} | {embeddings.shape[0]: >5} | {sorted_variance[0]: 12.9f} | {sorted_variance[-1]: 12.9f} |')

    # Variance of embeddings for individual authors
    authors_with_more_than_five_songs = list([name, occ] for [name, occ] in author_names_and_occurences if occ >= 5)
    for [author, _] in authors_with_more_than_five_songs[::-1]:
        single_author_info = info[info[MaestroHeaders.CANONICAL_COMPOSER] == author]
        single_author_idxs = list(name_to_idx[name] for name in single_author_info[MaestroHeaders.MIDI_FILENAME].str[5:])
        single_author_selector = np.array(single_author_idxs, dtype=np.int32)
        single_author_embeddings = embeddings[single_author_selector]
        single_author_sorted_variance = embeddings_sorted_variance(single_author_embeddings)
        print(
            f'| {author: ^50} | {single_author_embeddings.shape[0]: >5} | {single_author_sorted_variance[0]: 12.9f} | {single_author_sorted_variance[-1]: 12.9f} |'
        )


if __name__ == '__main__':
    main()
