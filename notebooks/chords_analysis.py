"""
Manual experiments for different generated midi files using chord based metrics
"""
from wimu10 import chords_histogram, chords_transition_matrix
from pathlib import Path
import matplotlib.pyplot as plt
import muspy as mp
import numpy as np
import sys
import os

DATA_GENERATED_PATH = './data/generated/'


def visualize_chord_transition(chords_hist: dict, chords_dict: dict, transition_matrix: np.ndarray, title: str = '') -> None:
    labels = chords_dict.keys()
    fig, ax = plt.subplots(nrows=1, ncols=2)

    # Plot Heatmap for transition matrix
    im = ax[0].imshow(transition_matrix)
    ax[0].figure.colorbar(im, ax=ax[0])
    ax[0].set_xticks(np.arange(len(labels)), labels=labels)
    ax[0].set_yticks(np.arange(len(labels)), labels=labels)
    plt.setp(ax[0].get_xticklabels(), rotation=90, ha='right', rotation_mode='anchor')
    ax[0].invert_yaxis()
    ax[0].set_title('Chord transition heatmap')

    # Plot histogram
    ax[1].bar(chords_hist.keys(), chords_hist.values())
    plt.setp(ax[1].get_xticklabels(), rotation=90)
    ax[1].set_title('Chord histogram')

    # Adjust and show both
    fig.subplots_adjust(bottom=0.3, left=0.15)
    fig.set_figheight(9)
    fig.set_figwidth(18)
    fig.suptitle(title)
    plt.show()


def analyze_chords_in_midi_file(path_to_file, title: str = '') -> mp.Music:
    # Retrive music from midi file
    music = mp.read_midi(path_to_file)
    track = music[0]
    # Calculate and visualize transitiona matrix
    chords_unique, trans_matrix = chords_transition_matrix(track, 'piano')
    # Calculate and visualize histogram
    chords_hist = chords_histogram(track, 'piano')
    visualize_chord_transition(chords_hist, chords_unique, trans_matrix, title)
    return music


if __name__ == '__main__':
    # GiantMusicTransformer, MidiRandomizer, TensorFlow-RNN
    gen_datasets = ['gmt', 'mr', 'tf_rnn']
    data_set = sys.argv[1]
    if data_set not in gen_datasets:
        data_set = 'gmt'

    file_names = [fn for fn in os.listdir(Path(DATA_GENERATED_PATH + data_set)) if fn.endswith('mid')]
    for file in file_names:
        file_path = Path(DATA_GENERATED_PATH + data_set + '/' + file)
        music = analyze_chords_in_midi_file(file_path, file)
