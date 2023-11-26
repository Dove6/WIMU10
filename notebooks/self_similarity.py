"""
Manual experiments with self-similarity metric
"""

from wimu10 import self_similarity
import muspy as mp
from os import makedirs
from pathlib import Path
import matplotlib.pyplot as plt
from math import modf, floor

from wimu10.tempo_utils import timestep_to_realtime

# Prepare music instance
path = Path("./tmp/dataset")
makedirs(path, exist_ok=True)
mp.MusicNetDataset(path, download_and_extract=True, cleanup=True, convert=True)
mp.download_musescore_soundfont()
path = Path("./tmp/dataset/_converted/000.json")
music = mp.load_json(path)

# Calculate self similarity
track = music.tracks[1]
track_end = music.get_end_time()

# Since resolution is in quarternotes, probing is in 1/16 notes
resolution = int(music.resolution / 4)
scores = self_similarity(track, resolution=resolution, track_end=track_end)

# Prepare labels
label_count = 16
label_indices = []
labels = []
for i in range(label_count):
    timestamp = (track_end - 1) * i / (label_count - 1)
    realtime = timestep_to_realtime(music, timestamp)
    sec, min = modf(realtime)
    label = f"{int(min)}m{floor(sec * 60)}s"
    label_indices.append(floor(timestamp / resolution))
    labels.append(label)

# Plot
fig, ax = plt.subplots()
ax.imshow(scores, cmap="hot", interpolation="nearest")
ax.set_xticks(label_indices, labels=labels)
ax.set_yticks(label_indices, labels=labels)
fig.gca().invert_yaxis()
plt.show()

# Uncomment for playback
# Requires `fluidsynth` to be installed
# music.write_audio("./tmp/000.wav")
