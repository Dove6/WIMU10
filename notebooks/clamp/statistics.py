import pandas as pd
from pathlib import Path
import numpy as np
from numpy.typing import ArrayLike
from json import load
from typing import List, Tuple
from collections import Counter
from itertools import product
import matplotlib.pyplot as plt


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


def embeddings_mean(data: ArrayLike) -> ArrayLike:
    return np.mean(data, axis=0)


def group_min_max_variance(
    info: pd.DataFrame, embeddings: ArrayLike, author_names_and_occurences: List[Tuple[str, int]], name_to_idx: dict[str, int]
):
    """
    Calculates and displays minimum and maximum variance in the embeddings for all music and for music of each author separately.
    """
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


def group_distance_heatmap(
    info: pd.DataFrame, embeddings: ArrayLike, author_names_and_occurences: List[Tuple[str, int]], name_to_idx: dict[str, int]
):
    centroids = []

    # Everyone
    everyone_centroid = embeddings_mean(embeddings)

    # Authors
    for [author, _] in author_names_and_occurences:
        single_author_info = info[info[MaestroHeaders.CANONICAL_COMPOSER] == author]
        single_author_idxs = list(name_to_idx[name] for name in single_author_info[MaestroHeaders.MIDI_FILENAME].str[5:])
        single_author_selector = np.array(single_author_idxs, dtype=np.int32)
        single_author_embeddings = embeddings[single_author_selector]
        centroids.append(embeddings_mean(single_author_embeddings))

    # Distances between author embeddings centroids
    authors_results = np.zeros((len(centroids), len(centroids)))
    for (i, a1), (j, a2) in product(enumerate(centroids), enumerate(centroids)):
        distance = np.linalg.norm(a2 - a1)
        authors_results[i, j] = distance

    occurence_strings = list(str(o) for [a, o] in author_names_and_occurences)

    # Distances between author embeddings centroids and everyone embedding centroid
    everyone_results = np.zeros(len(centroids))
    for i, a1 in enumerate(centroids):
        distance = np.linalg.norm(everyone_centroid - a1)
        everyone_results[i] = distance
    everyone_results = np.repeat(np.expand_dims(everyone_results, axis=1), repeats=len(centroids), axis=1)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.tight_layout(pad=5.0)
    plt.colorbar(a1.imshow(np.flip(authors_results, axis=1)), ax=a1, fraction=0.03)
    a1.set_title('Distance between per author embedding centroids')
    a1.set_xticks(range(0, len(centroids), 5), occurence_strings[::-5])
    a1.set_xlabel('[author A song count]')
    a1.set_yticks(range(0, len(centroids), 5), occurence_strings[::5])
    a1.set_ylabel('[author B song count]')
    plt.colorbar(a2.imshow(everyone_results), ax=a2, fraction=0.03)
    a2.set_title('Distance between all songs embedding\ncentroid and per author embedding centroids')
    a2.set_xticks([], [])
    a2.set_yticks(range(0, len(centroids), 5), occurence_strings[::5])
    a2.set_ylabel('[author song count]')
    plt.show()


def main():
    info = load_maestro_info()
    (names, embeddings) = load_maestro_clamp_embeddings()
    embeddings = normalize_embeddings(embeddings)
    author_names_and_occurences = list(dict(Counter(info[MaestroHeaders.CANONICAL_COMPOSER].iloc)).items())
    author_names_and_occurences.sort(key=lambda x: x[1])
    name_to_idx = {name: i for i, name in enumerate(names)}

    # group_min_max_variance(info, embeddings, author_names_and_occurences, name_to_idx)
    group_distance_heatmap(info, embeddings, author_names_and_occurences, name_to_idx)


if __name__ == '__main__':
    main()
