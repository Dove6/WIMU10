"""
Manual experiments for chord based metrics - wip
"""

from pathlib import Path
import pypianoroll as piano
import matplotlib.pyplot as plt
import muspy as mp

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import chords_histogram, chords_transition_matrix, get_chords_list

def visualize(music: mp.Music) -> None:
    mp.show_pianoroll(music)
    plt.show()

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/_converted/0001.json')
music = mp.load_json(path)
track = music.tracks[0]

chords = chords_histogram(track)
for chord in chords.items():
    print(chord )
visualize(music)