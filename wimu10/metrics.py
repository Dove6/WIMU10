import muspy as mp
import numpy as np


def dummy_metric():
    """Dummy metric."""
    pass


def score_matching_notes(a, b):
    score = 0
    for c in a:
        if c in b:
            score += 1
    return score


def score_perfect_match(a, b):
    return 1 if a == b else 0


def naive_midi_markov(
    track: mp.Track,
    resolution=16,
    squash=True,
    track_start=None,
    track_end=None,
    comparison_fn=score_perfect_match,
):
    """
    track: Track to calculate the metric on.
    resolution: How dense the comparison is.
    squash: Whether to squash pitch to a single octave
    track_start: Override for track start
    track_end: Override for trask end
    returns: Self-similarity matrix
    """
    # Find bounds
    track_start = track_start or min(note.start for note in track.notes)
    track_end = track_end or max(note.end for note in track.notes)
    # Represent as notes playing at specific times
    timestamps = []
    for t in range(track_start, track_end, resolution):
        notes = []
        for note in track.notes:
            if note.start <= t and t <= note.end:
                pitch = note.pitch
                if squash:
                    pitch = pitch % 12
                notes.append(pitch)
        timestamps.append(notes)
    # Compare all notes, skip identical and reversed pairs
    #   0 1 2
    # 0 _ _ _
    # 1 x _ _
    # 2 x x _
    timestamp_count = len(timestamps)
    scores = np.zeros((timestamp_count, timestamp_count))
    for i, a in enumerate(timestamps):
        for j, b in enumerate(timestamps[:i]):
            scores[i, j] += comparison_fn(a, b)
    return scores
