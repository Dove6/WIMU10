"""
Manual experiments for chord based metrics
"""
from pathlib import Path
import matplotlib.pyplot as plt
import muspy as mp
import numpy as np

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import chords_histogram, chords_transition_matrix


def visualize_pianoroll(ex_music: mp.Music) -> None:
    mp.show_pianoroll(ex_music)
    plt.show()


def visualize_chord_transition(chords_dict: dict, transition_matrix: np.ndarray) -> None:
    labels = chords_dict.keys()
    _, ax = plt.subplots()
    im = ax.imshow(transition_matrix)
    # Create colorbar
    ax.figure.colorbar(im, ax=ax)
    # Set labels
    ax.set_xticks(np.arange(len(labels)), labels=labels)
    ax.set_yticks(np.arange(len(labels)), labels=labels)
    plt.setp(ax.get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
    ax.invert_yaxis()
    plt.title('Chord transition heatmap')
    plt.show()


def visualize_chord_histogram(chords_hist: dict[str, int]):
    plt.bar(list(chords_hist.keys()), list(chords_hist.values()))
    plt.xticks(rotation=90)
    plt.title('Chord histogram')
    plt.show()


if __name__ == '__main__':
    # Prepare music instance
    dataset = 'musicnet'
    download_muspy_midi(dataset)
    path = Path(DATA_RAW_PATH + dataset + '/_converted/151.json')
    music = mp.load_json(path)
    track = music.tracks[0]

    # Visualizing pianoroll
    visualize_pianoroll(music)

    # Transition matrix testing
    ch_dict, t_matrix = chords_transition_matrix(track, 'piano')
    visualize_chord_transition(ch_dict, t_matrix)

    # Histogram testing
    chords = chords_histogram(track, 'piano')
    visualize_chord_histogram(chords)
