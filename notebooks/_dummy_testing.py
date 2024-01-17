"""
Manual experiments with self-similarity metric
"""

from pathlib import Path

import muspy as mp

from setup_dataset import DATA_RAW_PATH, download_muspy_midi

# Prepare music instance
dataset = 'maestro'
download_muspy_midi(dataset)
path = Path(DATA_RAW_PATH + dataset + '/_converted/0000.json')
music = mp.load_json(path)

print(music.metadata)
print(music.resolution)
print(music.beats)
print(music.tempos)
print(music.key_signatures)
print(music.time_signatures)
print(len(music.tracks))
for track in music.tracks:
    print(' ' + str(len(track.notes)))
