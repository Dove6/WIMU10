"""
Manual experiments with dynamics-related metrics
"""

from pathlib import Path

# import matplotlib.pyplot as plt
import muspy as mp
import json

from setup_dataset import DATA_RAW_PATH, download_muspy_midi
from wimu10 import (
    compute_dynamics_histogram,
    compute_dynamics_levels_histogram,
    compute_dynamics_variability,
    compute_dynamics_levels_variability,
    compute_dynamics_transition_matrix,
    compute_dynamics_levels_transition_matrix,
)

# Prepare music instance
dataset = 'musicnet'
download_muspy_midi(dataset)

test_pieces = range(0, 100)

total_scores = {}
for piece_idx, piece in enumerate(test_pieces):
    path = Path(DATA_RAW_PATH + dataset + f'/_converted/{piece:0>3}.json')  # beware, not all datasets have 100-999 elements
    try:
        music = mp.load_json(path)
    except Exception:
        continue

    print(f'Processing piece {piece_idx}.')
    # Since resolution is in quarternotes, probing is in 1/16 notes
    resolution = int(music.resolution / 4)
    track_end = music.get_end_time()
    total_scores[piece] = []
    for track_idx, track in enumerate(music.tracks):
        print(f'Processing track {track_idx}.')
        # Calculate self similarity
        if len(track.notes) == 0:
            total_scores[piece].append(None)
            print(f'  Skipping track {track_idx} (it has 0 notes).')
            continue
        bins = compute_dynamics_histogram(music, track_idx, resolution=resolution, track_end=track_end)
        level_bins = compute_dynamics_levels_histogram(music, track_idx, resolution=resolution, track_end=track_end)
        variability = compute_dynamics_variability(music, track_idx, resolution=resolution, track_end=track_end)
        level_variability = compute_dynamics_levels_variability(music, track_idx, resolution=resolution, track_end=track_end)
        transition_matrix = compute_dynamics_transition_matrix(music, track_idx, resolution=resolution, track_end=track_end)
        level_transition_matrix = compute_dynamics_levels_transition_matrix(
            music, track_idx, resolution=resolution, track_end=track_end
        )
        total_scores[piece].append(
            {
                'histogram': bins,
                'level_histogram': level_bins,
                'variability': variability,
                'level_variability': level_variability,
                'transition_matrix': transition_matrix.tolist(),
                'level_transition_matrix': level_transition_matrix.tolist(),
            }
        )

with open('results/dynamics_metrics.json', 'wt') as f:
    json.dump(total_scores, f, indent=4)
