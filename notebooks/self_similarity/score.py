"""
Manual experiments with self-similarity score
"""

from collections import defaultdict
from pathlib import Path

import muspy as mp
import json

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import compute_self_similarity

# Prepare music instance
dataset = 'musicnet'
download_muspy_midi(dataset)

test_songs = range(0, 100)

total_scores = defaultdict(dict)
for song_idx, song in enumerate(test_songs):
    path = Path(DATA_RAW_PATH + dataset + f'/_converted/{song:0>3}.json')
    try:
        music = mp.load_json(path)
    except Exception:
        continue

    print(f'Processing song {song_idx}.')
    # Since resolution is in quarternotes, probing is in 1/16 notes
    resolution = int(music.resolution / 4)
    track_end = music.get_end_time()
    for track_idx, track in enumerate(music.tracks):
        # Calculate self similarity
        if len(track.notes) == 0:
            continue
        score = compute_self_similarity(track, resolution=resolution, track_end=track_end)
        total_scores[song][track_idx] = score

with open('data/self_similarity_score.json', 'wt') as f:
    json.dump(total_scores, f, indent=4)
