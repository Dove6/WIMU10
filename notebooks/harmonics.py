"""
Manual experiments for chord based metrics - wip
"""

from pathlib import Path
import pypianoroll as piano
import matplotlib.pyplot as plt
import muspy as mp
import seaborn as sns
import numpy as np

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import chords_histogram, chords_transition_matrix, get_chords_list

def visualize_pianoroll(music: mp.Music) -> None:
    mp.show_pianoroll(music)
    plt.show()

def visualize_chord_transition(chords_dict:dict, transition_matrix:np.ndarray) -> None:
    labels = chords_dict.keys()
    _, ax = plt.subplots()
    im = ax.imshow(transition_matrix)
    # Create colorbar
    ax.figure.colorbar(im, ax=ax)
    # Set labels
    ax.set_xticks(np.arange(len(labels)), labels=labels)
    ax.set_yticks(np.arange(len(labels)), labels=labels) 
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
             rotation_mode="anchor")
    ax.invert_yaxis()
    plt.title("Chord transition heatmap")
    plt.show()

def visualize_chord_histogram(chords_hist:dict):
    plt.bar(chords_hist.keys(), chords_hist.values() )
    plt.xticks(rotation=90)
    plt.title("Chord histogram")
    plt.show()
    
# Prepare music instance
dataset = 'musicnet'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/_converted/149.json')
music = mp.load_json(path)
track = music.tracks[0]


### Transition matrix testing
chords_dict, transition_matrix = chords_transition_matrix(track)
visualize_chord_transition(chords_dict, transition_matrix)

### Histogram testing
chords = chords_histogram(track)
visualize_chord_histogram(chords)

### Visualizing pianoroll
visualize_pianoroll(music)