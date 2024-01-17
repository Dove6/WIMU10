"""
Manual experiments with self-similarity metric
"""

from math import floor, modf
from pathlib import Path

import matplotlib.pyplot as plt
import muspy as mp

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import self_similarity
from wimu10.tempo_utils import timestep_to_realtime

# Prepare music instance
dataset = 'musicnet'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/_converted/001.json')
music = mp.load_json(path)

# Calculate self similarity
track = music.tracks[1]
track_end = music.get_end_time()

# Since resolution is in quarternotes, probing is in 1/16 notes
resolution = int(music.resolution / 4)
scores = self_similarity(track, resolution=resolution, track_end=track_end)

# Prepare labels
label_count = 16
label_indices: list[int] = []
labels: list[str] = []
for i in range(label_count):
    timestamp = (track_end - 1) * i / (label_count - 1)
    realtime = timestep_to_realtime(music, timestamp)
    seconds, minutes = modf(realtime)
    label = f'{int(minutes) * 60 + floor(seconds * 60)}'
    label_indices.append(floor(timestamp / resolution))
    labels.append(label)

# Plot
fig, ax = plt.subplots()  # type: ignore
ax.imshow(scores, cmap='hot', interpolation='nearest')
ax.set_xticks(label_indices, labels=labels)
ax.set_yticks(label_indices, labels=labels)
plt.title("Track's self similarity")
plt.xlabel('Track [s]')
plt.ylabel('Track [s]')
fig.gca().invert_yaxis()
plt.show()  # type: ignore

# Uncomment for playback
# Requires `fluidsynth` to be installed
# mp.download_musescore_soundfont()
# music.write_audio('./tmp/000.wav')
