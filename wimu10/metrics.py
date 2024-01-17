from collections import defaultdict
from collections.abc import Callable, Collection
from typing import Optional
from numpy.typing import ArrayLike

import muspy as mp
import numpy as np

Notes = Collection[int]
Comparator = Callable[[Notes, Notes], int]
SimilarityGroups = Collection[(int, int), int]


def score_matching_notes(a: Notes, b: Notes) -> int:
    score = 0
    for c in a:
        if c in b:
            score += 1
    return score


def score_perfect_match(a: Notes, b: Notes) -> int:
    return 1 if a == b else 0


def self_similarity_matrix(
    track: mp.Track,
    resolution: int = 16,
    squash: bool = True,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
    comparison_fn: Comparator = score_perfect_match,
    **_,
) -> ArrayLike:
    """
    Calculates the top bottom of self similarity matrix.
    The diagonal is unset and the top triangle is symmetrical.

    track: Track to calculate the metric on.
    resolution: How dense the comparison is.
    squash: Whether to squash pitch to a single octave
    track_start: Override for track start
    track_end: Override for trask end
    comparison_fn: Comparison function for 2 points in time

    returns: Self-similarity matrix
    """
    # Find bounds
    track_start = track_start or min(note.start for note in track.notes)
    track_end = track_end or max(note.end for note in track.notes)
    # Represent as notes playing at specific times
    timestamps: list[list[int]] = []
    for t in range(track_start, track_end, resolution):
        notes: list[int] = []
        for note in track.notes:
            if note.start <= t and t <= note.end:
                pitch = note.pitch
                if squash:
                    pitch = pitch % 12
                notes.append(pitch)
        timestamps.append(notes)
    # Compare all notes, skip identical and reversed pairs
    # The following matrix is computed, `_` indicate skipped comparisons
    #   0 1 2
    # 0 _ x x
    # 1 _ _ x
    # 2 _ _ _
    timestamp_count = len(timestamps)
    scores = np.zeros((timestamp_count, timestamp_count))
    for i, a in enumerate(timestamps):
        for j, b in enumerate(timestamps[:i]):
            scores[i, j] = comparison_fn(a, b)
    return scores


def self_similarity_groups(matrix: ArrayLike, min_length: int = 64, step: int = 1, **_) -> SimilarityGroups:
    """
    Extracts groups from similarity matrix based on provided requirements.

    matrix: Self similarity matrix.
    min_length: Minimum length of the repeated fragment. [matrix resolution]
    step: Steps between similarity checks. [matrix resolution]

    returns: Starting points of both fragments together with lengths.
    """
    size = matrix.shape[0]
    # Time difference hitmap, to remove duplication
    hitmap = defaultdict(list)
    # For every starting point, skip starting points that won't match minimum length
    for i in range(0, size - min_length):
        for j in range(0, i):
            if matrix[i, j] == 0:
                continue
            # Check if this was already covered
            difference = i - j
            repeat = False
            for previous in hitmap[difference]:
                prev_start = previous[0][0]
                prev_length = previous[1]
                ahead_by, phase = divmod(i - prev_start, step)
                if ahead_by <= prev_length and phase == 0:
                    repeat = True
                    break
            if repeat:
                continue
            # Find longest diagonal (repeated sequence)
            length = 1
            delta = step
            while i + delta < size and matrix[i + delta, j + delta] > 0:
                length += 1
                delta += step
            if length * step > min_length:
                hitmap[difference].append(((i, j), length))
    results = list(v for vs in hitmap.values() if len(vs) != 0 for v in vs)
    results.sort(key=lambda x: x[1])
    return results


def self_similarity_score(matrix: ArrayLike, groups: SimilarityGroups, step: int = 1, **_) -> float:
    """
    Computes a self similarity coverage score. (repeated sections / all sections)

    matrix: Self similarity matrix.
    groups: Self similarity groups.
    step: Steps between similarity checks.

    returns: 0-1 value
    """
    coverage_length = matrix.shape[0]
    coverage = np.zeros(matrix.shape[0])
    for (a, b), length in groups:
        for i in range(length):
            for s in range(step):
                coverage[a + i + s] = 1
                coverage[b + i + s] = 1
    score = coverage.sum() / coverage_length
    return score


def compute_self_similarity(track: mp.Track, **kvargs) -> float:
    """
    Computes a self similarity coverage score from the track. (repeated sections / all sections)

    track: Track to calculate the metric on.
    kvargs: Check intermediate functions for additional arguments.

    returns: 0-1 value
    """
    matrix = self_similarity_matrix(track, **kvargs)
    groups = self_similarity_groups(matrix, **kvargs)
    score = self_similarity_score(matrix, groups, **kvargs)
    return score
